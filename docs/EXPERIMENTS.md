# Experiment journal — Hungry Shark World PS Vita

Use UTC timestamps. **VERIFIED**, **INFERRED**, **OWNER-REPORTED** and **UNTESTED** must not be conflated. Every actual run must record input hashes, tool/editor versions, commands/settings, sanitized evidence and next step. No private paths or copyrighted files.

| Date (UTC) | ID | Inputs/tools/command | Observed outcome | Evidence and next step |
| --- | --- | --- | --- | --- |
| 2026-10-15 | P00-001 | Owner-supplied 2.9.0/132 APK and main.132 OBB; Python stdlib SHA-256 + `zipfile.testzip()` | **VERIFIED PASS** both SHA-256 recorded in TECHNICAL_AUDIT; APK 769 ZIP entries/27,378,446 bytes, OBB 3,966 entries/92,431,553 bytes; 23 managed DLLs and `libmono.so`, no `libil2cpp.so`; Unity 2017.1.2p4 found in APK header | [Technical audit](TECHNICAL_AUDIT.md). **UNTESTED** Unity editor, source reconstruction or PSP2. Next: toolchain inventory and exact original Unity 2017 editor test |
| 2026-10-15 | P00-002 | Owner's Android installation of HSW 2.9.0 | **OWNER-REPORTED PLAYABLE** after in-app data download; not agent independently reproduced | Preserve Android original observations in upcoming P00 gameplay matrix; verify remaining downloaded/cache data before treating recovery complete |

## Excepción preparatoria autorizada — 2026-11-05 UTC

El propietario autorizó explícitamente extracción offline APK+OBB, recuperación
Mono/assets y preparación Unity 2017 sin Editor. No equivale a aprobación de fases.
`PHASE_GATES.json` permanece intacto, P00 ACTIVE y 0/13 aprobadas; trabajo en main,
sin modificar Evolution, instalar/ejecutar Unity, migrar ni preparar PSP2.

| Date (UTC) | ID | Inputs/tools/command | Observed outcome | Evidence and next step |
| --- | --- | --- | --- | --- |
| 2026-11-05 | PREP-RECOVERY-001 | APK `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d`; OBB `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72`; Python 3.14.4, verify_source_pair / prepare_private_recovery | **VERIFIED PASS** hashes/ZIP CRC, 4.735 entradas preservadas, 7 grupos/68 partes verificadas, 3.967 archivos Data, 23 DLL, 0 colisiones | [Procedimiento y límites](RECOVERY_UNITY2017_2026-11-05.md); manifiestos/checkpoints privados. Originales intactos |
| 2026-11-05 | PREP-RECOVERY-002 | AssetRipper 2.0.0+1ac666f, API localhost LoadFolder/Export/UnityProject; 2017.1.2p4, CSharp4, Level2/Hybrid, shaders YAML, unreadable assets conservados; dnSpyEx 6.6.0 | **VERIFIED** final de exportación, 23 escenas, 3.849 C# y 451 C# externos adicionales, 1.038 prefabs; proyecto privado preparado. Comparación de 3.961 métodos DLL sin cambios/añadidos. **STATIC_CHECK_ISSUES:** 2 scripts nulos de origen y 1 textura builtin vacía referenciada, preservados | Mismo informe; exportación intacta, copia preparada y evidencia privada. 16 referencias UI requieren Editor; **UNTESTED** importación, compilación, shaders, gameplay y contenido descargado adicional |
| 2026-11-05 | PREP-RECOVERY-ENV | Instalaciones locales reutilizadas; ejecución headless/API local | El primer proceso iniciado dentro del sandbox terminó sin servidor disponible; sockets localhost dieron WinError 10013. Reintento con ejecución local autorizada fuera del sandbox **PASS**. `dotnet --info` no pudo consultar Service Control Manager; no bloqueó AssetRipper/dnSpy. No hubo investigación ni descarga externa | Logs privados conservados; ninguna afirmación de PASS de Editor o gates por estos resultados |
| 2026-11-05 | PREP-RECOVERY-CHECKPOINT | Respaldo ZIP y comparación de hashes con exportación intacta | El ZIP y la comparación terminaron, pero la comprobación final de originales falló por rutas incorrectas guardadas por Path.resolve con entradas relativas en Windows/sandbox. Se corrigió únicamente la normalización del manifiesto y se revalidaron originales y ZIP existente, sin repetir extracción/exportación | Evidencia privada de corrección, integridad y checkpoint final; no se descartó el fallo anterior |

## Reparación de compilación autorizada — 2026-11-05 UTC

| Date (UTC) | ID | Inputs/tools/command | Observed outcome | Evidence and next step |
| --- | --- | --- | --- | --- |
| 2026-11-05 | COMPILE-2017-001 | Excepción expresa del propietario para reparar compilación; mismos SHA APK/OBB de PREP-RECOVERY-001; Unity 2017.1.2p4 / mcs C#4, dnSpyEx 6.6.0/dnlib y Python 3.14.4; response file real con salida privada; refresh en instancia existente | **VERIFIED PASS C#:** 39 errores iniciales corregidos en 6 scripts, 0 errores al compilar y recargar en Editor; 491 warnings principales conservados. 1.645 casos diferenciales idénticos al original, 0 excepciones. Dos assertions nativas de red preexistentes, no repetidas al recompilar, siguen pendientes | [Diagnóstico, cambios y límites](UNITY2017_FIRST_COMPILER_REPAIR_2026-11-05.md); evidencia privada CompileRepair01. Sin cambios de GUID, prefabs, gameplay, Evolution o gates; P00 ACTIVE / 0 aprobadas. Compilar no acredita funcionamiento |

## Reparación local de shaders y ejecución autorizada — 2026-11-05 UTC

| Date (UTC) | ID | Inputs/tools/command | Observed outcome | Evidence and next step |
| --- | --- | --- | --- | --- |
| 2026-11-05 | RUNTIME-SHADER-001 | Excepción expresa del propietario; mismos SHA APK/OBB de PREP-RECOVERY-001; Python 3.14.4, dnSpyEx 6.6.0/dnlib, programas GLES originales y Unity 2017.1.2p4 Direct3D11; traducción privada conservando GUID/fileID y estados; HSW Recovery/Audit + Probe shader passes | **VERIFIED:** 96 shaders reconstruidos y uno provisional, 428 materiales revisados, 374 pruebas pass/keyword sin fallos, 0 errores de shader y 63 warnings; 334 propiedades presentes. 563 referencias cambian únicamente tipo de importador. Cuatro pruebas de render UI PASS. **LIMITED:** un BlackSilhouette y nueve passes Meta requieren fidelidad posterior; no equivale a prueba visual de todos los efectos | [Causas, procedimiento y límites](UNITY2017_SHADER_RUNTIME_REPAIR_2026-11-05.md), evidencia privada RuntimeShaderRepair01; comparar Android, no rebake de GI todavía |
| 2026-11-05 | RUNTIME-EDITOR-001 | Mismos inputs, misma instancia Editor; adaptadores UNITY_EDITOR Native/AppsFlyer/DeepLink/teléfono/MoPub, tres renombres TextAsset preservando bytes, catálogo original528; mcs C#4 response files reales con salida separada; dos Play desde BootLoader25s | **VERIFIED:** 0 errores C# en firstpass/principal/Editor y ramas Android aisladas; JNI eliminado en los recorridos probados, 0 excepciones en dos arranques de seis escenas hasta FrontEnd/3D/Sharks. Captura de menú renderizado. No prueba automática de Splash/edad, gameplay completo o player Android | Mismo informe; logs y Before preservados. 51 recursos de catálogo ausentes, WallHackTexture no recuperado, dos scripts nulos y una Font Texture original siguen pendientes. Sin cambios de gates, Evolution o Vita |
| 2026-11-05 | RUNTIME-ITERATIONS | Iteraciones de traducción, refresh/compilación y pruebas Play; Unity2017 Mono Windows | **FAIL conservados:** variantes iniciales con matrices/MRT/Meta, DriveInfo no implementado, JNI subsiguiente DeepLink/teléfono/MoPub, catálogo vacío tras domain reload, CaptureScreenshot CS0619, define Android vacío y pruebas con ensamblado anterior. Se corrigieron causas concretas y repitieron ensayos; refresh síncrono desde Update retirado. Escape detuvo la UI al finalizar; cola temporal cancelada | Evidencia privada por iteración y ensayos Play01–05; los PASS finales no borran el historial. Siguiente paso: validación manual de partida, guardado y fidelidad visual |

## New-entry template

```text
YYYY-MM-DD HH:MM UTC | ID | SHA-256 APK/OBB; tools exact versions;
command/settings | VERIFIED PASS / FAIL / OWNER-REPORTED / UNTESTED |
sanitized log/screenshot/checkpoint reference; next action
```
