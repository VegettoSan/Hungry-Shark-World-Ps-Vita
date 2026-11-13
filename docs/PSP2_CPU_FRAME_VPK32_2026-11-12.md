# VPK 32 privada: CPU, continuidad y corrección del panel

Trabajo correctivo autorizado por el propietario, sin cambiar P00 ni sus gates. Se parte del checkpoint 31; VPK 29–31 y sus evidencias se conservan. Unity 2018.2.19f1, Mono, PSP2, Low+, 960×544, memoria y AOT actuales permanecen. No requiere overclock.

## Evidencia y decisiones

El propietario informa un núcleo cercano al 97–99 %. Es una observación del monitor, sin captura de frecuencias ni atribución a un hilo concreto. Los anteriores 7–10 ms de ManagedUpdates frente a frames de 44–70 ms no cubren todo el motor. Apagar cinco efectos no produjo una mejora consistente en los recorridos exploratorios; las frecuencias y rutas mezcladas impiden concluir que todo el renderizado sea barato.

La cámara MenuToIngame observada al comenzar la sesión desaparece antes del punto estable de gameplay usado por el A/B. El fixture de cámara terminó **FAIL: No MenuToIngame camera to audit**. Se conserva el fallo y se descarta modificar cámaras por esa hipótesis. SkinnedMeshRendererBatched no tiene referencias en las escenas/prefabs examinados. No se modifican las cámaras de plataforma ni los sistemas de IA, detección, población o físicas nativas.

El cambio dinámico de mipmaps de 31 queda retirado también de las rutas de restauración y destrucción. La fila es fija y el mando la omite. Los otros cinco efectos conservan sus controles y los efectos originales siguen activos por defecto. El congelamiento físico de 31 continúa registrado como **FAIL**; corregir la fuente no acredita todavía estabilidad física de 32.

## Agua: eliminación específica de trabajo redundante

Se reutilizan los planos actuales de cámara y se aplica, antes de recortar el horizonte, el mismo rechazo por visibilidad que ya impedía subir la malla desde 28. No cambia el kernel físico, el trabajador, su sincronización, las ondas ni las cantidades de geometría visible.

El primer candidato añadía un atajo para transformaciones de traslación pura. Aunque produjo datos idénticos, no mejoró el caso visible: 4,0933→4,1916 ms por 1.000 llamadas en Editor. **REJECTED ese atajo**, evidencia y fuente conservadas.

La versión final pasó 320 movimientos/transiciones de visibilidad, incluyendo rotación y escala: arrays físicos, iluminación, vértices, normales, tangentes y bounds de las mallas subidas idénticos a 31. Mediana de siete tandas de 1.000 LateUpdate en Editor: oculto 2,8964→1,4699 ms; visible con física inactiva 3,8952→3,8157 ms. El segundo cambio es pequeño y no demuestra ganancia significativa. El ahorro oculto es aproximadamente 1,43 microsegundos por llamada en ese equipo; **no es una mejora de FPS medida en Vita ni una solución al cuello dominante**.

## Hilos y medición del frame restante

La configuración ya solicita m_MTRendering=1. Eso no demuestra que PSP2 lo esté usando: se registra SystemInfo.graphicsMultiThreaded en ejecución. graphicsJobs y GPU skinning se conservan. La API C# Job System está presente en los ensamblados locales, pero esa presencia no prueba funcionamiento ni beneficio en este player PSP2/Mono. No se introduce Burst ni se activan jobs de forma especulativa.

System.Threading ya se usa mediante un trabajador persistente del agua y eventos. No se crea otro pool de hilos: las rutas de IA, GameObjects, cámaras y físicas revisadas dependen del hilo principal; el cálculo independiente del agua ya está separado. No hay evidencia que justifique alterar afinidades, prioridades o sincronización para repartir porcentajes de CPU.

Se amplían los diagnósticos de cinco segundos con tiempo acumulado de ejecución del hilo llamador obtenido mediante sceKernelGetThreadInfo, identificación/afinidad del hilo, GC, timeScale, pausa, foco y frames pausados. Dos timestamps por render de cámara miden pared entre pre-cull y post-render. Estos intervalos pueden incluir esperas del controlador y solaparse; no son tiempo GPU ni deben sumarse con los scopes administrados.

Se consultan únicamente Recorder nativos válidos, sin activar globalmente el profiler ni usar Development Build. En el player normal pueden no estar disponibles: se registra explícitamente la lista válida, nunca se interpreta ausencia como coste cero. La documentación local del módulo PSP2 reserva la conexión de Unity Profiler a Development Build; no se cambia el player funcional para forzarla.

## Validación local y límites

Compilación C# Editor y PSP2 sin errores. Recorrido aislado FrontEnd/Shop/popup/globo/Hawái, movimiento y turbo inyectados, grafo de ingesta/colisiones activo, pausa/reanudación/retorno y guardados/recuperación: **PASS**, cero errores nuevos del juego; cinco fallos deliberados de guardado separados. Cinco efectos, input, fila fija, partículas nuevas y restauración: **PASS**; imagen de cámara antes/restaurada idéntica en 27.648 bytes.

Once archivos existentes modificados, cero añadidos al proyecto canónico, otros 20.907 exactos a 31. Escenas, PNG, shaders y 150 caps de texturas de 31 intactos. Se restauraron dos entradas StreamingAssets ausentes en la caché por el aislamiento de pruebas, desde los originales canónicos; el verificador inicial fallido se conserva. Los fixtures se retiran del player y se mantiene el Fabric derivado por el importador ya verificado en 31.

Archivos runtime afectados: `WaterSurface.cs`, `HSWPSP2RenderProbe.cs`, `HSWPSP2RenderProbeGUI.cs`, `HSWPSP2BootDiagnostics.cs` y `HSWPSP2LiveLog.cs`. El plugin privado `HSWLiveTrace.cpp` amplía el poll de diagnóstico; se regeneran su suprx y stub. Los demás cambios corresponden a versiones en `HSWPSP2StartupProbe.cs`, `HSWPSP2StaticBatching.cs`, `ProjectSettings.asset` y versión/preflight de `HSWFirstVitaBuild.cs`. Manifiesto y diff exactos permanecen en el informe privado32.

Una sola compilación nativa solicitada en el Editor abierto. **Al escribir este checkpoint, paquete/auditoría nativa pendientes.** No se acreditan mejores FPS, pausas de menú, carga, memoria física, audio audible, guardado frío o estabilidad prolongada. Pools e instanciación siguen siendo el coste de carga conocido, sin una sustitución equivalente demostrada; no se difieren dependencias para aparentar una carga menor.


## Entrega privada verificada — 2026-11-13 03:17 UTC

El primer build compiló, pero la auditoría **FAIL** detectó cuatro objetos UIDrawCall y componentes generados por NGUI en la escena abierta del Editor. No se empaquetó. Un reintento encolado antes de verificar la recarga se canceló; se conserva como **Cancelled**, no como PASS. Se corrigió el preflight para abrir una escena vacía y se comprobó su IL compilado antes de volver a encolar. Unity quedó abierto; no fue necesario cerrarlo. Se preservan los logs, la escena nativa fallida, checkpoints y símbolos.

Build final: **Succeeded, 0 errores, 502 advertencias, 3:19,878**. Auditoría de 5.862 tipos/44.109 métodos: solo cambios permitidos; IA, físicas, spawning y guardados preservados. 61 contratos de arranque/guardado, 49 archivos serializados, **23 escenas byte-exactas a 31**, 63 mallas decodificadas/comprimidas exactas, 505 renderizadores agrupados y AOT4096. SELF, Mono/Fabric, otros módulos y todos los bancos de audio/texturas exactos a 31.

Los tres shaders recompilados difieren en el orden de índices dentro del mismo conjunto de keywords y en su compresión. Comprobación independiente tras LZ4: **78 programas GPU byte-exactos por plataforma e índice**, mismas keywords, passes, parámetros y render state. El mapa de recursos conserva 47.266 entradas y 66.908 dependencias; solo reordena entradas del mapa exterior, manteniendo las listas de cada recurso. El comparador inicial de arranque rechazó una permutación de dos callbacks en la misma fase. Prueba Cecil específica: FrameLimit solo asigna VSync1/cap60; Begin y su callback de escena ya aplican esas mismas asignaciones antes de observar el estado. Se acepta únicamente esa permutación idempotente, con todos los demás callbacks/fases intactos; no se ordenan tablas arbitrariamente para hacer pasar la prueba.

**Una sola VPK empaquetada:** `local-work/HSW_Recovery/Reports/PSP2_VPK32/HSW_Vita_Test_00.32_HGSKW1178.vpk`, **164.195.898 bytes, 288 entradas**, SHA-256 `56ffe8f21aa2e88a90fd39d994a663ef1bb34edae027aa02f56ffb55661cc238`. CRC y hash por miembro, símbolos exactos, checkpoints y rollback protegido en seco: PASS. VPK30/31 intactas. El rollback de fuentes a31 se conserva para análisis; su control dinámico de mipmaps sigue siendo un fallo conocido. P00 ACTIVE, 0/13; sin publicación, gates ni Evolution modificados.

Observador32 preparado con tres casos sintéticos: distingue CPU ejecutada de tiempo de pared, excluye ventanas que contienen pausa aunque ya se haya reanudado y rechaza deltas negativos tras reset/wrap de contador. Receptor UDP local preparado, sin paquetes físicos32 todavía. La ausencia de un Recorder en release se trata como no disponible, no como coste cero.

**Prueba física pendiente:** instalar32 y usar BlackTip/Hawái con todos los efectos originales activos durante al menos120s, indicando SinOC o MAX y sin cambiar reloj dentro de la muestra. Después probar pausa, retorno, segunda carga, comida, turbo, IA, colisiones, audio y guardado/recuperación. No cambiar varios efectos durante la muestra base. El panel conserva cinco efectos y la fila de texturas fija. **No se ha demostrado mejora de FPS32, reducción de pausas/cargas ni resolución del cuello dominante.** El ahorro local del agua es pequeño; la medición nativa nueva busca aislar el tiempo restante del frame antes de otro cambio.


## Checkpoint físico32 — tres partidas, 2026-11-13 UTC

El propietario confirmó primero sinOC y luego informó CPU500MHz y aumento deFPS. Se separan épocas con un margen conservador alrededor del cambio; GPU/bus no medidos. La etiqueta manual permaneció inicialmente en1 pese al cambio y luego pasó a2: no se usa como frecuencia medida ni se reasigna toda la captura aMAX.

Renderizado multihilo confirmado por SystemInfo.graphicsMultiThreaded=True. Profiler.supported=False y cero Recorder válidos en release: ausentes, no coste cero. El contador de ejecución del hilo principal funciona. Tramo sinOC/efectos originales80,688s:12,431finalesCPU/s,80,433ms/frame,76,459ms de ejecuciónOS/frame,95,04% del intervalo;ManagedUpdates.Update10,471ms/frame. TramosCPU500 con efectos originales rondan18finalesCPU/s,main≈95%,ManagedUpdate≈7–8ms. Recorridos/caché no controlados: no atribuir mejora aVPK32 ni declarar causaGPU excluida. Cámara principal≈8–16ms de pared según tramo; puede incluir esperas y solaparse.

La primera partida incluye35,321s con cinco efectos apagados a12,089finalesCPU/s;sin mejora consistente demostrada frente a tramos distintos. Los tramos iniciales seleccionados no tienen GC ni nuevas cargas del gestor instrumentado. **Corrección de alcance:**ese contador no cubre Resources.Load directos;IntroCinematic y otros sistemas los usan. Un avisoAttackDuration>30 conocido, sin nueva excepción/salida recibida al checkpoint. Arranque, tresSESSION_STARTED y retornos a menús observados;no certifican audio audible,guardado frío o estabilidad indefinida.

Propietario observa≈25FPS en zonas sin presas y bajadas/apariciones tardías con muchos peces. **OWNER-REPORTED**,sin contador simultáneo de población visible. Se localiza el camino de instancia libre frente a expansión diferida y activación en corutinas;no se prueba todavía su coste por aparición. Mantener cantidades,prioridades,IA y física. MultiScreenState admite varias escenas aditivas en un paso;WorldSelector/LevelSelect ya usan async desde30 y otras rutas siguen síncronas. No se acredita carga duplicada;faltan tiempos por escena y activación. LoadTimeProfiler.LevelLoaded está vacío.

El tirón al caer al agua es intermitente según propietario;en la tercera partida conOC respondió «Esta vez no ocurrió». Se conservaron los marcadores de carga: pools40,124s,Spawner4,307s,GSI44,536s antes de crear jugador. WaterHit dispara evento,splash,audio y estado de animación;no hay marcador físico específico suficiente para asignarle un frame largo concreto. No aplicar un parche especulativo al agua por esa correlación.

Se corrigió un error **del observador**:al cargar una partida posterior podía asociar el SESSION_STARTED anterior y producir una falsa ventana de2,596Hz durante carga. Resumen derivado erróneo y código conservados;se excluye cuando hay salida intermedia aLoading/Shop u otro estado fuera deIngame/OptionsPopupIngame. Paquetes crudos intactos. El propietario anuncia terminar voluntariamente;no interpretar silencio posterior como congelamiento. No hubo cambios del player ni compilaciones durante esta prueba.
