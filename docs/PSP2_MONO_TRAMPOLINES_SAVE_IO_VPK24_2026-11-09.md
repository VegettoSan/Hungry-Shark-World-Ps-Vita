# Reserva Mono y copias de guardado — VPK privado 24

## Causa demostrada en hardware 23

Sesión `d8599c27e0a9`, 5278 mensajes principales consecutivos, sin huecos. Los 5278 coinciden exactamente con el respaldo local de Vita. El nuevo canal nativo funciona; UDP y `vita_mono_native.log` contienen:

```text
Ran out of trampolines of type 0 in 'app0:/Media/Managed/mscorlib.dll' (1024)
```

Lo imprime el hilo principal nativo 1073808041 a us=252183414. El observador normal de salida de libc se ejecuta a us=252192443, 9029 microsegundos después. Último contexto principal: pool EnemyEntity, fila37, PF_Human_Policeman_Gun; BEFORE initialise. No implica que el prefab esté dañado. **VERIFIED:** el runtime agota una reserva finita de trampolines AOT y termina; no hay una excepción C# capturable en esa ruta. El contador LPDDR anterior es77594624 bytes, pero la prueba de causa es el fatal explícito, no una inferencia de RAM disponible. No se suministró un nuevo .psp2dmp en esta prueba.

VPK22 se detenía después de completar los pools;23 se detuvo dentro de ellos. Esto es compatible con consumo acumulado de una reserva compartida, y evita culpar al último recurso. El fatal está demostrado para23; no se atribuye retrospectivamente a todos los cierres16–22 sin sus mensajes o dumps.

## Reparación candidata de la reserva

El manual local del módulo PSP2 admite AOT Compilation Options. El IL de BuildMonoScript pasa PlayerSettings.aotOptions a CrossCompileAOTDirectoryParallel; el compilador instalado reconoce `ntrampolines=`. Se configura **`ntrampolines=4096`**, conservando Mono2x y BuildOptions.None. Se modifica la reserva específica que se agotó, sin cambiar otros presupuestos de trampolines, modo de memoria, motor o datos.

**VERIFIED binario:** la región specific_trampolines del módulo final pasa de1024 a4096 slots de28 bytes. Añade86016 bytes de código de esa tabla; no es una medida de toda la memoria de ejecución. mono-vita y SELF normal permanecen intactos. Se reconstruyen las assemblies AOT mediante la cadena original; no se parchean direcciones del runtime. La causa física está identificada, pero **UNTESTED hardware24:** reserva suficiente durante gameplay prolongado y múltiples niveles. El logger nativo sigue activo para detectar si aparece otro límite.

## Tiempo hasta el menú y cambio de IO

En23, primer envío CPU de cámara FrontEnd a116604ms desde inicialización del logger; no mide la parte anterior no instrumentada ni confirma el instante de scanout. Antes de esa marca:

| Operación | Cantidad | Tiempo observado |
| --- | --- | --- |
| SaveData hasta retorno de SaveFacade |12|67,143s|
| Copias verificadas cerradas |25|47,925s|
| Escritura de contenedor temporal |13|13,141s|
| InitSaveData de PlayerProgress |1|26,333s|

Estos intervalos incluyen padres e hijos; **no se suman**. Las escenas Sharks/3DBackground también contienen callbacks y trabajo anidado, de modo que sus intervalos no equivalen a IO puro de recursos. No se alteran GameDB32filas/2ms, órdenes de escenas ni esperas.

La partida original conserva un archivo reservado de1MiB, mayormente padding estable. La copia anterior reescribía todos sus bytes en cada commit/backup. Ahora, solo para la ruta del adaptador PSP2, se comparan bloques existentes de8KiB y se escriben los que difieren. Destino nuevo/corto: escritura completa; destino más largo: longitud final ajustada. Se abre primero el origen, se mantiene comprobación de longitud, se cierra/vacía destino y se compara después **cada byte del archivo completo**. Se conservan las solicitudes síncronas, retorno de errores, codec v3, partida anterior/backup, temporal validado y recuperación. No hay batching de guardados, pérdida de callbacks ni nueva promesa de atomicidad/fsync.

**VERIFIED local:** archivo de1MiB con un bloque modificado:8192 bytes escritos frente1048576, mismo hash final. Archivos nuevos, idénticos, tamaños0/1/8191/8192/8193/1MiB, colas largas/cortas, errores de rutas, overwritefalse, payload cifrado grande interrumpido, backup y recuperación pasan. Observadores/fallos inyectados existen solo enEditor y no aparecen en el IL del player. **UNTESTED:** reducción efectiva del tiempo Vita; se medirá en la próxima sesión, sin prometer un porcentaje de aceleración.

## Validación y alcance

result=Succeeded errors=0 warnings=492 bytes=270203274 duration=00:03:05.0721730. Único build nativo.58contratos generales,106diagnósticos,325marcadores;13tipos protegidos GameDB/savecodec/IA/spawner/transición con IL/campos exactos a23.49serializados y15bancos de recursos exactos,23escenas; auditorías históricas424HEVAG/480texturas/140shaders reutilizadas. Sin conversiones.60cap/VSync1,VeryLow,memoriaenum3,controles/audio/guardado/offline iguales a23.

**VERIFIED Editor:** guardado/casos de fallo y equivalencia; arranque aislado, GameDB109/3407, callbacks una vez, FrontEnd, carga original Hawaii/pools/SpawnPlayer/GameSessionStart, jugadores válidos más de8s,0errores del juego.5358UDPconsecutivos;un único error deliberado del autodiagnóstico de hilo. Fixture configura componente original de carga, no valida cada interacción UI. Primer intento con -nographics falló en GenericDynamicVBO/ParticleSystemRenderer nativo deEditor; evidencia conservada. Se repitió con la invocación batch con gráficos usada en23 y pasó; ningún workaround gráfico incorporado al player.

Ocho archivos existentes modificados,cero añadidos al proyecto; settings solo versiones23→24 y opción AOT. Fuente/cache coinciden,metadatos derivados restaurados con GUID,rollback23dry-run validado. VPK23/anteriores preservados;sin ramas/fases/publicación/Evolution/2017alterados.

## Entrega y comprobación física

`HSW_Vita_Test_00.24_HGSKW1178.vpk`: 179915111 bytes,SHA256 `bac9cf5a9f56b35eb91e5144d757241e30e32d12d6077dc39da4d20f8da27aa5`. CRC/hash/espejo y siete símbolos exactos más símbolos del plugin verificados. Mantener el paquete junto con `VPK24_ExactSymbols.zip`, `VPK24_NativePluginSymbols.zip` y manifiestos privados.

Instalar00.24,mantener receptorUDP18194 en192.168.1.8 y repetir el mismo nivel/partida, sin reiniciar progreso. Registrar arranque→menú y menú→control del jugador. Conservar logPC y respaldos vita_live.log,vita_live_watch.log,vita_mono_native.log,vita_native_exit.log de ux0:data/HSW_Vita;si hay nuevo dump, conservarlo con los símbolos24. No requiere botones nuevos.

**Estado: causa23 demostrada; corrección y optimización verificadas localmente; estabilidad y tiempos físicos24 pendientes.**


## Primer resultado físico de 24 — sesión activa

**VERIFIED:**sesión a05cafe54c6c supera poolfila37PolicemanGun,termina cuatro pools,grids/spawner,jugador/equipo/PlayerSpawned/InGameLoaded/cámaras. La marca GameStateInit call termina a236868ms y el proceso continúa enviando eventos después. No fatalMono,excepción gestionada ni salida normal registrados en el checkpoint;solo autopruebaMono. **Pendiente:**confirmación del dueño de control/visibilidad y estabilidad prolongada;no se declara gameplay completamente validado.

Primer envío CPU de cámaraFrontEnd:100511ms desde logger,frente116604ms en23 (16093msmenos). Mismas12ventanasSaveData:48,419s frente67,143s;25copias verificadas:24,643s frente47,925s. Intervalos anidados,no sumarlos. Sesiones distintas,medida observada,no benchmarkcontrolado ni promesa deaceleración. Snapshot privado con secuencias/hashes conservado.


## Resultado físico confirmado por el dueño

**FAIL jugabilidad24:**el gameplay abre pero modelos yHUD enormes,muerte inmediata,solo dentro del nivel. Se confirmó avance después del fatal anterior. Se reprodujo defecto de decimales dependientes de cultura en la DLL exacta24;[reparación25](PSP2_INVARIANT_GAMEDB_NUMBERS_VPK25_2026-11-10.md),sin cambios compensatorios de cámaras/salud/assets.
