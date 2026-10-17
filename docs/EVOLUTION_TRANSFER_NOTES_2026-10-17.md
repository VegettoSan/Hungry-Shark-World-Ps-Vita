# Lecciones de Hungry Shark Evolution aplicables a World — 2026-10-17

**Alcance:** investigación ligera de **P00**, sin recuperar el proyecto World, migrar el motor, compilar un VPK ni cambiar aprobaciones. Estas notas sirven como índice de *hipótesis comprobables* para cuando se retome World, después de estabilizar Evolution. Los dos juegos, sus fuentes, IDs y resultados de prueba permanecen separados.

## Fuentes y grado de certeza

- **Evolution:** [auditoría de fases](https://github.com/VegettoSan/Hungry-Shark-Evolution-Ps-Vita/blob/main/docs/PHASE_AUDIT_2026-10-17.md), [pantalla negra/texturas](https://github.com/VegettoSan/Hungry-Shark-Evolution-Ps-Vita/blob/main/docs/PSP2_BLACK_SCREEN_2026-10-17.md), [audio/memoria D05](https://github.com/VegettoSan/Hungry-Shark-Evolution-Ps-Vita/blob/main/docs/PSP2_LOAD_AUDIO_INPUT_D05_2026-10-17.md), [calidad D06](https://github.com/VegettoSan/Hungry-Shark-Evolution-Ps-Vita/blob/main/docs/PSP2_MEDIUM_D06_2026-10-17.md), [rendimiento D07](https://github.com/VegettoSan/Hungry-Shark-Evolution-Ps-Vita/blob/main/docs/PSP2_PERFORMANCE_D07_2026-10-17.md), [guardado D08](https://github.com/VegettoSan/Hungry-Shark-Evolution-Ps-Vita/blob/main/docs/PSP2_SAVE_CPU_D08_2026-10-17.md) y [D09](https://github.com/VegettoSan/Hungry-Shark-Evolution-Ps-Vita/blob/main/docs/PSP2_SAVE_IO_D09_2026-10-17.md).
- **World:** [auditoría 2.9.0 (132)](TECHNICAL_AUDIT.md), [extracción APK+OBB](DATA_EXTRACTION_AND_LAYOUT.md), [reglas](../AGENTS.md). Los dos archivos privados facilitados por el propietario fueron inspeccionados **solo de manera estática**. SHA-256 igual a los valores de `TECHNICAL_AUDIT.md`.
- Etiquetas: **CONFIRMADO-WORLD** = inspección de sus archivos; **DEMOSTRADO-EVOLUTION** = registros específicos de Evolution; **CANDIDATO** = posible método por verificar; **NO PROBADO-WORLD** = no deducir equivalencia.

## Comparación mínima

| Tema | Evolution 6.4.2 | World 2.9.0 (132) | Decisión para World |
| --- | --- | --- | --- |
| Motor | Unity **5.6.4p3**, Mono | Unity **2017.1.2p4**, Mono; **23 DLL Managed** | **CANDIDATO:** reutilizar flujo de AssetRipper/ILSpy y trazabilidad GUID/fileID; importar primero en **2017.1.2p4**, no en 2018 directamente |
| Distribución original | Unity Data en APK; 18 escenas serializadas | **APK + OBB inseparables**; `level0` en APK, `level1`–`level22` en OBB | **CONFIRMADO-WORLD:** combinar ambos sin colisiones; no usar extractor ni manifiesto de Evolution |
| División de datos | `.splitN` reconstruidos en Evolution | **6 grupos / 68 fragmentos**: `sharedassets0.assets` (37, APK); `level17` (3), `level21` (2), `level22` (3), `sharedassets17.assets` (18), `sharedassets3.assets` (3), `sharedassets7.assets` (2) en OBB | **CONFIRMADO-WORLD:** ordenar por sufijo numérico y preservar íntegros los objetos antes de AssetRipper |
| Salida PSP2 | Evolution tiene builds PSP2 de prueba ejecutados en consola | **No hay build Vita/Editor World verificado** | No transferir las afirmaciones de FPS, jugabilidad, memoria ni compatibilidad |
| Identidad | `HGSKE1178` | `HGSKW1178` | No cruzar Title ID, rutas de guardado, partidas, recursos ni `Assembly-CSharp.dll` |

## Hallazgos reutilizables, **no** parches automáticos

1. **Texturas, shaders y pantalla negra.** **DEMOSTRADO-EVOLUTION:** un player PSP2 contenía **671 texturas BC7** incompatibles en ese flujo; reimportar con PSP2 activo corrigió el empaquetado a formatos aceptados sin alterar los `.meta`. También hubo un error concreto de variantes/lightmap en un shader. **CANDIDATO-WORLD:** comparar los formatos de las texturas **del build PSP2 generado**, los programas ConsoleVS/ConsoleFS, import settings, keywords y variantes antes de editar shaders. **NO PROBADO-WORLD:** que World tenga BC7 o el mismo fallo de shaders.

2. **Audio y memoria.** **DEMOSTRADO-EVOLUTION:** convertir 302 clips Vorbis a HEVAG para PSP2 y aumentar el modo de memoria a ExpandBy109MB acompañó al VPK D05 que el propietario reportó jugable con sonido; el diagnóstico de un crash anterior señalaba un buffer gráfico sin memoria. **CONFIRMADO-WORLD:** su APK incluye `Fabric.Core.dll`, `libunity.so` y `libmono.so`; no está probado qué ruta de audio utiliza en runtime. **CANDIDATO:** inventariar clips/formato, dependencias Fabric/Unity y presupuesto LPDDR/CDRAM/PHYSCONT; aplicar overrides PSP2 solo si se demuestra necesidad. No copiar por inercia ajustes de memoria ni convertir todo el audio.

3. **Servicios Android y migración Unity.** **CONFIRMADO-WORLD:** aparecen `libubiservices.so`, `libadcolony.so`, `libgpg.so`, bibliotecas Facebook y `AndroidJava` en el ensamblado principal. **DEMOSTRADO-EVOLUTION:** adaptaciones acotadas para servicios Android/Unity 2018 y una corrección de nombres de `AnimationState` fueron necesarias para ejecutar contenido. **CANDIDATO-WORLD:** localizar llamadas realmente alcanzadas en escritorio/PSP2, aislar dependencias de Android bajo símbolos de plataforma solo con logs concretos; reconstruir y comparar nombres de clips/estados originales tras migración. **NO PROBADO-WORLD:** que existan el mismo bug de Animation o las mismas dependencias activas.

4. **Calidad visual y rendimiento.** **DEMOSTRADO-EVOLUTION:** la clasificación original de dispositivo elegía un perfil low/SD, y elevarlo a medium mejoró el detalle potencial pero expuso caídas a ~11 FPS en situaciones reportadas. D07 sugirió coste de render, sin demostrar que todo sea GPU-bound. **CANDIDATO-WORLD:** identificar *sus propios* niveles/escenas, clasificadores, atlas, distancia de visión y opciones antes de proponer cambios; medir en la misma escena/tiburón/reloj y separar CPU, GPU y memoria. Jamás copiar `DeviceType.medium`, nombres `Master_medium` o umbrales de Evolution sin prueba.

5. **Guardado y preferencias.** **DEMOSTRADO-EVOLUTION:** `PlayerPrefs`/identidad local, `local.sav` y `File.Copy` son rutas distintas; los intentos D08/D09 todavía **no acreditan persistencia correcta al reiniciar la Vita**. **CONFIRMADO-WORLD:** el binario `Assembly-CSharp.dll` contiene referencias nominales a `PlayerPrefs`, `SaveData`, `SaveGame` y `CloudSave`; estas cadenas **no prueban** el formato, algoritmo, archivos ni flujo World. **CANDIDATO:** mapear con ILSpy el propio ciclo de guardar/cargar de World y probar perfil → checkpoint → cierre total → reapertura del **mismo** VPK, sin borrar/reinstalar ni sobrescribir saves. No trasladar el codec ni los parches de Evolution.

6. **UI y controles.** **DEMOSTRADO-EVOLUTION:** navegación original mediante adaptación PS Vita, geometría del `UIWidget` en vez de `Collider.bounds` para el foco NGUI, y reconocimiento de slider. **CANDIDATO-WORLD:** identificar primero su framework UI, entrada táctil y jerarquía; solo adaptar los controles detectados. **NO PROBADO-WORLD:** que World utilice los mismos componentes NGUI ni geometría.

## Orden de consulta para una futura sesión World

1. **Ahora (P00, solo documentación):** conservar estos enlaces, los hashes de APK+OBB y las diferencias verificadas. **No iniciar el port paralelo a Evolution.**
2. **Cuando el propietario active P01:** recuperar ambos archivos en un conjunto coherente, inspeccionar tipos/escenas/referencias y generar una lista propia de componentes de World, sin modificar el código de juego.
3. **Después de demostrar World en Unity 2017.1.2p4 y obtener aprobaciones:** congelar baseline y migrar **copia separada** a Unity 2018.2.19f1; comparar animaciones, UI, servicios, audio y guardados con las pruebas originales.
4. **Solo en pruebas PSP2 autorizadas:** primero formatos de texturas y shaders reales del VPK, luego audio/memoria, controles, persistencia tras reinicio y diagnóstico A/B de rendimiento. Conservar un build y hashes de rollback por cambio.

**No se ha aprobado ninguna fase nueva ni realizado un experimento Vita de World.** Esta revisión no añade resultados a `EXPERIMENTS.md` porque no ejecutó Unity ni la consola. Tampoco crea ramas nuevas, copia código/recursos de Evolution ni altera la identidad `HGSKW1178`.
