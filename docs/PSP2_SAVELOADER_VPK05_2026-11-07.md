# SaveLoader y guardado local: ensayo privado 00.05

Encargo expreso del propietario, 2026-11-07 UTC. P00 ACTIVE, 0/13 aprobaciones;
ledger y rama existente intactos. Fuentes modificadas únicamente en la copia
privada PSP2 de Unity 2018.2.19f1 y su caché de compilación. Sin cambios en
Evolution, Unity 2017, base funcional 2018 ni recursos originales.

## Evidencia física y límites

**OWNER-REPORTED, VPK 4 / 00.04:** inicia, mantiene 60 FPS, muestra Loading,
se congela y vuelve al LiveArea sin crash visible. Estado SaveLoader, última
operación completada `screen loaded SaveLoader`, `persistent OK`; error
`GameDataManager.DeleteExpiredDailyEvents: Failed to delete data with exception - An empty file name is not valid.`
No se recibió un nuevo dump ni el registro completo del cierre. El resultado
anterior de Editor de 00.04 no acredita la transición física.

VPK 1 tuvo un crash inicial distinto; VPK 2 lo superó con player normal
`BuildOptions.None`; VPK 3 confirmó físicamente el límite de 60 FPS. VPK 4 sigue
fallando durante Loading. Se conservan los cuatro paquetes y sus evidencias;
no se atribuye el cierre actual a aquel primer crash. CapUnlocker activo y
reinicio completo fueron reportados por el propietario; no prueban su necesidad
para World. Sin nueva evidencia de GfxDeviceGXM/OOM, expansión de memoria None.

## Comparación con Evolution

| Referencia local, leída sin modificarla | Resultado documentado y aplicación a World |
| --- | --- |
| D03 / D04 | La captura física localizó una excepción de Facebook que abortaba una corrutina antes del guardado; D04 superó ese punto y reveló fallos posteriores independientes. El acceso directo a `ux0:` falló. Se conserva el diagnóstico visual/TTY y la ruta persistente, y se acotan servicios mediante sus contratos; World ya tiene proveedores offline. |
| D08 | La fixture de identidad pasó en PC, pero el propietario después reportó progreso reiniciado y un error al respaldar. No fue una solución física completa. World ya usa `PlayerPrefs.Save()` en `User.Save()`, y su cargador selecciona `local` si falta saveID; no necesita copiar la recuperación de identidad de Evolution. |
| D09 | Adaptó cuatro `File.Copy` a streams verificados. Las pruebas iniciales de PC no certificaban Vita. World usa `FileStream`, `File.Move` y `File.Replace` en su guardado, no esas cuatro copias. Se mantienen y se instrumentan; todavía no hay evidencia física de que deban sustituirse. |
| Guía de transferencia, sección 2.13 | El seguimiento D10 encontró JSON dependiente de cultura en archivos concretos; después se reportó persistencia física de monedas/nivel. Se comprueba el mismo defecto en World con una fixture propia antes de corregirlo. No se copian claves, codec o partidas de Evolution. |
| Preparación v1.0, 23 de octubre | El propietario confirmó la matriz de arranque, menús, gameplay, guardado/carga y reinicio. Es un resultado final reportado, sin aislamiento de la contribución de cada parche ni prueba de corte eléctrico; no convierte D08/D09 por separado en PASS físico. |

Referencias: repositorio local Evolution, `docs/PSP2_STARTUP_D03_2026-10-17.md`,
`PSP2_OFFLINE_SDK_D04_2026-10-17.md`, `PSP2_SAVE_CPU_D08_2026-10-17.md`,
`PSP2_SAVE_IO_D09_2026-10-17.md`, `RELEASE_V1_0_PREPARATION_2026-10-23.md`;
[guía World](EVOLUTION_TECHNICAL_LESSONS_2026-11-04.md).

## Rutas, cadena y bloqueos

**VERIFIED estático:** `DeleteExpiredDailyEvents` recibe directamente
`Application.temporaryCachePath` en el constructor de `DirectoryInfo`. No recibe
la ruta de partida ni el nombre de usuario. Su finalidad es borrar cachés `event*`
de más de 30 días; su excepción ya estaba capturada. Una fixture reproduce la
excepción al pasar cadena vacía. **INFERRED del error físico y ese código:** la
API de caché devuelve vacío en esa Vita; 00.05 registra ambas rutas para confirmarlo.
`persistent OK` únicamente acredita que se abrió el log de diagnóstico.

**Corrección PSP2:** si el directorio de caché es vacío o inexistente, se trata
como caché opcional no disponible. No se construye `/cached.gamedb` ni
`/<event>.gamedb`, ni se leen/escriben/eliminan archivos por esas rutas. Se omite
la limpieza y se conserva la preferencia de metadatos de eventos cuando no hay
caché disponible. Se conserva GameDB incorporada y los contratos originales
`null`/ausencia; no se inventa una ubicación, un evento ni un archivo sustituto.
Una caché válida sigue el recorrido original. Este error opcional no demuestra
la causa del cierre.

El recorrido auditado es:

1. `ScreenTracker.OnScreenLoaded` activa `ScreenRoot`, precarga y eventos de
   pantalla. Ese marcador original precedía operaciones adicionales: no significaba
   que SaveLoader ya hubiera solicitado o completado la partida.
2. `SaveLoaderState.OnStateLoaded` establece su disponibilidad y apaga el spinner;
   tras el retardo original, solicita `SaveFacade.Load`.
3. La fachada configura el servidor local/offline, carga GameDB incorporada/caché,
   dispara `OnGameDBLoaded`, y carga preferencias mediante `AuthManager.LoadUser`
   y `User.Load`. Conserva identidad, saveID y preferencias de nube originales.
4. La comprobación original de disco puede crear una partida nueva. `LoadSave`
   elige saveID o `local`, busca principal/temporal/respaldo y después el respaldo
   de preferencias original; valida cabecera, MD5, AES, compresión y JSON.
   Conserva migración de versiones, carga y orden de los SaveSystems.
5. `OnSaveLoaded` ejecuta `InitSaveData`, `OnLoadComplete`, y el guardado original
   del sistema de usuario. El suscriptor de SaveLoader solicita FrontEnd; otros
   suscriptores pueden ejecutarse antes o después. Una excepción puede interrumpirlos.
6. Se conserva el recorrido offline de 00.04, sin autenticar ni esperar nube para
   la carga local. No se fuerza un resultado de carga OK ni se concede contenido.

**Diferencias verificadas:** los cuatro archivos User/SaveData/SaveGameManager/
SaveUtilities de las bases 2017 y funcional 2018 coinciden por SHA-256. En Android,
NativeImplementationAndroid consulta almacenamiento externo por JNI y usa la ruta
Unity como alternativa. PSP2 ya usa su proveedor específico y
`Application.persistentDataPath`; esa selección y los nombres originales se conservan.
No se ha medido todavía el comportamiento físico de Move/Replace ni la persistencia
después de cerrar el proceso World.

## Defecto adicional reproducido: cultura del JSON

**VERIFIED, fixture propia anterior a la corrección:** con `en-US`, una fracción
317.25 se guarda y carga OK; con `es-ES`, el guardado devuelve OK pero su carga
devuelve Corrupted y registra un error de parseo. El contenedor original se generó
con su codec, sin editar bytes. MiniJSON usa ToString/TryParse dependientes de
cultura para números. La primera prueba se conserva como FAIL, aunque alcanzó
FrontEnd e Ingame: no se presenta como sesión limpia.

**Corrección PSP2 acotada:** cultura invariable únicamente durante `ToJSON` y
`FromJSON` del SaveData original, restaurada mediante `finally`. Se conservan
campos, versión 3, key derivada de identidad, padding de 1 MiB, MD5, AES, compresión,
rutas y operaciones de archivo. No se cambia la cultura global permanente ni el
JSON de servicios externos. No se intenta reparar JSON antiguo ambiguo ni borrar
partidas corruptas. La cultura real del cierre de Vita sigue sin conocerse; no
se declara que éste fuera su desencadenante.

## Instrumentación y pruebas

00.05 muestra `CURRENT` y la última operación completada por separado. Hay marcas
antes/después de ScreenRoot, precarga, SaveLoader listo, User.Load, comprobación
de archivos, lectura/codec, escritura temporal, Move/Replace y vaciado de preferencias.
Los eventos relevantes identifican cada suscriptor; InitSaveData/OnLoadComplete
conservan orden e invocación única. Si un suscriptor falla, se registra y se
propaga la excepción original, sin continuar artificialmente. Se conservan primera
incidencia, última excepción con stack, memoria, callbacks y marcas de quit/pausa.
El registro es acotado; no hay logs nuevos por frame ni dependencia de `ux0:`.

Las pruebas usan otra pareja companyName/productName únicamente en la caché del
Editor; tanto PlayerPrefs como persistentDataPath quedan separados de los reales.
La partida existente procede de la prueba nueva ficticia y se vuelve a abrir en
otro proceso. No se copian ni modifican partidas o preferencias del propietario.
El bootstrap ejecuta SplashLoader original y continúa BootLoader mediante el
fixture, sin aceptar ni modificar la edad; no prueba el diálogo legal completo.

**VERIFIED, Unity 2018.2.19f1 / target PSP2, ejecutado en PC:** las sesiones nueva y
existente pasan, alcanzan FrontEnd e Ingame con jugador activo, GameDB153, 0 errores
durante Play, 60/VSync1 y ningún callback offline pendiente. La identidad ficticia
persiste entre procesos. La fixture de codec recupera progreso317, actualiza318 y
conserva317 en el respaldo; pasan Move, Replace y los contratos de caché ausente.
Ambas culturas recuperan317.25 y restauran la cultura del hilo. Al detener Play
reaparece el error heredado de destruir un Transform wake, separado de la carga;
no se corrigió como si fuera el cierre físico. No se afirma validación visual
completa ni equivalencia de memoria/IO con Vita.

**VERIFIED build único PSP2 final:** Succeeded, **0 errores / 596 advertencias**,
3:12,586; Mono2x, `BuildOptions.None`, SELF normal exacto SHA256
`14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`.
58 comprobaciones IL y131 marcas; fixture de Editor ausente del player. Se
conservan23 escenas,480 texturas,424HEVAG y140shaders/245passes PSP2; sin nueva
conversión de audio ni reimportación correctiva de texturas. Fuentes/assets de las
dos bases protegidas coinciden con sus manifiestos; fuentes privadas/cache
coinciden. Limitador y helper offline00.04 exactos, recursos/escenas/metas/audio/
controles intactos. Únicos settings cambiados: versiones00.04→00.05; company/product
ficticios restaurados. Se añade el helper JSON y su meta; no falta ningún archivo.

**VERIFIED paquete privado:**
`local-work/HSW_Recovery/Reports/PSP2_VPK05/HSW_Vita_Test_00.05_HGSKW1178.vpk`,
**179705337 bytes /284 entradas**, SHA256
**`ef01ea98bf8ae1dad5774ce1515621cdcaeaf070334076b71d635e0d6706915b`**.
CRC y comparación de cada miembro con la salida nativa PASS; adaptación SFO de
identidad como en paquetes anteriores, HGSKW1178/00.05, ATTRIBUTE2=0 y cuota8192KiB.
VPK04 conserva su SHA exacto. No se publica ni se instala automáticamente.

Evidencias privadas: `Reports/PSP2_VPK05/`, Before/After y lista de fuentes,
SourceIntegrity, resultados New/Existing, prueba de cultura fallida, logs Unity,
ManagedVerification, NativeVerification, PackageReceipt y FinalLocalDelivery.
**UNTESTED físico00.05:** superación de Loading, causa del cierre, Move/Replace,
checkpoint después de reinicio y estabilidad. Ninguna compilación sustituye esa prueba.

## Siguiente prueba física

Instalar 00.05 conservando datos y paquetes anteriores. Fotografiar `CURRENT`,
última completada, FIRST/EXCEPTION y los tres valores de memoria antes del cierre;
conservar un eventual dump o log `HSW_VPK05_*`. La ausencia de una marca quit no
demuestra por sí sola crash nativo. Si alcanza FrontEnd, entrar por el flujo original
al gameplay y comprobar un checkpoint tras cerrar/reabrir el mismo VPK. Hasta esa
prueba, superar Loading, funcionamiento del IO Vita y durabilidad siguen UNTESTED.
