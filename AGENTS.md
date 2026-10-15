# Mandatory instructions for Codex, agents and contributors

Scope: **the entire Hungry Shark World PS Vita repository**. Read in order:
1. [PORTING_PLAN](docs/PORTING_PLAN.md) and [PHASE_GATES](docs/PHASE_GATES.json).
2. [TECHNICAL_AUDIT](docs/TECHNICAL_AUDIT.md), [EXPERIMENTS](docs/EXPERIMENTS.md), [DATA_EXTRACTION_AND_LAYOUT](docs/DATA_EXTRACTION_AND_LAYOUT.md).
3. [TOOLS](docs/TOOLS.md). Check the local ignored `Tool Codex/` inventory before downloading or installing anything.
4. Run `python tools/check_phase_gates.py` before and after any ledger change. **Do not silently change gates.**

## Locked, sequential methodology
- **P00 is ACTIVE**; P01–P12 are LOCKED. No source recovery, gameplay repair, Unity 2018 migration, PSP2 port or release packaging outside the approved phase scope.
- The owner **VegettoSan** alone approves phase transitions, explicitly and with a GitHub issue/PR reference, two evidence references and UTC timestamp. Assistant confidence, silence, compilation and CI success are not owner approval.
- Labels are **VERIFIED** (direct evidence), **INFERRED** (reasoned), **UNTESTED** (not run). A successful ZIP check is not successful gameplay.
- Failed work stays recorded as FAIL/BLOCKED; never rewrite history to claim PASS. Use small, topical commits, reversible local checkpoints and proof-oriented diffs.
- Record every meaningful experiment (including failures) in [EXPERIMENTS](docs/EXPERIMENTS.md): UTC date, input hashes, tool/editor versions, exact command/settings, actual outcome, sanitized evidence, next step.
- Do not silently weaken tests or bypass gate locks. Narrow corrective work needs explicit owner authorization if outside the active phase.

## Original game and recovery priorities
- Main baseline **Hungry Shark World 2.9.0 (132), Unity 2017.1.2p4, Mono**, **APK + versionCode 132 OBB**. Verify BOTH SHA-256 hashes and ZIP CRC first. Android playability was reported by the owner; editor/Vita are UNTESTED.
- Input `Assembly-CSharp.dll` and other Managed assemblies are **private reverse-engineering inputs**, not GitHub release assets. Recovered C# is not original Unity source and does not prove complete recovery.
- Reassemble `.splitN` pieces strictly by numeric suffix; merge `assets/bin/Data/` from APK and OBB, refusing collisions unless bytes/hash are identical. Never assume `levelN` filenames correspond to selectable game levels.
- Recover scripts/MonoBehaviours, GUIDs, fileIDs, namespaces, types, serialized fields, scene/build ordering and asset dependencies. Maintain original graph and log intentional remaps.
- **Original engine first:** actual Unity **2017.1.2p4** desktop gameplay + cold save/load + regression checks must pass and be **approved** before the migration clone into **2018.2.19f1**. Never upgrade the only baseline copy.
- Preserve original controls, shark stats, spawning, physics, AI, progression, saves, audio, visuals and scene behavior. No unrelated rewrites, bulk deletion, speculative optimizations or placeholder mechanics.
- Isolate Android-only APIs (ads, billing, platform services, Java/JNI, data downloads) behind tightly scoped adapters only when an evidenced failure requires it; do not blanket-delete classes.
- Unity 2018 PSP2 player/module **must be verified independently**; an editor installation or a previous Halo 2D build does not prove the module is installed. Android `libunity.so`/`libmono.so` cannot simply run as Vita native binaries.
- Unity 2018.2.19f1 is the **preferred** Vita-target editor from the owner's Halo 2D reference. Do not silently replace with Unity 2018.3+; 2018.3 dropped the legacy PSP2 target.
- For real-device tests, target stable ~30 FPS; consider 60 only if physically measured. No FPS claims from editor-only tests. Gameplay first, optimizations only in P11.
- **Owner-selected PS Vita identity (2026-10-15):** Title ID **`HGSKW1178`**; display name **Hungry Shark World Vita**. The canonical values are in [`config/port_identity.json`](config/port_identity.json); planned installed title path is `ux0:app/HGSKW1178/` (runtime `app0:`; actual PSP2 packaging/path behavior still UNTESTED). Never reuse Evolution's `HGSKE1178` or Halo 2D identity. Identity selection **does not approve or unlock a phase**.

## Git hygiene, provenance and release
- Keep all raw APK/OBB, exported Unity project, original/decompiled DLL/C# code, proprietary assets, tool binaries and SDK materials private and ignored. Never expose identifying personal machine paths or keys in logs.
- Public repo may contain only reproducible, legally shareable **instructions, scripts, tests, structured audit data and sanitized results**.
- Do not upload copyrighted game files, Sony/Unity restricted binaries or private signing material to Actions. Do not rely on a copyright-containing automatic download from CI.
- Keep **developer project recovery** separate from any **future end-user asset extractor**. Android asset files/OBB are not drop-in PSP2 runtime data.
- **Do not announce a playable Vita build or publish VPK** without verified physical Vita behavior, proper source-to-target asset path evidence and distribution-rights review.
- Any release/extractor/patch workflow remains LOCKED through P12.
