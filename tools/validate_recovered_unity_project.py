#!/usr/bin/env python3
"""Offline Unity export audit. Does not validate editor import or compilation.

Usage: python validate_recovered_unity_project.py PROJECT --output report.json
Reports paths and reference IDs only; keep reports from proprietary projects private.
"""
import argparse
import collections
import json
import re
from pathlib import Path

GUID = re.compile(r'^guid:\s*([0-9a-fA-F]{32})\s*$', re.M)
REF = re.compile(r'\{\s*fileID:\s*(-?\d+),\s*guid:\s*([0-9a-fA-F]{32}),\s*type:\s*\d+\s*\}')
SCRIPT = re.compile(r'^\s*m_Script:\s*\{([^}]+)\}', re.M)
DOC = re.compile(r'^--- !u!\d+ &(-?\d+)', re.M)
LOCAL_REF = re.compile(r'\{\s*fileID:\s*(-?\d+)\s*\}')
BUILTINS = {'0'*32, '0000000000000000e000000000000000', '0000000000000000f000000000000000'}
# Legacy editor extension GUID, independently recorded in installed GUISystem
# ivy.xml. Its fileIDs and availability still require the target Editor.
EDITOR_EXTENSIONS = {'f5f67c52d1564df4a8936ccd202a3bd8': 'UnityEngine.UI'}

def audit(project):
    project = Path(project)
    assets = project / 'Assets'
    missing_dirs = [n for n in ('Assets', 'ProjectSettings') if not (project/n).is_dir()]
    files = sorted(p for p in assets.rglob('*') if p.is_file())
    paths = collections.defaultdict(list)
    missing_meta = []
    orphan_meta = []
    invalid_meta = []
    counts = collections.Counter()
    for p in files:
        rel = p.relative_to(project).as_posix()
        if p.suffix == '.meta':
            m = GUID.search(p.read_text(encoding='utf-8-sig', errors='replace'))
            if m: paths[m[1].lower()].append(rel[:-5])
            else: invalid_meta.append(rel)
            if not p.with_suffix('').exists(): orphan_meta.append(rel)
        else:
            counts[p.suffix.lower() or '(no extension)'] += 1
            if not Path(str(p)+'.meta').exists(): missing_meta.append(rel)
    missing_folder_meta = [p.relative_to(project).as_posix() for p in assets.rglob('*') if p.is_dir() and not Path(str(p)+'.meta').exists()]
    yaml_docs = {}; yaml_paths = []
    settings_files = sorted(p for p in (project/'ProjectSettings').rglob('*') if p.is_file())
    for p in files + settings_files:
        if p.suffix == '.meta': continue
        with p.open('rb') as stream: header=stream.read(32)
        if not header.startswith(b'%YAML'): continue
        rel=p.relative_to(project).as_posix()
        text=p.read_text(encoding='utf-8-sig',errors='replace')
        yaml_paths.append(p)
        yaml_docs[rel]=set(DOC.findall(text))
    dangling=[]; bad_fileids=[]; bad_local_fileids=[]; scripts=[]; null_scripts=[]; total_refs=0
    editor_refs=[]; implicit_scene_refs=[]
    for p in yaml_paths:
        rel=p.relative_to(project).as_posix()
        text=p.read_text(encoding='utf-8-sig',errors='replace')
        for fid in LOCAL_REF.findall(text):
            if fid!='0' and fid not in yaml_docs[rel]:
                bad_local_fileids.append({'source':rel,'fileID':fid})
        for m in REF.finditer(text):
            fid,guid=m[1],m[2].lower()
            if fid=='0' or guid in BUILTINS: continue
            total_refs+=1
            targets=paths.get(guid,[])
            row={'source':rel,'fileID':fid,'guid':guid}
            if not targets and guid in EDITOR_EXTENSIONS:
                editor_refs.append(dict(row,provider=EDITOR_EXTENSIONS[guid],status='REQUIRES_TARGET_EDITOR_VERIFICATION'))
            elif not targets: dangling.append(row)
            elif len(targets)==1 and targets[0] in yaml_docs and fid not in yaml_docs[targets[0]]:
                if targets[0].endswith('.unity') and fid=='102900000':
                    # SceneAsset is the imported scene main object, not a YAML
                    # document inside the serialized scene hierarchy.
                    implicit_scene_refs.append(dict(row,target=targets[0]))
                else: bad_fileids.append(dict(row,target=targets[0]))
        for m in SCRIPT.finditer(text):
            fm=re.search(r'fileID:\s*(-?\d+)',m[1]); gm=re.search(r'guid:\s*([0-9a-fA-F]{32})',m[1])
            row={'source':rel,'fileID':fm[1] if fm else None,'guid':gm[1].lower() if gm else None}
            if row['fileID']=='0' or not gm: null_scripts.append(row)
            else:
                row['targets']=paths.get(row['guid'],[])
                scripts.append(row)
    duplicates={k:v for k,v in paths.items() if len(v)>1}
    missing_scripts=[s for s in scripts if not s['targets'] and s['guid'] not in BUILTINS and s['guid'] not in EDITOR_EXTENSIONS]
    build_scenes=[]; build_issues=[]
    build=project/'ProjectSettings/EditorBuildSettings.asset'
    if build.exists():
        text=build.read_text(encoding='utf-8-sig',errors='replace')
        for enabled,path,guid in re.findall(r'- enabled:\s*(\d+)\s+path:\s*([^\r\n]+)\s+guid:\s*([0-9a-fA-F]{32})',text):
            path=path.strip();guid=guid.lower()
            row={'enabled':enabled=='1','path':path,'guid':guid,'exists':(project/path).is_file(),'guid_matches':path in paths.get(guid,[])}
            build_scenes.append(row)
            if not row['exists'] or not row['guid_matches']:build_issues.append(row)
    status='STATIC_CHECK_PASS' if not any((missing_dirs,missing_meta,missing_folder_meta,orphan_meta,invalid_meta,duplicates,missing_scripts,null_scripts,dangling,bad_fileids,bad_local_fileids,build_issues)) else 'STATIC_CHECK_ISSUES'
    return {'status':status,'limits':'Only exported text YAML and GUID targets checked; binary subasset fileIDs, serialized type fidelity, editor imports, compilation and gameplay NOT TESTED.',
        'directories_missing':missing_dirs,'asset_extensions':dict(sorted(counts.items())), 'guid_count':len(paths),
        'missing_meta':missing_meta,'missing_folder_meta':missing_folder_meta,'orphan_meta':orphan_meta,'invalid_meta':invalid_meta,'duplicate_guids':duplicates,
        'yaml_files':len(yaml_paths),'external_reference_count':total_refs,'dangling_guid_references':dangling,'missing_yaml_fileids':bad_fileids,
        'missing_local_fileids':bad_local_fileids,
        'editor_provided_references_pending_verification':editor_refs,'implicit_scene_asset_references':implicit_scene_refs,
        'build_scenes':build_scenes,'build_scene_issues':build_issues,
        'script_reference_count':len(scripts),'script_targets':sorted({t for s in scripts for t in s['targets']}),
        'missing_script_references':missing_scripts,'null_script_references':null_scripts}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not args.project.is_dir(): parser.error('Project directory does not exist')
    result=audit(args.project)
    args.output.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:(len(v) if isinstance(v,(list,dict)) else v) for k,v in result.items() if k!='limits'}))
    return 0 if result['status']=='STATIC_CHECK_PASS' else 1

if __name__=='__main__': raise SystemExit(main())
