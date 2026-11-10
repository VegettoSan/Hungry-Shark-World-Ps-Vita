# VPK 26 privado: reducir el coste del diagnóstico

Autorización: el propietario pidió optimizar la copia privada actual y continuar con otra prueba física. No se modificaron las fases, ramas ni versiones anteriores. Candidato Unity 2018.2.19f1, Mono2x, BuildOptions.None. No es una publicación.

## Evidencia de VPK 25

**VERIFIED, hardware/propietario:** gameplay con proporciones normales, HUD normal y stick que responde entre pausas. Tras jugar un rato desaparecieron las pausas al comer, usar turbo y moverse. Volver a entrar al nivel sin cerrar el proceso cargó más rápido. El propietario estima unos 20 FPS en menú y menos de 15 en gameplay; son observaciones, no una medición de GPU.

El log confirma cultura es-ES con JSON `0.5=0.5` y valores originales de BlackTip/HUD/salud. La corrección numérica de VPK 25 se conserva. La sesión alcanzó el límite de 6000 llamadas al diagnóstico detallado; después continuaron los pulsos y el observador nativo. El informe de fluidez llegó después de ese corte. **INFERRED:** las escrituras de diagnóstico contribuyen a las pausas; la caché caliente también puede contribuir. No se ha aislado una causa exclusiva.

El tiempo desde el logger hasta la primera cámara del menú fue 226060 ms; Loading hasta SESSION_STARTED, 396578 ms. No se debe sumar indiscriminadamente ventanas anidadas ni interpretar todo el tiempo como carga de disco. GameDB decode tardó 4,614 s, sin evidencia de una regresión grande del parser.

## Cambios pequeños y reversibles

- Una sola copia primaria del diagnóstico: UDP y respaldo nativo se conservan. Cuando su estado almacenado indica escritura y vaciado correctos, las marcas rutinarias dejan de duplicarse en TTY y en el archivo secundario de inicio. Si ese respaldo no está disponible, se mantiene el fallback. Los errores conservan también ese respaldo secundario. El estado puede tardar hasta el siguiente sondeo en reflejar un fallo nuevo.
- El reloj de `sceIoSyncByFd` se actualiza **al terminar** el vaciado. Antes se usaba la hora anterior a la operación: si tardaba más de 250 ms, el paquete siguiente podía iniciar otro vaciado inmediato. Se conserva el intervalo de 250 ms; se corrige su referencia temporal. La presencia del defecto es verificable en código; su coste físico se medirá con VPK 26.
- Las marcas por fila de los pools dejan de exigir un vaciado síncrono individual; los límites principales y errores siguen siendo críticos. Los errores y eventos principales sobreviven al límite de marcas rutinarias y al cupo de paquetes. No se silencian excepciones.
- Las consultas rutinarias de memoria reutilizan una muestra hasta 250 ms e indican su antigüedad. Las etapas principales y los errores solicitan muestra fresca. No se fuerza GC ni se cambia el presupuesto de GameDB.

Las operaciones originales de `Resources.Load` y su política de referencias/caché permanecen iguales. No se adelantan cargas ni se retienen bancos nuevos. No se modifican controles, simulación, cámara, salud, audio, modelos, HUD, materiales ni shaders. Se conservan target 60/VSync 1, calidad original VeryLow, memoria modo 3 y reserva AOT de 4096 de las versiones anteriores.

## Medición de la siguiente prueba

Cada cinco segundos `PERF` registra cadencia de Update, frame más largo, tiempo acumulado/máximo del transporte, consultas de memoria, copias secundarias evitadas y tiempo real de `Resources.Load`. Las cargas lentas se registran de manera acotada. Cinco ventanas CPU cubren StateMachine.Update, ManagedUpdates.Update/FixedUpdate/LateUpdate y GameCamera.LateUpdate, sin modificar su orden ni sus operaciones originales.

Estos tiempos no son mediciones directas de GPU ni scanout. Los contadores acumulados pueden solaparse: no deben sumarse como costes independientes. Su objetivo es separar diagnóstico, carga real y ejecución normal antes de cambiar gráficos o precargas.

## Validación local

**VERIFIED:** compilación C# PSP2 sin errores. Editor es-ES completa el flujo original hacia Ingame, con una carga/callback/evento, jugador vivo al menos ocho segundos y cero errores del juego. GameDB conserva 109 tipos, 3407 filas y los 16847 campos numéricos comparados. El receptor local de prueba recibió 5497 paquetes consecutivos, sin fragmentos incompletos; los dos errores registrados son autopruebas intencionales del logger.

Pruebas dirigidas verifican la supresión de copia redundante, fallback al fallar su disponibilidad, errores después del cupo rutinario, clasificación de eventos críticos y consultas de memoria limitadas. La primera ejecución falló por el modo de apertura del lector del fixture frente al escritor compartido: se corrigió únicamente el lector de prueba a FileShare.ReadWrite. Se conservó ese fallo. Las dos ejecuciones posteriores pasaron; la última incluye las cinco ventanas CPU. No se afirma validación visual mediante capturas: ScreenCapture no emitió archivo en batch.

Las comprobaciones finales privadas incluyen IL de datos/guardado/gameplay, equivalencia de las operaciones originales en los métodos medidos, identidad de recursos serializados/bancos, ejecutable normal y símbolos de esta compilación. Los resultados y hashes exactos quedan en `PSP2_VPK26/FinalLocalDelivery.json`. No se repitieron conversiones de recursos.

**VERIFIED, entrega:** una compilación nativa, 0 errores, 492 advertencias, 3:19,836. Pasaron 58 contratos generales y 116 del diagnóstico; 27 tipos conservan todo su IL y campos respecto a VPK 25. En otros tres tipos solo se añadieron cinco ventanas de tiempo, conservando campos, IL de los métodos restantes, llamadas originales y equivalencia de las operaciones fuente. Los 49 archivos serializados y los 15 bancos son idénticos. Se preservaron el SELF normal y la tabla AOT de 4096. Solo cambiaron once archivos existentes, incluidos los dos campos de versión del archivo de ajustes; cero archivos nuevos en el proyecto. Rollback protegido a VPK 25 probado en seco, sin operaciones sobre partidas.

Paquete: 179919886 bytes, 288 entradas, CRC y hashes verificados. SHA-256: `0c637ec7158fb7c18de359c8b43b8cf856b2d0e64fc1b7efcc2a86d26dd9166f`. Se conservaron siete archivos de símbolos exactos y los símbolos/fuente del plugin nativo. El parser local acepta mensajes críticos por encima del cupo rutinario; prueba sintética en archivo, sin inyectar paquetes en el receptor real. El primer intento de esa prueba tenía una ruta relativa incorrecta al parser; se corrigió y pasó, sin cambio en runtime.

## Prueba física pendiente

Cerrar completamente VPK 25 antes de iniciar VPK 26, manteniendo la misma partida y el mismo nivel para comparar el primer arranque y la primera entrada. Probar movimiento, primera comida y turbo; después volver a entrar sin cerrar para comparar con caché caliente. Mantener el receptor UDP del PC abierto en el puerto 18194. La ventana superpuesta sigue desactivada.

Conservar `vita_live.log` del PC y los respaldos de `ux0:data/HSW_Vita/`, junto con cualquier `.psp2dmp`. El VPK exacto y sus dos archivos de símbolos se conservan en la entrega privada. **UNTESTED:** mejora de FPS, latencia y estabilidad prolongada de VPK 26 en Vita. No se promete alcanzar 60 FPS ni se declara resuelto el rendimiento solo por compilar.

## Seguimiento físico posterior, 10 de noviembre

**VERIFIED, checkpoint de una ejecución:** primera cámara del menú a 93,288 s desde el logger, frente a 226,060 s en la sesión anterior de VPK 25. Loading a SESSION_STARTED: 82,329 s frente a 396,578 s. Son ejecuciones distintas, sin control de caché del sistema ni benchmark repetido. El propietario confirma que las pausas al comer y usar turbo mejoraron claramente.

El proceso completó creación del jugador, sesión y regreso a Shop/SharkSelect. El guardado posterior verificó el respaldo de 1 MiB. El checkpoint de 8279 paquetes UDP consecutivos no tenía fragmentos incompletos, solicitud de salida ni fatal nativo. Esto acredita esos límites concretos, no estabilidad indefinida ni una prueba de carga fría de partida posterior.

**Pendiente:** gameplay sostenido de aproximadamente 14–16 Updates/s en las ventanas observadas, que no mide directamente GPU/scanout. En una ventana de 5034 ms sin nuevas cargas por ResourceLoaderManager, transporte consumió 150 ms; ManagedUpdates.Update completó 82 llamadas con 497,195 ms acumulados; las otras ventanas CPU tampoco cubren todo el frame. No se atribuye el tiempo restante exclusivamente a GPU. El bajo rendimiento persiste tras el cupo de marcas rutinarias: diagnóstico y primera carga no explican por sí solos todo el coste.

**Error nuevo observado, sin cierre:** siete registros del logger en dos ráfagas indican `AttackDuration > 30.0f`, con GlobalSpeedScale 1. Pueden incluir duplicados de callbacks; no equivalen a siete fallos independientes. El origen está en MachineShark.UpdateAttackStart, que obtiene duración de AnimControl.GetStateTime; las ramas coincidentes devuelven AnimatorStateInfo.length almacenado del estado actual/siguiente. El guard original registra error y restablece sus indicadores de ataque. La mención de audio en `after=` es contexto previo, no un stack trace ni evidencia de fallo de audio. No se suprime el error ni se altera la duración: faltan estado/capa/longitud/velocidades y parámetros de animación en la recurrencia. Su primera visibilidad en VPK 26 no demuestra que la optimización lo introdujera, porque anteriormente las cuotas podían ocultar errores tardíos.

Solo se añadieron herramientas locales de lectura y evidencias privadas durante esta observación. La compilación probada no cambió mientras estaba ejecutándose.

**Checkpoint posterior:** dos entradas al nivel completadas, ambas con Results y regreso al menú. La segunda carga dentro del mismo proceso tardó 56,698 s desde Loading hasta SESSION_STARTED. Se conservaron 10333 paquetes consecutivos, sin fragmentos incompletos ni fatal/salida registrados; el último estado de ese snapshot es FrontEnd. El aviso de ataque reapareció cerca del inicio de la segunda sesión (once registros acumulados, incluidos posibles duplicados). Se mantiene pendiente el rendimiento sostenido, aproximadamente 14–17 Updates/s en ventanas representativas. El receptor continúa capturando; este checkpoint no acredita vigilancia indefinida ni estabilidad prolongada.
