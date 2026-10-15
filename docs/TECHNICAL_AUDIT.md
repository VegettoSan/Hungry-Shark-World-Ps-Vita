# Reproducible technical audit — Hungry Shark World 2.9.0 (132)

**VERIFIED static input inspection, 2026-10-15**. The following data was read from the owner-supplied APK and OBB directly; no Unity editor or Vita runtime was executed in this audit.

| Property | APK / source | Matching OBB |
| --- | --- | --- |
| Package / version | `com.ubisoft.hungrysharkworld`, **2.9.0 / 132** (filename and prior package inspection) | `main.132.com.ubisoft.hungrysharkworld.obb` |
| File bytes | **27,378,446** | **92,431,553** |
| SHA-256 | `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d` | `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72` |
| ZIP entries | **769** | **3,966** |
| ZIP CRC | **PASS** | **PASS** |
| Unity player header | **2017.1.2p4** in APK `globalgamemanagers` | serialized content of original data pack |
| Backend | **Mono** | companion serialized assets |
| Managed DLLs | **23** under `assets/bin/Data/Managed/` | N/A |
| Native code | `lib/armeabi-v7a/libmono.so` and `libunity.so`; no `libil2cpp.so` | N/A |
| Scene naming | `assets/bin/Data/level0` | `level1`–`level22`, some split across pieces |

**VERIFIED**: exact input hashes; ZIP CRC; native backend presence; 23 managed DLLs; scene path names. The OBB contains `level17.split0`–`.split2`, `level21.split0`–`.split1`, `level22.split0`–`.split2`; count logical scene files *after* reconstructing fragments. The APK and OBB must be recovered as **one coherent source set** without overwriting collisions.

**OWNER-REPORTED (not independently replayed by agent):** Android 2.9.0 downloaded additional data and the resulting installation was playable. AssetBundle completeness and dynamic cache paths have not yet been measured independently.

**UNTESTED:** whether the full Unity editor project can be reconstructed, MonoBehaviour GUID/fileID fidelity, private Android cache dependencies, Unity 2017 editor compilation/gameplay, Unity 2018 migration, Vita PSP2 player availability, device runtime, VPK, real FPS and memory limits.

**Version 3.0.2** is a Mono research reference with a different APK and no owner-recovered functioning OBB: not a substitute for this baseline's input pair. The separate Evolution project must not be combined with these data or its Title ID.

## Audit reproduction (read-only, locally)
```sh
python tools/verify_source_pair.py "path/to/HSW_2.9.0.apk" "path/to/main.132.com.ubisoft.hungrysharkworld.obb"
python tools/check_phase_gates.py
```

Only metadata/checksums/logs belong in Git. Original inputs, exports and decompiled code stay in ignored private directories.
