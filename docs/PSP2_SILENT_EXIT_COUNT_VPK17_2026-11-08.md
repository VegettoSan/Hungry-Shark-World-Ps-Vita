# VPK 17 — investigación del cierre silencioso en GameDB

Estado: diagnóstico dirigido, sin reparación física demostrada. Se conserva el algoritmo de VPK 16. El informe completo de entrega añadirá los resultados finales del paquete.

## Evidencia de dos ejecuciones del mismo VPK 16

Se analizó el archivo completo antes de editar el proyecto. La primera captura tiene 298255 bytes, sesión 24c7e5ab117e, 1020 datagramas, secuencias 1–1020 y ningún hueco o fragmento incompleto. No hay excepción, solicitud de salida ni cierre normal del logger registrados. ImportDictionary pass=0 termina y el último mensaje es BEFORE de T82 OnBoardingData, fila0, op1, total3048.

El propietario repitió el mismo VPK 16 mientras se hacía el análisis. La copia conjunta tiene 611997 bytes. La segunda sesión, 937501b9dc71, recibe 1076 datagramas consecutivos: OnBoardingData completa sus tres registros y el último mensaje pasa a T83 HUDThreatDetectionData, fila0, op1, total3051. Tampoco hay error o cierre normal registrado. Ambas construcciones se observan en hilo administrado1 y SceUID1073808041; el identificador de sesión distingue los procesos aunque el sistema reutilice un UID.

VERIFIED: el punto observado cambia de tabla bajo el mismo ejecutable, conservando op1 como frontera común. Esto contradice que OnBoardingData sea siempre incapaz de procesarse. No demuestra por sí solo fallo en Count: el último envío podría no haber retornado, faltar el final de la captura o existir un fallo asíncrono. Las secuencias completas acreditan ausencia de huecos dentro del tramo recibido, no ausencia de mensajes posteriores perdidos.

Las grabaciones anteriores de14 situaban el progreso alrededor de77–83; un fotograma y PREVIOUS no son un stack ni una instrucción de fallo. Se conserva esa diferencia de calidad de evidencia.

## Instrucción exacta de op1

El código ejecuta Trace(1,detailed), comprueba list==null y, si existe, lee list.Count. En el IL exacto de16:

- IL018d: llamada a Trace(int,bool).
- IL0194–019f: referencia y rama de lista nula; una lista nula produce count0.
- IL01aa: callvirt System.Collections.ICollection::get_Count().
- IL01af: asignación del entero al campo count.
- IL01bd: Observe DONE, que incluye envío y diagnóstico de memoria.

El getter de List<T> del mscorlib incluido es ldarg.0; ldfld _size; ret. No enumera objetos, lee claves, importa JSON ni invoca getters de OnBoardingData. En este punto no se ejecuta reflexión del importador. El despacho de interfaz pasa por código nativo Mono2x: el AOT exacto de16 carga el vtable y salta indirectamente por su entrada de interfaz en ELF0x344028, dirección mostrada por el SDK0x81344028. Sin PC/stack de un dump no se puede afirmar que esa instrucción se ejecutara ni que su puntero fuera inválido. El getter simple tampoco demuestra que el despacho sea correcto.

En la primera captura PREVIOUS=none, por lo que Trace no debía escribir un checkpoint detallado en T82. En el segundo intento existe reproducción del checkpoint anterior: ese estado se conserva y registra, sin alterar el mecanismo.

Mapa de operaciones:0asociar tipo/lista;1Trace+Count;2crear diccionario por clave;3IList.get_Item;4ObjectData.key;5Dictionary.Add por clave;6Add de tabla por Type;7índice completo;8crear diccionario exterior. El contador total solo se incrementa tras Add exitoso.

## Datos, colecciones y excepciones

OnBoardingData hereda ObjectData y tiene tres campos serializados simples, además de la clave heredada. No sobrescribe Init; la implementación heredada está vacía. HUDThreatDetectionData y ObjectData también se compararon con el IL original recuperado. Sus campos serializados permanecen exactos.

ImportDictionary llama al importador original. Este crea List<T>, instancia registros, aplica campos mediante reflexión y agrega las referencias. El importador termina antes de construir el índice. Existe un catch original de Init que ignoraba excepciones;17lo hace observable solo para82/83 sin cambiar la política original ni ocultar nuevos errores. Los fallos que propaga el builder se registran con contexto y excepción antes del checkpoint y se vuelven a lanzar; los callbacks no se liberan ante un fallo.

En el Editor, usando la GameDB original y su descifrado normal, ambas listas son no nulas, Count3, _size3 y backing array de longitud3. Las referencias de IList coinciden con el array y las claves son no nulas. La comparación completa con GetAllItems original conserva109tipos/3407registros, claves, orden y las mismas referencias ObjectData. No se usan punteros administrados sin protección ni se intenta validar direcciones arbitrarias en Vita; una corrupción nativa sigue requiriendo dump o evidencia adicional.

## Terminación y memoria

El barrido IL de todas las DLL finales16 encuentra cinco llamadas del juego a Application.Quit: confirmación de salida deFrontEnd, fin dePerformanceTestAutomation, SaveLockedPopup.Finish, error de permiso deSplash y UnsupportedDevicePopup.ExitButtonOnClick. Todas tienen marca QUIT REQUEST previa, ausente en las dos capturas.17convierte esas marcas en eventos TERMINATION con razón, contexto GameDB, hilo y stack; también observa OnApplicationQuit. No se interceptan ni reemplazan funciones internas del player.

No hay llamadas directas del juego a Environment.Exit/FailFast ni importaciones propias de sceKernelExitProcess/exit/abort. Las bibliotecas incluyen declaraciones Mono.Posix y funciones de framework como Console.Cancel→Environment.Exit o terminación de un subproceso Ping; no son prueba de ejecución por GameDB. Unity/Mono incluyen sus propias rutas nativas de terminación. Su mera presencia en símbolos/importaciones no explica el cierre. La ausencia de OnApplicationQuit o UnhandledException deja abiertas una terminación del sistema, fallo nativo, excepción no notificable y pérdida/bloqueo del logger.

Los contadores se trazaron en el IL y el player exactos: LPDDR y PHYSCONT proceden del helper que llama a sceKernelGetFreeMemorySize y devuelve sizeMain y sizePhycont. CDRAM pasa por PSP2GetCDRAMFree: suma tamaños de bloques del dispositivo gráfico, y puede devolver-1 si no dispone de la estructura. No es intercambiable con sizeCdram del kernel. GC.GetTotalMemory(false) aproxima ocupación administrada y no representa RAM libre ni todo el heap nativo. No se fuerza colección.

Los últimos valores de la primera sesión son LPDDR38797312, CDRAM84790944, PHYSCONT27262976 y managed20643840bytes, unos19,69MiB administrados. No prueban reserva contigua suficiente, tamaño del mayor bloque, ausencia de fragmentación, éxito de la próxima reserva ni agotamiento. No hay crecimiento administrado descontrolado demostrado. El helper del player no publica aquí el retorno del syscall; no se añade una afirmación de éxito que el logger no registra.

Durante P0 se retienen intencionadamente el JSON importado, GameData y los registros, hasta construir el mapa completo. Se limpian referencias de la tabla actual y se solicita Destroy del owner en el finally original. ObjectData debe sobrevivir en el índice. Un marcador DestroyScheduled o weakAlive no prueba liberación nativa. Cada lanzamiento empieza otro proceso; el checkpoint guarda posiciones, no objetos de ejecuciones previas. No se añadieron GC.Collect, expansión ni cambios de backend.

## Instrumentación nueva y límites

COUNT_DETAIL divide Trace, comprobación de nulo, identidad con el campo del owner, tipo real y la llamada original a ICollection.Count. Se limita a77–83; las verificaciones de identidad/tipo se limitan a82/83. Se conservan las trazas previas de tablas77–83 y filas seleccionadas. No se sustituye Count por un getter tipado ni se añade una raíz AOT nueva para List<OnBoardingData>.Count. Las marcas críticas de entrada/salida aCount solicitan sync del respaldo existente.

El supervisor nativo usa un socket no bloqueante y archivo propios, stack32KiB, prioridad inferior a la predeterminada y un heartbeat por segundo. No accede a Unity, objetos administrados ni al lock del emisor principal. Observa únicamente escalares: última secuencia aceptada, última marcada como retornando y fase de escritura/sync/envío. La fase8significa que la función nativa está por retornar, no que el consumidor administrado ya continuó. Son snapshots aproximados; se correlacionan varias muestras y las secuencias.

Sus paquetes HSW17W llevan secuencia propia y el mismo ID de sesión. El receptor guarda ambos canales sin cambiarse. El analizador distingue secuencias del juego y del supervisor, operaciones pendientes, memoria y errores. Si siguen los heartbeats mientras cesa el hilo principal, sabemos que queda vivo el supervisor. Si cesan ambos, aún no se distinguen todas las causas: Wi-Fi, subsistema de IO/red, kernel y terminación del proceso pueden producir silencio. El respaldo y un dump son necesarios para reducir esa ambigüedad. Un fallo al crear el supervisor se registra y no impide cargarGameDB; solo se intenta una vez.

El diagnóstico añade asignaciones acotadas de texto y un hilo/socket/stack; no tiene coste cero y puede mover el punto de fallo. El presupuesto32registros/2ms, los yields, esperas, callbacks, datos y flujo automático siguen iguales. No hay botones nuevos ni se desactiva audio o renderizado.

## Dumps y archivos que conservar

En los Reports locales solo se encontró el dump histórico deVPK1. También se revisaron las carpetas personales de descargas/escritorio/documentos y el área de ports; no se recibió un dump16. El almacenamiento de la consola no está montado: no se afirma que allí no exista. No se analiza el dump1con símbolos16como si correspondieran.

Se conservan el VPK16 exacto, su manifiesto SHA y los siete contenedores de símbolos SELF/SUPRX deUnity, con sus secciones ELF y debug completas; no se reconstruye otro player para analizar ese intento.17conserva sus propios símbolos y fuente/objeto/mapa del plugin. El handler existente solo añade contexto a un dump que genere el sistema, sin llamadas de IO/red/heap/Unity; no garantiza que un cierre sin pantalla produzca.psp2dmp.

Para la siguiente prueba: mantener la Vita yPC en la misma red, receptor activo en192.168.1.8:18194 e instalar únicamente17. El juego avanza solo. Conservar vita_live.log delPC, ux0:data/HSW_Vita/vita_live.log, ux0:data/HSW_Vita/vita_live_watch.log, el log administrado HSW_VPK17_* y HSW_GameDB14.checkpoint del directorio persistente, y cualquier.psp2dmp nuevo. No borrar el checkpoint sin registrar esa acción. Los archivos de consola pueden copiarse después del cierre al directorio privado Dumps de17, conservando los originales. No es necesario leer la pantalla a tiempo.

Hipótesis pendientes: despacho Mono/AOT o referencia de lista corrupta; detención en Trace/diagnóstico; bloqueo o fallo nativo del emisor; terminación asíncrona del player/sistema; reservas o fragmentación no medidas. No se declara una de ellas como causa sin correlacionar la nueva captura o un dump. La corrección mínima se decidirá después de esa evidencia.

## Validación y entrega final

VERIFIED local: compilación Mono/mcs de3744fuentes sin errores; prueba enfocada de listas y paridad109/3407; Editor45s termina enFrontEnd/comunes con0errores del juego y una carga/evento/completado. Se recibieron1715paquetes sin huecos ni fragmentos incompletos; la única excepción registrada es la simulada HSW_LIVE_SELFTEST del ensayo threaded. El supervisor nativo no corre enWindows: solo se comprobó su compilación/enlace SDK, contrato de acceso y decodificación del protocolo con un archivo sintético separado. Su ejecución física sigue UNTESTED.

Build final: Succeeded,0errores/487advertencias,00:03:00.2948067; Mono2x, BuildOptions.None, expansiónNone.58contratos generales y70de diagnóstico sobre las DLL finales,216marcas. IL original/16/17 guardado; la llamada ICollection.Count sigue en17, sin sustituirla.49archivos serializados y15bancos byte-exactos16;480texturas,424clipsHEVAG,140shaders y245passes conservados por equivalencia binaria y auditorías previas. No nuevas conversiones. Fuentes/cache exactas; nueve archivos existentes de diagnóstico/versión/binarios, ningún archivo agregado al proyecto. Las únicas diferencias finales enPlayerSettings son bundleVersion y psp2AppVersion.

VPK17privado:179818351bytes,288entradas,HGSKW1178/00.17,ATTRIBUTE2=0,SHA256 `a64ee99e1d115a2869b9e6683fd2d8009f49ecc87ff0e6eaad92d03226f11374`. CRC y hashes por miembro, copia permanente independiente, siete símbolos exactos y archivo CPP/O/MAP/stub verificados. El SELF normal del engine permanece idéntico. No ramas, publicación, aprobaciones ni mutaciones deEvolution/2017/VPK anteriores.

Fallos de herramientas conservados: firma const void* incompatible conSceKernelThreadEntry, corregida con el headerSDK; dos arranques de fixture fallan por Object ambiguo y acceso a helper internal, corregidos y compilados antes del ensayo válido; comprobador host interpretó LASTEXITCODE nulo dePowerShell como error aunque sus58contratos pasaban, corregida la invocación. psp2bin rechazó una opción corta; la consulta siguiente del símbolo local produjo una sección completa, conservada junto al extracto acotado. El primer build17 pasó compilación pero fue rechazado por configuración companyName temporal del ensayo. No se empaquetó; se guardó por separado y se reconstruyó con ajustes originales. El build final y su fuente pasan la comprobación estricta. Estos fallos locales no explican el cierre delVPK16 físico.

El texto CONTROLLED de un evento TERMINATION identifica un punto observado por nuestro código. Si reason es OnApplicationQuit engine callback, ese callback por sí solo NO prueba solicitud voluntaria del juego. Solo una razón QUIT REQUEST identifica las cinco llamadas explícitas instrumentadas. El analizador mantiene esa distinción.

Pendiente: ejecutar17enVita y correlacionar COUNT_DETAIL, OP, heartbeat principal y HSW17W, respaldo y dump si aparece. No se entregó una corrección especulativa del algoritmo ni se declara causa o estabilidad física demostrada.

## Resultado físico posterior17

OWNER-REPORTED: vuelve aLiveArea sin pantalla decrash. VERIFIED en captura y respaldos entregados:1123paquetes del juego y58heartbeats idénticos entreUDP yarchivos locales. OnBoardingData termina; T83completaTrace, null=false eidentidad/tipo de lista; última marcaBEFORE ICollection.Count. Sin mensajes posteriores locales ni dump aportado. El último heartbeat corresponde alpaquete1063, seguido de60paquetes principales; no demuestra bloqueo en suphase2. Causa no confirmada;17no repara el cierre. Se prepara18 con una candidata limitada a la ruta deCount, documentada por separado.
