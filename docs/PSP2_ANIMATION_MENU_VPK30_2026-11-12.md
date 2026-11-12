# VPK 30 — animación y transiciones de menú

Optimización correctiva **privada**, autorizada expresamente por el propietario sobre VPK29. P00 ACTIVE, 0/13 aprobaciones; fases, rama y distribución pública intactas. Se mantienen Unity2018.2.19f1, Mono2x, BuildOptions.None, ExpandBy109MB, AOT4096, Low+,960×544, cap60/VSync1 y frecuencias originales. Sin dependencias nuevas ni cambios en Evolution. Los originales APK/OBB vuelven a pasar SHA/CRC; hashes canónicos sin cambios.

**OWNER-REPORTED29:** gameplay funcional sin cierres aparentes,15–20FPS habituales y picos aproximados25; Low+ correcto; pausas de menús y cargas largas. No se recibió una captura29 comparable de GPU/frametimes. Esta actualización conserva la historia previa, que marcaba29 como pendiente al entregarla.

## Evidencia y alcance

Se revisaron AGENTS, gates, experimentos26–29, herramientas locales, código privado, registros físicos27/28 y checkpoints. Se conservan las optimizaciones anteriores de diagnóstico, pools, agua y los505renderers agrupados. No se amplía el batching.

En Editor, el perfil temporal de referencia mide **9.048,54ms dentro de277instanciaciones base** de los pools. El scope enemigo180llamadas/9.085,14ms contiene esas instanciaciones: **no se suman**. RenderControl.Awake191llamadas/73,36ms y tres CacheComponents/6,12ms no explican ese coste. Es evidencia local de que eliminar búsquedas pequeñas no soluciona la construcción nativa; no es una medición exclusiva del disco, GPU o Vita.

Durante el gameplay, el perfil confirma escrituras repetidas de parámetros de animación dentro de la ruta de actualización de máquinas. Las muestras por tipo se afectan por instrumentación y cambios de población; no se presentan como benchmark A/B de FPS. El cuello dominante del frame físico continúa **sin aislar**. Los registros anteriores sin cargas nuevas tampoco permiten atribuir todo a texturas, CPU o GPU; no hay contadores nuevos válidos de draw calls/SetPass/GPU.

La ruta comprobada es **FrontEnd/Jugar→Shop→LevelSelect**, cuya variante carga **WorldSelector+LevelSelect** mediante ScreenTracker/MultiScreenState. No existe una clase WorldSelect en esta ruta; GlobeAppear es un identificador de audio. LoadingCurtain espera los eventos originales de carga. ShopState.OnStateLoaded ejecutaba una limpieza global y GC incluso al reanudar tras un popup. Esto identifica trabajo redundante; **no demuestra que explique íntegramente el frame físico de12,71s** registrado en28.

## Cambios implementados

1. **AnimControl.cs y AnimControlFish.cs:** omiten escrituras nativas del mismo valor para seis booleanos del controlador de peces y la velocidad global. Dos máscaras fijas guardan validez/valores; no crean diccionarios ni retienen recursos. Se invalidan al reactivar el componente, incluido el ciclo del pool. Los getters nativos permanecen; floats de curvas, evaluación de estados, eventos, root motion, capas, animaciones y frecuencia de actualización se conservan.
2. **ShopState.cs:** al regresar de PopupState evita la limpieza global redundante. Conserva GC automático y limpiezas originales en entradas reales, cambios de estado y regreso desde gameplay. No agrega una caché de modelos ni precarga recursos.
3. **ScreenTracker.cs:** únicamente WorldSelector y LevelSelect locales usan LoadSceneAsync y esperan su operación antes del tracker/eventos originales. Las rutas ya cargadas siguen inmediatas. No se retrasan resultados de pools/GameStateInit/Spawner ni se modifica LoadingCurtain. No hay precarga masiva ni una animación añadida para esconder una pausa. La activación/Awake de Unity todavía puede bloquear un frame.

Doce archivos existentes cambian: cuatro anteriores; tres identificadores gestionados de versión; plugin/stub de diagnóstico identificados30; dos scripts de Editor con rutas/versiones de informes; y dos campos de versión de ProjectSettings. **Cero archivos nuevos en el proyecto canónico;20.902 intactos.** Todo recurso fuente conserva sus bytes29. La instrumentación temporal y las fixtures quedan fuera del player.

## Resultados y validación

Microbenchmark de Editor: mediana de siete repeticiones,200.000escrituras del mismo valor:

| Operación aislada | Original | VPK30 |
| --- | ---: | ---: |
| Booleano de Animator | 6,9236ms | 2,9198ms |
| Velocidad de Animator | 2,8838ms | 1,6779ms |

Estos números miden esos bucles; **no demuestran una mejora de FPS en Vita**. Un intento de compartir frameCount en UI mostró100,29ms/84.131llamadas frente a100,90ms/84.134; se descartó y restauró exactamente29. La primera caché de booleanos con diccionario también se sustituyó antes del build por máscaras fijas más baratas.

**VERIFIED local:**

- FrontEnd→Shop→popup→Shop→globo→Hawái. Un callback por WorldSelector/LevelSelect; reanudación del popup sin repetir limpieza global.
- Controlador original:1.200pasos,3booleanos presentes,3.600escrituras solicitadas y cuatro ciclos de desactivación/reactivación; valores, estados y tiempos normalizados equivalentes. No se reduce la IA.
- Gameplay vivo, movimiento y turbo por entrada inyectada; pausa/reanudación y transición original IngameToMenu→Shop. Cero errores del juego durante la prueba. Eater y grafo físico activos; esto **no certifica una ingestión/contactos exhaustivos**.
- GameDB109tipos/3.407filas/16.847campos numéricos bajo es-ES; guardado, backup, escritura parcial, corrupción y recuperación. Cinco mensajes deliberados de fallo se clasifican aparte, sin silenciar errores del juego.
- Compilación C# PSP2 de118+3.745fuentes:0errores. **Una compilación nativa**,0errores/501advertencias,3:00,390.61contratos de arranque/guardado.
- Comparación de5.612tipos previos/42.552métodos: cambios limitados a once métodos existentes y tres nuevos de los cuatro tipos optimizados, más el iterador esperado. Campos originales y todo IL restante preservados tras normalizar textos de versión/números de iterador.
-49archivos serializados comprobados. Las23escenas son byte-exactas29;15bancos de recursos/audio idénticos.63mallas conservan geometría decodificada y datos comprimidos/índices/skin/bindposes.195palabras internas de cocinado se trasladan en las mismas posiciones documentadas27→28, con delta uniforme1.654.784; no se enmascaran otras diferencias. Tablas de arranque resueltas conservan callbacks, orden y fases pese a reordenar índices. Solo cambian versión y GUID de construcción donde corresponde.
-505renderers agrupados,16.041vértices/73.842índices y641.640bytes de vértices permanecen. SELF normal, Mono, otros DLL y módulos de plataforma coinciden con29. AOT4096 y símbolos exactos archivados.
-CRC y hashes por miembro del VPK verificados. VPK26/27/28/29 mantienen sus SHA. Rollback30→29 protegido por hashes pasa en seco y no contiene rutas de partidas.

Fallos de herramientas/fixtures conservados: suposición inicial de salto directo FrontEnd→LevelSelect; declaración duplicada y namespace de eventos ausente en la fixture; nombres de campos con distinta capitalización y aridad genérica omitida por el primer comparador IL; comparación inicial demasiado restrictiva de metadatos cocinados. Se corrigieron los verificadores con evidencia independiente, sin modificar el juego ni recompilar el player. Siete metas derivados que Unity reserializó se archivaron y restauraron en caché; los originales canónicos y los DLL del player permanecen exactos.

**Límites:** no se ha demostrado todavía mejora de FPS ni del tiempo total de carga en Vita. La construcción nativa de pools sigue completa, síncrona y sin cambios. Rendimiento físico, pausa máxima del selector, memoria libre real, comida/contactos, audio audible, calidad visual, guardado frío y estabilidad prolongada30 requieren consola. El retorno probado en Editor no acredita ausencia de fuga en sesiones físicas sucesivas. La caché nueva es fija y pequeña; omitir limpiezas de popups exige observar memoria durante navegación prolongada.

## Entrega y prueba física

Privado: `local-work/HSW_Recovery/Reports/PSP2_VPK30/HSW_Vita_Test_00.30_HGSKW1178.vpk`, **170.865.080bytes/288entradas**. SHA-256 **`2121c49003418e1b25785b0bc8e5c6f3547e7bb74205b016b3f142caee587cf4`**. Checkpoints, diffs privados, rollback, comandos exactos y evidencias en `PSP2_VPK30/`; ninguna publicación ni instalación automática.

Instalar como actualización de HGSKW1178 conservando partidas. Comparar con29 sin overclock, BlackTip/Hawái/mismo recorrido. Separar arranque frío y segunda entrada. Cronometrar Shop/popup/Jugar→globo y Loading→SESSION_STARTED; jugar al menos100s por recorrido denso/despejado. Revisar comida, turbo, enemigos, contactos, audio, HUD, pausa, vuelta y progreso tras cerrar/reabrir. Registrar LPDDR/CDRAM/PHYSCONT y managed antes/después de cada sesión y durante navegación de popups.

El receptor existente usa UDP18194; parser y observador locales aceptanHSW30. Comparar FPS presentados cuando estén disponibles, frame medio/p95/máximo y frames>33/50/100ms. endFrameHz mide finalizaciónCPU, **no scanout**. No sumar scopes solapados.25FPS y30FPS sostenidos siguen siendo metas, no resultados.

## Primer checkpoint físico30 — observación en curso

**VERIFIED al corte2026-11-12 03:07:49 UTC:**142paquetes consecutivos/0perdidos/0incompletos, protocolo30 y Low+texLimit1 confirmados después de inicializar. Llegó a FrontEnd, Shop, SharkSelect y LevelSelect, incluido regreso al selector; todavía sin SESSION_STARTED. Sin excepciones ni salida nativa recibidas al corte. Snapshots privados `Physical30_Input/20261112T030644Z/` y `Physical30_Input/20261112T030749Z/`.

Persisten pausas físicas:7,720s y3,412s tras la primera entrada observada enLevelSelect, y5,551s en otra entrada. En esas ventanas ResourceLoaderManager no registra nuevas cargas; no excluye deserialización/activación nativa ni otras rutas fuera del contador. La ventana de3,412s contiene3,287s acumulados enStateMachine.Update; la de7,720s no queda explicada por los scopesCPU parciales. No se asigna una causa exclusiva. La última ventana posterior muestra27,90finalesCPU/s y35,96ms medios:es menú, no gameplay ni scanout.

LPDDR libre al último estado≈57MiB y managed≈45MiB, después de navegar varios estados; no prueba fuga. La muestra aún no permite afirmar mejora de menús ni rendimiento sostenido. El player y el proyecto permanecen intactos mientras el propietario prueba.

## Aclaración del propietario sobre frecuencias

El propietario aclara durante esta sesión que **todas sus pruebas físicas anteriores se realizaron con overclock al máximo**, mientras que **la prueba actual30 se realiza sin overclock**. Es información **OWNER-REPORTED**; no se han capturado las frecuenciasCPU/GPU exactas. Las instrucciones previas de comparar sin overclock eran un protocolo propuesto, no evidencia de que las muestras anteriores cumplieran ese protocolo. No se reescriben sus resultados históricos.

No se deben agrupar muestras conMAX y sinOC como una comparación de builds a iguales frecuencias. La configuración del proyecto y la ausencia de overclock obligatorio del VPK son cuestiones distintas de los ajustes externos utilizados por el propietario. No se atribuyen diferencias deFPS/CPU/cargas al código sin controlar frecuencias, tiburón, recorrido, mejoras y caché. La optimización siguiente debe reducir coste y equilibrar detalle en condiciones sin overclock.

**Precisión posterior del propietario:** dentro de la misma sesión30, **la primera partida fue conMAX y la segunda sin overclock**. La primera muestra completa de135,646s/19,10finalesCPU/s corresponde por tanto aMAX. La mención inicial de «prueba actual sinOC» no debe extenderse retrospectivamente a la primera partida. Aún no hay frecuencias exactas ni recorridos/poblaciones equivalentes.


## Corte de gameplay físico30 — frecuencias separadas

Snapshots privados hasta2026-11-12 03:58:09UTC:1.044paquetes/0perdidos/0incompletos; último estado recibidoFrontEnd. Primera partida BlackTip/Hawái **MAX declarado**:135,646s válidos,19,10finalesCPU/s,52,36ms medios,máximo120,461ms. Segunda **sinOC declarado**:181,722s válidos,12,11finalesCPU/s,82,55ms medios,máximo261,417ms. Sin nuevas cargas ni tiempo de transporte informado durante esos tramos. No es una comparación causal de versiones ni una medida deGPU/scanout; rutas y frecuencias exactas sin controlar.

GameStateInit primera/segunda:42.038/58.408ms; pools38.322/52.402ms ySpawner3.604/5.891ms. Las pausas del selector persisten. Un mensaje deAttackDuration>30 ya conocido de26–28; sin nuevas excepciones/salida nativa recibidas. LPDDR al retornoShop≈47MiB y luegoFrontEnd≈43MiB, frente≈27MiB en gameplay; no demuestra fuga ni ausencia de ella.

Corrección del observador del host: la segunda sesión no tiene marcadorLoading de entrada inequívoco. Se eliminó la asociación errónea con unLoading anterior de retorno al menú; los snapshots originales permanecen y la métrica derivada132.862ms es inválida. No se utiliza para atribuir mejoras/regresiones. Tres casos sintéticos del selector de marcador se verificaron. Player30 y suVPK permanecen intactos.
