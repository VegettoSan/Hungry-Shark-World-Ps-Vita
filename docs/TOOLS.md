# World port toolchain — original engine first

This is the World-specific checklist; do not blindly import Evolution's Unity 5.6 dependencies or download redundant tools. Use the owner's ignored local `Tool Codex/` directory and record exact installed versions/hashes in [EXPERIMENTS](EXPERIMENTS.md). A link is **not evidence** that a tool has been installed or tested.

| Stage | Tool / reference | Purpose |
| --- | --- | --- |
| P00 | [Unity 2017.1.2p4 official archive](https://unity.com/releases/editor/archive) | Exact original editor, side by side; validate blank PC project. Legacy download/license availability remains to be checked locally |
| P00 | Python 3 and 7-Zip, Git for Windows | Audit SHA/CRC and unpack ZIP source pair in later approved phase |
| P00 | [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) | Optional Android gameplay reference and OBB/cache backups |
| P01 | [AssetRipper](https://github.com/AssetRipper/AssetRipper) | Recover Unity scene/prefab/assets with full APK+OBB Data and original Managed assemblies |
| P01 | [ILSpy](https://github.com/icsharpcode/ILSpy), [dnSpyEx](https://github.com/dnSpyEx/dnSpy) | Read original Mono IL/types/fields and decompile locally; do not publish code |
| Conditional | [UABEA](https://github.com/nesrak1/UABEA), [AssetStudio](https://github.com/Perfare/AssetStudio) | Focused troubleshooting when AssetRipper cannot resolve an object |
| P02–P04 | Unity 2017.1.2p4 Console / Editor Play Mode / Profiler | Original-engine compilation, visual/gameplay/save regression |
| P05–P06 | [Unity 2018.2.19f1](https://unity.com/releases/editor/whats-new/2018.2.19f1) | Target editor evidenced by [Halo 2D PSP2 reference](https://github.com/VegettoSan/Halo2D_PsVita); keep a clone of frozen Unity 2017 project |
| P07+ | Actual supported Unity PSP2 module + physical PS Vita | **Not verified**. Prove lawful smoke test independently before World VPK gameplay claims |
| Only if evidenced | [JADX](https://github.com/skylot/jadx), [Apktool](https://github.com/iBotPeaches/Apktool), [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Investigate Android-only Java/JNI/native plugin contracts when they block gameplay |

Do not install Cpp2IL/Il2CppDumper for the **2.9.0 Mono** primary baseline; those tools target IL2CPP versions. Do not install VitaGL/FalsoJNI as substitutes for a native Unity PSP2 route. Use the original project's serialized inputs and built-in mapping; do not rewrite controls early.

**PSP2 caveat:** Unity 2018.2.19f1 being historically used for the owner's Halo 2D does not guarantee this workstation has a usable PSP2 build module or license. Verify it at P00 (inventory only) and P07 (device test).
