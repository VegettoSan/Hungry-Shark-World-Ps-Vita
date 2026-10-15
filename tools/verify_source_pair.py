#!/usr/bin/env python3
"""Read-only SHA/ZIP/Unity pair audit; does not extract or reproduce game assets."""
import collections
import hashlib
import pathlib
import re
import sys
import zipfile

APK_SHA = "6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d"
OBB_SHA = "c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72"
DATA = "assets/bin/Data/"
SPLIT = re.compile(r"^(.+)\.split([0-9]+)$")


def verify(path, digest):
    if not path.is_file():
        raise ValueError(f"Not a regular file: {path.name}")
    with path.open("rb") as fp:
        got = hashlib.file_digest(fp, "sha256").hexdigest()
    if got != digest:
        raise ValueError(f"{path.name}: SHA-256 mismatch; wrong game version or modified input")
    with zipfile.ZipFile(path) as arc:
        names = arc.namelist()
        if arc.testzip() is not None:
            raise ValueError(f"{path.name}: ZIP CRC check failed")
        files = {n for n in names if n.startswith(DATA) and not n.endswith("/")}
        splits = collections.defaultdict(list)
        for name in files:
            m = SPLIT.fullmatch(name)
            if m:
                splits[m.group(1)].append(int(m.group(2)))
        for base, indices in splits.items():
            if sorted(indices) != list(range(len(indices))):
                raise ValueError(f"{path.name}: missing/duplicate split fragment for {base}")
            if base in files:
                raise ValueError(f"{path.name}: split group conflicts with whole file {base}")
        return names, files, splits


def main(argv):
    if len(argv) != 3:
        print("Usage: python tools/verify_source_pair.py path/to/2.9.0.apk path/to/main.132.obb")
        return 2
    apk, obb = map(pathlib.Path, argv[1:])
    try:
        apk_names, apk_files, apk_splits = verify(apk, APK_SHA)
        obb_names, obb_files, obb_splits = verify(obb, OBB_SHA)
        if apk_files & obb_files:
            raise ValueError("Overlapping Data archive entries: check for duplicate/conflicting resources")
        if "lib/armeabi-v7a/libmono.so" not in apk_names or "lib/armeabi-v7a/libil2cpp.so" in apk_names:
            raise ValueError("Backend is not expected ARMv7 Mono")
        dlls = [n for n in apk_files if n.startswith(DATA+"Managed/") and n.endswith(".dll")]
        if "assets/bin/Data/Managed/Assembly-CSharp.dll" not in dlls or len(dlls) != 23:
            raise ValueError("Expected 23 managed DLLs including Assembly-CSharp.dll")
        expected_levels = {DATA+f"level{i}" for i in range(23)}
        logical = {SPLIT.fullmatch(p).group(1) if SPLIT.fullmatch(p) else p for p in (apk_files | obb_files)}
        if not expected_levels.issubset(logical):
            raise ValueError("One or more expected serialized level0-level22 files missing")
        with zipfile.ZipFile(apk) as arc:
            if b"2017.1.2p4" not in arc.read(DATA+"globalgamemanagers")[:256]:
                raise ValueError("Original Unity 2017.1.2p4 player header missing")
        print(f"VERIFIED: 2.9.0/132 Unity 2017.1.2p4 Mono source pair")
        print(f"APK: SHA/CRC PASS, {len(apk_names)} entries, {len(dlls)} DLLs, {len(apk_splits)} split groups")
        print(f"OBB: SHA/CRC PASS, {len(obb_names)} entries, {len(obb_splits)} split groups")
        print("Logical level0-level22 names present; gameplay/editor compatibility NOT TESTED.")
        return 0
    except (OSError, ValueError, zipfile.BadZipFile, KeyError) as exc:
        print(f"SOURCE PAIR ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
