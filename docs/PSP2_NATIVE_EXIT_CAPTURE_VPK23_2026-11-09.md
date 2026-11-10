# Salida nativa: VPK privado 23

## Resultado físico de 22

**VERIFIED:** sesión `368167b6ad62`, 5172 mensajes principales consecutivos sin huecos; terminan los cuatro pools, incluido CrabLarge. Último registro principal: BEFORE GameStateInit spawner init. Además se recibe:

```text
HSW22E|368167b6ad62|k=NATIVE_LIBC_EXIT|us=219242978 nt=1073808041 accepted=5172 returned=5172 phase=8 libc_atexit_observer_status_not_available
```

El observador normal de salida de libc se ejecutó. No proporciona código, motivo ni stack; no demuestra una salida solicitada por gameplay. Sin excepción gestionada/OOM/quit registrados ni dump nuevo proporcionado. Última muestra principal: LPDDR 68157440, CDRAM 82334560, PHYSCONT 27262976, managed 27262976 bytes; contexto, no prueba de suficiencia de memoria. Las reparaciones funcionales de IA de 22 se conservan y el límite anterior de CrabLarge se supera; gameplay sigue pendiente en Vita.

## Investigación y cambios

Se revisaron singleton/constructor SpawnerManager, estado guardado, consulta de amenaza, detector, grids, spawners, SpawnPlayer, equipo, mascotas y callbacks. No apareció otro defecto funcional reproducible que justifique una reparación nueva. Hipótesis de wrappers genéricos/arrays multidimensionales permanecen **UNTESTED**; no se sustituyeron estructuras ni presupuestos AOT.

El runtime exacto contiene una ruta fatal de `g_logv` que vacía stdout/stderr y llama `exit(-1)`; su ejecución física concreta sigue sin demostrar. También exporta `mono_unity_set_vprintf_func`, cuyo setter instala el callback de impresión; el callback inicial corresponde a libc `vprintf`. Se utiliza ese API mediante el stub existente, sin parchear Unity/Mono o direcciones nativas.

23 añade captura `HSW23M` con sesión/secuencia/tiempo/hilo, buffers acotados en stack, va_copy y retorno a vprintf con argumentos originales. Restaura vprintf al cerrar el logger y durante la salida normal observada. Respaldo append/sync/cierre en `ux0:data/HSW_Vita/vita_mono_native.log` y UDP no bloqueante al receptor actual. No usa Unity/objetos gestionados ni manejadores de señales. Captura 128 mensajes ordinarios; trampolin/JIT/fatal/assert evitan ese límite; textos largos pueden truncarse. No se promete capturar otros canales nativos. Autoprueba explícita al iniciar: `HSW_SELFTEST native printf text=preserved value=23 real=1.25`.

BEFORE/DONE separan resolución del singleton, entrada del spawner, arrays/grids, jugador, equipo, mascotas y callbacks. Permanecen operaciones/orden originales, sin pausas ni nuevos botones. Se mantienen UDP principal, heartbeat y respaldos anteriores; analizador actualizado para canales M/E separados. La captura añade IO cuando Mono imprime, no por cada iteración del gameplay; comportamiento real pendiente en hardware. La ausencia de un mensaje fatal M no excluiría errores por otros canales o terminación asíncrona.

## Validación local

**VERIFIED:** único build Unity 2018.2.19f1, Mono2x, BuildOptions.None, 0 errores/492 warnings, 03:01.4111487. SELF normal exacto SHA `14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`; sin Development/Razor. Memoria enum3, VeryLow original, 60cap/VSync1 y presupuestos AOT/GameDB 32 filas/2ms iguales a 22.

58 contratos generales, 104 diagnósticos, 325 marcadores; diez tipos protegidos GameDB/save/IA con IL/campos exactos a 22. Los 49 serializados y 15 bancos de recursos son byte a byte iguales; 23 escenas. Auditorías históricas 424 HEVAG/480 texturas/140 shaders reutilizadas, sin conversiones. Comparación de fuentes mantiene operaciones de SpawnerManager/Grid tras retirar marcas; singleton evaluado una sola vez. Diez archivos existentes cambiados, cero nuevos; settings solo dos versiones 22→23. Fuente/cache coinciden, GUID conservados, rollback22 dry-run validado, sin partidas modificadas.

**VERIFIED Editor:** GameDB109/3407, guardado/callbacks una vez, FrontEnd, transición original de carga/Hawaii_low/pools/SpawnPlayer/GameSessionStart; App.InGame y jugadores válidos más de ocho segundos, cero errores del juego. Fixture configura componente original de carga, no valida cada interacción UI. 5594 paquetes completos consecutivos; un único error deliberado de autoprueba del logger. API/ABI de captura nativa **UNTESTED hardware**.

## Entrega y próxima prueba

`HSW_Vita_Test_00.23_HGSKW1178.vpk`: 179832045 bytes, 288 entradas, SHA:

```text
9136a2e76f018f8bbc035a9bbe838ee5a757c70ac69fe8c8774fa4467ba7a2f8
```

CRC/hashes/espejo/siete símbolos exactos y símbolos adicionales del plugin verificados. VPK22/anteriores preservados; sin ramas, fases, publicación o alteraciones Evolution/2017.

1. Mantener receptor Python en 192.168.1.8:18194, sin borrar el log acumulado. Instalar 00.23 y repetir el mismo nivel; sin botones nuevos.
2. Tras el resultado, conservar log del PC y copiar de `ux0:data/HSW_Vita/`: vita_live.log, vita_live_watch.log, **vita_mono_native.log**, vita_native_exit.log; conservar cualquier nuevo .psp2dmp.
3. Guardar VPK exacto, VPK23_ExactSymbols.zip, VPK23_NativePluginSymbols.zip, manifiestos/recibos privados. Correlacionar sesión/hilo/heartbeats; la última línea no identifica por sí sola la causa.

**Estado:** diagnóstico que conserva las reparaciones funcionales de 22. No hay nueva reparación demostrada del cierre posterior. No se declara solucionado ni gameplay estable en hardware.


## Resultado físico posterior de 23

**FAIL hardware:**cierre durante poolfila37;5278UDP/localexactos. **VERIFIED:**captura nativa Mono reporta agotamiento type0/mscorlib1024 y observadorlibcexit9029usdespués,mismo hilo. Causa de23 identificada;sin dump nuevo. [Reparación candidata24](PSP2_MONO_TRAMPOLINES_SAVE_IO_VPK24_2026-11-09.md).
