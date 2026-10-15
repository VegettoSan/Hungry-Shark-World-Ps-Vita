# End-to-end gated plan — Hungry Shark World PS Vita

Authoritative state: [PHASE_GATES.json](PHASE_GATES.json). Validator: `python tools/check_phase_gates.py`.
**2026-10-15: P00 ACTIVE; 0/13 phases APPROVED. P01–P12 LOCKED.**

## Invariants

The original data pair is **HSW 2.9.0 versionCode 132 APK + matching main.132 OBB**. Start with Unity **2017.1.2p4 Mono**; achieve and freeze a tested original-editor **desktop** baseline; clone/migrate to Unity **2018.2.19f1**; validate **equivalent desktop gameplay**; verify PSP2 and then **physical Vita**. Do not port Android native `.so` files directly. A playable original Android install has been reported by the owner, not independently tested here.

**Owner approval** is necessary **between every phase**. Format: `ACTIVE` → `AWAITING_APPROVAL` after passing evidence → `APPROVED` only with VegettoSan's explicit issue/PR approval → next phase `ACTIVE`. A failed gate remains `BLOCKED`, with a documented corrective plan. Never auto-approve, skip or silently modify acceptance criteria. No work in future phases without explicit limited exception from the owner; an exception is not phase approval.

Acceptance proofs: source APK+OBB hashes, exact editor/tool versions, steps/settings, sanitized logs, PASS/FAIL case matrix, preservation/regression evidence, and GitHub issue/PR approval. Two independent evidence references in the ledger for any APPROVED gate. CI checks the **ledger structure**, not whether the claimed test actually happened.

Owner-approved **testing format inherited from Evolution:** desktop gameplay evidence may be gathered via **Unity Editor Play Mode** instead of a standalone Windows build; that does not waive the full gameplay matrix, cold save/load, reproducibility, parity or owner approval.

## Strict phases

| ID | Milestone | Acceptance gate |
| --- | --- | --- |
| **P00** ACTIVE | Source pair audit and original Unity editor environment | APK/OBB SHA-256+ZIP verified; editor 2017.1.2p4 opens/runs blank scene; original Android reference gameplay matrix and tool inventory logged |
| P01 LOCKED | Full private assets and managed code recovery | Joint APK+OBB recovery; all numeric `.splitN` groups reconstructed; AssetRipper / DLL inventory; GUID/fileID & missing script report |
| P02 LOCKED | Buildable recovered Unity 2017 editor project | Editor opens, clean compilation or fully accounted targeted errors; original scenes/scripts linked with recorded remaps |
| P03 LOCKED | Actual Unity 2017 desktop gameplay | Menu, camera, shark movement, feeding, health/death, audio, UI, loads, shop/progression and representative levels in PC Play Mode; Android comparison |
| P04 LOCKED | Frozen original-engine baseline | Reproducible clean import, cold save/load, stable editor gameplay regression, owner approval and immutable checkpoint |
| P05 LOCKED | Controlled clone migration to Unity 2018.2 | Only cloned project upgraded; all API/script/shader/platform issues traced; no undocumented gameplay rewrites |
| P06 LOCKED | Unity 2018.2 desktop gameplay parity | Repeat P03/P04 matrix; compare visuals, gameplay, loads, saves, audio and scene behavior |
| P07 LOCKED | Independent PSP2 toolchain smoke test | Real PSP2 build module verified; lawful minimal test app boots on physical Vita; log filesystem/runtime paths |
| P08 LOCKED | World Vita boot and menus | Actual World scene/menus render on physical Vita; no fake splash-only success |
| P09 LOCKED | World Vita core gameplay | Shark movement, feeding, enemies, health/death, level transitions, progression on physical Vita |
| P10 LOCKED | Controls, audio, saves and lifecycle | Vita buttons/analog mapping, audio, suspend/resume, save/load and offline flows verified |
| P11 LOCKED | Vita performance and stability | Profile CPU/GPU/memory; measured stable gameplay target ~30 FPS, optional 60; longer repeatable sessions |
| P12 LOCKED | Release readiness | Device regression, data installation/extractor/patch strategy, legality, user docs and maintainable packaging validated |

## Scope and non-goals

- Keep *World* entirely separate from *Evolution* (different game/package/engine baseline/assets, Title ID and release). World **`HGSKW1178`** / **Hungry Shark World Vita** is owner-selected; Evolution **`HGSKE1178`** must never be reused. Planned World title location: `ux0:app/HGSKW1178/`; verify actual PSP2 layout later. Identity approval is not a phase-gate approval.
- Use Mono `Assembly-CSharp.dll` plus Unity serialized data, but do not assume automatic full source recovery.
- Avoid Android JNI/FalsoJNI/VitaGL loader speculation as substitute for the **native Unity PSP2 player** route.
- Do not mix the 3.0.2 APK with 2.9.0 OBB without independent compatibility evidence.
- Do not release original copyrighted assets, DLLs, APK, OBB or restricted platform toolchains.
- All blocked paths, workarounds and owner-requested exceptions belong in [EXPERIMENTS](EXPERIMENTS.md). 
