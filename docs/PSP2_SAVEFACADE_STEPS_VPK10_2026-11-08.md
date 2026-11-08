# SaveFacade por etapas — VPK 10 privado

Fecha: 2026-11-08. **Es un diagnóstico; todavía no se ha probado físicamente en Vita ni se declara reparado el cierre.**

## Evidencia física de 00.09

El propietario confirma que B3a permanece estable y el juego se cierra al pulsar «Iniciar carga original de partida». T no produjo sonido; M reprodujo los tres segundos de música original. Esto valida la reproducción directa de ese clip HEVAG, sin demostrar que todos los clips o Fabric funcionen. No hay un dump ni un log nuevo del cierre.

## Cambios temporales

Solo el modo B, bajo `UNITY_PSP2 && HSW_PSP2_BOOT_LOG`, introduce pausas antes de estas operaciones:

| Paso | Operación original |
| --- | --- |
| S1 | Suscriptores de OnLoadStarted |
| S2 | Certificados offline |
| S3 | HSXServer.Configure y configuración local |
| S4 | GeoLocation, incluida la persistencia de PlayerPrefs |
| S5 | Inicialización offline y AppActivation |
| S6a | Resources.Load de GameDB/gameDB.gdb |
| S6b | Obtener TextAsset.bytes |
| S6c | Descifrado AES y parser JSON originales |
| S6d | Crear GameData e importar el diccionario |
| S6e | GameDB.Initialize |
| S6f | Caché original y máscaras EdibleData |
| S7 | Suscriptores de OnGameDBLoaded |
| S8 | AuthManager.LoadUser |
| S9 | StartLoadFlow/HandleError y callbacks originales |

Cada botón muestra la operación antes de ejecutarla. WAIT/BEFORE/DONE registran memoria libre, sin GC forzado ni texturas o render textures diagnósticas nuevas. El comparador contra el checkpoint verifica que Load conserva su cuerpo original salvo el despacho B y que LoadGameData permanece intacto. El iterador B usa las mismas entradas y algoritmos; conserva guardado, escenas y suscriptores.

Las pausas alteran tiempos y duración de las referencias. Si B llega al menú, eso por sí solo no demuestra una reparación del modo Original ni identifica una causa de memoria. No se eliminó audio ni se amplió memoria.

## Validación real

**VERIFIED — compilación:** 3.742 fuentes con UNITY_PSP2 y HSW_PSP2_BOOT_LOG explícitos, 0 errores y 514 advertencias.

**VERIFIED — Editor:** dos procesos de 45 segundos, Original y B/R2. Ambos llegan a FrontEnd, 3DBackground y Sharks con 0 errores durante Play, una llamada de carga y límite 60/VSync1. B espera y completa los 14 pasos una vez; Original no activa esos pasos. Se usan datos ficticios aislados y una continuación de Splash exclusiva del runner, sin aceptar edad. La fixture se retiró y los ajustes reales se restauraron antes del build. No son pruebas del motor GXM ni del audio nativo Vita.

**VERIFIED — único build nativo:** Succeeded, 0 errores, 596 advertencias, 03:25,9348988. BuildOptions.None, Mono2x, expansión None. SELF normal exacto, SHA256 `14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`. Sin Development Build ni modificación del player. Pasan 58 contratos de arranque/guardado y 47 de diagnóstico; 199 marcas.

**VERIFIED — recursos:** 23 escenas, 480 texturas, 424 clips HEVAG y 140 shaders con 245 passes ConsoleVS/ConsoleFS. Los 15 bancos de recursos son idénticos byte a byte a 00.09. No hubo conversiones ni reimportaciones correctivas adicionales. No hay archivos completamente cero; XML, recursos estáticos, Fabric y helper pasan sus comprobaciones.

**VERIFIED — preservación:** solo cinco fuentes y dos valores de versión cambian. No se añaden ni eliminan assets o metas originales. Audio, controles, FPS, adaptaciones offline y codec de guardado permanecen intactos. Se archivaron y restauraron siete metas de caché reserializadas por Unity; la comparación completa fuente/caché pasa. Los 20.870 hashes de Unity 2017 y los 20.887 de la base funcional 2018 coinciden con sus manifiestos; VPK 09 conserva su SHA. Rollback 09: dry-run de seis archivos aprobado. Sin cambios de ramas, fases, ledger, Evolution o publicación.

## Paquete y símbolos

Artefacto privado: `local-work/HSW_Recovery/Reports/PSP2_VPK10/HSW_Vita_Test_00.10_HGSKW1178.vpk`.

179.742.903 bytes, 285 entradas. SHA256:
`824889a856bf64cbb101edc85c535f2421c1bde1d9ad9b776dd07d5bc21be3b4`.

HGSKW1178/00.10, ATTRIBUTE2=0, cuota 8192 KiB. CRC y hash de cada miembro verificados; copia permanente en E con SHA idéntico. `VPK10_ExactSymbols.zip` contiene los cinco archivos exactos de símbolos 10, 36.423.229 bytes, con CRC y hashes internos comprobados. No se usaron símbolos 09 para representar el AOT 10.

## Fallos conservados

Antes del reinicio, los procesos del Editor se detenían antes de Play. El propietario confirmó un problema del PC y reinició; después se verificaron las cinco fuentes contra la caché. La inspección de ventanas no mostró diálogos Unity y no efectuó acciones de interfaz ni cambios del sistema. Esos fallos locales no se atribuyen al cierre físico Vita.

El primer compile sin BOOT_LOG tenía cobertura insuficiente y no se acepta como prueba de la rama nueva. Un comando de lectura tuvo un error de sintaxis antes de los checks y se corrigió. El runner nuevo perdió su estado al recargar el dominio y quedó en Splash sin resultado válido; se guardaron log y fuente, se añadieron marcadores persistentes y después pasaron ambos ensayos. Tras BuildSucceeded y la salida Unity 0, el host seguía esperando descendientes; se interrumpió esa espera. El exit 1 de la consola queda separado del resultado nativo correcto.

Los fallos y recuperaciones se conservan en `Preparation_Failures_And_Recovery.json`. El informe 09 mantiene la auditoría OBB: 23 escenas incluidas, 477 rutas recuperables incluidas, 51 faltantes históricos y ninguna omisión nueva del catálogo. No se atribuyen esos faltantes al cierre sin observar qué recurso solicita el player.

## Prueba física pendiente

Entrar en B, seleccionar R2 y avanzar hasta B3a. Pulsar «Iniciar carga original de partida» y ejecutar los botones S1…S9, incluidos S6a…S6f, uno por uno. Comunicar el último botón pulsado antes del cierre. Si S1 no aparece, indicarlo. Si todos pasan, continuar las escenas hasta el menú. No hace falta repetir T/M. La causa nativa, estabilidad y llegada al menú en Vita siguen UNTESTED.