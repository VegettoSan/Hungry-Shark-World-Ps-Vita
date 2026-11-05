# Primera reparación de compilación — 2026-11-05 UTC

**VERIFIED: 0 errores C# en Unity 2017.1.2p4**, en la sesión del propietario que
ya estaba abierta. No se abrió una segunda instancia ni se ejecutó gameplay.
La consola conserva dos assertions nativas anteriores, distintas de errores C#.

El propietario autorizó directamente corregir la compilación del proyecto privado
recuperado. Esta tarea es una excepción acotada de reparación, no aprobación de
P00/P01/P02. Se mantiene `main`, ledger intacto, P00 ACTIVE, 0/13 aprobaciones.
Evolution no se modificó; no hay adaptación Vita, optimización ni VPK.

## Diagnóstico y cambios

Se preservó el Editor.log inicial y la última configuración real de compilación
generada por Unity. El log contenía **39 errores C# por compilación**, repetidos
en varios intentos; 35 líneas de diagnóstico distintas. Todos correspondían a
estos seis archivos bajo `Assets/Scripts/Assembly-CSharp/`:

| Archivo | Causa y reparación |
| --- | --- |
| ByteReader.cs | CS0165 en un bucle decompilado do/continue. Se reconstruyeron las ramas del IL: leer el byte antes de comparar LF/CR y conservar el incremento al alcanzar el final del buffer. No se añadió un valor inicial arbitrario. |
| Dreamteck/Splines/IO/CSV.cs | CS0165 en asignaciones de array/índice compactadas. Se restauraron asignaciones compuestas válidas; AddFloat conserva el Single.ToString dependiente de cultura que muestra el IL original. |
| EventDispatcher.cs | CS0165 en temporales de diccionario/clave. Ahora se capturan antes de leer, combinar o retirar el delegate y escribir el resultado. Se conserva orden y multiplicidad de listeners. |
| FGOL/Analytics/AnalyticsFacade.cs | Mismo patrón CS0165. Se conserva el control de listeners duplicados y el flujo de registro/desregistro. |
| XMLParser.cs | CS0165 en el receptor temporal del indexador. Se asigna el nodo antes de leer/concatenar/escribir su texto; no se alteran las ramas de parsing. |
| PlatformSupport/Collections/ObjectModel/ObservableDictionary.cs | CS0079: lecturas, referencias e invocaciones apuntaban al evento explícito. Se corrigieron 18 usos para emplear sus campos privados ya existentes. Se mantienen eventos públicos, interfaces, add/remove, CompareExchange y notificaciones. |

Se consultó el IL de **Assembly-CSharp.dll original** y las notas técnicas de
Evolution, sin copiar implementaciones entre juegos. No se añadieron DLL del
juego a Assets ni tipos duplicados. Los seis `.meta` conservan sus bytes; no se
modificaron escenas, prefabs o configuraciones para corregir la compilación.

## Validación observada

- Compilador **mcs de Unity 2017.1.2p4**, C#4, mismas referencias/defines del
  response file de la sesión abierta: **exit 0**, sin errores. Solo se cambió la
  ruta de salida a un directorio de evidencia separado, sin escribir en Library.
- Se activó la ventana existente mediante control de UI local.
  Unity recompiló automáticamente: `Compilation succeeded - 491 warning(s)`,
  `compilationhadfailure: False`, ninguna línea nueva `error CS`.
- La sesión generó `Library/ScriptAssemblies/Assembly-CSharp.dll` y
  `Assembly-CSharp-Editor.dll`. El firstpass ya compilaba antes de los cambios.
- **1.645 casos diferenciales** en procesos Mono separados contra el ensamblado
  original y el reparado: 1.570 de ByteReader, 10 XML, 9 títulos CSV, 54 números
  CSV (en-US/es-CO/fr-FR), un escenario múltiple de EventDispatcher y otro de
  ObservableDictionary. Mismo digest de observaciones, **0 excepciones** del
  ensayo. No prueban todo el juego ni cubren ejecución de AnalyticsFacade.

Las herramientas son las ya existentes: Python 3.14.4, dnSpyEx 6.6.0/dnlib y
Mono/mcs incluidos en 2017.1.2p4. No hubo investigación o descarga externa.
Entradas originales de referencia:

- APK: `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d`.
- OBB: `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72`.

## Assertions y advertencias pendientes

**VERIFIED:** las dos assertions `m_AssetToPrefab.empty()` ya estaban en el log
inicial. El origen registrado es **Runtime/Network/NetworkManager.cpp:162**; una
ocurre expresamente al importar `ProjectSettings/NetworkManager.asset`.
Ese archivo contiene **1.038 entradas** en `m_AssetToPrefab`. No existe un stack
trace completo en el log. **INFERRED:** el registro serializado de prefabs del
player/exportador entra en conflicto con la expectativa del gestor nativo del
Editor. No es evidencia de GUID corruptos o prefabs ausentes. La recompilación
posterior no añadió ninguna assertion y finalizó correctamente.

**Pendiente:** confirmar la causa exacta y su corrección en un ensayo separado.
Se conserva NetworkManager.asset íntegro; no se vació el registro, borraron
prefabs, regeneraron GUID o eliminaron cachés. Las dos entradas históricas siguen
visibles en Console; no se limpiaron para aparentar cero mensajes rojos.

El ensamblado principal completo produjo **491 advertencias**, más que las
visibles cuando la compilación fallaba a mitad. No se suprimieron warnings:

| Código | Cantidad principal | Clasificación |
| --- | ---: | --- |
| CS0414 / CS0649 / CS0219 | 166 / 39 / 95 | Campos o locales no usados/asignados; algunos campos pueden rellenarse mediante serialización/reflexión. |
| CS0252 | 164 | Comparaciones potenciales de referencia; revisar contra IL antes de cambiar semántica de igualdad. |
| CS0618 | 16 | APIs obsoletas aún disponibles en este motor. |
| CS1717 | 6 | Autoasignaciones en MeshCombiner/UIAttributeGauge: revisión de fidelidad pendiente, sin inferir qué variable pretendía el desarrollador. |
| CS0429 / CS0162 | 2 / 1 | Expresiones/código inalcanzable; pendientes de revisión dirigida si afectan ejecución. |
| CS0660 / CS0661 | 1 / 1 | Operadores de igualdad sin Equals/GetHashCode en InputControlState. |

La consola observada mostraba **596 advertencias acumuladas** y dos assertions
históricas; ese contador incluye mensajes de otras etapas/importación. No es el
total del ensamblado principal. Los avisos de shaders Android y de extensiones
nativas de build siguen fuera de esta reparación de C#.

## Evidencia privada y continuación

Proyecto: `local-work/HSW_Recovery/HSW290_Unity2017_ReadyToOpen`.
Evidencia: `local-work/HSW_Recovery/Reports/CompileRepair01/`:
Before (seis scripts/metas), hashes/diff, IL original, Editor_Before/After,
Editor_Recompile_Only, response files, salida de mcs y contratos diferenciales.
La exportación intacta y el ZIP PreEditor anteriores no se modificaron.

Los primeros intentos también se conservaron: un contador de precondición de la
automatización esperaba 14 accesos de CollectionChanged en vez de los 12 reales;
se corrigió y se reanudó desde los backups, sin sobreescribirlos. Ejecutar Mono
antiguo dentro del sandbox falló con WinError 623; la ejecución local autorizada
del mismo compilador terminó correctamente. Ninguno se atribuye a errores del juego.

La compilación ya está comprobada en el Editor. Siguiente comprobación del
propietario: revisar la Console y abrir SplashLoader. Importación visual,
comportamiento, servicios Android, guardado y gameplay aún **UNTESTED**; no se
acredita un proyecto completamente funcional a partir de este PASS de C#.
