# GameDB con acceso directo a las listas — VPK 12 privado

## Evidencia física recibida

**OWNER-REPORTED:** en 00.11, S6e1 se completa. Las dos opciones S6e2 cierran el proceso antes de S6e3. El candidato que solo cambiaba el recorrido de las listas no resuelve el cierre. No hay dump nuevo ni registro persistente que identifique una instrucción nativa.

Antes de S6e2, el propietario leyó LPDDR libre 36.700.160 bytes (35 MiB), CDRAM libre 84.788.896 bytes (80,86 MiB), PHYSCONT libre 27.262.976 bytes (26 MiB) y managed 21.299.200 bytes (20,3125 MiB). Managed no es memoria libre. No se conoce el mayor bloque contiguo ni el pico de la operación; los números no demuestran agotamiento ni descartan fragmentación. Se mantiene memoria None.

La prueba anterior M reprodujo tres segundos del clip original de menú. T fue silente. Esto confirma la reproducción directa de ese HEVAG concreto en Vita, sin demostrar todos los clips ni el sistema Fabric completo. B2 estable y el cierre al ejecutar la construcción del índice reorientan el diagnóstico hacia GameData.GetAllItems, manteniendo los recursos y la transición SaveLoader → FrontEnd.

## Cambio localizado

**INFERRED:** ambas opciones 11 compartían reflexión para descubrir los campos y extraer sus valores; esa parte merece aislarse. No se ha demostrado un defecto concreto de AOT, de reflexión ni de memoria.

El candidato PSP2 12 enlaza explícitamente cada una de las 109 listas originales con su tipo y construye los mismos diccionarios por clave. Evita GetType/GetFields/GetGenericArguments/FieldInfo.GetValue y el diccionario intermedio Type→IEnumerable en esa ruta. Un helper no genérico recorre IList por posición. Conserva las tablas vacías, referencias a los objetos originales, claves, orden, errores por duplicados y todos los datos importados. No añade campos serializados ni cambia la importación, cifrado, guardado, suscriptores, autenticación o carga de escenas. La ruta normal PSP2 usa este candidato; las otras plataformas mantienen el algoritmo original.

B mantiene S6e1 (constructor), S6e2 (construcción) y S6e3 (asignación). En S6e2 hay dos botones:

- **Indice directo PSP2:** ejecuta el candidato con las 109 referencias explícitas.
- **Reflexion por pasos:** ejecuta el algoritmo de control con ocho puertas manuales: I1 diccionario temporal, I2 tipo, I3 campos, I4 tipos genéricos, I5 valores de campos, I6 registro de tipos/listas, I7 diccionario final, I8 registros originales por tabla.

El control conserva las operaciones originales, distribuidas en varios frames, y usa dos arrays temporales de 109 referencias para separar descubrimiento y extracción. Cambia los tiempos y la vida de los temporales; un éxito del control tampoco probaría que la operación monolítica es segura. La ruta directa no usa esos arrays diagnósticos. Ninguna ruta evita registros o inventa resultados de carga.

## Verificación local

**VERIFIED:** compilación manual Mono/mcs de 3742 fuentes con UNITY_PSP2 y HSW_PSP2_BOOT_LOG: 0 errores, 405 advertencias. Hay 109 advertencias menos por campos que ahora se leen de forma directa.

Tres procesos independientes de Unity 2018.2.19f1, 45 segundos de Play cada uno: B directo, B reflexión y normal directo. Todos llegan a FrontEnd con 3DBackground y Sharks, cero errores durante Play, una carga real de SaveFacade y cap 60/VSync1. B directo completa 16 puertas; B reflexión, 24; normal, cero. El fixture usa datos y preferencias aislados y se excluye del player. Su continuación de Splash es exclusiva del ensayo y no altera consentimientos del producto.

Sobre la misma instancia original recién importada, la comparación del algoritmo original frente al directo verifica 109 tipos y 3407 registros: mismas claves, orden y referencias ObjectData. Tras S6e3 se comprueba también el diccionario realmente asignado a GameDB, con los mismos 109 tipos/3407 referencias. Los campos serializados y las 109 asociaciones explícitas coinciden exactamente con el orden y los tipos originales. El cuerpo normal de GameDataManager.LoadGameData sigue idéntico; el algoritmo original completo GetAllItems de 00.10 permanece como control.

El primer comprobador de asociaciones esperaba espacios alrededor de las comas y encontró cero coincidencias. Se corrigió únicamente su expresión regular; las fuentes ya usadas por el Editor no cambiaron. No fue un fallo del juego.

## Prueba física pendiente

Primero usar B y el perfil R2 habitual, avanzar hasta S6e2 y seleccionar Indice directo PSP2. Si aparece S6e3, continuar las etapas originales hasta el menú y observar el resultado. Después, con un arranque nuevo, seleccionar Reflexion por pasos y anotar la última operación I1–I8 cuya ejecución cierre el proceso. Un cierre en la ruta directa también debe registrarse como fallo del candidato, sin atribuirlo automáticamente a reflexión.

No se elimina música, modelos, texturas, shaders ni escenas; no se combinan nuevas exclusiones de audio y gráficos. No Development Build, Razor, expansión de memoria ni modificación del reproductor Unity. No se confirma reparación nativa por resultados del Editor.
## Build, paquete y preservación verificados

Único build nativo: **result=Succeeded errors=0 warnings=487 bytes=270154674 duration=00:02:57.6921699**. BuildOptions.None, Mono2x, memoria None. SELF normal exacto SHA256 `14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`. Pasan 58 contratos de arranque/guardado y 58 de diagnóstico; 201 marcas. No se modifica el reproductor Unity.

El player conserva 23 escenas, 480 texturas, 424 clips HEVAG y 140 shaders con 245 passes ConsoleVS/ConsoleFS. Sus 15 bancos de recursos son idénticos byte a byte a 00.11, sin nuevas conversiones ni reimportaciones. Fabric/helper y archivos estáticos coinciden; XML válido y ningún archivo completamente cero. Esto comprueba preservación, no compatibilidad física de todo recurso.

VPK privado `local-work/HSW_Recovery/Reports/PSP2_VPK12/HSW_Vita_Test_00.12_HGSKW1178.vpk`: 179743252 bytes, 285 entradas, SHA256 `3b1d7e376e4e209875163a2a6377c985bf716cccb3eebd861abc31212795b89c`. HGSKW1178/00.12, ATTRIBUTE2=0, cuota 8192 KiB. CRC y hash por miembro y SHA del espejo permanente comprobados. Símbolos exactos: cinco archivos, ZIP 36422122 bytes, CRC/hashes internos y espejo comprobados.

Solo cambian cinco fuentes y dos valores de versión. Sin assets originales añadidos o eliminados. Comparación completa fuente/caché exacta después de archivar/restaurar siete metas derivadas reserializadas por Unity. Los 20.870 archivos de la base Unity 2017 y 20.887 de Unity 2018 mantienen sus hashes; VPK11 mantiene SHA `a089c614fe8703fb33388dd975ec7c46769f68eacd251f37223fbcbb295d6b24`. Rollback11 dry-run de seis archivos aprobado. Todo queda privado e ignorado, sin ramas, publicación, cambios del ledger ni de Evolution; excepción limitada autorizada por el propietario.

**UNTESTED físico 12:** resultado de ambos botones, operación nativa exacta, llegada al menú y estabilidad. Se entrega un candidato con control diagnóstico, sin declarar el cierre reparado.
