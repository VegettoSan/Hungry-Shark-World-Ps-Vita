# Hungry Shark World — PS Vita Port

Research and development for a **native PlayStation Vita port** of *Hungry Shark World*. The priority is recovering and faithfully adapting the original Unity/Mono game, **not recreating its gameplay or substituting another engine**.

**Status: P00 ACTIVE / 0 of 13 gates approved.** Source APK/OBB audit is complete at ZIP/header level; **no recovered Unity editor game, desktop regression, Vita build or VPK is verified**.

## Reference inputs (private, user-supplied)
- Android package: `com.ubisoft.hungrysharkworld`
- Game: **2.9.0 (132)**
- Original player: **Unity 2017.1.2p4, Mono, ARMv7**
- Required pair: `2.9.0-132 APK` + `main.132.com.ubisoft.hungrysharkworld.obb`
- APK SHA-256: `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d`
- OBB SHA-256: `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72`
- The owner reports the original Android installation downloaded its data and is playable; **this does not validate a reconstructed editor build**.
- Version **3.0.2** is a *separate Mono comparison reference*, not an interchangeable OBB or the port baseline.

## Non-negotiable engine order

1. Audit the original **2.9.0 APK + matching OBB** and validate a clean Unity **2017.1.2p4** editor.
2. Recover the original project's Unity scenes, assets and Mono C# locally; repair only with evidence.
3. Prove representative **real gameplay and save/load in Unity 2017.1.2p4 on PC**, and freeze the original-engine baseline after owner approval. Unity Editor Play Mode is an acceptable desktop test format with complete evidence.
4. **Clone** the approved baseline for migration to **Unity 2018.2.19f1**, and prove desktop gameplay parity again.
5. Independently verify the **PSP2 build module and physical Vita**, then port/test boot, gameplay, controls, saving, audio, performance and release readiness.

Do not skip or auto-approve any stage. Stage ledger: [docs/PHASE_GATES.json](docs/PHASE_GATES.json); validator: `python tools/check_phase_gates.py`; methodology: [docs/PORTING_PLAN.md](docs/PORTING_PLAN.md).

## Documentation
- [AGENTS.md](AGENTS.md): mandatory Codex/agent/contributor rules.
- [Porting plan and approvals](docs/PORTING_PLAN.md).
- [Technical audit with evidence](docs/TECHNICAL_AUDIT.md).
- [APK/OBB extraction and proposed Vita layout](docs/DATA_EXTRACTION_AND_LAYOUT.md).
- [Experiment journal](docs/EXPERIMENTS.md).
- [Tools and local environment](docs/TOOLS.md).

## Separation and distribution
This repository is for **Hungry Shark World only**. The separate [Hungry Shark Evolution PS Vita project](https://github.com/VegettoSan/Hungry-Shark-Evolution-Ps-Vita) supplies methodology, **not source files, title ID, game assets or progression claims**.

The public repository intentionally does **not** contain APKs, OBBs, proprietary Unity data/DLLs, decompiled game code, Sony/Unity private platform binaries, credentials or unlicensed VPKs. Recovery outputs belong in ignored local folders. Original game content remains the property of its rights holders. Not affiliated with Ubisoft.
