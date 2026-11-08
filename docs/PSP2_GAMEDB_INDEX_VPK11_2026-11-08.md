# GameDB: índice por posición y control original — VPK 11 privado

## Evidencia física que motiva el cambio

El propietario confirma cierre al ejecutar S6e en 00.10. Ese botón ejecutaba tres operaciones: construir GameDB, evaluar GetAllItems y asignar el resultado con Initialize. Initialize solo asigna la referencia; no se ha demostrado cuál de las tres operaciones provoca el cierre. La lectura, descifrado e importación anteriores devolvieron el control antes de mostrar S6e. No hay un nuevo dump ni log físico.

## Candidato localizado

GetAllItems refleja las 109 listas de GameData y construye el índice por tipo y clave. El cambio, exclusivo de UNITY_PSP2, conserva la reflexión y los diccionarios; sustituye solamente el foreach sobre IEnumerable por acceso IList.Count/get_Item. Conserva objetos, claves, orden, tablas vacías y comprobación de claves duplicadas. No se omite ninguna lista ni registro. Si una lista no admite IList, produce error en lugar de ignorarla.

El recorrido original sigue compilado como control. El candidato por posición es el predeterminado en PSP2. En B, S6e se divide en S6e1 (constructor), S6e2 (índice) y S6e3 (asignación). S6e2 ofrece dos botones: «Índice PSP2 por posición» y «Original (control)». La elección no se guarda en preferencias y se restablece por arranque/captura de SaveLoader.

Una posible diferencia de compatibilidad al enumerar tipos genéricos es una hipótesis. No se ha demostrado un fallo específico de AOT. Los temporales .s de 00.10 ya no estaban disponibles tras cerrar Unity; se conservan los símbolos exactos 10 y no se deduce ausencia de código a partir de ello. Los campos privados base de UnityEngine.Object no justifican agregar tipos inesperados al recorrido; se compararon los metadatos Editor/player. No se modifica el motor Unity ni se amplía memoria.

## Pruebas completadas

Compilación principal PSP2 con BOOT_LOG: 3.742 fuentes, 0 errores y 514 advertencias. Tres procesos Editor de 45 segundos: B por posición, B original de control y modo normal. Llegan a FrontEnd, 3DBackground y Sharks con 0 errores durante Play, una carga, 60/VSync1 y audio original. Los dos modos B completan los 16 pasos una vez.

La comparación usa el mismo GameData importado por el juego: ambos índices conservan 109 tipos y 3.407 registros con idénticas claves, orden y referencias ObjectData. Se compara cada registro; no se clonaron ni alteraron sus valores. Se corrigió el recuento preliminar de 153 listas: el recuento verificado de listas declaradas/reflejadas es 109.

El escaneo de fuentes prueba que los 109 campos serializados no cambiaron y que al retirar el bloque candidato el método GetAllItems coincide con el original. LoadGameData y los demás recursos permanecen sin cambios. Los tests usan namespaces ficticios y una continuación de Splash exclusiva del runner, sin aceptar consentimientos. La fixture se retira antes del build.

## Build y paquete verificados

Único build nativo: Succeeded, 0 errores, 596 advertencias, 03:07,5860387. BuildOptions.None, Mono2x y memoria None. SELF normal exacto, SHA256 `14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`. No Development Build ni modificación del player Unity.

Pasan 58 contratos de arranque/guardado y 51 de diagnóstico; 200 marcas. El player conserva 23 escenas, 480 texturas, 424 clips HEVAG y 140 shaders con 245 passes ConsoleVS/ConsoleFS. Los 15 bancos de recursos son idénticos byte a byte a 00.10, sin conversiones ni reimportaciones correctivas adicionales. Los archivos estáticos, Fabric y helper coinciden con 10; no hay archivos completamente cero y el XML es válido.

VPK privado permanente: `local-work/HSW_Recovery/Reports/PSP2_VPK11/HSW_Vita_Test_00.11_HGSKW1178.vpk`.

179.743.424 bytes, 285 entradas, SHA256 `a089c614fe8703fb33388dd975ec7c46769f68eacd251f37223fbcbb295d6b24`. HGSKW1178/00.11, ATTRIBUTE2=0, cuota 8192 KiB. CRC/hash de cada miembro y SHA de la copia permanente E verificados. Símbolos 11 exactos: cinco archivos en ZIP de 36.423.448 bytes, con CRC/hashes internos y SHA del espejo comprobados.

Solo cambian cinco fuentes y dos valores de versión. Sin assets/metas originales añadidos o eliminados, ni cambios en audio, gráficos, controles, FPS, adaptaciones offline o codec de guardado. Se archivaron/restauraron siete metas de caché reserializadas por Unity; la comparación completa fuente/caché pasa. Los 20.870 hashes de Unity 2017 y los 20.887 de la base funcional 2018 coinciden con sus manifiestos; VPK 10 conserva su SHA. Rollback 10: dry-run de seis archivos aprobado. Sin ramas, fases, ledger, publicación ni modificación de Evolution; excepción privada limitada autorizada por el propietario.

## Fallo de verificación conservado

La concatenación del verificador PowerShell omitió un salto de línea. Pasó 47 contratos y falló antes de los últimos cuatro por variable nula. Se archivaron el script y JSON parcial, se corrigió la unión y pasaron los 51 contratos sobre el mismo DLL. No fue un fallo del juego ni motivó otro build. La ausencia de temporales AOT .s y de un nuevo dump permanece documentada como límite de investigación, sin afirmar código AOT ausente.

**UNTESTED físico 11:** causa del cierre, resultado de las dos opciones S6e2, menú y estabilidad nativos. Es un candidato de compatibilidad con control diagnóstico, no una reparación física demostrada. No se activa ExpandBy109MB ni se eliminan recursos.

## Protocolo físico

Primera prueba: B/R2, pasos habituales hasta S6e1. Ejecutar S6e1, elegir «Índice PSP2 por posición» en S6e2 y continuar S6e3 y los demás pasos/escenas hasta el menú. Si cierra, indicar exactamente qué botón se pulsó.

Control: en otro arranque, repetir y elegir «Original (control)» en S6e2. No mezclar ambas opciones dentro del mismo proceso. El contraste dentro de la misma versión permite distinguir el recorrido del índice de los cambios de temporización al dividir S6e. No hace falta repetir T/M. Cualquier diferencia observada queda pendiente de explicación nativa hasta obtener evidencia suficiente.