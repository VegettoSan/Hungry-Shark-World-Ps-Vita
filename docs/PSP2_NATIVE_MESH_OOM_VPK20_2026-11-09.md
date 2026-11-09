# VPK 20 — carga de nivel tras OOM nativo comprobado

## Evidencia física nueva, distinta del cierre antiguo de GameDB

El propietario confirmó que VPK19 abre el menú, responde a los controles y reproduce música. Al intentar jugar, la carga de Hawái terminó en un crash. La captura de esa sesión contiene 4737 paquetes consecutivos, sin huecos ni fragmentos incompletos. GameDB había terminado sus 109 tipos/3407 registros; guardado, FrontEnd, 3DBackground, Sharks y música habían avanzado por sus rutas originales.

La excepción nativa sí tiene evidencia de memoria: Unity registra `System out of memory`, al intentar reservar **76056 bytes**, alineación32, etiqueta **VertexData**, en UnityPreload. En el contexto inmediatamente anterior se observaron LPDDR=0 y después 2–3MiB durante la carga de recursos/Hawaii_low. No se señala un prefab como defectuoso solo por ser el último nombre recibido.

El dump aportado se conserva byte por byte. SHA256 `99e2d1155a46a5eaae895f21fa38df6678c8ade767647407338de351152af4a2`. Usando el reproductor/símbolos exactos de19, PC `0x812b2f78` cae en PackedFloatVector::UnpackFloats, offset0x126. La instrucción es `vstr s0,[r2]` y R2=0: escritura nula durante descompresión de geometría. El UID del hilo coincide con el del error de reserva. Las palabras de stack compatibles con CompressedMesh::Decompress/MemoryManager son candidatos, no un unwind completo.

**VERIFIED:** fallo nativo de escritura nula y error explícito de reserva en el mismo hilo/carga. **INFERRED:** la descompresión recibe un destino inválido tras fallar la reserva. No se ha demostrado la distribución exacta de fragmentación, el Mesh concreto o toda la cadena de retorno del allocator. Esta evidencia no explica retrospectivamente los cierres de16/17 en Count, que no tenían dump ni OOM registrado. No se atribuye el fallo actual al audio, a AOT o a un registro GameDB corrupto.

Los contadores conservan el significado auditado en17: LPDDR y PHYSCONT usan sizeMain/sizePhycont de sceKernelGetFreeMemorySize; CDRAM suma bloques libres del dispositivo gráfico de Unity; managed usa GC.GetTotalMemory(false). No representan el mayor bloque disponible ni pueden sumarse como pools intercambiables. Aquí la evidencia de fallo de reserva es el mensaje nativo, además de los contadores.

## Cambios acotados de20

- **Memoria:** se solicita `ExpandBy109MB` mediante la propiedad pública de Unity, enum3, después de la evidencia física anterior. Native SFO y SFO empaquetado conservan ATTRIBUTE2=`0c000000`. No se parchea el reproductor. La cantidad realmente disponible debe medirse en20 físico. Evolution usa modo3 en su copia privada; se comprobó en lectura, sin modificarlo ni copiar sus ajustes en bloque.
- **Gráficos originales mínimos:** QualitySettings ya estaba en Very Low/índice0, texturas en su ajuste original2 y escenas `_low`. No hay nuevas conversiones. La ruta PSP2 mantiene rating efectivo0 y aplica una vez los ajustes originales aun cuando el rating inicial también sea0; antes esa igualdad podía saltarse la aplicación inicial. Conserva LOW_DETAIL_ON, su warmup y la planificación mínima original del pool1/1/8. Cambia la cantidad procesada por frame según el preset original, no el total de entidades o datos. No reescribe la preferencia guardada del usuario.
- **Carga coordinada:** la transición original lanzaba tres UnloadUnusedAssets y tres GC.Collect, sin esperar los AsyncOperation. PSP2 descarga las mismas referencias/bundles/equippables y reúne la limpieza en una sola operación, espera `isDone` y después llama al PushState original con Ingame y el nivel original. No se añaden GC.Collect ni pausas temporizadas; se retiran las tres llamadas explícitas de esa ruta PSP2. Los demás consumidores de UnloadAllEquippables conservan el método original y su limpieza. Un guard evita reentrada; finally lo libera; los errores siguen propagándose.
- **Ventana retirada:** OnGUI de los dos componentes de diagnóstico no se compila en el player PSP2 y se excluyen las llamadas a reconstruir el overlay. Se conserva la interfaz funcional del juego.
- **Logs conservados:** UDP inmediato, secuencias, callbacks, capturas de errores, respaldo nativo en ux0:data/HSW_Vita y watcher siguen activos. El plugin nativo solo cambia el identificador19→20. Se reducen sync críticos por cada callback de rutina; las fronteras principales/errores y el diagnóstico crítico GameDB mantienen su tratamiento. El StreamWriter secundario deja AutoFlush por línea y vacía periódicamente mientras hay escrituras, cada250ms, o inmediatamente para errores/fronteras críticas. ThreadLog conserva vaciado inmediato y no llama a APIs Unity. No se prometen fsync/atomicidad de ese stream administrado; el respaldo nativo y el watcher siguen disponibles.

No se cambia la implementación19 de guardado ni la candidata Count ya superada en hardware. No se modifica el presupuesto GameDB de2ms, sus claves, referencias, orden, errores, callbacks ni publicación al finalizar. Audio original, controles, adaptaciones offline y límite60/VSync1 permanecen.

## Validación local real y límites

Una compilación nativa Unity2018.2.19f1: **Succeeded, 0errores, 492warnings, 00:03:06.7637044**. Mono2x, BuildOptions.None; sin DEVELOPMENT_BUILD/Razor. El SELF es byte idéntico a la plantilla normal y al motor de19, SHA256 `14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`.

58 contratos generales,86 de diagnóstico y214 marcadores. Los tipos GameData, HSWPSP2GameDBIndex, HSWPSP2SaveIO, SaveData y SaveGameManager conservan todos sus métodos IL/campos nativos exactamente iguales a19. Se verificó que no hay OnGUI de diagnóstico, llamadas nativas de actualización del overlay, GC.Collect ni WaitForSeconds en la transición PSP2 nueva; sí hay espera de AsyncOperation y guard de reentrada.

**49 archivos serializados y15 bancos de recursos byte idénticos**, sin conversiones de audio/texturas. Se reutiliza la auditoría previa480texturas/424HEVAG/140shaders/245passes.23escenas y módulos/StreamingAssets/UI originales conservados. Scope exacto10archivos existentes, ninguno añadido:7fuentes,2artefactos del plugin y ProjectSettings. Settings solo cambian dos versiones y memoria0→3. Siete metadatos de plugin reserializados por Unity se restauraron a sus bytes/GUID originales; fuente privada y caché coinciden completamente.

Editor, datos aislados del propietario: arranque automático,109/3407, menú y escenas comunes, un load/evento/completado, calidad mínima/pool originales y60cap/VSync1. Prueba dirigida de la coroutine: limpieza comienza/termina, libera guard, añade payload una vez y no produce errores del juego.2032paquetes UDP consecutivos; único error recibido es el selftest deliberado del callback de hilo secundario. Se conserva captura/log local.

**FAIL conservados:** primer fixture no importaba FGOL; se corrigió solo el test. La navegación sintética del Editor primero pasó variante vacía en lugar de null y después encontró NullReference en SharkSelectScrollController.OnEnable al navegar UI sin interacción. No se arregló ese código ajeno ni se presenta esa navegación como PASS. La prueba dirigida final evita un salto artificial de interfaz y valida la limpieza real; **no valida entrada completa al nivel**. El primer verificador IL tenía una llave faltante y el contrato Flush esperaba StreamWriter en vez del operando real TextWriter virtual; se corrigieron las herramientas y todos los contratos finales pasan, sin cambios adicionales al player.

VPK19,2017,Evolution y los anteriores se conservan. No hay ramas nuevas, cambios de fases/aprobaciones, publicación ni descargas. Reversión20→19 guardada y verificada en dry-run; no toca savedata.

## Entrega y prueba física pendiente

Paquete privado **HSW_Vita_Test_00.20_HGSKW1178.vpk**,179823913bytes,288entradas. SHA256 `2d7053f83fac1664430e497212b9cf9cd5d4c654df44274921884769d8a057e1`. CRC y hashes de todos los miembros correctos. SFO nativo solo cambia la identidad de staging al título del propietario al empaquetar; la configuración de memoria ya procede de Unity y no se parchea. Se conservan VPK20_ExactSymbols.zip (7archivos), VPK20_NativePluginSymbols.zip, manifiestos y fuente/backup reversibles.

El receptor PC continúa abierto en192.168.1.8:18194 y añade a vita_live.log. El receptor de tests localhost18195 se detuvo. Instalar20 sobre el título actual sin borrar partida, esperar el menú y repetir el mismo tiburón/nivel de Hawái. No hay botones de diagnóstico ni ventana superpuesta. Comprobar música, controles, entrada al nivel y juego unos minutos. Informar al entrar o al cerrarse para analizar la nueva sesión; no borrar capturas previas. Conservar vita_live.log del PC, ux0:data/HSW_Vita/vita_live.log y vita_live_watch.log, nuevo .psp2dmp si aparece, VPK exacto y ambos archivos de símbolos de20.

**UNTESTED físico20:** mayor margen LPDDR real, tiempo de carga, entrada al nivel, estabilidad y persistencia fría del guardado. No se declara reparado el crash hasta esa comprobación.
