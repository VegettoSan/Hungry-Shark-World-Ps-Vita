# VPK 27 privado: rendimiento sin diagnóstico intensivo

El propietario autorizó expresamente optimizar el estado funcional de VPK 26 y generar una prueba privada VPK 27. No se cambian fases ni se publica el paquete. Se mantienen Unity 2018.2.19f1, Mono2x, BuildOptions.None, memoria modo 3, AOT 4096 y los ajustes gráficos, controles y simulación de VPK 26. No se añade overclock.

## Evidencia y cambios

El log físico local de VPK 26 termina con 11070 paquetes y 112828 ms acumulados de transporte. Dos inicializaciones completas duran 40757 y 36655 ms: pools 35817/32505 ms y Spawner 4777/4013 ms. La primera inicialización registrada de CrabLarge ocupa 830 ms, incluyendo instrumentación. Hay 1616 registros de fronteras de AudioSource. Estas ventanas incluyen diagnóstico y no aíslan coste nativo de audio, GPU ni instanciación. Gameplay continúa lento sin cargas nuevas: eliminar logging no demuestra resolver todo el frame.

Se implementaron tres grupos reversibles:

1. **Diagnóstico primero.** Las llamadas detalladas y sus argumentos se excluyen al compilar. Se eliminan el contexto de pulso por frame, registros por audio/objeto/fila, enumeración diagnóstica de suscriptores y diario de diagnóstico de GameDB. Los pasos rutinarios de guardado dejan de transportar mensajes y forzar sincronizaciones. El observador nativo periódico no se inicia. Los errores importantes, incluidos los de hilos secundarios, y los límites generales de carga conservan respaldo local; se evita duplicar errores del hilo principal.
2. **CPU y audio.** En PSP2 normal se excluyen las llamadas a geometría de depuración cuyo código recuperado solo calculaba puntos sin dibujarlos. Fabric.Core permanece idéntico; su adaptador evita nombres, claves y getters de clips destinados a trazas cuando Trace es null. Las operaciones originales de cargar, asignar y reproducir audio siguen ejecutándose. No se filtran eventos sonoros.
3. **Pools.** Tres colas reutilizan espacio de ordenación estable en lugar de crear listas LINQ. Se conserva el orden descendente, incluidos empates, NaN e infinito; el espacio auxiliar borra referencias. No cambian prioridades, cantidades, presupuestos por frame ni activación. La población inicial sigue completa y síncrona: no se introducen yields dentro de GameStateInit, cuyo llamador utiliza inmediatamente sus resultados.

El detalle se activa con `HSW_PSP2_VERBOSE_DIAGNOSTICS` en los símbolos PSP2; el constructor nativo acepta la variable del mismo nombre con valor `1`. La entrega normal omite ambos. `HSW_PSP2_BOOT_LOG` conserva únicamente diagnóstico básico y métricas agregadas.

## Validación local

**VERIFIED:** compilación C# normal y detallada; una compilación nativa, 0 errores, 501 advertencias, 3:13,666. Pasan 61 contratos generales y 39 de rendimiento/preservación. Quince tipos conservan IL completo de VPK 26; se verifican también campos originales y el IL de cabecera/integridad del guardado. Los 49 archivos serializados y 15 bancos de recursos son idénticos, igual que el SELF normal y Fabric.Core. No se modifican APK/OBB, texturas, materiales, shaders ni el proceso de datos del usuario; SHA/CRC de ambos originales verificados.

Editor es-ES: 109 tipos, 3407 filas y 16847 campos numéricos originales; menú, Hawái, jugador vivo más de ocho segundos, una carga/callback/evento, cero errores del juego. Ordenación equivalente para 260 longitudes con casos especiales y reutilización sin referencias residuales. Guardado nuevo, sobrescritura, respaldo, copia diferencial, corrupción/fallo parcial y recuperación pasan. Se clasifican exactamente cinco mensajes esperados de esas inyecciones, sin silenciar errores del juego.

La captura local final contiene 108 paquetes completos y 13 ventanas PERF, sin OP/GDB/PULSE/LIFETIME ni registros individuales de recursos. Es evidencia de reducción del diagnóstico, **no de mejora de FPS en Vita**. EndOfFrame no progresa en este Editor batch; su cadencia requiere validar el player físico. No hay verificación visual nueva mediante captura.

Se conservaron los fallos de herramientas/fixture: compilador/editor bloqueados por sandbox y ejecutados con escalación; errores de codificación/quoting durante preparación; fixture con doble BootLoader; recuento de errores que inicialmente incluía las corrupciones deliberadas. Se corrigió la fixture y pasó el flujo completo; no se parcheó el juego para ocultarlos.

## Comparación física

Usar la misma partida, tiburón, Hawái y recorrido, sin overclock. Comparar primer arranque tras cerrar por completo y segunda entrada sin cerrar; observar también regreso a tienda/selector, música, efectos, comida, turbo y guardado/carga posterior.

PERF sale cada cinco segundos por UDP **sin escritura ni sync periódicos al disco**; conservar el receptor del PC en puerto 18194. `updateHz` cuenta Update; `endFrameHz` cuenta finales de frame de Unity en CPU, no scanout ni tiempo GPU. Comparar FPS medidos en consola, `frameMeanMs`, `frameP50BucketMs`, `frameP95BucketMs`, `frameMaxMs`, `over33`, `over50`, `over100`; objetivo 30 FPS ≈33,3 ms. Los buckets son de 1 ms y 120 significa ≥120 ms. Ignorar ventanas de transición para evaluar gameplay sostenido.

Comparar además diferencias de contadores acumulados de transporte y CPU, `resourceCalls`/`actualLoadTotalMs`, tiempos BEFORE/DONE de pools/Spawner y pausa máxima al guardar. Las ventanas CPU se solapan: no sumarlas como costes independientes. `cacheHits` no se recopila en modo normal y se ignora. Registrar managed, LPDDR/CDRAM/PHYSCONT antes/después de cada partida y al volver al selector; no se afirma fuga ni liberación nativa a partir de memoria administrada solamente.

**UNTESTED:** FPS, latencia, audio físico, persistencia tras reinicio y estabilidad prolongada de VPK 27. No se promete alcanzar 30 FPS. Evidencia, hashes, cambios fuente, checkpoints de reversión y símbolos exactos permanecen en el directorio privado `PSP2_VPK27/`.

Entrega privada: `HSW_Vita_Test_00.27_HGSKW1178.vpk`, 179888724 bytes, 288 entradas, CRC/hash por miembro verificados. SHA-256: `ce89a202d00a3e231220db11a429cd87a095042177615de7c8b406f64718dc01`. Se preservan VPK 26 y símbolos exactos de ambas versiones. Dieciséis archivos existentes modificados, cero añadidos al proyecto; ajustes solo cambian las dos versiones. Reversión protegida a VPK 26 comprobada en seco, sin rutas de partidas.

## Primer checkpoint físico, 10 de noviembre

**VERIFIED al corte 2026-11-11 03:03 UTC:** sesión27 con 211 paquetes consecutivos, cero fragmentos incompletos y ningún error/salida recibidos. FrontEnd a 41088 ms frente a 80331 ms en26 para el mismo marcador; ejecuciones distintas sin control de caché. Ventanas estables FrontEnd50–51 endFrameHz/p9520–22ms; visor39–45/p9524–27ms. Se confirma que WaitForEndOfFrame avanza en el player físico; sigue siendo finalización CPU, no scanout.

Tienda/selector muestran ventanas lentas, algunas con 7–8 cargas y 2,7–3,0s dentro de Resources.Load en aproximadamente5s, sin coste apreciable de transporte en esas ventanas. También hay pausas sin cargas nuevas; no se atribuye todo al cargador. Tras navegar muchos tiburones hay unos63MiB LPDDR libres y34MiB managed: no demuestra fuga. El último estado es SharkSelect; todavía no hay Loading, GameStateInit ni SESSION_STARTED en este corte. Gameplay sostenido, audio y persistencia fría siguen pendientes. Snapshot y análisis privados en `Physical27_Input/20261111T030300Z/`; no se modificó el runtime durante la prueba.

## Gameplay físico, checkpoint posterior

**VERIFIED al corte 2026-11-11 03:06:34 UTC:** SESSION_STARTED a361165ms. Loading→sesión50470ms frente a82329ms de la primera entrada26; GameStateInit32594ms frente a40757ms, pools29553 frente a35817ms y Spawner2935 frente a4777ms. Son ejecuciones distintas, con navegación, acciones, mejoras del tiburón e historia de caché diferentes; no es un benchmark A/B controlado.

Excluyendo los primeros10s de partida,20ventanas/100,753s registran1557finales de frame: **15,45/s**, rango por ventana12,42–18,52; frame medio ponderado64,71ms, p95 por ventana57–97ms, máximo169,13ms y11frames superiores a100ms. No se acredita una mejora importante del rendimiento sostenido frente a las14–17llamadas Update/s de26, ni30FPS. EndFrame sigue siendo finalización CPU y no scanout.

En esa muestra no hay nuevas llamadas de ResourceLoaderManager y el contador de transporte no aumenta a su resolución entera de1ms. ManagedUpdates.Update mide7,42ms por llamada; StateMachine1,64ms, FixedUpdate0,42ms, LateUpdate0,26ms y cámara0,50ms. Las ventanas se solapan y no cubren todo Unity: no se suman ni permiten atribuir el resto exclusivamente aGPU, audio, animación o física.

Reaparece un registro del guard original `AttackDuration >30`, ya observado en26, después del inicio; no se suprime ni modifica.368paquetes consecutivos,0incompletos y ninguna salida/fatal recibida. Durante la muestra managed pasa32,19→36,25MiB, LPDDR libre61→57MiB y CDRAM libre permanece78,2MiB: variación acotada de esta ventana, no evidencia suficiente de fuga. Análisis privado `GameplayPhysical27Summary.json` y snapshot `Physical27_Input/20261111T030634Z/`. La compilación permanece intacta durante la prueba.
