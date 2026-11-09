# VPK 19 — guardado PSP2 basado en la adaptación de Evolution

## Resultado físico de VPK 18

El propietario mantiene el juego abierto y confirma que ya no vuelve a LiveArea, pero aparece el diálogo de espacio insuficiente con Reintentar. El log verifica que GameDB completa 109 tipos/3407 registros, hace COMMIT con 153 máscaras y termina los callbacks OnGameDBLoaded. Los heartbeats y frames continúan. Esto verifica que la candidata Count supera aquella frontera en esta ejecución; no establece por sí solo una causa de Mono ni valida todo el juego.

El fallo nuevo ocurre al guardar: termina la serialización/cifrado original, se escribe y cierra el temporal de 1 MiB y aparece BEFORE File.Move new destination, seguido del error genérico de SaveData.Save. Se repite en Reintentar. El catch deja SaveState.DiskSpace como valor inicial para excepciones genéricas; CheckDiskRequirements lo convierte en OutOfDiskSpace y SaveFacade muestra el texto de espacio insuficiente. No es una medición del espacio libre. La clase/mensaje exactos de la excepción no llegaron por Debug.LogException en esta captura; no se atribuye un errno ni se declara File.Move universalmente incompatible.

La ruta observada es savedata0:/persistentdata. No se cambia a otro título ni se borra el directorio. La captura parcial se conserva con su hash; el receptor sigue recibiendo la sesión abierta.

## Comparación solicitada con Evolution

Se leyeron HSEVitaSaveIO, SaveData y los informes D09/D10 de la copia privada Unity2018 de Evolution. Allí las copias pasaron a streams de 8 KiB, abriendo el origen antes de tocar el destino y comparando longitud/bytes después de cerrarlo. Su procedencia y los hashes de los dos fuentes efectivos se guardan en EvolutionReadOnlyComparison. Evolution se vuelve a verificar sin cambios al cerrar el trabajo.

World tiene un contenedor de versión3 distinto del de Evolution versión1 y otro esquema de datos. No se copian el header, campos de progreso, claves, identidad, player, cuota o ajustes de memoria de Evolution. Solo se adapta el mecanismo de IO comprobable. La evidencia de World justifica sustituir la promoción que falla, sin asumir que cualquier operación File.* falla en PSP2.

## Corrección candidata

Solo en PSP2, SaveData conserva la creación del temporal, serialización, compresión, cifrado, metadatos, prefijo y relleno originales. Prepare protege el principal válido en .backup antes de tocar el destino. Si solo existe un temporal válido, se conserva antes de reescribirlo. Commit compara el contenido lógico con los bytes serializados, valida el temporal usando el códec original en una instancia aislada y copia el archivo completo mediante streams. Se reabre y compara cada byte del destino antes de informar éxito. El temporal permanece como recuperación.

La comprobación inicial intenta recuperar un principal ausente o incompleto desde .temp y después .backup, siempre con el códec original. Un candidato incompatible no se degrada a una partida vacía. Los candidatos corruptos se conservan una sola vez con .psp2-corrupted; no se crean copias sin límite por guardado. Un fallo no devuelve OK y no dispara callbacks de éxito. Se retira la eliminación del principal tras un fallo de creación en PSP2, para no destruir evidencia o datos recuperables.

El copy abre el origen primero, respeta overwrite/CreateNew, rechaza mismo archivo, comprueba longitud estable y todos los bytes, y propaga errores. Los nuevos eventos SAVE_IO/SAVE_IO_ERROR llevan etapa y excepción directamente por el logger existente. No se modifica la interfaz para saltar el aviso, la comprobación de espacio ni los consentimientos.

Límite: una copia por streams no es un reemplazo atómico ni una garantía de fsync. Se retienen temporal y respaldo y se valida la recuperación para reducir esa ventana. Hace falta probar guardado y carga tras cerrar el proceso en Vita. La reserva de 1 MiB y cuota de8192KiB permanecen; principal/temporal/respaldo consumen espacio real. No se afirma disponibilidad de tarjeta a partir de RAM ni se aumenta la cuota sin medición.

## Validación

- Editor: guardado nuevo y actualización; prefijo/relleno original; backup exacto del principal anterior; descifrado, descompresión, parser y recuperación del marcador/fracción ficticios mediante el cargador original.
- Fallos dirigidos: origen ausente, overwrite=false y mismo archivo dejan el destino intacto. Una excepción tras escribir un primer bloque deja un principal parcial y devuelve fallo; se conserva la copia previa, se recupera el temporal válido y se comprueba el contenido original. Archivos inválidos no provocan reset y una versión futura no se sobrescribe.
- Editor45s: FrontEnd y comunes, 0errores del juego, una carga/evento/completado, 109tipos/3407registros y cap60/VSync1. Captura de2006paquetes completos; la única excepción está etiquetada como self-test threaded. Los ensayos negativos ocurren antes del arranque aislado y quedan registrados por separado.
- Mono/mcs PSP2:3745fuentes,0errores/406advertencias. Native Unity2018.2.19f1: Succeeded,0errores/488advertencias,00:03:00.0237232. La advertencia adicional corresponde al local savePath retenido del código previo al excluir su borrado PSP2; no se suprime.
- IL real de los players18/19: SaveToStream, LoadFromStream, IsValidFile y GenerateEncryptionKey son exactos, junto con todos los campos SaveData. Save PSP2 ya no llama a Move/Replace. GameDB y su Count son byte-exactos en los fuentes18; sus presupuestos y callbacks no cambian.
- 58contratos generales y81de IO/diagnóstico;212marcas.49archivos serializados y15bancos byte-exactos18; ninguna conversión nueva de audio/texturas/shaders. Mono2x,BuildOptions.None,expansiónNone,60cap/controles/offline intactos.

Fallos locales conservados: InvalidDataException no estaba disponible en el perfil de compilación y se sustituyó por IOException sin añadir dependencias. Una comparación preliminar de IL de mcs debug con el player release falló por nop/offsets; la comparación correcta entre ambos players finales verifica los cuatro métodos exactos. No fueron fallos de Vita ni motivaron cambios del códec. Solo se realizó un build nativo19.

El contrato antiguo que exigía mantener Move/Replace se sustituye explícitamente por los checks de la adaptación, ahora justificada por el fallo físico. Los checks de formato, claves, integridad y carga permanecen y se refuerzan; no se hace pasar un fallo como éxito.

## Entrega y prueba

VPK19 privado:179825479bytes,288entradas,HGSKW1178/00.19/ATTRIBUTE2=0,SHA256 `13f3ca44a11ff75508377889ac3824e3ddb24f4d099d15fb5a34a98e54fc2a9e`. CRC, hashes de miembros/runtime y copia permanente verificados. Se conservan los siete símbolos exactos y el CPP/O/MAP/stub del módulo. Cambian nueve archivos existentes y se añade el helper con su meta; las únicas diferencias finales de PlayerSettings son los dos valores de versión. Rollback18 queda preparado en seco; no toca los saves.

La captura18 ya está preservada: se puede cerrar18 e instalar19 sobre el mismo título conservando guardados. No borrar .temp/.backup ni preferencias. Mantener receptor UDP en192.168.1.8:18194.19debe intentar validar y recuperar el temporal18 antes de crear otro guardado y continuar el flujo original. Si aparece un error, los eventos de IO deben identificar la etapa y tipo real. Conservar ambos logs de Vita y cualquier dump nuevo.

Si llega al menú, comprobar primero el guardado por un checkpoint normal y después cerrar/reabrir el mismo VPK sin reinstalar para comprobar recuperación real. Esa validación física y la persistencia en frío siguen UNTESTED; el éxito del Editor no las sustituye. No se declara el juego completo estable ni se publica el VPK. Evolution, Unity2017 y todos los paquetes anteriores permanecen intactos; P00 continúa activo con0/13aprobaciones.


## Actualización física posterior — 2026-11-09

El propietario confirmó menú visible, controles funcionales y música audible en19. GameDB109/3407, guardado y callbacks completan en la captura. La prueba posterior de entrada a Hawái sufrió OOM nativo VertexData y escritura nula en descompresión de Mesh; dump y símbolos correlacionados. La entrega original conservó correctamente su etiqueta UNTESTED a aquella fecha. No se valida persistencia fría ni gameplay estable con19. Véase [análisis y candidata20](PSP2_NATIVE_MESH_OOM_VPK20_2026-11-09.md).
