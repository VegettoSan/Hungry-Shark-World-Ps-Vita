# I8: enumeración e inserción de GameDB por operaciones — VPK 13 privado

## Evidencia física que motiva este diagnóstico

**OWNER-REPORTED:** en 00.12 también cierra el botón Indice directo PSP2. En el control Reflexion por pasos, I1–I7 terminan, el botón EJECUTAR I8 llega a verse y el proceso se cierra al pulsarlo. El propietario confirmó expresamente la diferencia entre ejecutar I7 y ejecutar I8. No hay nuevo dump ni log nativo entregado.

El candidato directo 12 no reparó el cierre. La reflexión para descubrir tipos/campos y obtener valores no basta para explicar ambos resultados: el control ya la completó antes de I8 y la ruta directa la evita. I8 aún contiene varias operaciones; no se ha demostrado cuál falla ni si el cierre es una excepción gestionada, un fallo AOT/nativo, una asignación o un fallo asíncrono.

Los valores anteriores a S6e2 de 00.11 siguen como evidencia histórica: LPDDR libre 36700160, CDRAM libre 84788896, PHYSCONT libre 27262976 y managed 21299200 bytes. No se reutilizan como medición de I8 ni prueban un mayor bloque disponible. Se mantiene memoria None, sin ExpandBy109MB.

## Cambio localizado: diagnóstico, sin reparación nueva afirmada

Solo cambia el bloque I8 del coroutine diagnóstico de GameData y las etiquetas/versiones 13 de tres fuentes. El cuerpo normal de GetAllItems, el candidato directo PSP2 y el algoritmo original de control permanecen idénticos a 12. GameDataManager, SaveFacade, importación, AES/JSON, datos, eventos y carga de escenas no cambian. No se modifica el player Unity.

La opción Reflexion por pasos conserva I1–I7 y sustituye la única puerta I8 por estas puertas manuales:

| Botón | Operación después de pulsarlo |
| --- | --- |
| I8a | Obtener la colección Keys del diccionario temporal |
| I8b | Crear el enumerador de tipos |
| I8c | Avanzar al primer tipo |
| I8d | Leer el primer tipo |
| I8e | Crear Dictionary<string,ObjectData> de la primera tabla |
| I8f | Obtener la primera lista con TryGetValue |
| I8g | Crear el enumerador de esa lista |
| I8h | Avanzar al primer registro |
| I8i | Leer el primer registro |
| I8j | Convertir el registro a ObjectData |
| I8k | Leer su propiedad key original |
| I8l | Insertar el primer registro por clave |
| I8m | Completar los registros restantes de esa primera tabla |
| I8n | Cerrar el enumerador de la lista |
| I8o | Añadir la primera tabla al índice por tipo |
| I8p | Completar las tablas restantes con el algoritmo original |
| I8q | Cerrar el enumerador de tipos |

Se conserva el orden original de enumeración, los registros originales y el cierre de enumeradores mediante finally, incluso ante una excepción. No hay datos inventados ni saltos de tablas. I8m e I8p siguen agrupando trabajo; si el cierre se identifica allí, todavía hará falta acotar registro/tabla. Las otras puertas distinguen la operación inicial sin exigir pulsar por cada uno de los 3407 registros.

Cada puerta usa el mecanismo existente WAIT/BEFORE/DONE, con memoria nativa disponible y managed sin GC forzado, y se muestra antes de ejecutar la operación. Solo funciona en B. No añade texturas, render targets, pruebas de audio ni escrituras por registro. La división cambia frames y la vida de temporales; un éxito del diagnóstico no demuestra por sí solo que las rutas monolíticas sean seguras.

## Validación y límites

La comparación de fuentes comprueba que todo GameData fuera del antiguo bloque I8 conserva exactamente su cuerpo 12, incluidos los 109 campos serializados y las rutas de índice normal/directa/original. Solo cuatro fuentes previstas cambian antes del build, sin altas ni bajas. Las demás comprobaciones y resultados se agregan después de ejecutarlos.

No se repiten conversiones de audio, texturas o shaders. La música original de menú ya sonó tres segundos en la prueba M; eso acredita ese clip directo, no todo Fabric. Los recursos y la transición SaveLoader → FrontEnd permanecen completos en este diagnóstico.

## Prueba física propuesta

En 00.13 usar B/R2 y avanzar a S6e2. Elegir **Reflexion por pasos**, completar I1–I7 y ejecutar I8a, I8b y los siguientes. Anotar el último botón que se pulsó antes del cierre. Si llegan a completarse I8q y S6e3, continuar las etapas originales hacia FrontEnd y registrar el resultado. No hace falta repetir audio T/M ni la ruta directa ya reportada como fallida.

**UNTESTED físico 13:** resultado de los subpasos I8a–I8q, causa nativa exacta y menú/estabilidad. La finalidad es localizar el cierre, manteniendo los sistemas originales; no se declara una corrección física.
## Resultados locales verificados

Compilación manual Mono/mcs: 3742 fuentes, UNITY_PSP2 y HSW_PSP2_BOOT_LOG, 0 errores y 405 advertencias. Dos procesos independientes del Editor Unity2018.2.19f1, 45 segundos cada uno: B reflexión con 40 puertas y normal con cero puertas. Ambos llegan a FrontEnd, 3DBackground y Sharks, con cero errores durante Play, una llamada real de carga y cap60/VSync1. I8a–I8q se detienen y completan una vez cada uno. El fixture usa preferencias/datos aislados y queda fuera del player; su continuación de Splash solo pertenece al ensayo, sin alterar consentimientos del producto.

La paridad se verifica sobre la misma instancia GameData original importada y también sobre el diccionario realmente asignado después de S6e3: 109 tipos y 3407 registros, mismas claves, orden y referencias ObjectData. No se eliminan ni copian registros para simular éxito. Esto acredita equivalencia local, no comportamiento nativo PSP2.

Único build nativo: **result=Succeeded errors=0 warnings=487 bytes=270157746 duration=00:03:34.4511319**. BuildOptions.None, Mono2x, memoria None. SELF normal exacto SHA256 `14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`. Pasan 58 contratos de arranque/guardado y 76 de diagnóstico; 201 marcas. Símbolos exactos del 13: cinco archivos, ZIP 36423378 bytes, CRC y hashes internos comprobados.

Player: 23 escenas, 480 texturas, 424 clips HEVAG, 140 shaders con 245 passes ConsoleVS/ConsoleFS. Los 15 bancos de recursos son idénticos byte a byte a 12. Sin nuevas conversiones/reimportaciones, ni archivos completamente cero; XML válido, archivos estáticos y Fabric/helper exactos. No Development/Razor ni modificación del player Unity.

VPK privado `local-work/HSW_Recovery/Reports/PSP2_VPK13/HSW_Vita_Test_00.13_HGSKW1178.vpk`: 179745132 bytes, 285 entradas, SHA256 `4c95551bf4d6f3a962e4595b273d1ecdccb2188d43d456a5a629fa3655d3bca8`. HGSKW1178/00.13, ATTRIBUTE2=0 y cuota8192KiB. CRC/hash de cada miembro y SHA de espejos permanentes VPK/símbolos verificados.

Solo cuatro fuentes y dos valores de versión cambian. Sin assets/metas originales añadidos o eliminados; 7 metas derivadas de caché reserializadas por Unity archivadas/restauradas. Fuente/caché coinciden por completo. Las bases Unity2017 (20870 archivos) y Unity2018 (20887 archivos) mantienen sus hashes; VPK12 conserva SHA `3b1d7e376e4e209875163a2a6377c985bf716cccb3eebd861abc31212795b89c`. Rollback12 dry-run de cinco archivos aprobado. Sin ramas, publicación, cambios de fases ni de Evolution; excepción limitada privada autorizada por el propietario.

La espera de consola Start-Process -Wait permaneció abierta después de la salida explícita Unity0 y sin proceso Unity. Se canceló solo esa espera tras verificar build, player y paquete; no fue un fallo nativo ni motivó otro build.
