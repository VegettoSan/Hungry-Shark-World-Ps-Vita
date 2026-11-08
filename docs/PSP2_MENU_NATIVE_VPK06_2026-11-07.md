# Menú, audio y cierre nativo: diagnóstico privado 00.06

Encargo expreso del propietario, 2026-11-07 UTC, incluida comparación de lectura
con su copia funcional local de Evolution. Excepción limitada para investigar,
validar y empaquetar esta prueba; P00 ACTIVE, 0/13 aprobaciones. No se modifica
el ledger ni se crea rama. Trabajo de World limitado a la copia privada PSP2
Unity 2018.2.19f1 y su caché existente. Sin publicar ni instalar automáticamente.

## Evidencia y conclusión provisional

**OWNER-REPORTED físico 00.05:** inicia, límite de 60 FPS funcional, ya no aparecen
los errores de guardado/carga, pero continúa Loading, se congela y vuelve a
LiveArea sin crash visible. No se recibió fotografía de CURRENT/última completada,
registro de esa ejecución ni dump nuevo. No es evidencia de que SaveLoader haya
completado todas sus operaciones ni de que el fallo sea necesariamente audio.

**VERIFIED estático:** VPK05 SHA256
`ef01ea98bf8ae1dad5774ce1515621cdcaeaf070334076b71d635e0d6706915b`, CRC válido.
Se revisaron sus recursos y símbolos exactos. El único dump disponible en los
informes World es el de 00.01, ya atribuido a Razor en InitializeGXM. No se
simboliza ese dump con símbolos 00.05 ni se atribuye su causa al cierre actual.
El índice privado VPK05_ExactSymbols conserva hashes de SELF/símbolos y rutas
de funciones FMOD/AudioManager/GXM para un futuro dump de la versión correcta.

**No se ha demostrado un recurso incompatible ni la causa física del cierre.**
00.06 es una prueba diagnóstica; no incluye una supuesta reparación de audio,
una conversión masiva ni una ampliación de memoria especulativa.

## Secuencia y recursos

La máquina serializada GameStateMachine comienza en SaveLoader y solicita
FrontEnd al finalizar la carga. Sus únicas escenas comunes del menú son
3DBackground y Sharks, en ese orden. Audio_Common no está en esa lista:
no se debe confundir su existencia entre las 23 escenas con su carga en el menú.

| Etapa | Evidencia estática y observación en Editor |
| --- | --- |
| SplashLoader | Sin clips en la clausura de referencias YAML; bootstrap/servidor offline original. La selección diagnóstica detiene únicamente la petición original de BootLoader, sin aceptar edad ni alterar consentimientos. |
| BootLoader | Clausura estática de 89 clips: música, stings y efectos UI, incluida `hsx_mus_frontend`. Fabric inicializa AudioComponents/AudioSources aquí, antes de SaveLoader. Referenciar un clip no prueba que sus datos estén residentes o reproduciéndose. |
| SaveLoader | Clausura estática sin clips; GameDB local, preferencias/partida y suscriptores originales conservados. Continúan todos los marcadores de 00.05. |
| FrontEnd | 18 clips propios de efectos UI, 6 materiales y 8 texturas por referencias YAML transitivas. Fabric registra el grupo del frontend. En el Editor normal, la solicitud de escena y las dos comunes preceden a la asignación/reproducción de la música. |
| 3DBackground | 7 materiales, 6 texturas, 9 AnimationClip referenciados; paisaje, skydome, estrellas, rayos cáusticos y partículas. Sin clips directos en la clausura. |
| Sharks | 11 materiales, 11 texturas, un AnimationClip y un controller en la clausura. Carga dinámica observada de `Sharks/Frontend/PF_FrontendSharkBlackTip`; no basta el inventario estático de la escena para cubrir los modelos. |
| Audio_Common | Clausura de 248 clips, principalmente efectos de gameplay/ambiente. No fue solicitada al entrar al menú en las tres pruebas descritas. |

Las clausuras son dependencias de archivos, no recuentos de objetos activos,
residencia, memoria máxima ni cobertura de todo recurso solicitado por nombre.
Static_Audit.json contiene los GUID/rutas y materiales/texturas concretos,
y los timelines documentan el orden realmente observado en Editor.

Los atlas relevantes incluyen TEX_Atlas_GUI/Main/Play, TEX_Numerals y PF_Atlas_Logo;
el fondo incluye FE_BG_Landscape, FE_BG_SkydomeGradient, FE_BG_Stars y CausticRays.
Se conservan modelos, animaciones, cámaras, renderers, prefabs y sus referencias.

## Audio y comparación con Evolution funcional

**VERIFIED en player 00.05:** 424 HEVAG, todos con contenedor FSB5 y rangos
offset/tamaño dentro de su archivo real. No basta leer el override del importer.
385 CompressedInMemory (8,034 MiB codificados), 35 Streaming (51,074 MiB) y
4 DecompressOnLoad (0,161 MiB). Los tamaños codificados no son RAM residente.
108 clips tienen precarga automática y 288 carga en background.

La música del menú es `hsx_mus_frontend`: HEVAG, Streaming, estéreo, 22050 Hz,
103,38458 segundos, 16 bits declarados, 2.605.408 bytes de banco;
`sharedassets1.resource`, offset 34.190.624. Precarga y background están desactivados.
Fabric termina solicitando AudioSource.clip y PlayScheduled para ese clip.
AudioClipHandle también tiene rutas explícitas LoadAudioData/IncRef; en la prueba
normal de Editor la música se resolvió mediante asignación del clip.

La copia funcional Evolution indicada por el propietario se inspeccionó sin
modificarla. Su controlador es SoundController, con canales propios; World usa
Fabric.Core y AudioManager. Su música `FrontendTheme1` también es HEVAG Streaming,
estéreo, 44100 Hz y 112 segundos; tiene precarga activada. La auditoría D05 de su
player verifica 302 HEVAG/3 PCM y cuatro clips Streaming. Esto demuestra que
HEVAG Streaming no puede declararse incompatible por sí solo. La diferencia
22050/44100 Hz o precarga no demuestra un defecto; no se cambian por analogía.

Ambos proyectos tienen audio habilitado, AcquireBGM=1, muestreo y DSP automáticos,
32 voces reales y sin spatializer; Evolution permite 512 voces virtuales frente
a 256 de World. Evolution tiene expansión de memoria 3 por su fallo gráfico
demostrado; World mantiene 0. No se trasplanta ese ajuste ni su controlador.
Comparación privada: Evolution_Working_Comparison.json, metas originales y
Audio_BankAudit.json. AudioManager.asset de World no cambia.

## Instrumentación y pruebas elegibles

00.06 conserva BuildOptions.None, Mono2x, el SELF normal, memoria None, 60/VSync1,
offline, guardado y controles. El selector usa botones táctiles y no escribe
preferencias: cada arranque comienza con la selección pendiente.

1. **0 — Original + registros.** Tras seleccionar, se continúa la petición
   original de BootLoader. Se mantienen los métodos de carga y concurrencia
   originales. Es la primera prueba física requerida.
2. **A — Datos/reproducción Fabric diferidos, gráficos originales.** Los sitios
   reales de Fabric que llaman LoadAudioData, asignan un clip no nulo o llaman
   Play/PlayScheduled pasan por una frontera gestionada temporal. En A no se
   ejecutan esas operaciones nativas; LoadAudioData devuelve false, sin inventar
   estado Loaded. La inicialización de Fabric y la creación de AudioSource siguen
   instrumentadas y activas. No se usa AudioListener mute/volume como aislamiento.
   Al alcanzar el menú se puede probar un clip original durante tres segundos:
   metadatos → LoadAudioData → espera de estado → crear fuente → asignar → Play →
   observar isPlaying → Stop. Se registra cada frontera. La lista respeta el orden
   de primera solicitud observado; no se carga toda la biblioteca artificialmente.
   Reiniciar el proceso y seleccionar 0 restaura el recorrido original completo;
   esta prueba no intenta reconstruir voces Fabric antiguas en la misma sesión.
3. **B — Escenas por etapas, audio original.** El botón inferior permite solicitar
   una escena y después autorizar su activación al alcanzar progress≥0,9. Se
   serializan las peticiones diagnósticas de pantalla/comunes/precarga, conservando
   las escenas solicitadas y su orden de petición. No se desactiva audio ni se
   sustituye geometría/materiales. Esperar en WAIT es intencional, no un bloqueo.

**Límite de A:** no evita deserializar AudioClips ni las precargas automáticas
anteriores a C#. No es un player sin audio ni una prueba negativa concluyente
de toda inicialización FMOD. Sí impide la asignación/reproducción original de la
música sospechosa, cuya precarga está desactivada. Si A llega al menú pero 0 no,
se estrecha el candidato; reproducir el fallo al probar ese clip y/o un dump
correcto aporta evidencia adicional. El cambio de memoria/timing también debe
considerarse antes de declarar causalidad exclusiva.

La DLL **gestionada** Fabric.Core se instrumenta únicamente en la copia privada,
con respaldo exacto y lista de 28 cambios de frontera/probes. No se parchea el
player nativo ni se reimplementa Fabric. En modo 0 se conservan argumentos,
retornos y excepciones de sus operaciones. La ayuda adicional referencia solo
UnityEngine y no crea una dependencia circular con Assembly-CSharp. En modo
normal no retiene AudioClips adicionales que impedirían su descarga.

Hay marcas antes/después de inicialización Fabric/AudioManager, Resources.Load,
ScreenRoot, SharksManager, primer upload de malla NGUI (material/shader/atlas),
creación de RenderTexture WaterFX y primera cámara de cada escena. Las marcas de
cámara/end-of-frame son envío CPU, **no confirmación de finalización GPU**.
No se crean capturas, texturas de prueba ni RenderTextures por el diagnóstico.

CURRENT, última completada, AUDIO y GFX aparecen por separado. Se muestrean los
tres pools Vita y GC.GetTotalMemory(false), sin GC forzada; no se mide tamaño del
mayor bloque libre, por lo que memoria total libre no descarta fragmentación.
Los mensajes Error/Exception/Assert y FMOD/GXM/OOM también se registran mediante
callback de logging threaded, acotado, sin llamar APIs Unity desde ese hilo.
Se conservan TTY, archivo persistente, primera/última excepción y marcas quit.
La ausencia de quit o excepción gestionada no demuestra por sí sola crash nativo.

## Renderizado y relación con el caso Evolution

Se reutilizó el censo de 480 texturas y 140 shaders/245 passes del player 00.05:
234 DXT1, 191 DXT5, 20 RGBA32, 33 ARGB4444, un RGB24 y un Alpha8.
No hay BC7/ETC1/ETC2, el defecto de importación que motivó la reparación anterior
de Evolution. Los atlas GUI/Main son DXT5 2048² sin mips; el paisaje FrontEnd es
DXT1 2048² sin mips. Sus payloads teóricos son 4 MiB por atlas y 2 MiB por paisaje,
antes de alineación/copias del motor; no son medidas físicas de memoria.
El lightmap RGBA32 2048² con 12 mips sigue intacto; su presencia en el player no
demuestra que esté residente durante el menú.

Las variantes empaquetadas siguen siendo PSP2 con ConsoleVS/ConsoleFS. No se
fuerza WarmupAllShaders, SetPass masivo, calidad diferente ni nuevo rebake.
Los shaders builtin VideoDecode con advertencias históricas no se identifican
como causa sin una llamada/objeto que los utilice en el recorrido fallido.

El dump D04 de Evolution apuntaba a BufferGXM.UpdateInternal en el hilo gráfico,
objeto nulo tras fallo de asignación y evidencia de reserva física fallida. Su
error FMOD de formato era independiente; ambos problemas se trataron allí.
World no tiene todavía evidencia equivalente de GXM/OOM. Se conserva expansión
None y no se modifica el reproductor.

## Validación y pendientes

**VERIFIED compilación directa PSP2 sin UNITY_EDITOR:** 118 fuentes firstpass,
0 errores/81 warnings; principal 3742 fuentes, 0 errores/515 warnings antes del
build. **VERIFIED Editor Unity2018.2.19f1 target PSP2:** tres procesos y namespaces
ficticios separados de datos del propietario, 28 segundos por sesión. Los modos
0, A y B llegan a FrontEnd con 3DBackground/Sharks y cero errores durante Play;
60/VSync1 conservados. A prueba la música original individual y observa Loaded e
isPlaying=true; B confirma lectura≥0,9 y activación de las tres escenas.

La primera versión del runner perdió su estado al recargar el dominio del Editor;
se detuvo solo ese proceso batch, se conservó Archived_Mode0_RunnerDomainReload.log
y se corrigió el runner usando su marcador de ejecución. No se presenta ese
intento como PASS. No era una excepción del juego.

Estas pruebas continúan desde Splash Awake hacia BootLoader mediante fixture;
no aceptan edad y no certifican el diálogo legal completo. Usan el backend PC
con destino PSP2 seleccionado: **no ejecutan FMOD/GXM nativos de Vita**.
El fixture sale de Assets antes del build y se restauran company/product reales.

**VERIFIED build PSP2 final único:** Succeeded, **0 errores / 596 advertencias**,
3:02,946; BuildOptions.None / Mono2x. SELF normal exacto SHA256
`14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`.
58 checks anteriores de startup/save y 21 contratos diagnósticos pasan;
174 marcadores gestionados. Se conservan 23 escenas, 480 texturas, 424 HEVAG,
140 shaders/245 passes ConsoleVS/ConsoleFS. Los 15 blobs .resource/.resS son
idénticos byte a byte a 00.05 y se compararon también precarga/background,
offset/tamaño y todos los metadatos efectivos de los 424 clips. No hubo nueva
conversión de audio ni reimportación correctiva de texturas.

**VERIFIED paquete privado:**
`local-work/HSW_Recovery/Reports/PSP2_VPK06/HSW_Vita_Test_00.06_HGSKW1178.vpk`,
**179.725.409 bytes / 285 entradas**, SHA256
`206e6399d4a3433471a92b94fb736e9480b84f75cc466d03bdffad7cc4105068`.
ZIP/CRC y comparación por miembro con salida nativa PASS; HGSKW1178/00.06,
ATTRIBUTE2=0 y cuota8192KiB. La entrada adicional es HSW.NativeTrace.dll.
Símbolos exactos privados conservados en Player/SymbolFiles, con manifiesto.

**VERIFIED integridad:** bases Unity2017/Unity2018 funcional idénticas a sus
manifiestos protegidos. Recursos originales, escenas, prefabs, metas existentes,
AudioManager/InputManager/QualitySettings, limitador, helper offline y JSON de
guardado conservan hashes. ProjectSettings cambia solo versiones00.05→00.06.
La copia privada y su caché coinciden en fuentes finales. VPK05 conservaSHA.
Evolution solo se leyó; no se ejecutó, reimportó ni modificó. Se verificó además
su player actual BetterWinds v2, no únicamente el informe D05 histórico.

Fallos de verificación conservados: el auditor de cámaras inicialmente buscó
accessors de eventos, pero esta API expone delegates; se verificaron sus campos
y Delegate.Combine reales, sin cambiar el player. La comprobación de fuentes
detectó la reserialización por Unity del meta del plugin diagnóstico **nuevo**
(campos heredados y plataforma Windows Store deshabilitada). Se conservó el diff,
GUID/Any/PSP2 y se sincronizó ese meta con la fuente privada; metas originales
intactos. No se ocultaron esos FAIL como PASS inicial ni se repitió el build.

Checkpoint/reversión privada: Before_VPK06.zip y manifiestos Before/After;
restore_vpk05.py permite revisar y restaurar exactamente00.05, sin tocar VPK,
partidas ni evidencias. Las sondas siguen en esta copia privada de diagnóstico
para reproducir la prueba, pendientes de retirar al identificar la causa.
**UNTESTED físico00.06:** llegar al menú con sistemas originales, audibilidad,
causa del cierre, comportamiento de la sonda y estabilidad nativa.

## Prueba física y criterios de diagnóstico

Conservar los VPK anteriores y los datos al instalar 00.06. Ejecutar primero 0 y
guardar foto/log con CURRENT, AUDIO, GFX, última completada y los tres pools antes
del cierre. Reiniciar el proceso para cada comparación. Después A; si llega al
menú, probar el clip 0 si su nombre es hsx_mus_frontend y registrar si se cierra
en carga, asignación o Play. No se interpreta silencio como éxito audible.
Después B, pulsando una etapa cada vez y anotando la última solicitud/activación.

| Evidencia recogida | Conclusión admisible |
| --- | --- |
| QUIT REQUEST más lifecycle quit | Petición gestionada identificada; revisar su condición y callsite. |
| Excepción/Assert, con stack | Fallo gestionado o assertion identificado; no ocultarlo ni completar eventos artificialmente. |
| FMOD/error de clip o fallo reproducible al cargar/reproducir un clip individual | Candidato de audio concreto; contrastar con dump y memoria antes de cambiar su importación PSP2. |
| Dump exacto en UnityGfxDeviceWorker/GXM con asignación fallida | Fallo gráfico nativo/memoria demostrado según registros/instrucciones, como el antecedente independiente de Evolution. |
| Cambio grande de pools, sin stack ni fallo de reserva | Indicio de presión de memoria; no prueba OOM ni fragmentación. |
| Se detiene antes de DONE scene data o durante activación | Se localiza la etapa de carga/activación; todavía puede ser audio, gráficos, deserialización u otro código de Awake. |
| Fin del proceso sin más evidencia | Finalización sin diagnóstico suficiente; recuperar TTY/dump correspondiente a 00.06. |

Los símbolos privados se conservan para cada versión. No usar los de 00.05 para
el AOT 00.06 ni los del VPK01 para atribuir este cierre. El objetivo pendiente
sigue siendo menú físico con audio/gráficos originales y sin sondas permanentes.


## Actualización física posterior — 00.06

**OWNER-REPORTED, 2026-11-07 UTC:** las tres opciones0/A/B vuelven a cerrar.
En B el propietario recuerda una marca parecida a SaveLoaderScreen/SaveCamera;
solo la vio en pantalla antes del cierre y no dispone de las líneas exactas.
**FAIL físico en los tres modos.** Los PASS anteriores siguen limitados al Editor
como se indicaba; 00.06 no ha conseguido el menú físico.

**VERIFIED estático:** no hay un recurso/objeto textual llamado exactamente
SaveCamera o SaveLoaderScreen. La sonda compone etiquetas escena/objeto, y existe
`SaveLoader/Camera`: cámara ortográfica de interfaz, depth4, máscara UI32,
RenderTexture nula, HDR desactivado; componentes UICamera, CustomInputCamera y
AudioListener. **INFERRED:** esa puede ser la etiqueta recordada, sin confirmación
visual. No demuestra fallo de cámara ni petición de un archivo con ese nombre.
El campo GFX retiene su última marca independientemente de CURRENT; puede seguir
mostrando esa cámara durante guardado, callbacks o transición. Un DONE de cámara
acredita retorno CPU, no finalización de GPU.

No apareció un nuevo dump en la carpeta local usada para el anterior ni en los
informes World. No se interpreta ausencia de dump como ausencia de fallo nativo.
No se cambia cámara/material/shader ni se recompila a partir de un nombre incierto.
La comparación0/A/B negativa tampoco descarta precarga o inicialización de audio
fuera de la frontera Fabric. Sigue pendiente recuperar el último CURRENT,
última completada, GFX y la etapa inferior request/activation de B. Una grabación
con móvil permite extraer el último fotograma legible sin tener que memorizarlo.


### Fotos físicas recibidas después

El propietario aportó tres fotos de B: petición SaveLoader pendiente; datos≥0,9
con activación pendiente; y Loading visible con `DONE first camera CPU submission
SaveLoader/Camera` (edad0,1s). FabricManager.Awake terminado. No aparece en esas
capturas FrontEnd, reproducción de la música del menú ni excepción. No se ha
confirmado si hubo marcas posteriores antes del cierre. Los valores de memoria
y la prueba siguiente que separa cámara/carga de partida están documentados en
[el diagnóstico B1/B2/B3 de 00.07](PSP2_SAVELOADER_FIRST_FRAME_VPK07_2026-11-07.md).
Las imágenes originales se conservan en privado con sus hashes.
