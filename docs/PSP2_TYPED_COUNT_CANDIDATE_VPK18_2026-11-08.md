# VPK 18 — candidata PSP2 para la lectura de Count en GameDB

Estado: corrección de compatibilidad candidata. No se declara resuelto el cierre físico ni se atribuye una causa nativa demostrada.

## Evidencia nueva de VPK 17

El propietario informa otro cierre a LiveArea sin pantalla de crash. Se leyó el archivo completo del PC y se conservaron los respaldos proporcionados en la carpeta Vita antes de modificar el proyecto.

La sesión a5a500a258f7 contiene 1123 datagramas principales consecutivos y 58 heartbeats nativos, sin huecos o fragmentos incompletos. El archivo local de Vita contiene exactamente los mismos 1123 paquetes de esa sesión, y el archivo local del supervisor los mismos 58. No hay mensajes locales posteriores. Esto reduce la hipótesis de pérdida exclusiva de la cola UDP, pero no identifica una instrucción de fallo ni confirma el retorno nativo del último envío.

OnBoardingData termina sus tres registros. En T=83, HUDThreatDetectionData, fila 0, se registran DONE Trace, lista no nula, ownerMatches=True y tipo concreto List<Definitions.HUDThreatDetectionData>. La última marca es BEFORE ICollection.Count; falta su DONE. No hay excepción, TERMINATION, QUIT REQUEST ni cierre normal registrado. El último heartbeat indica accepted=1063, returned=1062, phase=2; es una muestra anterior al final, porque después llegaron los paquetes 1064–1123. Por tanto, esa phase=2 no demuestra un bloqueo final en escritura. No hay heartbeat posterior al límite de Count.

El último snapshot informa LPDDR 38797312, CDRAM 84790944, PHYSCONT 27262976 y managed 18612224 bytes. El valor administrado es inferior al final de la primera captura16; no aparece crecimiento descontrolado demostrado. La disponibilidad de pools no acredita el mayor bloque ni excluye fragmentación o fallos de reserva. No se cambia memoria ni se fuerza GC.

No se proporcionó .psp2dmp en la carpeta de respaldo. Se conservan los símbolos exactos y el VPK17 probado. La falta de dump o callback de salida no prueba salida voluntaria. Siguen abiertas una terminación nativa/asíncrona y un fallo en el retorno final del logger, además del despacho de Count.

Las tres capturas relevantes se sitúan en op1: T82 en el primer16, T83 en el segundo16 y T83 en17. Ahora Trace y las referencias de la lista han retornado antes de la llamada. La evidencia justifica probar una ruta concreta alternativa para esta operación, conservando el resto del constructor. No demuestra por sí sola un defecto de AOT, una lista dañada ni una instrucción exacta del motor.

## Cambio mínimo y alcance

El constructor sustituye una expresión: la lectura list.Count a través de ICollection pasa a GameData.ReadPSP2IndexCount(table,list). El helper recibe la MISMA referencia que se acaba de asociar y selecciona el List<T>.Count correspondiente al tipo declarado original. Se genera mecánicamente a partir de las 109 asociaciones existentes y no utiliza reflexión, clones, datos inventados ni un tamaño almacenado a mano. Una lista nula sigue devolviendo cero.

Se aplica la misma ruta a las 109 tablas porque la frontera problemática apareció con dos tipos distintos; limitarla a una tabla trasladaría la incertidumbre al siguiente tipo. La modificación se limita a Count. Se conservan IList.get_Item, ObjectData.key, Dictionary.Add, detección de duplicados, orden, referencias, callbacks y commit transaccional. No se omite ningún registro.

El resto del código del builder es idéntico al17 al normalizar esa única expresión y sus etiquetas de log. GameData solo añade el helper sin campos serializados. El presupuesto de 32 registros y 2 ms, yields, esperas y control de escenas permanecen iguales. No se desactiva audio, gráficos ni funciones de guardado/offline.

Matiz del IL: List<T>.get_Count está marcado virtual/final/newslot en el mscorlib incluido, aunque su propiedad C# no sea sobreescribible. El nuevo IL utiliza el método del tipo concreto List<T>, en lugar de ICollection.get_Count. No se afirma que cualquier callvirt implique despacho por interfaz ni que solo la presencia de la raíz AOT pruebe la causa. La inspección del AOT final se conserva por separado.

Se mantienen UDP, respaldo, subpasos y supervisor nativo. El módulo del supervisor solo cambia su identificador de versión; la implementación probada de17 permanece igual. Los paquetes principales llevan HSW18 y los del supervisor HSW18W, con secuencias separadas y el mismo ID de sesión. El receptor original no cambia. El analizador admite ambas versiones y distingue sus canales. La clasificación TERMINATION ahora usa REQUEST para una solicitud explícita y LIFECYCLE para el callback; este último no prueba voluntariedad.

## Validación dirigida

La prueba del Editor descifra e importa la GameDB original, compara las 109 lecturas tipadas con ICollection.Count y comprueba la semántica nula de cada entrada. Compara después con GetAllItems original: 109 tipos, 3407 registros, mismas claves, orden y referencias. La prueba de arranque de 45 segundos alcanza FrontEnd y escenas comunes, sin errores del juego, con una carga, evento y completado, y cap60/VSync1. Se reciben 1715 paquetes de ensayo sin huecos ni fragmentos incompletos; la única excepción está marcada como self-test del callback threaded.

Mono/mcs compila 3744 fuentes sin errores y 405 advertencias para la rama PSP2. La fixture y sus hooks quedan fuera del player. La configuración aislada del ensayo se restaura desde la copia privada original antes del build; no se entrega el companyName temporal que invalidó el primer intento17. La verificación final exige que solo cambien los dos valores de versión en PlayerSettings.

El IL de la candidata contiene 109 llamadas Count de los List<T> concretos y ninguna llamada ICollection.Count en Step. El verificador final también compara los tipos y su orden con los campos originales. Esta validación establece equivalencia local y un cambio real de ruta; no garantiza estabilidad nativa PSP2.

## Prueba física y archivos

Instalar18 y dejarlo avanzar automáticamente con Vita yPC en la misma red. El receptor sigue dirigido a192.168.1.8:18194 y añade al vita_live.log existente. No se requieren botones nuevos ni borrar partidas o checkpoints. Las marcas de op1 indican BEFORE/DONE typed List.Count, para distinguir esta ruta de16/17. El objetivo de esta candidata es completar GameDB y continuar por el flujo original haciaFrontEnd.

Si cierra, conservar el archivo delPC, ux0:data/HSW_Vita/vita_live.log y vita_live_watch.log, log administrado HSW_VPK18_*, checkpoint HSW_GameDB14.checkpoint y cualquier .psp2dmp nuevo. Los respaldos17 ya están guardados por separado. Se conservarán los símbolos exactos de18 y el VPK, además de los17 anteriores. Una llegada al menú será evidencia favorable de esta ruta; no bastará por sí sola para identificar una instrucción defectuosa deMono ni validar todo el gameplay.

## Resultado final local

El AOT exacto de18 compila ReadPSP2IndexCount como109 lecturas del campo de tamaño después de los controles de tipo; no conserva el patrón de salto IMT de Count de16/17 en ese helper. El offset observado pertenece al código generado porMono: la reparación C# no usa desplazamientos escritos a mano ni punteros sin protección. Esto confirma el cambio de ruta en el binario, no identifica el PC del cierre anterior.

Build único18: Succeeded,0errores/487advertencias,00:02:59.0152373, Mono2x/BuildOptions.None/expansiónNone.58contratos generales,74de candidata y216marcas;49archivos serializados y15bancos byte-exactos17. No se repiten conversiones ni auditorías masivas. La única diferencia final dePlayerSettings son bundleVersion ypsp2AppVersion17→18. Fuentes privadas y caché coinciden; rollback17 preparado y validado en seco sin aplicarse.

Paquete privado:179820545bytes,288entradas,HGSKW1178/00.18/ATTRIBUTE2=0,SHA256 `e36edfb186f34a28050a433c07ec9f9cc84d5f4bdfb18cc5f750f78590e9628f`. CRC, hashes por miembro y espejo permanente verificados. Se guardan siete archivos de símbolos exactos, además deCPP/O/MAP/stub delplugin, IL y disassembly acotado delhelper. SELFnormal delengine exacto; VPK17 y los anteriores intactos. Sin ramas, publicación, cambio de fases o modificaciones enEvolution/2017.

Los contratos heredados17 que exigían ICollection.Count y ausencia de getters concretos se sustituyen explícitamente por los de la candidata18: ausencia de ese despacho enStep,109getters concretos y coincidencia de tipos/orden con los109campos originales. No se oculta una regresión ni se reduce el conjunto de registros esperado. No hubo un build nativo fallido18.

UNTESTED físico18: falta ejecutar la candidata. No se afirma que el fallo sea falta deAOT o deRAM, ni que esté solucionado por compilar o alcanzarFrontEnd enEditor.

## Resultado físico posterior18

OWNER-REPORTED: no se cierra; aparece aviso de espacio insuficiente. VERIFIED en UDP:109tipos/3407registros, COMMIT máscaras153 y callbacksGameDB terminados; proceso y heartbeats continúan. La lecturaCount supera el punto anterior en esta ejecución. El bloqueo nuevo es el guardado tras cerrar el temporal, al ejecutarFile.Move. El código convierte cualquier excepción genérica enDiskSpace; no hay medición que pruebe tarjeta llena. La candidata19adapta IO porstreams basándose enEvolution y conserva el códec deWorld. Menú y persistencia física todavía pendientes.
