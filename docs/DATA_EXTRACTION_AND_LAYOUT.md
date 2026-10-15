# APK + OBB recovery and proposed Vita filesystem — RESEARCH ONLY (P00)

## Developer source pair

Inputs: user-owned Hungry Shark World **2.9.0 / 132 APK** and matching **main.132 OBB**. Validate checksums in [audit](TECHNICAL_AUDIT.md) before unpacking. Both are ZIP containers with Unity files in `assets/bin/Data/`. The APK holds `Managed/` assemblies and `level0`; the OBB holds `level1` through `level22` (some split).

**Future P01 recovery flow (not yet authorized):** verify both archives → unpack into *private* staging directories → reject archive path traversal and accidental collisions → join `.splitN` in **numeric order** with contiguous sequences → preserve the original Unity serialized naming/identities and all `Managed/` DLLs → import the complete combined dataset with AssetRipper → inspect recovered script identities using ILSpy → export to a **throwaway Unity 2017.1.2p4 project** and log missing MonoBehaviour links. Track OBB, AssetBundles and cache dependencies. A scene file name is not a user-level stage.

**Never simply copy the Android Unity Data folder or Android ARM `.so` into a PSP2 VPK.** Unity Android data and asset bundles can contain platform-specific serialization, shaders and texture formats. A runnable PSP2 Unity build requires a working editor/module and validated platform-specific asset build; recovery alone is not that build.

## Two distinct distributions

1. **Developer recovery**: faithful private whole-project staging to restore gameplay and serialize for target PSP2.
2. **End-user extractor** (P12 only): possible user-supplied original APK+OBB and a verified limited manifest/conversion/patch recipe, determined only after successful physical Vita tests. A raw ZIP extractor cannot automatically convert Android Unity assets to PSP2.

## Vita paths (unverified for this port)

- `ux0:app/<FUTURE_WORLD_TITLE_ID>/` / runtime `app0:` is the proposed installed application location; **Title ID not selected**.
- `Application.dataPath`, `streamingAssetsPath`, `persistentDataPath` on PSP2: capture real values during P07–P08 tests. Do not guess them from Android or another port.
- Save files must use verified writable storage separate from installed app payload. Test retention through reinstall/update. Never overwrite generated `eboot.bin`, `sce_sys` or PSP2 Unity Data with an Android extraction.
- Optional **xdelta3** end-user patch delivery can be studied after successful source/target hashes, real PSP2 data layout, test coverage and distribution-rights review. It is **not** an APK→Vita converter.

All files and outputs containing copyrighted game content remain excluded from Git.
