# GameDB incremental PSP2 — candidato funcional privado 00.14

El candidato cambia la construcción y su integración en el flujo real de arranque; no añade botones de diagnóstico. **UNTESTED físico 14:** solo una prueba satisfactoria del propietario puede acreditar que el cierre está reparado y que alcanza el menú en PS Vita.

## Evidencia y límites de la causa

**OWNER-REPORTED:** VPK13 completa I8a–I8o y cierra al ejecutar I8p. La primera tabla completa, sus claves, inserciones y registro por tipo funcionan; I8p agrupa las otras 108 tablas. La causa exacta continúa sin demostrarse. No se atribuye a audio, shaders, servicios online, agotamiento de memoria ni código AOT ausente.

En el Editor, la base original recuperada contiene 109 tipos y 3407 registros. KillableData, primera tabla según la enumeración verificada localmente, tiene 163 registros; siguen EdibleData153 y EntityData350. Los mayores grupos incluyen EntityData350 y MasterKeys287. Las comparaciones completas no encuentran claves duplicadas, nulos ni diferencias entre el índice original y el candidato. Esto no excluye un fallo nativo específico de PSP2.

Se examina el módulo AOT exacto 13, SHA `c37133bfc8fa618b87a596af395d5f29c0aa2dcb74cb2c7f09d0858973daeb90`: 266041 símbolos de función y 25 coincidencias relevantes. Están presentes GetAllItems, GetAllItemsPSP2Direct, el helper de listas y el coroutine diagnóstico MoveNext (6676 bytes). La presencia de código no acredita que todo despacho genérico funcione físicamente. Solo está disponible el dump histórico VPK1/Razor; no sirve para atribuir este cierre a una instrucción 13. No se inventa un stack actual.

## Reparación candidata

HSWPSP2GameDBIndex construye una sola tabla por avance y como máximo 32 registros por frame. Comprueba además un presupuesto blando de 2ms después de cada registro; una operación nativa individual no es interrumpible. Las tablas vacías también respetan un avance separado. Usa los 109 campos/tipos originales mediante enlaces directos, IList por posición, las referencias ObjectData originales y Dictionary.Add con sus errores por claves duplicadas. No crea un diccionario Type→IEnumerable, arrays de reflexión ni enumeradores por cada tipo de lista. Preasigna capacidades conocidas para reducir redimensionados y espacio sobrante.

El índice completo permanece privado en el builder. Result lanza mientras no haya terminado. GameDataManager espera todos los registros, posibles cachés y máscaras EdibleData antes de publicar y marcar disponibilidad. SaveFacade espera explícitamente esa coroutine antes de OnGameDBLoaded, LoadUser y StartLoadFlow. El bombeo explícito de los IEnumerator propaga los errores al flujo superior: un hijo fallido no permite continuar callbacks como si hubiera acabado bien. La petición duplicada de Load durante la construcción queda coalescida.

Se revisaron los consumidores: SaveFacade y la recarga de LoadingCurtainToGame usan la ruta asíncrona/callback correspondiente. La API síncrona original permanece para los dos estados de edición IngameEditor/IngameRaceEditor, conservando su contrato, y para otras plataformas; no se transforma silenciosamente en una operación que devuelva datos parciales.

## Cachés y publicación

La ruta histórica de caché podía volver a importar y reconstruir el índice de forma síncrona. LoadCachedEventData devuelve incluso el diccionario base cuando no hay modificaciones, lo que activaba esa segunda construcción redundante.

El candidato conserva la lectura, validación, mezcla y efectos originales de cachés. Solo reconstruye cuando hay una caché de base válida o eventos efectivamente mezclados; esa reconstrucción también usa lotes. Las mezclas de JSON son in-place: no se usa ReferenceEquals para inferir ausencia de cambios. Los callbacks síncronos de caché que consultan GameDB ven temporalmente una base COMPLETA, como antes; en un finally se restaura la instancia anterior antes de volver a ceder un frame. Los demás frames conservan la instancia previa (o null en arranque frío) hasta la publicación final. No hay tablas parcialmente inicializadas visibles.

## Progreso y recuperación sin botones

El arranque selecciona automáticamente el flujo original, sin A/B ni puertas de guardado. El overlay muestra tablas completadas, tabla activa, registros, último completado y el checkpoint previo. Los mensajes de progreso al log se limitan a uno por segundo, más finales/errores.

Un archivo propio de 192 bytes, separado de guardados y PlayerPrefs, contiene dos ranuras de 96 bytes con secuencia y checksum. Se actualiza antes de cada lote, no por cada registro durante el recorrido normal. Conserva pase (base/caché), tabla y rango de registros, último completado, operación y memoria muestreada. La CRC permite conservar la otra ranura si una escritura queda incompleta. No se promete atomicidad frente a pérdida de energía en Vita; la validación de recuperación aquí es del Editor.

Si un cierre deja un lote pendiente, el siguiente arranque reconstruye desde la base original y afina automáticamente ESE rango a un registro por paso, registrando acceso al objeto, lectura de clave y Add. No restaura objetos desde disco ni salta registros. Así un primer cierre deja una tabla/rango de hasta32 registros; una reproducción en el mismo tramo precisa registro/operación sin otro VPK. El checkpoint refleja lo solicitado/completado, no prueba por sí solo la instrucción causal si el fallo es asíncrono. Si su IO falla, se muestra como no disponible; nunca se inventa un éxito de GameDB.

## Validación dirigida

Mono/mcs: 3743 fuentes, UNITY_PSP2 y HSW_PSP2_BOOT_LOG, 0 errores/405 advertencias. Cold y Warm usan el guardado aislado del ensayo, 45s cada uno, y alcanzan FrontEnd/3DBackground/Sharks sin errores: una petición, un evento OnGameDBLoaded y un OnLoadComplete. La instancia publicada permanece anterior/null entre frames hasta estar lista. Sin puertas manuales, sin retener audio y con cap60/VSync1. El fixture solo continúa Splash en el ensayo, sin modificar consentimientos del producto, y se excluye del VPK.

La base original se importa una vez por comparación: 109 tipos/3407 registros, mismas claves, orden y referencias; las consultas y enumeradores GameDB coinciden. Se verifican Result inaccesible durante construcción, presupuesto máximo32, reproducción precisa de lote interrumpido y recuperación tras corromper la ranura más reciente. El recorrido verificado usó183 avances, máximo32registros, con las tablas vacías incluidas.

Los errores originales por duplicado y registro nulo se conservan. Un tercer ensayo Fault inyecta un duplicado solo en la instancia transitoria del Editor: provoca una excepción esperada, deja SaveLoader esperando, GameDB sin publicar y cero callbacks de éxito. No toca el recurso original ni los guardados del propietario.

## Memoria

Sin GC forzado, expansión o cambio de backend. Las capacidades de arrays internos del diccionario exterior bajan de1004 a488 slots y las de los109diccionarios de tablas de25796 a15460 slots en el runtime del Editor. Son capacidades agregadas, no bytes ni pico de memoria de Vita.

Las mediciones gestionadas netas sin GC no muestran menor consumo global del ensayo: por ejemplo, Warm observó409600bytes para el original y524288 para el candidato, incluyendo diagnóstico/IO/objetos retenidos y contextos distintos. No se presentan como una comparación de picos equivalentes. El menor espacio sobrante y la distribución por frames son hechos locales; el efecto nativo y cualquier fragmentación requieren Vita. El checkpoint y las marcas del candidato muestrean los tres pools libres y managed sin colección forzada. Los35MiB libres informados antes de S6e2 en00.11 son históricos, no una medición de I8p/14 ni prueba de OOM.

Se mantienen Mono2x, BuildOptions.None, memoria None, cap60, recursos originales, audio, gráficos, controles, guardados y offline. No cambios en Evolution, Unity2017, base2018, ramas o aprobaciones de fases.
## Build y paquete finales

Un único build nativo: **result=Succeeded errors=0 warnings=487 bytes=270173794 duration=00:02:59.6157271**. BuildOptions.None, Mono2x, memoria None; SELF normal SHA `14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`. Pasan58 contratos de arranque/guardado y44 de reparación/Fabric; 197 marcas. El fixture y sus hooks de prueba de checkpoint no están en el player.

Los49 archivos serializados y los15bancos de recursos son idénticos byte a byte a13. Se reutiliza por esa evidencia la auditoría de480texturas/424HEVAG/140shaders245passes, sin repetirla. Las23escenas y su orden se comprueban en el player14. Archivos estáticos, Fabric/helper y XML válidos, sin archivos completamente cero. Se conserva la fidelidad de recursos del proyecto recuperado; no se afirma que eso demuestre su compatibilidad física completa.

VPK privado `local-work/HSW_Recovery/Reports/PSP2_VPK14/HSW_Vita_Test_00.14_HGSKW1178.vpk`: 179784184 bytes,285entradas,SHA `ce4c1081dbb61b07d9017d470f55c483c6546b4f66df1496af7c9a72ca9d4a28`. HGSKW1178/00.14,ATTRIBUTE2=0,cuota8192KiB. CRC/hash por miembro y espejos de VPK/símbolos comprobados. Símbolos14 exactos:5archivos,ZIP 36457765 bytes,CRC/hashes internos verificados.

Alcance:7fuentes existentes, un nuevo builder y su meta, y2valores de versión.109campos serializados/enlaces en orden exactos; índices síncronos normal/directo/original conservados como referencia. Sin originales de assets/metas/audio/gráficos/controles/codec/offline añadidos o eliminados. Fuente/caché exactas después de archivar/restaurar 7 metas derivadas. VPK13 mantiene SHA `4c95551bf4d6f3a962e4595b273d1ecdccb2188d43d456a5a629fa3655d3bca8`. Se reutilizan las evidencias congeladas13 de2017/base2018, sin escrituras en esas bases/Evolution ni repetir escaneos históricos. Rollback13dryrun8archivos+2altasPASS. Sin ramas, publicación ni cambios de fases; excepción privada autorizada por el propietario.

Fallo del verificador conservado: la búsqueda textual del float2ms no coincidió con su representación IL. Se archivaron script/JSON parcial y se comparó el operando ldc.r4 numéricamente; pasan los44contratos sobre el mismo DLL, sin tocar el candidato ni recompilar el player.

## Prueba física

Instalar00.14 y arrancar normalmente. No seleccionarB ni pulsarI8: el índice debe avanzar automáticamente y seguir hacia FrontEnd. Si vuelve al LiveArea, relanzar el MISMO VPK una vez: el checkpoint permite afinar automáticamente el lote anterior. Registrar las líneas DB/PREVIOUS y cualquier error. Esta recuperación no omite datos ni constituye una reparación de un registro incompatible. Si alcanza menú, comprobar música, controles y una segunda entrada en frío con guardado conservado.

**UNTESTED físico14:** no se declara resuelto el cierre ni alcanzado el menú en Vita hasta recibir la prueba real.
