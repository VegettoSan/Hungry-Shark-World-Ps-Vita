# VPK 29 — batching selectivo de Hawái

Prueba privada autorizada para **Hungry Shark World**, `HGSKW1178`. Se conserva Unity 2018.2.19f1, Mono, BuildOptions.None, memoria ExpandBy109MB, AOT4096 y frecuencias originales. P00 continúa activo; no se aprueban fases ni publicación. APK/OBB originales: SHA y CRC verificados nuevamente; no se modifican ni requieren procesamiento manual adicional.

## Evidencia que dirige el cambio

El propietario observa mayor fluidez con menos elementos visibles y confirma que Low+ se ve correcto y más nítido. VPK28 registró 17,48 finales CPU/s con Porbeagle y 18,56/s con BlackTip; este último tramo duró 100,49 s, con 53,88 ms medios y máximo de 172,88 ms. VPK27 había registrado 15,45/s, pero cambiaron recorrido, mejoras y caché: no es un A/B controlado ni FPS presentados.

**VERIFIED:** Hawaii_low contiene 4.687 MeshRenderers y no tenía grupos estáticos. La configuración PSP2 consultada devolvía static=0/dynamic=0. Es trabajo de envío potencialmente evitable; su coste exclusivo y la proporción CPU/GPU dominante siguen sin medirse.

## Implementación

Un pase específico de construcción PSP2 hornea **505 renderers inmóviles** de Hawaii_low en un buffer compartido, con 16.041 vértices y 73.842 índices. Una malla compartida no significa una sola draw call medida. La selección es determinista por coste y ruta con índices de hermanos; excluye shaders ajenos a la lista de lightmap, transformaciones no uniformes o reflejadas, Rigidbody, Animator, Animation y comportamientos desconocidos en su jerarquía.

El presupuesto estimado es 2 MiB, reservando dos copias de datos y margen por renderer. La malla combinada mide **1.638.820 bytes en Editor**; el player contiene 641.640 bytes de vértices y sus índices. No es memoria Vita medida. Se recalculan límites conservadores más ajustados: todos los triángulos originales quedan contenidos y mantienen su posición. Las referencias de colisión permanecen intactas.

El horneado ocurre durante la construcción; no añade combinación de mallas por frame. Activa static batching PSP2 y mantiene dynamic=0. Se preservan Low+, 960×544, masterTextureLimit=1, límites de textura de28, HUD, shaders, materiales, LOD, enemigos, partículas, audio, controles y guardados. Los tres scripts runtime modificados solo cambian identificación/protocolo a29. Siete archivos existentes cambian y se añaden dos archivos de Editor; todos los recursos originales fuente conservan sus bytes.

## Validación

**VERIFIED local:** cinco vistas A/B no vacías, idénticas píxel a píxel; posiciones de todos los triángulos seleccionados, límites conservadores y referencias de colisión comprobados. Flujo original esES de Hawái, jugador vivo, 109 tipos/3.407 filas/16.847 campos numéricos, cero errores de juego y guardados/backup/recuperación pasan; cinco errores deliberados de guardado separados.

Compilación final: 0 errores, 501 advertencias, 3:03,38. Pasan 61 contratos de arranque/guardado. Los 5.612 tipos de ambos ensamblados del juego conservan IL, campos y manejadores tras normalizar únicamente textos de versión. Se comparan **11.742 registros nativos** de tres escenas: jerarquía, transformaciones, valores de los 60 componentes de script, cámaras, luces, colisiones verificadas y controlador de animación. El lector resuelve referencias reordenadas, incluidos los clips del controlador. Se confirma **0→505 renderers agrupados en el player**. SELF, Mono, otros DLL y bancos de audio coinciden con28; símbolos exactos y AOT4096 verificados.

Fallos conservados: comprobaciones iniciales incorrectas de matriz de renderer, igualdad literal de AABB y ubicación de API; el primer presupuesto real excedió 2 MiB y se redujo la selección. Faltó inicialmente un informe de textura en el preflight. Un player compiló con marcado de flags pero **no produjo batching nativo**: se descartó sin empaquetar y se sustituyó por horneado explícito. Los validadores también se corrigieron para distinguir identidad de componentes y referencias reubicadas de diferencias de contenido. Evidencias privadas en `PSP2_VPK29/Failures/` y `Attempts/FlagsOnly/`.

## Entrega y prueba pendiente

Privado: `PSP2_VPK29/HSW_Vita_Test_00.29_HGSKW1178.vpk`, **170.864.022 bytes**, 288 entradas; CRC y hashes verificados. SHA-256: **`2dc9d8caacbfbfc02a5dab2426edd804063025a06854ebb1408a167a7cda6fad`**. VPK26/27/28 y checkpoints preservados; reversión protegida a28 comprobada en seco, sin rutas de partidas.

**UNTESTED físico29:** FPS, frametimes, memoria, aspecto, audio, persistencia fría y estabilidad prolongada. El objetivo de30FPS sigue pendiente. Comparar con28 usando BlackTip, Hawái y el mismo recorrido, zonas densas y despejadas, sin overclock; separar carga fría y segunda entrada. Medir al menos100s: FPS presentados si están disponibles, endFrameHz como finalizaciónCPU, media/p50/p95/máximo, frames>33/50/100ms, pausas, carga y guardado. Revisar LPDDR/CDRAM/PHYSCONT, managed y retorno al selector, comida/turbo, colisiones y audio. No sumar scopes CPU solapados ni atribuir el tiempo no instrumentado exclusivamente a GPU.
