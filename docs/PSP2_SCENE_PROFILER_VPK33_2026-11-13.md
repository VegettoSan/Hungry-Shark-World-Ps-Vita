# VPK33 privada: escenas, consultas y Profiler

Autorización correctiva expresa del propietario; prioridad actual: cerrar solo la tarea pendiente del pool y después revisar escenas/cargas. P00 ACTIVE, 0/13; no se cambian gates ni se publica el proyecto recuperado. Unity2018.2.19f1/Mono/PSP2,Low+,960×544,memoria/AOT actuales y datos originales conservados. Entrada VPK32 SHA256 `56ffe8f21aa2e88a90fd39d994a663ef1bb34edae027aa02f56ffb55661cc238` y checkpoint privado protegidos. Fecha local de continuidad13nov; ejecuciones posteriores registran UTC14nov.

## Tarea pendiente completada

**VERIFIED Editor:** EntityPool.ProcessData expandía aun si una instancia había vuelto al pool mientras la petición esperaba. Se reutiliza únicamente la cabeza libre válida por el camino ReturnData original; si falta o está destruida, continúa la expansión original. PoolList.TryPeekFree no consume la lista. Sin cambios de población,prioridad,presupuesto,callback ni IA.

Ocho contratos PASS: retorno tardío,miss real,cabeza destruida,orden callbacks,cantidad activa,dos peticiones distintas,LIFO y prioridad/inicialización. RecorridoCPU33PoolFinal terminaShop,0errores de juego,un flujo de guardado y callbacks,es-ES,Hawái/movimiento/turbo/pausa/retorno/recuperación. Reutilizar objetos no garantiza una secuencia RNG global idéntica a clonar más objetos. El caso redundante observado fue una partícula de0,2704ms en Editor; el pico distinto de316,168ms correspondía aTubeMan sin instancia libre. **No atribuir ese pico al ahorro del pool.**

## Referencia de escenas

`Scene33Baseline` y `Scene33Final`: dos visitas mediante transición original aSharkSelect/back,Shop/popup,LevelSelect/WorldSelector,Hawái,pausa,retornoShop. Inventario por escena/raíz,componentes activos,cámaras,animadores/renderers,colisiones y memoriaEditor,con instantáneas fuera de ventanasCPU. No se desactiva ni descarga nada para medir.

**VERIFIED:** SharkSelect permanece como caché pero vuelve a0objetos activos,0cámaras,0renderers,0animadores. Shop queda con su UI inactiva durante selector/globo. Sharks/3DBackground son escenas comunes intencionales: muestran el tiburón/fondo y reciben callbacks de varias pantallas. La cargaSingle deMenuToIngame descarga las escenas anteriores del menú. En gameplay,Results permanece preparada con0cámaras/renderers/animadores;su raíz y servicios no justifican descargarla. MenuToIngame también contiene clones de gameplay como raíces hermanas: descargar la escena por su nombre rompería la partida. Su cámara de introducción queda inactiva después del inicio.

Shop vuelve de las dos visitas con745objetos activos,35renderers,19animadores en ambas muestras;SharkSelect inactiva en ambas. Hay calentamiento inicial de UI y cantidades dinámicas de tiburones/presas,pero no acumulación creciente demostrada en este recorrido corto. MemoriaEditor no es memoriaVita ni prueba ausencia de fugas a largo plazo. Se conservan audio,Fabric,IA,física y cámaras de plataforma.

## Correcciones implementadas

* NextScreenPreLoader: una consulta de jerarquía en lugar de dos;reutiliza el array para las dos pasadas,manteniendo destinos multi-screen antes de single-screen y su orden original.
* ScreenTracker y finalización del preload: consultar primero SceneRegistry ya existente;mantener GameObject.Find como fallback. Sin nueva caché,retención ni cambios del orden de carga,activación o eventos.
* Corrección del pool pendiente descrita arriba. Sin nuevos recursos ni batching adicional.

A/B aislado sobre las mismas jerarquías reales,siete tandas alternadas de100consultas,mediana. En una muestraSharks20,6765→10,3407ms por100consultas;Shop7,6327→3,5348ms. En el globo,otra muestraLevelSelect9,9018→5,1788ms por100. Registro deWorldSelector0,0287ms/100 frente búsqueda global1,1686ms/100. Identidad de raíces activas y orden completo de transiciones PASS. Se eliminan una búsqueda nativa y un array por notificación;no son costes por frame ni una gran reducción acreditada de las pausas físicas.

## Profiler y límites

Se usa la misma instancia/proyecto privado;al recuperar esta continuación estaba cerrado y se abrió únicamente ese proyecto. VentanaProfiler confirmada. Capturas normales acotadas a90frames por estado;sin grabaciones binarias continuas adicionales. El frame dump profundo anterior conserva sobrecarga importante y avisosAttackDuration conocidos: **FAIL de recorrido**,no benchmark válido. CapturaAfter inicial detenida por ensamblados anteriores: **INVALID**,sin resultado atribuido.

Dos intentos de lectura multihilo en vivo produjeron `Unknown profiler data message in thread block`;ambos **FAIL** se conservan. Leer el frame previo tampoco corrigió el fallo. Se retiró ese lector del fixture y se usaron Recorder nativos válidos y ventanaProfiler,con un guardado acotado de gameplay. El fixture estricto no filtra esos errores para conseguirPASS. `Scene33Final` completo **PASS:0errores de juego**,guardado/recuperación,controles y callbacks originales;cinco fallos deliberados de guardado separados. Imagen de cámara antes/restaurada exacta27.648bytes.

Una ventana de90frames de gameplayEditor registraCamera.Render≈1,905ms,ManagedUpdates.Update≈0,490ms,Physics.Processing≈0,146ms,Animators.Update≈0,157ms yMeshSkinning≈0,075ms. Los marcadores pueden solaparse/incluir otros hilos o trabajoEditor;no sumarlos ni convertirlos en FPSVita. GC.Alloc son bloques,no bytes;PlayerLoop válido con0muestras no equivale a coste0. No hay A/B global de frame equiparable entre el lector previo y losRecorder finales. El A/B causal disponible es de consultas sobre la misma escena.

Vita32 física: hilo principalOS≈95%,12,431finalesCPU/s sinOC en una ventana y≈18Hz conCPU500 en rutas diferentes;Managed7–10ms deja costes sin aislar. Estas evidencias no demuestran que las escenas caché sean el cuello dominante. **La mejora sostenida de FPS y la reducción de pausas/cargas en Vita33 siguen UNTESTED.** No se promete25/30FPS. No se añade overclock ni se fuerza paralelismo.

## Entrega

**VERIFIED local:** una compilación nativa,Succeeded0errores502warnings,3:15,045. Un único paquete privado00.33/HGSKW1178,164197143bytes,288entradas,SHA256 `05c51275edb60c082243a1036870e5f324fdccfbcdbcf8d9ac696c71c9e4b861`. CRC y hashes de cada entrada PASS. No se publica el VPK.

Auditoría completa:5.862tipos/44.117métodos existentes comparados;únicamente los métodos previstos en cuatro tipos runtime yTryPeekFree nuevo.61contratos,23escenas byte-exactas32,63mallas decodificadas/comprimidas iguales,78programasGPU y sus estados iguales,505renderersbatch,AOT4096. SELF,Fabric y214archivos de motor/audio/plugins/streaming exactos32;recursos .resource/.resS exactos.12archivos existentes modificados,0añadidos,20.906intactos. Versiones/settings y etiquetas del shim nativo cambian solo de32a33.

El control de fuentes bloqueó cinco materiales modificados únicamente en la copiaEditor por las pruebas. Se archivaron y restauraron desde el canónico32 antes del build;ningún cambio de material se admitió en producción. La primera comparación estricta de la tabla de arranque falló por reindexado de diccionarios de nombres y orden de dos callbacks de cap;inspección por índices resueltos y pruebaCecil independiente acreditan pertenencia/flags/fases intactos y únicamente asignaciones idempotentesVSync1/cap60 en distinto orden. Se conserva el fallo inicial;no se recompila para ocultarlo ni se ordenan otros callbacks.

Before/AfterZIP,patch privado,siete símbolos exactos+plugin yrollbackguardado33→32 en seco PASS. VPK32 preservada. Unity queda abierto;fixtures fuera del player. Solo documentación saneada en el repositorio;P00ACTIVE0/13.

**UNTESTED físico33:** FPS sostenidos,pausas/cargas,memoria,audio audible,guardadofrío y estabilidad prolongada. Son mejoras acotadas de trabajo redundante;no se presenta como resuelto el cuello dominante de gameplay. Las cifras deSharks son un benchmark deconsulta sobre esa jerarquía,no prueba de frecuencia de invocación del preloader para cada raíz. Evidencias,fuentes recuperadas,capturas,perfiles binarios y checkpoints permanecen privados e ignorados.
