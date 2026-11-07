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

## Reparación local de entrada y UI autorizada — 2026-11-05 UTC

| Date (UTC) | ID | Inputs/tools/command | Observed outcome | Evidence and next step |
| --- | --- | --- | --- | --- |
| 2026-11-05 | INPUT-UI-001 | Excepción expresa del propietario; mismos SHA APK/OBB de PREP-RECOVERY-001, DLL originales; Unity 2017.1.2p4, mcs C#4, dnSpyEx 6.6.0/dnlib, Python 3.14.4; inspección NGUI/InControl + clic real antes/después en instancia existente | **VERIFIED:** RAW_MOUSE no producía eventos; ProcessFakeTouches original sin callers, cámara móvil sin mouse. Ruta original conectada solo en Editor. Opciones, slider y About responden con press/release/click únicos en los casos registrados. Principal/Editor/rama Android compilan sin errores. Metas preservados y comparación de IL Android | [Causas y límites](UNITY2017_INPUT_UI_REPAIR_2026-11-05.md); evidencia privada InputRepair01. Sin cambios de fases, escenas/prefabs o Evolution |
| 2026-11-05 | INPUT-XBOX-001 | Xbox conectado por propietario; perfil original Xbox360WinProfile; observador pasivo NGUI/InControl/VirtualPad; InputManager224/200 ejes; prueba manual de menús y partida | **VERIFIED:** perfil, stick, A/B, liberaciones, navegación y retorno a cero. D-Pad derecho llega a Direction pero no a VirtualPad, según ruta original. Captura/snapshot de gameplay Hawaii con stick y boost entregados/liberados, sin errores en ese intervalo. **OWNER-REPORTED:** resaltados de Ajustes y selector recuperados, incluida Información tras reparar su target compartido. 231 targets TV originales conectados por UIButtonColor/UIButton identificados | Mismo informe; no se inventaron resaltados, navegador o bindings Vita. Start, pausa/reanudar y cobertura completa pendientes. Una incidencia audio al detener una sesión anterior queda registrada, sin ocultarla |
| 2026-11-05 | INPUT-TOOLS-001 | Observador temporal y lectura YAML; misma instancia Editor | **FAIL preservados:** CS1061 por miembro no público retirado del observador; lectura YAML con encoding Windows falló, repetida en UTF-8. Compilaciones finales PASS. Gestos automatizados demasiado rápidos fueron clicks, no prueba de drag sostenido. Escape físico detuvo UI; propietario confirmó después ambos resaltados reparados. Registro físico adicional Start/Back con pulsación/liberación, sin inferir una asignación de pausa | Logs privados; no inferir PASS de interacciones no observadas ni borrar el historial |
| 2026-11-05 | INPUT-PAUSE-CURSOR-001 | Prueba manual Hawaii por propietario y señales Xbox/teclado; mismos inputs/motor; revisión de UICamera.currentKey, GameStateMachine, CustomInputCamera y órdenes originales -900/-462/-5/0 | **OWNER-REPORTED FAIL inicial:** mouse bloqueado tras mando, Escape abre/cierra pausa y Start no la activa. **VERIFIED:** cursor bloqueado por scheme; Escape duplicado como Action2; HUD/Butt_pause ligado a B. Reparación Editor del cursor y consumo por dispositivo/UpdateTick, 0 errores al compilar. **VERIFIED y OWNER-REPORTED PASS posterior:** Escape/B/mouse pausan y reanudan, con una transición por pulsación. Start no reasignado | Mismo informe y transiciones por frame privadas. Observador detuvo una partida al vencer su plazo; corregido para detener únicamente la grabación. Se preservan errores de audio/destrucción al salir de Play |
| 2026-11-05 | INPUT-MODAL-001 | Diálogo mapa dejado abierto por propietario; inspección del prefab original, UIKeyNavigation.Start y snapshot de foco, sin confirmar compra | **OWNER-REPORTED FAIL inicial:** mando no controla ese diálogo. **VERIFIED:** foco retenido en UI anterior; botones con startsSelected y enlaces explícitos, Start condicionado a TV. Restaurada esa inicialización, sin nuevo navegador; compilaciones PASS. **OWNER-REPORTED PASS posterior:** diálogo responde al mando. Auditoría de56 prefabs/324 nodos/111 defaults/0 enlaces rotos;46 prefabs configurados y31 consumidores del MessageBox común | Mismo informe; callbacks/economía intactos. Dos ventanas/add-ons sin default y tres sin navegación inventariados; no se declara prueba física completa |
| 2026-11-05 | INPUT-PORTABLE-001 | Instrucción adicional del propietario: las reparaciones comunes deben servir al futuro destino Vita; mismas herramientas y motor, macros genéricas no Android/iOS; compilación aislada del principal sin UNITY_EDITOR ni UnityEditor.dll | **VERIFIED:** lógica UI/input común compila también fuera del Editor, 0 errores; Android conserva IL de las8 clases y metas. Se filtra foco con collider deshabilitado usando el fallback NGUI existente. Mouse simulado, cursor Windows y servicios Editor siguen aislados. Guarda de existencia en OptionsIngamePopup.OnDisable tras NRE real al destruir InputControlManager, compilada y pendiente de repetir cierre. **UNTESTED:** player PSP2, perfiles físicos y servicios nativos del futuro port | Mismo informe y pruebas privadas. Sin APIs/bindings PSP2, migración2018 o aprobación de fases; respaldo final privado CRC verificado |

## Excepción de migración y preparación PSP2 — 2026-11-05 UTC

Autorización explícita del propietario: copia privada Unity2018, incompatibilidades,
servicios offline y entrada PSP2. No aprueba fases. Inputs SHA-256 APK/OBB idénticos
a los registrados arriba y en PHASE_GATES; sin nueva extracción ni descargas.

| Fecha UTC | ID | Herramientas y procedimiento | Resultado real | Evidencia y siguiente paso |
| --- | --- | --- | --- | --- |
| 2026-11-05 | MIG18-COMPILER-001 | Unity 2018.2.19f1 instalado, Mono/mcs local; RSP real del Editor; perfil original .NET2 Subset/C#4; UnityUtil/MathUtil/MemDump | **FAIL inicial preservado:** OSXDashboardPlayer retirado; después sintaxis Quaternion y enums ATC obsoletos. **VERIFIED PASS final:** 118/3737/4 fuentes Editor, 0 errores; 81/519/0 warnings. Se conservan formatos ATC e identidades de plataforma vigentes | [Informe](UNITY2018_MIGRATION_PSP2_PREP_2026-11-05.md); logs privados Compile/editor y reload del Editor |
| 2026-11-05 | MIG18-PLAY-001 | Única instancia Editor, Xbox del propietario, flujo original hasta Hawaii; copia2017 protegida | **VERIFIED:** gameplay visible, input y sin cascada de excepciones durante intervalo registrado. **OWNER-REPORTED:** animación/audio/pausa sin problemas visibles. **FAIL al salir:** Destroy Transform del wake y CullingGroup sin Dispose; este último conectado a DeInit al retirar último componente, pendiente repetir cierre | Mismo informe; no se declara cobertura de todas las escenas ni cold save/load |
| 2026-11-05 | MIG18-RENDER-001 | Auditor nativo ShaderUtil/SetPass, DX11, definiciones heredadas y pruebas de píxel, Unity2018 | **VERIFIED PASS:** 97 shaders/428 materiales, 0 missing/unsupported, 374 pases sin fallo, UI 4/4. Re-serialización de un campo nulo de material por Unity sin cambio visual. **UNTESTED:** compilador GPU PSP2 | ShaderProbe2018.json/UI_RenderChecks.json privados; mismas limitaciones de recuperación2017 |
| 2026-11-05 | MIG18-OFFLINE-001 | Compilación con UNITY_PSP2 sin UNITY_EDITOR/UnityEditor, módulos locales PSP2; NativeBinding/proveedores Null/Billing/Request/certificado Android | **VERIFIED:** 118/3737 fuentes, 0 errores, sin referencia Facebook.Unity.Android en esta compilación. 27 aserciones ejecutadas con Mono host: error/indisponible, callbacks únicos/diferidos, sin compra/auth/recompensa ficticia, sin mutación save de notificaciones. **UNTESTED:** ejecución de player PSP2, SDK directo por rutas futuras | Compile/psp2 y ContractProbe privados; runner host usa fallback runtime4, no demuestra runtime Vita |
| 2026-11-05 | MIG18-INPUT-001 | Manual del módulo instalado; perfil PSP2 preferido conservando59 originales; delegate NGUI original, GameInput/VirtualPad | **VERIFIED lógico:** D-Pad en eje NGUI, Start separado de Action1/2, Rboost press/hold/release y neutral. 60 perfiles player/59 Editor, InputManager224 intacto. **UNTESTED:** índices/signo/deadzone físicos, pause contextual, touch y cada modal en Vita | Mismo informe; sin copiar índices de Evolution/Halo, sin nuevo navegador/controlador |
| 2026-11-05 | MIG18-INTEGRITY-001 | SHA256 de20.869 archivos 2017, auditor YAML, backup privado de16 archivos locales (2.209.830bytes) CRC, rama main | **VERIFIED:** 2017 sin cambios ni archivos nuevos; 23 escenas de build correctas, sin metas/GUID nuevos rotos. Heredados1 referencia interna Font y2 scripts nulos. Save solo respaldado, no convertido. Fases0/13 intactas | Unity2017_Protection_Result/StaticReferences2018 y checkpoint privados; falta cold save/load y hardware |
| 2026-11-05 | MIG18-PROBES-001 | Runner privado y probe PluginImporter en Editor existente | **FAIL preservados y corregidos:** filtro de fuentes excluía FGOL/Plugins/CP2; RSP antiguo omitía fuentes nuevas; comentario cerraba llave generada; fixture duplicaba referencias framework, usaba constructor privado y ruta incorrecta CoreModule; reflexión ambigua del overload de PluginImporter. No eran fallos de gameplay. Exclusión de plugin mediante YAML no bastó; comprobar API del Editor | Iteration logs privados y PlatformProbe; no borrar historial ni confundir compilación con prueba de player |

| 2026-11-05 07:49 UTC | MIG18-FINAL-BOOT-001 | Unity2018 instancia existente; bridge temporal privado `playboot:FinalBoot2018.json`, 25s, sin segunda instancia; API PluginImporter | **VERIFIED PASS:** 25,47s/645frames, flujo original hasta FrontEnd/3DBackground/Sharks, 0 errores registrados y consola final0. Any=true/excludePSP2=true/excludeAndroid=false. No prueba GPU/player Vita ni cierre tras gameplay | FinalBoot2018 y Platform2018 privados. Observadores desactivados al terminar; continuidad manual desde SplashLoader |

## Primer VPK PSP2 privado autorizado — 2026-11-05 UTC

Excepción expresa del propietario para compilar y empaquetar una prueba privada.
No aprueba fases ni distribución: main, P00 ACTIVE y 0/13 aprobaciones; ledger intacto.
Mismos inputs verificados: APK `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d`
y OBB `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72`.
Unity **2018.2.19f1 / PSP2 Mono2x**, .NET2 Subset, Development, SDK y herramientas locales;
sin descargas, publicación, nueva rama, modificación de Evolution o instalación en Vita.

| Fecha UTC | ID | Procedimiento | Resultado real y evidencia privada |
| --- | --- | --- | --- |
| 2026-11-05 | VPK01-PREP | Checkpoint de configuración, 23 escenas originales; copia privada Unity2018; API del módulo y plugins | **VERIFIED:** PSP2 soportado, Mono2x, perfil/bindings PSP2 y proveedores offline. Unity2017: 20.869 hashes sin cambios. Bloqueo temporal de escrituras de procesos llevó a usar copia privada de build en C:, sin atribuir fallo físico a E: |
| 2026-11-05 | VPK01-FAILURES | Builds01–04, mismos recursos, correcciones dirigidas | **FAIL preservados:** lightmap ETC1; cuota de save cero; Content ID inválido por formato/longitud. Algunos fallos del postproceso retornaron Succeeded con un error: no se cuentan como PASS. Cuota 8192KB con margen sobre respaldo World de 2.209.830bytes; ID técnico nativo validado antes del build |
| 2026-11-05 | VPK01-TEXTURES | Reimportación PSP2 de 426 PNG con caché BC7; único lightmap NativeFormatImporter ETC1 decodificado a RGBA32 | **VERIFIED:** sin cambios de GUID o propiedades de iluminación, 2048x2048/12 mips; decodificación sin pérdida adicional, +18,67MiB de payload. No se borró contenido ni se sustituyeron shaders. 480 texturas del player: cero BC7/ETC1 |
| 2026-11-05 | VPK01-AUDIO | Player05 compiló sin errores; auditoría nativa detectó 424 Vorbis pese al fallback HEVAG de API. Overrides PSP2 explícitos y reimportación localizada | **FAIL de preparación de audio en Player05**, conservado. **VERIFIED final:** 424 HEVAG, frecuencia/canales/duración/loadType idénticos y recursos resueltos; defaults y GUID conservados, solo overrides PSP2 y reserialización del importador. OGG originales intactos |
| 2026-11-05 08:44 UTC | VPK01-BUILD | Build06: `-batchmode -quit -buildTarget PSP2 -projectPath <copia_privada_2018> -executeMethod HSWFirstVitaBuild.Build -logFile <privado>` | **VERIFIED PASS:** Succeeded, 0 errores, 602 warnings, 3:07.474 de BuildPipeline. 23 escenas serializadas en orden, arranque SplashLoader; 140 shaders/245 passes, programas ConsoleVS/ConsoleFS. Warnings deferred de Wiggler conservados; fidelidad en hardware UNTESTED |
| 2026-11-05 | VPK01-PACKAGE | SELF nativo y runtime completos; procedimiento local de empaquetado, ajuste exclusivo de SFO al ID del propietario | **VERIFIED PASS integridad:** `224906503` bytes, 291 entradas, ZIP/CRC y hashes de runtime PASS, SHA256 `4180fb1eaefae3b5ec3351d49cc2efd47aee998e05d34e0dd9768e25daab9d36`. TITLE_ID **HGSKW1178**, APP_VER **00.01**. El módulo AOT mantiene su ID técnico de generación como la referencia Evolution; no se parchea su binario. No demuestra ejecución en hardware |

Evidencia ignorada: `local-work/HSW_Recovery/Reports/PSP2_FirstVPK_01`:
Build01–06, checkpoints antes/después, NativeResourceVerification, Final_Managed,
Final_SourcePreservation, PackageReceipt/Manifest, FinalLocalDelivery e instrucciones privadas.
Copia PSP2 permanente: `local-work/HSW_Recovery/HSW290_Unity2018_PSP2_Private01`.
La base Unity2018 conserva su configuración previa; ningún gate cambió.
Sin expansión de memoria; perfil PSP2 original Medium conservado, sin forzar FPS/resolución.
Logger mínimo de Development, sin overlay ni supresión de excepciones, destinado a
`ux0:data/HGSKW1178/first_boot.log`; su escritura en Vita también es UNTESTED.
**Pendiente físico:** arranque, menús, botones/touch, audio, gameplay, save/load, memoria,
rendimiento y suspensión. Persisten los límites heredados de recuperación, incluido catálogo
incompleto y shader provisional. Siguiente paso: instalación manual privada, conservar log y
cualquier código/volcado de cierre. No es versión pública ni certificación de port jugable.

## Primer crash físico y corrección del player — 2026-11-05 UTC

| Fecha UTC | ID | Evidencia y cambio | Resultado real |
| --- | --- | --- | --- |
| 2026-11-05 | VPK02-CRASH | Dump SHA256 `618e9e2c6f0259e4bcbd2c97eac57e094db0be65a173358e305f85c8d873fabb`; símbolos exactos 00.01 y herramienta SDK local | **VERIFIED FAIL de arranque 00.01:** Unity_main_thread PC=0, LR=0x81e89c9d en InitializeGXM +0x9a, llamada sceRazorGpuCaptureEnableSalvage. Mono/AOT ya cargados; Razor ausente entre módulos. **OWNER-REPORTED:** solo imagen inicial/LiveArea. No se atribuye a OOM/audio/texturas ni se cambia expansión de memoria |
| 2026-11-05 09:15 UTC | VPK02-NORMAL | BuildOptions.None, logger propio bajo HSW_PSP2_BOOT_LOG, APP_VER 00.02; mismo Unity2018 PSP2 Mono2x y recursos | **VERIFIED PASS compilación:** 0 errores/602 warnings, 3:06.498. Player normal coincide con plantilla instalada; InitializeGXM omite Razor. 23 escenas, 480 texturas compatibles, 424 HEVAG y proveedores/perfil PSP2 verificados. Sin eliminación de contenido o cambios de calidad/memoria |
| 2026-11-05 | VPK02-PACKAGE | Empaquetado privado, SFO HGSKW1178/00.02 | **PASS integridad:** 179698719 bytes, 284 entradas, CRC/runtime hashes. SHA256 `9e0f3b10e978d3e782a8738f51e28fcff6ca47bb2bf5f62acd876e6dcda5a1e1`. **UNTESTED:** arranque y funcionamiento físico de 00.02; instalar manualmente y conservar nuevo dump/log si falla |

Evidencia ignorada: `local-work/HSW_Recovery/Reports/PSP2_Crash01`.
00.01 y sus resultados anteriores se conservan; no se reescribe su historia.
Base Unity2018, Unity2017 y Evolution intactos. P00 ACTIVE, 0/13 aprobaciones;
sin cambio de ledger, distribución ni instalación automática.

## Segundo VPK físico y tercer ensayo autorizado — 2026-11-07 UTC

Excepción expresa del propietario en el encargo actual para investigar/corregir,
validar Editor y generar VPK 3 privado; no aprueba fases. Se preserva el cambio del
player normal de VPK 2, la base Unity2017 y Evolution; sin ramas nuevas ni descargas.
Mismos inputs APK/OBB SHA-256 registrados en PREP-RECOVERY-001.

| Fecha UTC | ID | Evidencia/procedimiento | Resultado real |
| --- | --- | --- | --- |
| 2026-11-07 | VPK02-HARDWARE-UPDATE | Aclaración expresa del propietario en este chat, vigente sobre la mención contradictoria a VPK1 | **OWNER-REPORTED:** VPK2/00.02 supera crash inicial, muestra primera escena/carga y vuelve a LiveArea sin crash visible, PSVShell >100 FPS y UI anormal. CapUnlocker activo tras reinicio completo, confirmado. No se recibió nuevo dump/log; cierre todavía **NO DIAGNOSTICADO**. No es evidencia de repetición del crash Razor 00.01. |
| 2026-11-07 | VPK03-RESEARCH | Lectura local D03/D04/D05/BlackScreen/CapUnlocker Evolution y guía de lecciones World; contraste con registros/paquetes/código World existentes | **VERIFIED estático:** conservar BuildOptions.None; audio424HEVAG y adaptaciones offline existentes; World tiene selector de calidad propio y VSync0. **Sin evidencia** para ExpandBy109MB o eliminación de recursos. [Comparación y procedimiento de prueba](PSP2_VPK03_LOADING_DIAGNOSTICS_2026-11-07.md). Resultados de ejecución se añaden al completar; hardware00.03 UNTESTED. |
| 2026-11-07 | VPK03-EDITOR | Unity2018.2.19f1 PSP2 seleccionado; dos Play35s, SplashLoader y prueba aislada BootLoader; mismos inputs SHA indicados arriba | **VERIFIED:** límite60/VSync1 en cinco calidades, reloj intacto; Splash0 errores sin avanzar/interacción; BootLoader llegó FrontEnd/3DBackground/Sharks con **6 errores Editor** auth/DNA/red documentados. No equivale a PASS limpio ni a PSP2; exclusión DNA ya existente del player conservada. Logs privados separados. |
| 2026-11-07 | VPK03-BUILD | `-batchmode -quit -buildTarget PSP2 -projectPath <copia_privada> -executeMethod HSWFirstVitaBuild.Build -logFile <privado>`; BuildOptions.None, memoriaNone, diagnóstico propio | **VERIFIED PASS:** 0errores/602warnings, 4:45,410. SELF normal exacto, 18 checks IL/64 marcadores, 23escenas/480texturas/424HEVAG/140shaders245passes conservados. Sin reconversión/reimportación. Fuente original2017/base2018, escenas/assets/metas intactos; comparación de serializados y diferencias opacas de blobs generados documentada, sin patch. |
| 2026-11-07 | VPK03-PACKAGE | HGSKW1178/00.03, empaquetado privado y copia local verificada | **PASS integridad:**179708740bytes,284entradas,CRC/runtime hashes; SHA256 `5669eff27fb2accae45628111a80ee118dae6f3bfbd9f196ce2d3a244ca5b1f9`. VPK1/VPK2 intactos. **UNTESTED hardware**; cierreVPK2 sin diagnóstico confirmado. Evidencia `Reports/PSP2_VPK03`, [informe y prueba física](PSP2_VPK03_LOADING_DIAGNOSTICS_2026-11-07.md). P00 ACTIVE,0aprobaciones,ledger intacto. |

## New-entry template

```text
YYYY-MM-DD HH:MM UTC | ID | SHA-256 APK/OBB; tools exact versions;
command/settings | VERIFIED PASS / FAIL / OWNER-REPORTED / UNTESTED |
sanitized log/screenshot/checkpoint reference; next action
```
