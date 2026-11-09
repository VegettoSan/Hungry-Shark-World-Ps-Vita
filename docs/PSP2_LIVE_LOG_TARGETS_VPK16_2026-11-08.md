# Captura Wi-Fi y GameDB — VPK 16 privado

Fecha local: 2026-11-08. Evidencia técnica fechada en UTC, 2026-11-09. Estado: validación local satisfactoria; captura física pendiente. No se declara reparado el cierre.

## Interpretación del resultado físico de VPK 14

El propietario informa que BootLoader completa LoadSceneAsync, SaveLoader alcanza ready flag/spinner y comienza GameDB. El último fotograma muestra P0, T=77/109, ItemShopData, row=64, records=2353, last=77:63 y etiqueta type Add; el cierre ocurre aproximadamente a los 36,3 segundos. PREVIOUS muestra otra posición, T=83 Count. No se recibió un dump nuevo ni una captura UDP de ese intento.

La base original tiene 2289 registros antes de la tabla 77. La suma 2289 + 64 = 2353 coincide con el contador visible. ItemShopData contiene 213 registros: ese fotograma no demuestra que finalizara la tabla ni que empezara la 78.

| Índice, desde cero | Tipo original | Registros |
| --- | --- | --- |
| 76 | MasterKeys | 287 |
| 77 | ItemShopData | 213 |
| 78 | ItemUIData | 50 |
| 79 | ItemGameData | 182 |
| 80 | ItemGenericData | 258 |
| 81 | ConsumableSharkData | 56 |
| 82 | OnBoardingData | 3 |
| 83 | HUDThreatDetectionData | 3 |
| 84 | DailyRewardsMysteryChestData | 155 |

PREVIOUS es un snapshot leído al arrancar el logger y conservado durante la sesión; no representa otro cursor de la ejecución actual. El overlay anterior mezclaba la próxima tabla con el nombre anterior mientras actualizaba sus campos. La etiqueta mostraba la última solicitud. VPK 16 separa próximo cursor, último completado y última etiqueta solicitada; transmite PREVIOUS identificado como checkpoint anterior.

Los símbolos exactos de VPK 14 contienen 266141 entradas de función, con 23 coincidencias pertinentes. Esto no confirma ni descarta un problema de despacho Mono/AOT: existen funciones compartidas entre genéricos. No hay evidencia suficiente para atribuir el cierre a memoria, AOT, audio, gráficos o servicios.

## Instrumentación dirigida

Se conserva el algoritmo incremental: máximo de 32 registros por avance, una tabla por avance, presupuesto blando de 2 ms y el mecanismo de reproducción del checkpoint. No se cambian esperas, yields, callbacks, cachés ni datos. El logging añade coste de observación y puede afectar la reproducción.

Se registran entrada y salida de asociación de lista, Count, creación del diccionario e inserción por tipo en las tablas 76–84. El detalle de acceso IList, lectura de key y Dictionary.Add se limita a las filas 60–70 y últimas cinco de la tabla 77, las primeras ocho de la 78 y todas las de 82 y 83. Se conserva la clave ya leída; no se invocan getters derivados para diagnóstico. El resto mantiene trazas por lote y el afinado automático del checkpoint previo. Las excepciones se registran y propagan: no se consideran operaciones completadas ni se omiten registros.

BATCH_DONE separa tabla/fila inicial, próximo cursor y último registro completado. Los snapshots de memoria tienen sus propios BEFORE/DONE e incluyen LPDDR, CDRAM y PHYSCONT libres y GC.GetTotalMemory(false). No se fuerza GC ni se suman pools distintos. El analizador conserva pares pendientes, memoria y contexto dirigido; una entrada sin salida es una pista, no prueba de la instrucción que falló.

La construcción sigue siendo bombeada por la coroutine de App desde SaveFacade; no se introducen workers. El Editor confirma hilo principal. Los paquetes incluyen hilo administrado y SceUID nativo para comprobarlo en hardware y distinguir callbacks de otros hilos.

Se observa creación y solicitud de Destroy en sus ubicaciones originales. Ocho referencias débiles acotadas evitan que el diagnóstico retenga cargas. Reachability administrada y DestroyScheduled no demuestran liberación nativa ni una fuga. Durante la construcción se espera que el owner actual siga vivo; las referencias ObjectData deben conservarse. En una recarga, la GameDB anterior permanece válida hasta el commit. Los callbacks de éxito siguen esperando a la inicialización completa.

## Transporte y respaldo

VPK 15 ya estaba construido cuando llegó la evidencia nueva de tablas 77/83. Se conserva como intermedio no entregado con sus símbolos; VPK 16 incorpora esta petición. Ningún VPK anterior se sobrescribe.

No había DebugNet integrado. El logger existente se conecta a un módulo pequeño construido con el SDK local y el ABI del ejemplo oficial de plugins de Unity 2018.2.19f1. Reutiliza o inicializa NET/libnet/netctl comprobando retornos; reserva un pool de 64 KiB únicamente si libnet no estaba inicializada. Nunca termina servicios compartidos ni descarga NET.

UDP se dirige a la IPv4 configurada del PC, puerto 18194, con socket no bloqueante y MSG_DONTWAIT. No hay DNS, connect ni espera de Wi-Fi. Sin dirección IP no se intenta enviar. Las excepciones del transporte están aisladas de GameDB. La rama nativa requiere validación física; el fallo de socket se ensayó en el Editor.

Los paquetes contienen versión, sesión, secuencia, mensaje/fragmento, UTC, reloj monotónico, hilos y tipo. El envío se limita a 1200 bytes por paquete y 20000 datagramas por sesión, sin cola ilimitada. El callback threaded no usa APIs Unity; UnhandledException observa sin cambiar la política de terminación.

El receptor existente guarda y vacía cada mensaje en vita_live.log del entorno de trabajo. Solo se añadió configuración UTF-8 de consola y buffer de recepción de 1 MiB. El propietario habilitó la regla temporal de firewall limitada a Python, dirección local, subred y UDP 18194. El receptor real permanece activo. Los ensayos del Editor usan loopback:18195 y un archivo separado.

El módulo intenta append en ux0:data/HSW_Vita/vita_live.log, escribe antes de enviar y sincroniza en operaciones críticas o cada 250 ms. Publica códigos de apertura, escritura, sync, red y registro del handler. El acceso real a esa ruta sigue sin comprobarse en Vita. Se conserva el respaldo anterior en Application.persistentDataPath con AutoFlush.

El callback de coredump solo añade el último contexto mediante sceCoredumpWriteUserData, con stack de 16 KiB, sin UDP, archivos, heap ni código administrado. No reemplaza otro handler existente. No garantiza que una Vita retail genere .psp2dmp ante un cierre; no se provoca un crash ni se activa Development/Razor. Se conservan los siete archivos de símbolos exactos del player, módulo y wrapper, más CPP/O/MAP/stub/receta del plugin.

## Validación y límites

- Compilación de 3744 fuentes: cero errores, 405 advertencias.
- Editor 16: 45 segundos, FrontEnd y escenas comunes, 109 tipos y 3407 registros, cero errores del juego, una carga/evento/completado, cap 60/VSync 1. Captura de 1664 paquetes sin huecos ni fragmentos incompletos. La excepción simulada está etiquetada como ensayo del Editor.
- Editor 15: captura completa de 1144 paquetes y prueba de socket fallido; ambas llegan a FrontEnd. Los hooks de ensayo quedan excluidos del player.
- Build 16: Succeeded, cero errores, 487 advertencias, duración 00:03:04.5039386; Mono2x, BuildOptions.None y expansión de memoria None. La espera del host termina con código cero.
- Contratos sobre el player final: 58 generales y 64 de diagnóstico; 208 marcas. Los 49 archivos serializados y 15 bancos de recursos son idénticos a 15 y, por comparación previa, a 14. Se reutiliza la auditoría de texturas/audio/shaders, sin conversiones masivas.
- Alcance final: nueve archivos existentes, incluidas dos versiones y dos binarios del módulo; ninguna fuente nueva respecto a 15. Fuentes privadas y caché coinciden. Rollback a 15 validado en seco, sin aplicarlo. Originales, Evolution, Unity 2017, datos, audio, gráficos, controles, guardados y offline conservados.

Fallos de herramientas registrados: flag SNC no soportado, cast con warning, indentación inicial del receptor y variable del empaquetador de símbolos 15. Se conservaron las evidencias y se corrigieron sobre el mismo trabajo; no fueron fallos físicos de Vita. Una captura inicial incompleta se repitió satisfactoriamente. El build 16 responde a evidencia nueva recibida después del 15.

Paquete privado: 179810989 bytes, 288 entradas, HGSKW1178/00.16, ATTRIBUTE2=0. SHA-256: `878d4691ff5858a47c89dfd74e107ea790cc2f009811ef19bbe43d39579c3db3`. CRC, miembros/runtime, símbolos y copia permanente verificados. Sin publicación, ramas ni cambios del ledger; P00 permanece activo y 0/13 aprobaciones.

El log físico tiene cero bytes al preparar la entrega. Falta ejecutar VPK 16, revisar secuencias, pares de operaciones, memoria y hilos, y correlacionar cualquier dump con sus símbolos exactos. La última línea puede preceder a un fallo asíncrono o faltar por pérdida UDP; no basta para determinar la causa.
