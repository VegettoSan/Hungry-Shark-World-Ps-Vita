# VPK 34 privada: guardados y pausas de menús

Continuación correctiva autorizada por el propietario, sin cambios de gates: P00 ACTIVE, 0/13. Fecha local: 13 de noviembre de 2026; cierre UTC: 14 de noviembre. Se conserva VPK 33, SHA-256 `05c51275edb60c082243a1036870e5f324fdccfbcdbcf8d9ac696c71c9e4b861`, y su checkpoint. El propietario confirmó su funcionamiento físico, sin mejora significativa de FPS y con pausas persistentes. Es **OWNER-REPORTED**, sin una nueva captura causal. Se reverificaron los hashes y CRC del APK/OBB 132; se utilizaron herramientas locales y Unity 2018.2.19f1, sin Internet.

## Coste común y corrección

**VERIFIED en Editor:** las rutas probadas de recompensa de monedas y compra de mascota ejecutan tres guardados completos por acción. La recompensa base duró 85–88 ms; sus tres llamadas a `SaveFacade.Save` acumularon 82–83 ms. Los scopes internos se solapan y no deben sumarse otra vez. Esto demuestra el coste dominante de esas rutas en Editor; no demuestra que explique exclusivamente los segundos de congelamiento físico.

Solo cambian funcionalmente `FGOL.Save.SaveData` y `HSWPSP2SaveIO`:

- El temporal mantiene su contenedor reservado y padding exactos, pero se construye en bloques de 8 KiB y solo se escriben diferencias. También se comprueban y reparan padding incorrecto, truncamiento y crecimiento; no se confía en una caché del archivo.
- Las copias verificadas comparan todos los bytes mediante `Buffer.BlockCopy`, dos arrays locales de longs y una comparación de la cola. Se conserva la comprobación del archivo cerrado.

No se fusionan ni retiran guardados. Se mantienen la validación del principal, el respaldo validado, el temporal, su comparación contra el payload, el códec original y la copia verificada al principal. No hay hilos nuevos ni operaciones diferidas. JSON invariante, LZF, AES, MD5, cabeceras y esquema v3 permanecen intactos.

## Mediciones

| A/B en Editor, 30 tandas alternadas | Mediana antes → después | p95 antes → después | Máximo antes → después |
| --- | --- | --- | --- |
| Guardado completo, mismo perfil/payload | 26,4048 → 15,7187 ms | 31,1930 → 17,1872 ms | 33,2086 → 29,0381 ms |
| Copia y verificación cerrada | 7,9938 → 2,4475 ms | 8,5555 → 3,0033 ms | 8,7003 → 3,1707 ms |

El guardado completo reduce aproximadamente un 40 % su mediana en ese PC. El A/B comprueba 4952 bytes de códec original idénticos y valida ambos archivos cerrados en cada iteración. **No son resultados de FPS en Vita.**

En el fixture de 7000 bytes, cambiar un bloque escribe 1048576 → 8192 bytes; un temporal idéntico escribe cero. Un perfil mayor puede necesitar varios bloques. El escritor temporal aislado aún cuesta algo más en el disco del PC: mediana 0,950 → 1,2243 ms. El ahorro de las copias permite que el conjunto sí mejore.

Memoria: la estimación estructural del escritor anterior es aproximadamente 2 MiB de arrays y crecimiento, frente a 32772 bytes de scratch y un buffer de stream de 65536 bytes. Cada copia añade 16 KiB de scratch para reducir CPU. Una estimación inicial de 3,1 MiB era incorrecta y queda corregida expresamente. No se dispone de un pico de memoria comparable ni de una medición física en Vita. El snapshot de gameplay del Editor ronda 50 MB managed; no permite atribuir un ahorro de memoria al cambio.

## Validación y evidencia descartada

**PASS en perfiles aislados:** recompensa simple y doble; cantidades y avance; doble pulsación del botón original con una sola concesión; cancelación sin cobro; fondos insuficientes sin concesión; cierre de la oferta sin transacción real; compra con débito exacto e inventario actualizado. La prueba corta final compró `PetSharkPorbeagle` por 2000 monedas ficticias. Se fijó una puntuación de 1000 como precondición del fixture, sin modificar criterios de desbloqueo ni precios.

Los contratos cubren diez tamaños, límites de bloques, padding alterado, truncamiento, crecimiento, treinta escrituras exactas, todos los posibles bytes distintos y colas. Interrumpir el temporal en el bloque 2 conserva principal y respaldo exactos y válidos. Los cinco fallos de guardado deliberados del fixture heredado siguen separados de errores del juego.

Dos recorridos completos del comparador final pasan menús, selector y flechas de tiburones, LevelSelect/WorldSelector, Hawái, movimiento, turbo, pausa, reanudación, retorno y guardado/recuperación con cero errores. El perfil fresco también pasa; la prueba corta posterior vuelve a cubrir las transacciones con el código final. La imagen del panel antes/restaurada coincide en 27648 bytes.

Se conservan todos los fallos: captura con ensamblado viejo inválida; fixtures de retorno de oferta, sprite sintético nulo y tutorial inicial corregidos; comparación con `BitConverter` rechazada por ser más lenta; escritor diferencial con comparación por bytes rechazado por regresión de CPU. Una ruta intermedia falló por un seek inválido de Unity/Fabric al reanudar audio: no se filtró ni se declara reparado por este cambio. Los recorridos finales pasan y el audio nativo es exacto a 33. Los fallos de arranque del SDK bajo sandbox, resolución de dependencias en PowerShell 5 y ruta de un informe se corrigieron sin otro build Unity. Detalle privado: `ValidationFailures.json`.

## Modelos, transiciones y gameplay

No se repite la auditoría de escenas caché de 33 ni se descarga ninguna. LevelSelect y su retorno pasan, pero su coste dominante de activación sigue pendiente. No se alargan cortinas ni se cambia el orden de callbacks.

El primer acceso registrado al selector incluyó llamadas inclusivas a `GUISharkSpawner.Spawn` de 345–704 ms; alternar los dos modelos visitados produjo llamadas de unos 2 ms. Hay calentamiento del Editor: aún no se separan Resources.Load, Instantiate y activación. Ocho alternancias del preview de mascotas usan su ruta original; la mediana base fue aproximadamente 1,8 ms y el máximo, 3 ms. Estos datos no justifican retener más modelos en Vita. No se añaden cachés ni precarga general.

Se utilizó la ventana Profiler/Timeline y capturas normales breves con Recorder válidos. Sin Deep Profile ni lectura multihilo en vivo. No hay atribución nueva exclusiva del Render Thread. Los contadores pueden solaparse y GC.Alloc cuenta bloques, no bytes. La muestra de Hawái tenía solo tres controles de peces, dos con renderer visible: **no representa una zona densa** ni resuelve el tiempo físico del frame todavía sin atribuir. No hay nuevas modificaciones de IA, física, spawning, pools, animación o población.

## Oclusión

En la fuente actual, los 4994 objetos de Hawaii_low tienen flags estáticos cero. No aparecen ajustes/datos Umbra ni recursos de oclusión en los 49 archivos nativos examinados. La casilla de oclusión de las cámaras está activada; eso no acredita un bake. El snapshot contiene cero occluders/occludees, cero LODGroup, far clip 1000 y distancias por capa cero. Se conservan tres bounds grandes: no se demuestra que sean incorrectos. Existe código de culling por agua y hulls, pero no apareció una instancia activa de `CullingInjectedECS` en esa instantánea.

No se hizo bake ni A/B de oclusión. Falta demostrar un ahorro que justifique su CPU y memoria, especialmente ante el hilo principal físico cercano al 95 % observado en 32. La compatibilidad y el beneficio de un bake aditivo en PSP2 quedan pendientes. Los 505 renderizadores agrupados del player se conservan; los flags del Editor de pruebas no los representan.

## Entrega y checkpoint

Un build PSP2/Mono/Low+ normal: **0 errores, 497 advertencias, 3:16,0117**. Pasan 64 contratos y la comparación de 5862 tipos/44118 métodos existentes: únicamente Save/Copy modificados y WritePadded/EqualBytes añadidos. Se preservan 49 archivos serializados, 23 escenas exactas a 33, 63 mallas, 78 programas GPU, 505 renderizadores agrupados, AOT 4096, SELF, Fabric y otros 214 archivos de motor/audio/plugins/streaming. Cambian diez archivos existentes, ninguno añadido; los otros 20908 siguen exactos. Los cambios restantes son etiquetas de versión y plugin.

VPK privada: `local-work/HSW_Recovery/Reports/PSP2_VPK34/HSW_Vita_Test_00.34_HGSKW1178.vpk`. Tamaño: 164201971 bytes; 288 entradas. SHA-256: `f48f3edfd85617cb61bf8c4b393ae1240e381a41739c304a7deaa798a004c533`.

CRC y hashes por miembro, Before/After, símbolos exactos y rollback 34→33 en seco: PASS. VPK 33 queda intacta. Fuentes, perfiles, capturas y fixtures permanecen privados, fuera del player. No publicación ni gates aprobados.

**UNTESTED físico 34:** reducción real de pausas, guardado frío y durabilidad, memoria, FPS, audio audible y estabilidad prolongada. Siguiente paso: comparar reclamar/confirmar con 33 en Vita; después separar la primera carga/activación de modelos y LevelSelect. En gameplay, medir zonas escasas y densas con recorrido y reloj controlados, conservando población. No repetir la auditoría ni descargar las cachés ya resueltas.


## Prueba física posterior — 2026-11-14

REPORTED por el propietario: VPK34 no aporta una mejora perceptible de gameplay. La compra del mapa sí se completó con una pausa aproximada de3s, menor que antes; es una observación subjetiva, sin A/B controlado. Persisten las trabas al aparecer objetos en menús.

El selector quedó sin responder a controles, volver y tacto durante el primer tutorial después de una partida. Reiniciar y no tocar los controles permitió completar el recorrido. También reportó sonido humano superpuesto en dos partidas. Causas físicas no confirmadas.

Reportó reinicio de progreso al instalar34, pero no recuerda si sobrescribió33 o eliminó la burbuja. No se atribuye la pérdida al instalador o al guardado sin inspeccionar savedata; no se modificó su partida. Los pendientes marcados UNTESTED en la entrega original son históricos: esta prueba aporta las observaciones anteriores y deja persistencia/reset, audio y medidas físicas controladas abiertos. Continuación correctiva y culling: [VPK35](PSP2_CULLING_INPUT_VPK35_2026-11-14.md).
