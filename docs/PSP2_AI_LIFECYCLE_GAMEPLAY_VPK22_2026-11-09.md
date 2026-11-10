# VPK 22 — reparación funcional de IA y validación de entrada a gameplay

## Evidencia nueva de VPK21

5084mensajes UDP coinciden exactamente con el respaldo de Vita. No faltan secuencias ni hay excepción registrada o nuevo dump aportado. Cámara y pools anteriores completan; se carga `Enemies/PF_Crab_Large` y el último BEFORE corresponde a inicializar ese pool, tipo3/fila11/tamaño1. No se recibió su DONE. Los snapshots marcan LPDDR82837504 antes; el último watcher informa memRc0/kernelMain125829120. No hay un OOM registrado. Estos datos no prueban la instrucción fallida ni permiten acusar al prefab de corrupción; el watcher también puede observar memoria liberada durante terminación.

La creación original del cangrejo pasó en Editor, con el código21, GameDB y la base de IA originales. El cierre específico PSP2 sigue sin reproducirse localmente. Se inspeccionaron prefab/componentes, instanciación, cache de componentes, asignación de IA y de máquinas/estados, además de la ruta posterior de spawners, jugador, callbacks de carga, primera confirmación, intro/HUD y GameSessionStart. No se cambian datos para superar el fallo.

La medición de21 registra la primera cámara de menú a73,475s, frente a98,176s en20. Las ventanas de copias de guardado antes de esa frontera bajan de39,226s a12,152s. Son capturas reales de sesiones distintas, con guardados/estado potencialmente diferentes y overhead de observación; no son un benchmark controlado ni una promesa de tiempos futuros. Se conserva el búfer64KiB de21.

## Defectos reproducidos y correcciones mínimas

La prueba del código anterior dejó cuatro resultados comprobados:

1. `AIEntityData` es un struct. El getter del diccionario devolvía una copia; GetAISM cargaba y asignaba m_aism solo en esa copia. El recurso retornaba, pero la entrada propietaria seguía sin cache, de modo que Destroy tampoco encontraba ese asset para liberarlo. Se persiste la copia modificada en el mismo diccionario, conservando clave y referencia. No se inventa una caché separada.
2. OnLoadTransition borraba las transiciones normales y conservaba las de cualquier estado. Repetir la reconstrucción del mismo AICrab lanzaba clave duplicada por entradas viejas. Ahora vacía ambos mapas antes de ejecutar los Add originales. Los duplicados reales dentro del mismo input siguen lanzando ArgumentException.
3. AssignStateMachine podía recibir el mismo asset ya configurado y dejar m_stateMachineInstance nulo. Ahora crea la instancia si falta, aun siendo el mismo asset. Si ya existe una instancia sana del mismo asset, se conserva, sin reinitializarla ni resetear IA.
4. Al retirar un template de estado sin instancias de componentes, Remove intentaba recorrer un array nulo. El template no tiene callbacks de instancia que ejecutar; se retorna en ese caso. Los componentes runtime inicializados mantienen sus callbacks originales. Este ajuste permite la liberación de templates que ahora sí conserva la caché corregida.

En PSP2 se sustituyen dos búsquedas List.Find por recorridos directos: datos de IA y componentes compartidos por tipo exacto. Eliminan predicados/closures temporales y el despacho asociado, conservando primer match, orden, identidad y resultado nulo. Esto no demuestra un fallo de AOT en21. No se cambian backend, opciones/budgets de trampolines, engine, datos, estadísticas ni número/tamaño de pools.

El diagnóstico se limita al scope de creación del cangrejo: antes/después de Instantiate, EntityInstance, CacheComponents, SetAIControl, lookup/carga de IA, clone de máquina y clone/inicialización de estados/componentes. Preserva la activación original de la instancia; no se crea inactiva para saltar Awake/OnEnable. El presupuesto es128detalles por proceso y no requiere botones. Una salida por finally se etiqueta LEAVE, no éxito; DONE solo se publica al retornar correctamente.

## Salida nativa sin crash visible

Se inspeccionaron los símbolos/assembly del mono-vita exacto de21. g_logv contiene una ruta fatal que llama a exit(-1), después de imprimir/vaciar stdio. Esto demuestra que existe un mecanismo capaz de terminar fuera de los callbacks C# sin un crash de memoria. **No demuestra que se ejecutara en esta prueba**, ni que se agotaran trampolines. Se vieron pools AOT finitos y el texto de agotamiento, pero no se midió su uso en hardware; no se cambian sus presupuestos a ciegas.

El plugin22 registra un observador normal de libc con atexit. No llama a exit/abort ni altera la máscara fatal, no engancha Mono, no modifica handlers de señales y no modifica el reproductor. Escribe un registro acotado y el último paquete en `ux0:data/HSW_Vita/vita_native_exit.log`, con intento UDP no bloqueante si el transporte continúa activo. No consulta Unity/Mono ni objetos gestionados. La API no proporciona el código de salida; se indica expresamente. Puede ejecutarse en una salida normal, y puede no ejecutarse si la terminación usa otra ruta; se interpreta junto con QUIT/CLOSE, watcher y dumps. El handler de coredump previo permanece separado, escribiendo user-data únicamente. El receptor/analizador conserva las sesiones anteriores y reconoce el registro de salida separado, sin falsificar secuencias del emisor principal.

## Validación realizada

Antes de modificar: cangrejo original crea sin errores en Editor; se reproducen las cuatro condiciones defectuosas anteriores. Después:1313comparaciones sobre160entidades de IA conservan primer match/referencia/tipo; se comprueban ausencia de doble inicialización sana, compartición de componentes, rechazo de duplicados reales y descarga/limpieza de la caché.

Prueba aislada de arranque y gameplay en Unity2018.2.19f1:109tipos/3407registros, un load/evento/completado, FrontEnd/escenas comunes, cangrejo, transición original de limpieza, MenuToIngame y escenas de Hawái, pools originales, spawners, jugador y callbacks. La fixture configura un componente de transición con los mismos campos del original de LevelSelect, empezando desde FrontEnd; no valida todos los clics de selección. La confirmación de primera partida se invoca mediante su método original una vez que su callback está preparado; el player no contiene esa automatización. Se verifica Hawaii_low cargada, gamePlayer/activePlayer válidos, App.InGame verdadero y más de8s de actualizaciones, con0errores. No es prueba física de input, GPU o estabilidad prolongada.

5547paquetes de la sesión final del Editor consecutivos, sin huecos; el único error de transporte capturado es el selftest deliberado del callback de hilo. Se conservaron los resultados fallidos de fixture: string de aislamiento anterior, carga manual de Pools con root aún inactivo y un parche de fixture que leyó UTF8 con encoding incorrecto. Se corrigió solo el test y se usó la ruta de carga original; no se parcheó gameplay para satisfacer una escena artificial.

Build nativo único: Succeeded,0errores,492warnings,03:19.6313386,Mono2x/BuildOptions.None.58contratos generales+100de diagnóstico,282marcadores.49archivos serializados y15bancos byte idénticos;23escenas. IL/campos GameData, índice, SaveData, SaveGameManager y SaveIO exactos21. SELF normal byte idéntico; sin Development/Razor.60cap/VSync1,VeryLow,ExpandBy109MB=3/ATTRIBUTE2=0c,IO64KiB,controles,audio/offline y presupuesto GameDB2ms conservados. No se reconvierten recursos.14archivos existentes,0añadidos; ProjectSettings solo cambia dos versiones. Metadatos derivados de Unity restaurados a bytes/GUID canónicos; fuente privada/caché coinciden. Sin cambios a Evolution,2017,VPKanteriores,fases,ramas o publicación.

## Entrega y prueba física necesaria

`HSW_Vita_Test_00.22_HGSKW1178.vpk`,179829845bytes/288entradas. SHA256 `508a441ee67206cfc6855697f7e5c72ca71075375e8dfdc17d02d5a90ac45e4c`. CRC y hashes por miembro/espejos correctos. Se conservan VPK22_ExactSymbols.zip (7archivos), VPK22_NativePluginSymbols.zip, manifiestos, pruebas anteriores y rollback21 guardado/dry-run. Material propietario/SDK y trazas completas permanecen privados.

El receptor18194 permanece abierto. Instalar22 sobre el título actual sin borrar la partida, entrar con el mismo tiburón a Hawái y confirmar la pantalla original cuando esté preparada. Informar si entra a gameplay o dónde cierra. Copiar después vita_live.log y vita_live_watch.log de ux0:data/HSW_Vita; si existe, añadir vita_native_exit.log y cualquier .psp2dmp nuevo. Conservar VPK y ambos ZIP de símbolos22 exactos. No borrar sesiones anteriores.

**VERIFIED:** reparaciones funcionales de lifecycle/cache y equivalencia local; entrada a gameplay del Editor. **UNTESTED físico22:** superación del cierre nativo, comportamiento GPU/input, estabilidad, siguientes partidas/niveles y persistencia fría. No se declara demostrada la causa del cierre21 ni solucionado en Vita antes de esa prueba.


## Resultado físico posterior de 22

Sesión `368167b6ad62`: 5172 mensajes principales consecutivos; cuatro pools completos, incluido CrabLarge; último BEFORE spawner. Se recibió observador `NATIVE_LIBC_EXIT`, sin código o razón disponibles. No excepción/OOM/quit ni dump nuevo proporcionado. **FAIL físico:** cierre antes de gameplay; reparaciones IA conservadas, causa posterior pendiente. [Captura nativa 23](PSP2_NATIVE_EXIT_CAPTURE_VPK23_2026-11-09.md).
