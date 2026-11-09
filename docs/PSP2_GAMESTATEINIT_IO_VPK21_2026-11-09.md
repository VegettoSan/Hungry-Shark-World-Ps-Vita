# VPK 21 — guardado con búfer mayor y frontera GameStateInit

## Resultado físico20 comprobado

El propietario informa que el menú abre, pulsa Jugar, aparece la imagen de controles y después vuelve a LiveArea sin pantalla de crash. UDP y respaldo local contienen los mismos4427paquetes de la sesión, en orden, sin huecos, errores gestionados registrados ni cierre normal registrado. El watcher nativo continúa con accepted=returned=4427, phase8 y Wi-Fi3 hasta una antigüedad de fase de26,466s. Phase8 indica que el emisor nativo está retornando, no prueba por sí sola la continuación de C#.

Se completan GameDB109/3407, FrontEnd y todas las escenas del nivel: Results, IngameHUD, Pools, Audio_Hawaii, Audio_Common, SP_Hawaii_XS y Hawaii_low. Se registran las primeras cámaras de Hawaii_low. Esto supera la reserva VertexData que fallaba en19. No prueba finalización GPU ni gameplay. El último evento es `Ingame scenes loaded; GameStateInit begins`, con LPDDR91226112bytes (87MiB), CDRAM83045952, PHYSCONT27262976, managed27197440. No se ha proporcionado dump nuevo para20. Esos contadores previos no excluyen una reserva posterior fallida ni identifican la instrucción del cierre.

Las operaciones siguientes originales son GameInfo.OnGameSessionStart (buscar MainCamera, GetComponent<GameCamera>, deshabilitar cámara), PoolsManager.GeneratePools, SpawnerManager.OnGameStateInit, asignar transform de cámara, publicar InGameLoaded y configurar cámaras. Pools enumera el diccionario original y genera los pools precacheando prefabs/instancias con sus tamaños originales. No hay evidencia que permita acusar una de ellas o reescribirla todavía.

## Coste de arranque medido

El primer envío CPU de cámara FrontEnd ocurre a98,176s del reloj del transporte. Antes, las ventanas entre abrir destino de una copia de guardado y verificar el destino cerrado suman39,226s; durante toda la sesión suman65,688s. Varias tardan3–6,8s cada una. Son intervalos instrumentados que incluyen lectura/escritura/cierre y observación, no un benchmark aislado del dispositivo. Los guardados siguen siendo síncronos y no se omite ni agrupa ninguna solicitud lógica.

La copia lee/escribe8KiB por iteración. El mscorlib exacto del player confirma que FileStream con cuatro argumentos utiliza búfer8192, no el default4096 de otros perfiles. La única modificación funcional de21 en HSWPSP2SaveIO es pasar65536 al constructor del stream de salida. Agrupa las escrituras pequeñas; conserva lectura/comparación8KiB, Flush/Close, longitud, comparación de todos los bytes, codec, temporal, respaldo, recuperación y propagación de errores. Añade un búfer administrado limitado; no un cache de partidas ni cambios de formato. La mejora real de tiempo en Vita queda UNTESTED.

También se quita la generación de stack de LogType.Log ordinario: se conserva Debug.Log/TTY y la configuración anterior de Error, Exception y Assert. Los errores y sus stacks no se desactivan. Los mensajes siguen enviándose por UDP y guardándose localmente.

## Instrumentación focalizada

BEFORE/DONE identifican llamada y retorno de GameStateInit y su base, los tres pasos de cámara, generación de pools, creación/avance/current del enumerador, cada pool y carga/inicialización de sus prefabs con fila/ruta/tamaño. No hay un botón por recurso ni logs por cada entidad. El catch PSP2 registra INGAME_EXCEPTION y relanza la misma excepción. Se conservan orden, tamaños, asociaciones, enumeración, readiness y callbacks originales. GameDB y presupuesto2ms permanecen idénticos.

El supervisor existente añade una consulta por segundo a sceKernelGetFreeMemorySize desde su hilo nativo normal. Registra memRc y kernelMain/kernelCdram/kernelPhycont incluso cuando el hilo principal no avanza. Estructura en stack, sin Unity, Mono, GC, objetos gestionados ni asignaciones nuevas de heap. kernelCdram es el contador del kernel y no equivale al CDRAM del dispositivo gráfico Unity. No se consulta desde el handler de crash; ese handler conserva su función de escribir user-data. ABI/exportaciones del plugin permanecen iguales.

## Validación y entrega

Editor: pruebas de nueva partida, sobrescritura, respaldo exacto, copia cerrada, fallos parciales y recuperación, rechazo de datos inválidos/versiones futuras; PASS. Arranque aislado,109tipos/3407registros, menú, un load/evento/completado, perfil mínimo original,60cap/VSync1 y limpieza async previa al nivel; PASS, cero errores reales.2027paquetes UDP consecutivos; único error de captura es el selftest deliberado del callback de hilo. La entrada completa al nivel y el nuevo diagnóstico GameStateInit no se presentan como validados por el fixture de menú.

Una compilación nativa2018.2.19f1: Succeeded,0errores,492warnings,03:09.9301305. Mono2x y BuildOptions.None, SELF normal intacto, sin Development/Razor. ExpandBy109MB=3/ATTRIBUTE2=0c y calidad Very Low son los mismos de20; ninguna expansión adicional.58contratos generales y93de diagnóstico,254marcadores.49archivos serializados y15bancos byte idénticos;23escenas. GameData, índice GameDB, SaveData y SaveGameManager conservan todo su IL/campos exactos20; en SaveIO todo excepto el constructor de Copy es exacto20. Se verificó el delta de fuente único de ese helper.13archivos existentes,0nuevos; ProjectSettings solo cambia las dos versiones. Plugins/metadatos de recursos, audio, modelos, texturas, shaders, controles, progresión y datos no se reconvierten ni recortan. Se conservan Evolution,2017,VPK20 y anteriores; sin ramas/fases/publicación.

Se conservan fallos locales de herramientas: catch nuevo sin namespace System, corregido a System.Exception antes de compilar; contrato nuevo que consultaba Copy antes de obtener su IL, reordenado; recibo trataba la lista de marcadores como número, corregido. Ninguno requirió otro build nativo o un workaround funcional. El default de FileStream se confirmó en el mscorlib real y se corrigió la descripción inicial4096→8192, sin cambio adicional al player.

Paquete privado `HSW_Vita_Test_00.21_HGSKW1178.vpk`,179827934bytes/288entradas. SHA256 `f521641e8114e68b2b5069148e7dd270549f4bfcdc56163e5cea40d518ba89fc`. CRC/hashes de todos los miembros y espejos correctos. Se conservan VPK21_ExactSymbols.zip (7archivos), VPK21_NativePluginSymbols.zip, manifiestos y rollback20 guardado/dry-run. Archivo diagnóstico y resultados privados en Reports/PSP2_VPK21.

Receptor PC18194 continúa abierto y añade a vita_live.log; el receptor de tests18195 se cerró. Instalar21 sobre el título existente sin borrar la partida, esperar menú y repetir la misma entrada a Hawái. No hay ventana ni botones de diagnóstico. Avisar al llegar o cerrar; copiar después ux0:data/HSW_Vita/vita_live.log y vita_live_watch.log, y cualquier nuevo .psp2dmp, conservando VPK/símbolos21 exactos. Comparar las mismas fronteras de arranque y los nuevos BEFORE/DONE/kernelMain. **UNTESTED físico21:** tiempo real, punto preciso del cierre, entrada/estabilidad de gameplay. No se declara solucionado el cierre20.
