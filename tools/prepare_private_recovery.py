#!/usr/bin/env python3
"""Owner-authorized offline source-pair staging. Proprietary output MUST stay ignored.

Usage: python tools/prepare_private_recovery.py APK OBB PRIVATE_OUTPUT
Retains all container entries, refuses differing collisions, and resumes only
when the completed checkpoint and every staged file still match their hashes.
"""
import collections
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import zipfile

from verify_source_pair import APK_SHA, OBB_SHA, DATA, SPLIT, verify


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding='utf-8')


def prepare(apk, obb, root):
    repo = Path(__file__).resolve().parent.parent
    root = root.resolve()
    relative = root.relative_to(repo)
    subprocess.run(['git', 'check-ignore', '--quiet', str(relative/'probe.cs')],
                   cwd=repo, check=True)
    checkpoint = root/'Checkpoints/02_extracted.json'
    if checkpoint.exists():
        result = json.loads(checkpoint.read_text())
        for row in json.loads((root/'Reports/Staged_Manifest.json').read_text()):
            assert sha(root/row['path']) == row['sha256'], row['path']
        assert sha(apk) == APK_SHA and sha(obb) == OBB_SHA
        print('Existing complete checkpoint verified:', json.dumps(result))
        return
    for name in ('Extracted_APK', 'Extracted_OBB', 'Combined_Unity_Data'):
        assert not (root/name).exists(), 'Incomplete staging exists; inspect before resuming: '+name
    root.mkdir(parents=True, exist_ok=True)
    inputs = []
    for path, expected in ((apk, APK_SHA), (obb, OBB_SHA)):
        names, _, _ = verify(path, expected)
        # Normalize relative '..' lexically; resolving through sandbox/reparse
        # mappings can produce a nonexistent input path on Windows.
        inputs.append(dict(path=os.path.abspath(path), bytes=path.stat().st_size,
                           sha256=expected, zip_entries=len(names), crc='PASS'))
    save(root/'Original_Inputs/Manifest.json', inputs)
    save(root/'Checkpoints/01_verified.json', dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), inputs=inputs))
    manifest = []
    logical = {}
    collisions = []
    groups = collections.defaultdict(dict)
    # ZIP reads verify each entry CRC again while extracting. No data is discarded.
    for path, label in ((apk, 'Extracted_APK'), (obb, 'Extracted_OBB')):
        seen = set()
        with zipfile.ZipFile(path) as arc:
            for entry in arc.infolist():
                name = entry.filename
                rel = PurePosixPath(name)
                assert not rel.is_absolute() and '..' not in rel.parts and '\\' not in name and ':' not in name, name
                assert not (entry.external_attr >> 16) & 0o170000 == 0o120000, name
                if entry.is_dir():
                    (root/label/rel).mkdir(parents=True, exist_ok=True)
                    continue
                key = name.casefold()
                assert key not in seen, 'Case/duplicate archive path: '+name
                seen.add(key)
                target = root/label/rel
                target.parent.mkdir(parents=True, exist_ok=True)
                with arc.open(entry) as source, target.open('xb') as dest:
                    shutil.copyfileobj(source, dest, 1024*1024)
                row = dict(path=target.relative_to(root).as_posix(), bytes=target.stat().st_size, sha256=sha(target), crc32=f'{entry.CRC:08x}')
                assert row['bytes'] == entry.file_size
                manifest.append(row)
                if not name.startswith(DATA):
                    continue
                data_rel = name[len(DATA):]
                if data_rel.casefold() in logical:
                    previous = logical[data_rel.casefold()]
                    assert previous['row']['sha256'] == row['sha256'], 'Differing Data collision: '+data_rel
                    collisions.append(dict(path=data_rel, identical=True))
                    continue
                logical[data_rel.casefold()] = dict(rel=data_rel, target=target, row=row)
    combined = root/'Combined_Unity_Data/Data'
    for item in logical.values():
        match = SPLIT.fullmatch(item['rel'])
        if match:
            groups[match[1]][int(match[2])] = item
            continue
        dest = combined/item['rel']
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Copies isolate the preserved extraction from any consumer writes.
        shutil.copy2(item['target'], dest)
        manifest.append(dict(path=dest.relative_to(root).as_posix(), bytes=dest.stat().st_size, sha256=item['row']['sha256']))
    split_report = []
    for base, parts in sorted(groups.items()):
        assert sorted(parts) == list(range(len(parts))), base
        assert base.casefold() not in logical, 'Whole/split collision: '+base
        dest = combined/base
        dest.parent.mkdir(parents=True, exist_ok=True)
        expected = hashlib.sha256()
        size = 0
        with dest.open('xb') as output:
            for number, item in sorted(parts.items()):
                with item['target'].open('rb') as source:
                    for block in iter(lambda: source.read(1024*1024), b''):
                        output.write(block)
                        expected.update(block)
                        size += len(block)
        assert dest.stat().st_size == size and sha(dest) == expected.hexdigest(), base
        row = dict(path=dest.relative_to(root).as_posix(), bytes=size, sha256=expected.hexdigest())
        manifest.append(row)
        split_report.append(dict(base=base, parts=[dict(index=n, path=i['row']['path'], bytes=i['row']['bytes'], sha256=i['row']['sha256']) for n, i in sorted(parts.items())], **row))
    assert len(groups) == 7 and sum(map(len, groups.values())) == 68
    assert len(list((combined/'Managed').glob('*.dll'))) == 23
    assert all((combined/f'level{i}').is_file() for i in range(23))
    save(root/'Reports/Staged_Manifest.json', manifest)
    save(root/'Reports/Split_Reconstruction.json', split_report)
    save(root/'Reports/Data_Collisions.json', collisions)
    result = dict(status='EXTRACTED_VERIFIED', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  extracted_files=sum(1 for r in manifest if r['path'].startswith('Extracted_')),
                  logical_data_files=sum(1 for r in manifest if r['path'].startswith('Combined_')),
                  groups=len(groups), fragments=sum(map(len, groups.values())),
                  managed_assemblies=23, logical_scene_files=23, identical_collisions=len(collisions),
                  unresolved_collisions=0, editor='NOT RUN')
    save(checkpoint, result)
    print(json.dumps(result))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    prepare(*map(Path, sys.argv[1:]))
