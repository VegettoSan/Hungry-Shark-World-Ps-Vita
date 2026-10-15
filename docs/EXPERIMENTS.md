# Experiment journal — Hungry Shark World PS Vita

Use UTC timestamps. **VERIFIED**, **INFERRED**, **OWNER-REPORTED** and **UNTESTED** must not be conflated. Every actual run must record input hashes, tool/editor versions, commands/settings, sanitized evidence and next step. No private paths or copyrighted files.

| Date (UTC) | ID | Inputs/tools/command | Observed outcome | Evidence and next step |
| --- | --- | --- | --- | --- |
| 2026-10-15 | P00-001 | Owner-supplied 2.9.0/132 APK and main.132 OBB; Python stdlib SHA-256 + `zipfile.testzip()` | **VERIFIED PASS** both SHA-256 recorded in TECHNICAL_AUDIT; APK 769 ZIP entries/27,378,446 bytes, OBB 3,966 entries/92,431,553 bytes; 23 managed DLLs and `libmono.so`, no `libil2cpp.so`; Unity 2017.1.2p4 found in APK header | [Technical audit](TECHNICAL_AUDIT.md). **UNTESTED** Unity editor, source reconstruction or PSP2. Next: toolchain inventory and exact original Unity 2017 editor test |
| 2026-10-15 | P00-002 | Owner's Android installation of HSW 2.9.0 | **OWNER-REPORTED PLAYABLE** after in-app data download; not agent independently reproduced | Preserve Android original observations in upcoming P00 gameplay matrix; verify remaining downloaded/cache data before treating recovery complete |

## New-entry template

```text
YYYY-MM-DD HH:MM UTC | ID | SHA-256 APK/OBB; tools exact versions;
command/settings | VERIFIED PASS / FAIL / OWNER-REPORTED / UNTESTED |
sanitized log/screenshot/checkpoint reference; next action
```
