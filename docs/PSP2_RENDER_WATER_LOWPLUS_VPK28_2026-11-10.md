# VPK 28 — agua y perfil Vita Low+

Prueba privada autorizada por el propietario para **Hungry Shark World**, `HGSKW1178`. No cambia fases, rama, distribución pública ni proyecto original 2017. Unity **2018.2.19f1**, Mono2x, BuildOptions.None, memoria3/AOT4096 y frecuencias originales. APK SHA `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d` y OBB SHA `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72`: SHA/CRC verificados nuevamente.

## Cuello de botella y cambios

**VERIFIED local:** Hawaii_low creaba una `WaterFX camera` habilitada, máscara de todas las capas y RenderTexture256², aunque su material no admite `_ReflectionTex`. La cámara renderizaba sin que el agua utilizase el resultado. El A/B dentro del mismo frame produjo una imagen principal PNG idéntica al deshabilitarla. VPK28 evita crear esa cámara/RT cuando no hay soporte; conserva las reflexiones manuales cuando sí lo hay y libera los recursos propios. Elimina una cámara activa y393216bytes de RT en la prueba Editor.

Tres optimizaciones adicionales, específicas y reversibles:

- WaterSurface reutiliza entradas y arrays, calcula una vez el seno dependiente solo del tiempo y recorre normales contiguas. Mantiene simulación, iteraciones y resultado numérico.
- Omite las tres subidas de datos de la malla de agua cuando sus límites quedan fuera del frustum actual. La simulación continúa; se suben los datos vigentes al volver a entrar.
- RenderControl y ScrollingUVs reutilizan listas de materiales. Se evita reasignar identidades sin cambios; conserva tintes, fades, UV y cambios de shader necesarios.

**UNTESTED:** proporción CPU/GPU dominante en Vita. No se encontró un límite configurado a15FPS: cap60/VSync1 siguen intactos. El profiler disponible en Editor informa GPU emulada y contadores de GPU/draw calls/SetPass sin muestras válidas; cero muestras no significa coste cero. Los slots de materiales inventariados tampoco son draw calls. No se atribuyen los64,7ms completos a GPU, audio ni scripts.

## Calidad final

**Vita Low+**, con escenas, geometría, LOD, sombras, partículas y shaders originales de Low. `LOW_DETAIL_ON` permanece; no equivale a Medium. `masterTextureLimit=1`, frente a2 real deVPK27, permite un mip más nítido en148 de las300 texturas3D catalogadas.

Se modifican únicamente22 overrides PSP2:19 texturas3D sin mip quedan limitadas a512; tres atlas con mip tienen fuente lógica1024 y mip superior residente previsto512. El catálogo3D queda en512 efectivos salvo dos fondos frontend originales, conservados para no degradar la interfaz. HUD y fuentes no se redimensionan. PNG, meshes, shaders, escenas y prefabs fuente permanecen intactos; no hay preparación manual nueva de APK/OBB.

Estimación del catálogo comprimido:22.866.160→18.979.824bytes; **no es memoria física medida**. La reducción de texturas grandes compensa los mips más nítidos. Salida y render principal siguen en **960×544**. No se implementan90/85%, cámaras de escalado ni Blit: no se dispone de una validación PSP2 que justifique su coste y seguridad. La comparación visual controlada disponible valida eliminar la cámara inútil; superioridad visual global de Low+ y comparación con Medium requieren consola.

## Validación y límites

**VERIFIED:** una compilación nativa,0errores/501warnings,2:58,95. Pasan61 contratos generales y54 de rendimiento. Editor esES:109tipos/3407filas/16847campos numéricos; flujo original de Hawái, jugador vivo12+s y0errores de juego. Guardado, backup, escritura parcial y recuperación pasan, con cinco errores deliberados separados.

Kernel de agua: arrays exactos tras300pasos/15rejillas, incluida223×16 con dos iteraciones. Mediana de64pasos:95,44→85,54ms en Editor, aproximadamente10% menos para **ese kernel**, no FPS Vita. Pruebas de materiales y reentrada visible pasan.

34archivos existentes modificados,0añadidos al proyecto; settings solo cambian dos versiones. Las23escenas binarias y15tipos centrales IL coinciden con27. Las63mallas con diferencias de serialización conservan todos sus campos decodificados/comprimidos;195palabras de metadatos cocinados cambian exactamente+8192. Payloads no afectados, audio/Fabric y SELF original preservados. No se cambia IA, física, spawning, controles ni formato/rutas de saves.

Fallos conservados en evidencia privada: error inicial de preprocesador, ubicación del componente de prueba, getter de materiales incorrecto y reserialización amplia de importadores; corregidos antes del build final. La comparación binaria inicial rechazó diferencias; validaciones independientes delimitaron versiones, GUID, offsets y metadatos. No se rebautizan esos intentos como PASS.

**UNTESTED físico28:** FPS, memoria real, colisiones, audio, persistencia fría y estabilidad prolongada. `AttackDuration >30` continúa sin modificación. VPK27 midió15,45finalesCPU/s y64,71ms medios; VPK28 aún no tiene una muestra equivalente.

## Artefacto y siguiente prueba

Privado: `local-work/HSW_Recovery/Reports/PSP2_VPK28/HSW_Vita_Test_00.28_HGSKW1178.vpk`,170257864bytes/288entradas. SHA-256 **`5e98c75865dd4e4e22bb9f1b9f53a4a01c6793c48ddaae24c5d3aec5f57f254b`**. CRC, hashes de miembros y símbolos exactos verificados; VPK26/27 preservados. `restore_vpk27.py` pasa en seco, protege contra sobrescribir cambios posteriores y no toca saves. Diffs, snapshots, contratos y resultados: directorio privado `PSP2_VPK28/`.

Comparar mismo tiburón/Hawái/recorrido sin overclock, entrada fría y segunda entrada por separado; al menos100s estables. Registrar FPS reales si están disponibles; `endFrameHz` mide finalizaciónCPU y `updateHz` llamadasUpdate, ninguno acredita scanout. Comparar frame medio/p50/p95/máximo y frames>33/50/100ms, pausas, Loading→SESSION_STARTED, pools/Spawner y guardado. Medir managed y LPDDR/CDRAM/PHYSCONT antes/después de partida y selector. Revisar nitidez, agua, enemigos, HUD, comida/turbo, colisiones, audio y save tras reinicio. CPU5 mide WaterSurface.LateUpdate y CPU6 su espera física anidada: no sumar. Transporte agregado cada5s y diagnóstico detallado desactivado.

## Primer checkpoint físico — noche del 10 de noviembre

**VERIFIED al corte 2026-11-11 04:43:44 UTC:** el propietario inicia28; sesión física con94 paquetes consecutivos, cero incompletos y ningún error, fatal ni salida recibidos. HELLO confirma00.28; PERF confirma texLimit1, cap60/VSync1. Llegó a FrontEnd, Shop y ShopPurchasePopup; todavía no hay Loading/GameStateInit/SESSION_STARTED. Snapshot privado `Physical28_Input/20261111T044344Z/` y `Observe28_Checkpoint.txt`. No se modificó el player durante la prueba.

Dos ventanas estables del menú registran51,24–51,63finalesCPU/s,19,37–19,51ms medios y p95 de19ms, semejantes a27. En tienda hay ventanas de9,61–32,41/s; algunas incluyen2,2–3,0s de Resources.Load, pero también aparecen pausas sin nuevas cargas. Después del popup de compra se registra un frame de12,71s; ManagedUpdates.Update marca un máximo acumulado de11,06s. La coincidencia no identifica por sí sola qué operación interna lo causó.

El contador de transporte acumula4,98s y máximo1,79s por llamada; incluye backup/sync nativo más UDP, no mide exclusivamente red. En varias ventanas estables el incremento es0–25ms. No se mantiene la suposición de coste despreciable para todo este arranque. Memoria final del corte: managed23,44MiB, LPDDR libre98MiB y CDRAM libre75,29MiB; no demuestra fuga. **UNTESTED gameplay28:** sin muestra equivalente de rendimiento ni verificación física de agua/colisiones todavía. El receptor existente queda abierto, sin promesa de vigilancia indefinida.

## Gameplay físico — checkpoint posterior

**VERIFIED al corte 2026-11-11 04:48:06 UTC:** 281 paquetes consecutivos, cero incompletos, sin error/fatal/salida recibidos. Sesión iniciada a233499ms; Loading→SESSION_STARTED **66,195s**. GameStateInit47,156s, pools43,252s, Spawner3,792s: más lentos que27 (50,470/32,594/29,553/2,935s), sin control de caché, tiburón ni navegación. Snapshot privado `Physical28_Input/20261111T044806Z/GameplaySummary.json`.

VPK28 utiliza **Porbeagle**; VPK27 había utilizado **BlackTip**. Se excluyen diez segundos tras inicio/reanudación, ventanas que cruzan cambios de estado y el popup de opciones. El primer tramo tiene85,390s a17,402finalesCPU/s y57,456ms medios. Agregando el segundo tramo válido:22ventanas/110,547s,1974finalesCPU, **17,857/s y55,998ms**; rango13,794–20,773/s, p95 por ventana56–91ms, máximo142,317ms y10frames>100ms. Últimas seis ventanas:19,142/s y52,212ms. La muestra27 fue15,454/s y64,705ms, pero **no es un A/B equivalente ni prueba de ganancia atribuible al build**, y tampoco scanout. No se alcanzan30FPS sostenidos.

Durante las ventanas válidas hay cero cargas y transporte0ms a resolución entera. CPU por llamada: ManagedUpdates.Update7,936ms; WaterSurface.LateUpdate1,766ms, con espera física anidada0,202ms donde se ejecutó. Son scopes parciales/solapados; el resto del frame no identifica automáticamente GPU. El agua optimizada no explica por sí sola los56ms. Memoria entre primer y último punto válido: managed33,25→37,06MiB, LPDDR libre47→42MiB; CDRAM libre77,24MiB constante. Requiere observar retorno y partidas sucesivas antes de inferir fuga. **UNTESTED:** comparación visual del propietario, FPS presentados, persistencia fría y estabilidad prolongada. No se modifica el runtime mientras continúa la observación solicitada.

**Actualización 04:49:31 UTC:** el propietario confirma que Low+ se ve correcto y más nítido en consola. Es validación visual reportada por el propietario, no captura A/B controlada. La primera partida llega a Results sin errores/fatal/salida registrados,349paquetes consecutivos/0incompletos. Tramos válidos totales155,784s: **17,479finalesCPU/s,57,209ms medios, máximo337,119ms**. Cero cargas/transporte0ms en las ventanas válidas; no alcanza la meta de30. Evidencia inmutable en `Physical28_Input/20261111T044931Z/GameplaySummary.json`, copia `FirstGameplayPhysical28Summary.json`. Continúa la observación del regreso y posible segunda partida, sin modificar el juego.

## Segunda partida física: BlackTip

**VERIFIED al corte 2026-11-11 04:54:36 UTC:** segunda partida y Results, 561 paquetes consecutivos, cero incompletos, sin error/fatal/salida recibidos. Tiburón BlackTip, como la muestra27, pero con mejoras, recorrido e historial de caché distintos. Evidencia privada `Physical28_Input/20261111T045436Z/GameplaySummary.json` y `SecondGameplayPhysical28Summary.json`.

| Muestra física | Tiburón | Segundos válidos | Finales CPU/s | Frame medio | Máximo |
| --- | --- | ---: | ---: | ---: | ---: |
| VPK27 | BlackTip | 100,75 | 15,45 | 64,71 ms | 169,13 ms |
| VPK28, partida1 | Porbeagle | 155,78 | 17,48 | 57,21 ms | 337,12 ms |
| VPK28, partida2 | BlackTip | 100,49 | 18,56 | 53,88 ms | 172,88 ms |

La segunda muestra registra1865finales CPU en20ventanas; rango14,15–23,23/s, p95 por ventana49–116ms y12frames>100ms. Últimos30,17s:20,92/s y47,80ms. **La media es mejor que la muestra27; no acredita una mejora causal del build ni estabilidad a30FPS.** Los picos persisten y no se confunde finalizaciónCPU con FPS presentados.

Cero cargas y transporte0ms durante las20ventanas válidas. ManagedUpdates.Update7,217ms/llamada, agua1,113ms, espera física anidada0,138ms donde se ejecutó: no bastan para atribuir el resto aGPU. LPDDR libre recupera19→27MiB tras inicializar y se mantiene27MiB en toda la muestra válida; managed35,88→37,63MiB, CDRAM libre76,87MiB constante. El descenso de memoria libre entre partidas requiere seguimiento; no prueba por sí solo fuga.

La segunda entrada no mejora la carga: Loading→SESSION_STARTED67,152s, GameStateInit49,464s, pools44,598s y Spawner4,755s. El perfil más nítido, selección de tiburón, navegación y memoria son factores no aislados. No se afirma que la carga en caliente se haya optimizado. El juego continúa sin modificaciones mientras se observa el retorno.
