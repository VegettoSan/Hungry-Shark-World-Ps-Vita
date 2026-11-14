# VPK 35 privada: recuperar el culling original y resolver una espera de centrado

Fecha UTC: 2026-11-14. Autorización correctiva del propietario: continuar desde VPK 34 funcional y su prueba física, investigar culling y conservar los problemas reportados. P00 ACTIVE; 0/13 gates aprobados. Sin publicación.

## Resultado

**VERIFIED en Editor 2018.2.19f1:** el gestor original `CullingInjectedECS_Hawaii` se carga con 4072 entradas, 4016 referencias a renderizadores y cero hulls. El código original destruye el componente al encontrar `GameCamera.enabled=false`. La inicialización desactiva temporalmente esa cámara y la reactiva después: el gestor ya había desaparecido al comenzar gameplay. La captura base registra presencia a los 27,51 s y ausencia a los 40,88 s. **No es una observación física del componente en Vita.**

La corrección conserva el gestor durante esa suspensión. Restaura una sola vez la visibilidad original y sus bits de estado; al reactivarse la cámara, vuelve a aplicar las máscaras por agua originales. No añade culling de IA, física ni población. Con cero hulls, evita calcular seis planos y recorrer las 4072 entradas buscando hulls inexistentes. Mantiene la ruta original cuando sí existen hulls.

El A/B reversible en la misma sesión/cámara desactiva 531 renderizadores con la vista sumergida y 3485 con la vista aérea. Cinco vistas de 480×272, 391680 bytes cada una, coinciden exactamente entre culling desactivado/activado y restaurado. Conserva 505 renderizadores en batching. El coste estable de Update fue aproximadamente 0,000512 ms en ese PC, incluida la reflexión del fixture; no representa coste físico en Vita.

| Camera.Render: 30 tandas alternadas por vista, Editor | Mediana antes → después (ms) | p95 (ms) | Máximo (ms) |
| --- | --- | --- | --- |
| Sumergida inicial | 0,3604 → 0,324 | 0,4459 → 0,4177 | 0,4552 → 0,4388 |
| Aérea inicial | 0,5977 → 0,2814 | 0,9008 → 0,415 | 1,0129 → 0,4163 |
| Profundidad | 0,3721 → 0,3024 | 0,4319 → 0,3757 | 0,4653 → 0,4394 |
| Sumergida desplazada | 0,3589 → 0,3284 | 0,5287 → 0,3887 | 0,576 → 0,3957 |
| Aérea desplazada | 0,6131 → 0,3039 | 0,8568 → 0,4216 | 0,92 → 0,4229 |

Estos tiempos miden la llamada de render de cámara, no el frame completo ni FPS de Vita. Los 90 frames normales del Profiler por ruta quedan preservados; sus condiciones de arranque no fueron idénticas y no se usan como A/B de FPS. Falta una zona densa representativa y atribuir el tiempo físico restante del hilo principal.

## Oclusión de Unity: prueba descartada

Se hizo un único bake sobre una copia privada de Hawaii_low: 3568 occludees, 2680 occluders conservadores, smallest occluder 5, hole 0,25, backface 100, target PSP2. Tardó 69,29 s y produjo 22187152 bytes de datos Umbra. La lectura inmediata devolvió cero antes de terminar la serialización; se conservó ese fallo y se reabrió el bake existente, sin repetirlo.

En seis vistas estáticas y con el mismo batching, activar oclusión aumentó la mediana de Camera.Render en todos los casos: 0,2801→0,4444; 0,2973→0,4977; 0,2137→0,4605; 0,2575→0,4449; 0,2034→0,4480; 0,2315→0,4062 ms. Cero diferencias de imagen; muestras no uniformes. **REJECTED:** coste de CPU mayor y 22,2 MB de datos sin beneficio demostrado. No se incorporan flags, bake ni escenas de la copia. Compatibilidad nativa/aditiva de ese bake UNTESTED. Frustum de Unity, culling masks, clips, LOD, bounds y gráficos Low+ se conservan.

## Bloqueo del selector

La prueba aislada reproduce una acción que espera centrar A, recibe una orden de centrar B y permanece esperando después de terminar el spring de B. La corrección recupera el destino de la acción original. Dispose retira su callback e impide que una notificación tardía de una acción cancelada recupere el centro. No salta el tutorial ni fuerza flags de progreso.

Pasan el retarget, la finalización al destino correcto, la cancelación, el callback tardío y los tutoriales completos con/sin una pulsación temprana, con desbloqueo de volver y retorno original a Shop. Esa pulsación aislada no reprodujo el bloqueo completo observado por el propietario. La correlación física es reinicio sin tocar controles → tutorial completo; **no se declara atribución exclusiva ni reparación física confirmada**. Se descarta el candidato DisableSpring del scroller por falta de reproducción que lo justifique.

## Validación y problemas abiertos

La prueba de culling llega a gameplay sin errores y conserva el gestor. Dos recorridos estrictos fallan al reanudar audio: error nativo `AudioSource.Play` / `Fabric.AudioComponent.Pause`, invalid seek. El mismo fallo quedó registrado en VPK 34. Se conservan ambos FAIL sin filtros. Un recorrido de observación continúa, reanuda gameplay y vuelve a Shop, y termina explícitamente **FAIL_WITH_RETURN_REACHED** con dos errores; no es un PASS de regresión. No hay cambios de audio. El sonido humano superpuesto reportado en Vita sigue sin atribución.

No se repiten compras/recompensas de 34: economía, inventario, guardado y sus métodos se verifican exactos a esa versión. Sus pruebas aisladas anteriores siguen conservadas, pero no se presentan como pruebas nuevas de 35. Las trabas de primera carga de modelos y LevelSelect permanecen pendientes. No se añade precarga global ni se descargan las escenas caché auditadas en 33.

Prueba física 34 del propietario: compra de mapa completada con pausa aproximada de 3 s, percibida como menor; sin mejora perceptible de gameplay. Reportó reinicio de progreso al instalar 34 y no recuerda si eliminó antes la burbuja. Causa pendiente: no se inspeccionó ni modificó su savedata, no se atribuye a la instalación o al guardado sin evidencia. Respaldar el guardado antes de otra instalación y conservar la burbuja.

## Integridad y entrega

result=Succeeded errors=0 warnings=497 bytes=243620098 duration=00:03:21.1333794

Cambian diez archivos existentes: dos fuentes funcionales y etiquetas/settings/plugin de versión. Cero archivos añadidos; otros 20908 exactos. CIL: únicamente OnSharkCentered, Dispose añadido, Update de culling y CullConvexHulls. Se preservan 23 escenas byte a byte, 49 archivos serializados auditados, 63 mallas, 78 programas GPU, 505 renderizadores agrupados, AOT 4096, SELF, Fabric y los demás módulos nativos. Guards y CRC del paquete, símbolos y rollback 35→34 en seco pasan. Los fixtures y la escena del bake quedan fuera del player; checkpoints y fallos, privados.

VPK privada: `local-work/HSW_Recovery/Reports/PSP2_VPK35/HSW_Vita_Test_00.35_HGSKW1178.vpk`. 164199777 bytes; 288 entradas. SHA-256: `e50d09cd53c8008a469fc9ba6e46525f2578085918d2ecfdbb203fc22a243bbe`.

Pendiente físico: efecto del culling sobre FPS/estabilidad y menús; tutorial con controles tempranos; persistencia y causa del reset; audio humano y pausa/reanudación. Próximo trabajo técnico: separar Resources.Load/Instantiate/activación de modelos y selector de niveles, investigar audio con estado del clip en el error y medir entidades densas sin reducir población. No se proclaman mejoras de FPS en Vita.
