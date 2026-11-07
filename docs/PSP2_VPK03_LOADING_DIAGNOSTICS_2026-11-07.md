# World: VPK 2 físico y preparación del VPK 3

Registro UTC 2026-11-07 (6 de noviembre en Colombia). Autorización expresa del
propietario en este encargo: investigar, corregir con evidencia, validar en Editor y
generar un tercer VPK **privado**, usando exclusivamente la copia Unity 2018.
No aprueba fases: P00 ACTIVE, 0/13 aprobadas; ledger intacto, rama existente main.

## Identificación de pruebas

La aclaración inicial del propietario sustituye la mención contradictoria a
«primer VPK» incluida después en el mismo mensaje. El ensayo físico actual es el
**segundo VPK**. No se reinterpreta su cierre como repetición del primer crash.
Los hashes identifican los artefactos locales; no se ha vuelto a medir el paquete
instalado desde la consola.

| Ensayo | Identidad / SHA-256 | Resultado real |
| --- | --- | --- |
| VPK 1 | HGSKW1178 / 00.01; `4180fb1eaefae3b5ec3351d49cc2efd47aee998e05d34e0dd9768e25daab9d36` | **OWNER-REPORTED FAIL:** crash al iniciar. **VERIFIED dump:** PC=0, LR en InitializeGXM, llamada sceRazorGpuCaptureEnableSalvage; player Development. |
| VPK 2 | HGSKW1178 / 00.02; `9e0f3b10e978d3e782a8738f51e28fcff6ca47bb2bf5f62acd876e6dcda5a1e1` | **OWNER-REPORTED:** desaparece el crash inicial; primera escena, pantalla de carga y regreso a LiveArea sin crash visible; PSVShell >100 FPS y movimiento anormal de UI. CapUnlocker activo tras reinicio completo, confirmado por el propietario. |
| VPK 3 | HGSKW1178 / 00.03 | Nuevo ensayo de presentación y diagnóstico; resultados de preparación se añaden abajo. Ejecución física **UNTESTED**. |

No se ha recibido un dump/log **del VPK 2** en este encargo. Tiempo hasta cierre,
última operación completada, memoria libre y mecanismo de salida: **pendientes de
confirmar**. La ausencia de crash visible no demuestra salida voluntaria ni OOM.
No reutilizar el dump de 00.01 para diagnosticar 00.02.

## Mejora del VPK 2 que se conserva

`EXPERIMENTS.md`, sección de corrección del player, y evidencia privada
`Reports/PSP2_Crash01`: `Correction_Settings.json`, `NormalPlayer_Verification.json`,
`SymbolizedStack.json`, disassembly GXM, log y recibo del paquete.

**VERIFIED:** 00.02 cambió a `BuildOptions.None`, manteniendo diagnóstico propio
`HSW_PSP2_BOOT_LOG`. Su SELF coincide exactamente con la plantilla normal instalada
(SHA-256 `14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`),
cuya inicialización omite la llamada Razor de 00.01. No hubo recorte de contenido,
cambio de calidad ni expansión de memoria. Las siete entradas retiradas del VPK
fueron símbolos `.mdb`, no recursos del juego.

**OWNER-REPORTED:** el avance físico de 00.02 es coherente con esa corrección.
No se promete que todo fallo posterior haya quedado solucionado. El tercer VPK
mantiene el player normal; activar Development para diagnosticar reintroduciría
la ruta que falló. No se parchea el binario Unity.

## Referencias Evolution contrastadas localmente

Se leyeron los cinco documentos solicitados de Evolution, su helper de límite y
la guía World `EVOLUTION_TECHNICAL_LESSONS_2026-11-04.md`. Evolution permanece de
solo lectura. No se descargaron herramientas ni se copiaron sus clases del juego.

| Referencia | Evidencia en Evolution | Aplicación a World |
| --- | --- | --- |
| D03 Startup | ~135 FPS reportados; límite temprano `vSyncCount=1`, `targetFrameRate=60`, tras escenas y calidad. Captura posterior target60/VSync1/Update60,1. | World sí tiene `ApplicationInitialization.Awake` con target30, cinco perfiles con VSync0, selector `DeviceQualityManager` y `FPSTest` que deslimita. Adaptar esos puntos propios y el inicio temprano; no tocar timestep, curvas ni velocidad de animación. El contador Update no mide scanout. |
| D04 Offline SDK | Excepción Facebook demostrada por captura; callbacks offline permitieron avanzar. Escritura directa ux0 falló; persistent/franja/TTY sirvieron. | World ya posee NativeImplementationPSP2, proveedores Null, BillingFacadePSP2, guardas SDK y Request offline. No repetirlos por analogía. Instrumentar antes/después de inicialización y callbacks; la presencia de un SDK no prueba que se ejecute. |
| D05 Audio | FMOD rechazó Vorbis; 302 clips HEVAG/3 PCM después. | World ya tiene **424 HEVAG** verificados en ambos players previos. Fabric usa AudioClip Unity; instrumentar cargas Audio_Common/Audio_Hawaii sin volver a convertir ni eliminar audio. Un eventual error nuevo requiere su propio log. |
| D05 GfxDeviceGXM | Dump en BufferGXM.UpdateInternal con r0=0, rama de Alloc fallida y memoria física escasa; ensayo ExpandBy109MB. Gameplay posterior reportado, sin aislar contribución de cada cambio. | Crash 00.01 en InitializeGXM/Razor es distinto. No hay evidencia equivalente de 00.02: **conservar expansión None**, medir LPDDR/CDRAM/PHYSCONT. No inferir RAM por tamaño VPK. |
| Black Screen | Caché BC7 y una variante de shader fallaban; auditoría del player antes de cambios. | World ya verificó 480 texturas sin BC7/ETC1 y programas PSP2; no repetir reimportación masiva, reemplazar shaders, borrar lightmaps ni escenas. Conservar el lightmap RGBA32 ya preparado. |
| CapUnlocker | Dependencia física reportada para Evolution v1.0; función exacta no aislada. | Propietario confirma plugin activo/reinicio en esta prueba World. Su simple ausencia no explica el cierre reportado. Dependencia específica World sigue **UNTESTED**; no exigir reinstalar ni atribuir una API concreta sin evidencia. |

## Alcance del tercer ensayo

Helpers propios compartibles en `tools/unity/`; aplicación solo al proyecto privado
PSP2 2018 y su caché de build existente. Base 2017 y base funcional 2018 protegidas
mediante manifiestos SHA-256; cambios anteriores preservados en checkpoint privado.

- Límite de presentación antes de la primera escena, tras cargas y después del
  selector de calidad World. La inicialización y FPSTest respetan 60/VSync1 en
  PSP2, conservando las ramas originales de otros destinos. La selección de
  calidad, rating, keywords y calentamiento de shaders siguen siendo los originales.
- Diagnóstico propio mejorado: franja sin botones, cuatro marcas recientes,
  última operación completada, primera excepción, target/VSync/Update por segundo
  y memoria libre LPDDR/CDRAM/PHYSCONT. Marcas BEFORE/DONE acotan operaciones; una
  llamada asíncrona que retorna no significa que su carga/callback haya finalizado.
- Registro acotado de excepciones con stack y Unity/TTY, incluso si falla el
  archivo; archivo nuevo por sesión en `Application.persistentDataPath` real,
  con flush. No se cambia ni borra el guardado. No se depende de `ux0:` directo.
- Instrumentación de inicialización nativa/CP2/social/servicios/notificaciones,
  validación, expansión, carga BootLoader, warmup de shaders, escenas normales,
  comunes y precargas, carga de save y solicitudes `Application.Quit`.
- Mantener escenas/recursos/GUID, proveedores offline, HEVAG, input y player normal.
  No reducir memoria por eliminación especulativa, cambiar físicas o aplicar
  ExpandBy109MB sin dump/medición que lo justifique.

Los límites anteriores de recuperación (51 entradas de catálogo ausentes, dos
scripts nulos y una referencia Font Texture de origen, además del shader
provisional documentado) siguen pendientes. No se borran ni se rellenan por
conjetura y no se les atribuye el cierre sin una traza correspondiente.

## Próxima prueba física

Instalar 00.03 sobre HGSKW1178 sin borrar datos. Conservar los dos VPK anteriores.
Mantener la configuración actual con CapUnlocker para comparar la misma condición.
Grabar desde el arranque hasta el cierre permite leer marcas aunque el archivo no
sea accesible. Registrar última línea BEFORE, última DONE, primera excepción,
LPDDR/CDRAM/PHYSCONT, segundos, target/VSync y PSVShell abierto/cerrado. No equiparar
Update/s con presentaciones reales ni afirmar 60 FPS estables de gameplay.

Si vuelve al LiveArea, conservar **el dump nuevo y la versión a la que corresponde**.
Buscar `HSW_VPK03_*.log` en la ruta persistente real/montada del título; un contenedor
binario de savedata no es texto sin errores. Si no existe o no se puede recuperar,
registrarlo y usar video/franja/TTY. Símbolos y player exactos se guardan privados
para analizar ese dump. No forzar completar callbacks o saltar escenas para ocultar
el cierre.

Resultado físico esperado: máximo solicitado 60, menú si la carga lo permite;
si continúa el cierre, nueva evidencia para localizarlo. **Causa del cierre de
00.02 y funcionamiento físico de 00.03 siguen sin confirmar.**

## Resultados locales de validación

**VERIFIED:** pareja original APK/OBB revalidada con
`python tools/verify_source_pair.py <APK_original> <OBB_original>`: ambos SHA-256 y
CRC PASS. Sin extracción o conversión repetida.

Unity 2018.2.19f1 / PSP2 seleccionado, caché privada existente, ejecuciones acotadas
`-batchmode -buildTarget PSP2 -projectPath <copia_privada> -executeMethod
HSWVPK03EditorValidation.Run -logFile <privado>`:

| Prueba | Resultado real |
| --- | --- |
| SplashLoader, 35,00 s / 2.113 frames | Cero errores registrados; permaneció en SplashLoader sin interacción. No acredita menú ni causa de espera. target60/VSync1 y diagnóstico activos. |
| BootLoader, 35,01 s / 1.901 frames | Llegó a SaveLoader, FrontEnd, 3DBackground y Sharks. **Seis errores registrados:** autenticación automática fallida, dos NRE DNA/UbimobileToolkit, tres errores de servicio/red. No es un PASS sin errores. |
| Cinco niveles de calidad en ambas sesiones | Cada nivel acepta target60/VSync1 después de Apply; selector de calidad original conservado. |
| Reloj de simulación | `timeScale=1`, `fixedDeltaTime=0.01666665`, `maximumDeltaTime=0.33333`, idénticos antes/después. Ninguna corrección de velocidad de UI mediante el reloj. |

BootLoader es únicamente el punto de entrada de la segunda **prueba de subsistemas
en Editor**. No se cambia el orden de arranque del player ni se fuerza la edad,
un callback o el guardado. Se añadieron marcas de idioma/edad sin registrar sus
valores privados. La espera observada en SplashLoader queda documentada sin
inventar una causa.

Las excepciones DNA del Editor pasan por `HSXAnalyticsManager.SaveLoaded` a
`DNAFactory.Init` / `DnaToolkitUtil` / `UbimobileToolkit`. **VERIFIED estático:** la
exclusión PSP2 ya existente de SaveLoaded evita construir esos proveedores;
`FGOL.Server.Request` también conserva su fallback offline PSP2. No se reescriben
esas reparaciones para limpiar la prueba del Editor. `AuthManagerUnity` conserva
otras solicitudes mediante UnityWebRequest: no hay evidencia de que causen el
cierre físico, ni se declara que todas las rutas online estén cubiertas. El
recibimiento asíncrono del save y sus excepciones quedan visibles en el diagnóstico.

Manifiestos privados antes/después verifican íntegros 20.870 archivos de la base
2017 y 20.887 de la base funcional 2018, contando `Packages` además de Assets y
ProjectSettings. No hubo cambios ni añadidos durante este encargo. El número
20.869 de informes anteriores se refería al inventario sin ese archivo Packages.

Fallos de preparación conservados: el primer sondeo de hashes se interrumpió por
falta de progreso visible y se repitió con progreso; dos aserciones del aplicador
fallaron **antes de escribir fuentes** (sección SaveFacade ya instrumentada en
memoria y recuento de dos versiones, no tres). Se reutilizaron los manifiestos
completados. El sandbox impidió cargar las DLL de Unity; la misma ejecución local
fuera del sandbox pudo iniciar. No se atribuyen estos fallos al juego ni a Vita.
Evidencia ignorada: `Reports/PSP2_VPK03`, checkpoint Before, manifiestos protegidos,
logs separados Splash/BootLoader, errores completos y helpers de validación.

## VPK 3 privado generado

**VERIFIED build:** Unity 2018.2.19f1 / PSP2 Mono2x, `HSWFirstVitaBuild.Build`,
`BuildOptions.None`: **Succeeded, 0 errores / 602 advertencias, 4:45,410**.
Mismo SELF normal exacto de 00.02, sin define DEVELOPMENT_BUILD, con diagnóstico
propio. `ATTRIBUTE2=0`, expansión None, calidad original; ajustes persistentes
solo cambian bundleVersion y psp2AppVersion de 00.02 a 00.03.

**VERIFIED player:** 18 comprobaciones IL PASS, 64 marcas de etapa/salida;
inicio BeforeSceneLoad y llamadas al límite en inicialización, calidad y FPSTest;
diagnóstico visual/TTY/persistente y tres pools Vita presentes. Proveedores PSP2,
input y exclusión existente de analytics DNA conservados. Sin escrituras al reloj.
23 escenas en orden original, **480 texturas**, **424 HEVAG** con metadatos y recursos
idénticos, **140 shaders / 245 passes** PSP2 ConsoleVS/ConsoleFS. Listas de conversión
HEVAG y reimportación de texturas vacías: no se repitieron esas reparaciones.

Comparación entre builds: añadir el MonoScript del helper renumera referencias
internas y cambia los serializados generados; no se exige identidad binaria de
esos archivos entre VPK2 y VPK3. Se comprobaron **119.784 objetos**: mismos conjuntos
de objetos en las 23 escenas/recursos examinados; **5.070 MonoBehaviours** conservan
la misma clase resuelta y campos serializados, cambiando solo el PPtr de script.
PreloadData y metadatos generados también cambian. Hay diferencias pequeñas en
blobs de **63 mallas** generadas: todos sus campos geométricos interpretados por
AssetStudio son idénticos; el significado exacto de esos bytes opacos queda
pendiente, sin parchearlos ni atribuirles el cierre. Los archivos fuente de mallas,
escenas, prefabs, materiales, texturas/audio y metas originales están intactos.

La primera aserción privada que esperaba cambios en solo tres miembros del VPK
falló por esa serialización; se conservó el fallo y se añadió la comparación de
objetos/referencias/geometría, además de CRC y comparación del paquete con **su
propio player**. Otros fallos del auditor corregidos: resolver/lectura de atributo
Cecil y filtro de mallas que confundía pathIDs iguales entre dependencias distintas;
no eran fallos del juego ni exigieron reconstruir el VPK. El build registró salida
correcta 0; se interrumpió posteriormente la espera del shell que seguía abierta,
sin modificar el resultado ni los archivos ya generados.

**Artefacto local:** `local-work/HSW_Recovery/Reports/PSP2_VPK03/HSW_Vita_Test_00.03_HGSKW1178.vpk`.
**179.708.740 bytes**, 284 entradas, SHA-256
`5669eff27fb2accae45628111a80ee118dae6f3bfbd9f196ce2d3a244ca5b1f9`.
CRC PASS, todos los miembros runtime idénticos a la salida nativa salvo la adaptación
de identidad de `param.sfo`; TITLE_ID **HGSKW1178**, APP_VER **00.03**.
Se conserva el ID técnico de generación dentro del módulo AOT, igual que en VPK2;
no se parchea su binario. Los hashes de VPK1 y VPK2 se comprobaron sin cambios.
Símbolos/player exactos, recibos y checkpoints permanecen privados en el mismo
informe. No se publica ni se instala automáticamente.

**UNTESTED físico:** límite efectivo de presentación, movimientos de UI, menú,
audio, guardado y cierre de 00.03. Este ensayo mejora el diagnóstico; no demuestra
haber corregido el cierre de 00.02. Instalar manualmente y registrar franja/video,
log persistente y cualquier dump nuevo según el procedimiento anterior.
