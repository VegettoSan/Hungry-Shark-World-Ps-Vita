# Reparación de shaders y arranque — 2026-11-05 UTC

**VERIFIED:** el proyecto privado compila con Unity 2017.1.2p4 y llegó al menú
con tiburón y fondo 3D en dos pruebas de arranque de 25 segundos, sin excepciones
registradas durante esos intervalos. No acredita gameplay completo ni equivalencia
visual de todos los efectos con Android.

Excepción de reparación local autorizada expresamente por el propietario.
`main`, P00 ACTIVE, 0/13 aprobaciones; ledger intacto. Sin cambios en Evolution,
adaptación PSP2, VPK, descargas o instalaciones. Código y assets siguen privados.

## Causas independientes y cambios

1. **Materiales:** UIDrawCall creaba materiales con Shader.Find nulo. Los 96
   shaders exportados como `.asset` contenían programas Android GLES, no fuentes
   importables para Direct3D11; solo 12 eran compatibles en la auditoría inicial.
   Se extrajeron sus programas y estados serializados y se reconstruyeron 96
   `.shader` con sus nombres, propiedades, tags, colas, passes y estados de
   render. Se conservaron GUID y fileID 4800000. Solo se cambió el tipo de PPtr
   del importador (2 a 3) en 563 referencias de 414 archivos; no se regeneraron
   GUID o prefabs. No se reemplazaron globalmente por shaders genéricos.
2. **JNI:** NativeBinding elegía siempre Android. Su inicialización fallida
   contaminaba VirtualPad/GameInput. Se añadió NativeImplementationEditor y se
   selecciona exclusivamente con UNITY_EDITOR. AppsFlyer y DeepLink también
   elegían Android: ahora el Editor utiliza las implementaciones World existentes
   AppsFlyerEditor y DeepLinkImplementationDummy. El receptor telefónico omite
   exclusivamente su inicialización nativa en el Editor.
3. **Anuncios:** MoPub seguía llamando JNI cada frame al llegar a FrontEnd. Solo
   en Editor se usa AdProviderMoPubNonMobile, adaptado para informar que no hay
   anuncios disponibles. No simula reproducción, recompensas ni aplicaciones
   instaladas. Las selecciones originales Android se conservan.
4. **Importadores binarios:** tres TextAssets tenían extensiones no reconocidas.
   Se renombraron data.zip.zip, IncludedInBuildAssetBundles.crc.crc y
   gameDB.gdb.gdb a sus correspondientes nombres terminados en `.bytes`.
   Payload, GUID y bytes de sus metas se conservan; los nombres de Resources
   tampoco cambian. El decoder del DLL original procesa gameDB: 108 entradas raíz.
5. **Catálogo:** GameAssetDatabase descartaba su lista serializada tras indexarla,
   lo que dejaba cero entradas después del domain reload del Editor. Solo en
   Editor se conserva la lista y, si falta, se reconstruye mediante su Import
   original y el JSON original incluido. Catálogo y JSON coinciden en las 528
   identidades/rutas; el índice vuelve a contener 528. No se modificaron los datos.
6. UIDrawCall ya no invoca DontDestroyOnLoad fuera de Play Mode en el Editor.
   No se ocultaron excepciones ni se suprimieron warnings.

## Validaciones y límites

| Comprobación | Resultado observado |
| --- | --- |
| Compilación final mcs C#4 de 2017.1.2p4, referencias/defines de la sesión | firstpass, principal y herramientas Editor: exit 0, 0 errores |
| Compilación aislada con ramas Android, sin UNITY_EDITOR | firstpass y principal: exit 0; no es una prueba de player Android |
| Auditoría nativa Direct3D11, en la instancia ya abierta | 97/97 shaders compatibles, 428/428 materiales con shader válido |
| Pruebas nativas de passes y keywords recuperados | 374 pruebas SetPass, 0 fallos; GrabPass contado separadamente como operación sin dibujo |
| Diagnósticos nativos de shaders | 0 errores, 63 warnings de compilador conservados, incluidos outputs no completamente inicializados |
| Propiedades originales | 334 nombres presentes en el censo nativo; no demuestra equivalencia de cada cálculo |
| UI renderizada contra colores calculados | 4/4 pruebas PASS: transparencia, premultiplicación, clipping dentro/fuera; tolerancia RGB 0,02 |
| Resources.Load de agua HI y transparente HI | Ambas búsquedas resueltas |
| Dos arranques desde BootLoader en Play | 25,41 s / 649 frames y 25,36 s / 688 frames, 0 excepciones en cada intervalo |
| Grafo estático final | 0 metas ausentes/huérfanos, GUID duplicados, fileID locales/YAML perdidos, scripts no nulos sin destino o problemas en las 23 escenas de build |

Las pruebas de arranque cargaron SplashLoader, BootLoader, SaveLoader, FrontEnd,
3DBackground y Sharks. La segunda conserva una captura del Game View con menú,
tiburón, barco y entorno sin materiales rosas visibles. Se entró directamente
en BootLoader como prueba de desarrollo: no se acredita la transición automática
de Splash/age gate ni se fabricó una respuesta de edad. No se guardaron escenas.

Pendientes explícitos:

- **Un shader provisional:** BlackSilhouette tenía shader nulo en la fuente.
  Solo ese material utiliza HSWRecovery/Provisional BlackSilhouette, negro opaco;
  el comportamiento original de profundidad/culling no es recuperable todavía.
- **Nueve passes Meta de bake:** el programa extraído dejaba emisión sin asignar.
  Se inicializó a negro exclusivamente en esos passes para compilar en D3D;
  no se cambió su pass de runtime. Lista privada MetaEmission_Provisional.json.
  No se rehízo iluminación; el resultado de un nuevo bake no está validado.
- Los warnings de outputs de shaders requieren inspección visual dirigida antes
  de atribuirles efectos. Soporte y SetPass no prueban todas las combinaciones
  de luz, hardware, keyword o fidelidad de agua, partículas y posprocesado.
- 51 de las 528 rutas del catálogo carecen de recurso dentro del conjunto
  recuperado; no hay candidatos exactos en Assets. Se conserva el inventario,
  sin placeholders ni suposición de que estaban incluidas en APK/OBB.
- Hidden/ACTk/WallHackTexture no tiene fuente encontrada; la búsqueda está en
  código anti-cheat no recorrido por estos ensayos. No se inventó ni desactivó.
- Permanecen una referencia original a Font Texture builtin vacía y dos scripts
  nulos de origen (LevelSelect y Hawaii_low). Las 16 referencias UI suministradas
  por el Editor se distinguen de GUID perdidos en el censo estático.
- Assertions históricas m_AssetToPrefab.empty() conservadas; ninguna observada
  en los intervalos finales. No se alteró el registro de prefabs de red.
- Gameplay, controles en partida, otras regiones, guardado/carga en frío,
  servicios externos y comparación visual completa con Android siguen UNTESTED.

## Evidencia, herramientas y ensayos fallidos

Proyecto: `local-work/HSW_Recovery/HSW290_Unity2017_ReadyToOpen`.
Evidencia privada: `local-work/HSW_Recovery/Reports/RuntimeShaderRepair01`.
Incluye Before, programas GLES originales, traducción, inventarios, remaps,
recibos de hashes, auditorías nativas/estáticas, logs, response files y captura.
La exportación intacta y el ZIP PreEditor anteriores permanecen preservados.

Se reutilizaron Python 3.14.4, dnSpyEx 6.6.0/dnlib y Mono/mcs del Editor
2017.1.2p4. Se adaptó el método genérico local de traducción GLSL de Evolution;
no se copiaron shaders del juego Evolution. Se usaron los includes del propio
Editor 2017. No hubo investigación externa.

Entradas de procedencia, ya verificadas en recuperación:

- APK SHA-256: `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d`.
- OBB SHA-256: `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72`.

Se conservan los FAIL intermedios: traducciones iniciales fallaban con matrices
array, samplerCube, MRT y emisión Meta; se corrigieron de forma dirigida. Un
refresh síncrono desde Update produjo un diagnóstico nativo de recarga y fue
retirado. DriveInfo no implementado en este Mono Windows se sustituyó por
GetDiskFreeSpaceEx solo en el adaptador Editor Windows. Dos ensayos cargaron un
ensamblado anterior antes del refresh; no se cuentan como PASS. Un response file
Android tenía un define vacío y se corrigió. La llamada antigua CaptureScreenshot
produjo CS0619 y quedó sustituida por ScreenCapture.CaptureScreenshot; las tres
compilaciones Editor finales terminan sin errores. Los logs históricos no se
limpiaron para ocultar esos fallos.

El propietario interrumpió el control de interfaz con Escape al cerrar la
verificación. No se realizaron más acciones UI. Se retiraron el comando pendiente
y la bandera temporal de automatización; no quedan pruebas Play encoladas.

## Comprobación posterior del propietario

1. Abrir el mismo proyecto con **Unity 2017.1.2p4** y permitir refresh/compilación.
2. Abrir SplashLoader, entrar en Play e interactuar con el flujo de inicio
   original. Revisar Console por mensajes nuevos, distinguiéndolos del historial.
3. Comprobar menú y selección, iniciar una partida y revisar controles, agua,
   transparencias, partículas, iluminación, audio y cambios de calidad.
4. Ejecutar `HSW Recovery/Audit shaders and materials`,
   `HSW Recovery/Probe shader passes` y `HSW Recovery/Render UI reference checks`
   para repetir las comprobaciones compatibles con este Editor. Sus reportes
   quedan en la evidencia privada. Comparar otras escenas con Android antes
   de declarar fidelidad completa. Evitar un nuevo bake hasta revisar los Meta.
