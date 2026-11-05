# Entrada e interacción UI — 2026-11-05 UTC

Excepción local autorizada por el propietario para Unity 2017.1.2p4. P00 ACTIVE,
0/13 aprobaciones, ledger intacto, rama main. No se modificaron Evolution,
InputManager, escenas, prefabs, GUID, shaders, servicios JNI o controles PSP2.

## Diagnóstico y reparación

Los menús observados utilizan **NGUI**, incluyendo UICamera, colliders,
UIKeyNavigation, UIButton/UIButtonColor, UISlider y UIScrollView. InControl
alimenta GameInput y sus métodos Universal/Joystick, VirtualPad y los consumidores
originales de acciones. La presencia de UnityEngine.UI como dependencia no convierte
estos menús en un sistema EventSystem/uGUI.

| Archivo privado modificado | Causa y reparación acotada |
| --- | --- |
| UICamera.cs | FrontEnd tiene useTouch=true y useMouse=false. En Windows no llegan toques; se observó RAW_MOUSE sin OnPress/OnClick. La rutina original ProcessFakeTouches no tenía callers en el DLL Android. Se conecta únicamente en Editor cuando no hay toques reales, conservando raycast, coordenadas, thresholds y eventos. Además, el cambio a Controller bloqueaba/ocultaba el cursor; solo en Editor se mantiene libre y visible para poder regresar al mouse. No se llama directamente a acciones del menú. |
| UIButton.cs | El sprite Hover estaba condicionado a TV. En Editor y destinos no Android/iOS se permite también cuando NGUI ya está en ControlScheme.Controller. Se usan las propiedades hoverSprite/hoverSprite2D existentes, sin generar sprites o valores de sustitución. |
| ConsoleObjectDisabler.cs | El primer slider recibe navegación, pero su tweenTarget es un PF_ControllerHighlight que se desactiva fuera de TV. En Editor y destinos no Android/iOS se mantienen los widgets originales referenciados por UIButtonColor.tweenTarget y el objeto original ConsoleScrollShark. Se buscan también targets compartidos entre hermanos dentro de la misma raíz UI. Se respetan sus filtros joypad/remote. No se activan todos los objetos o layouts TV. |
| ConsoleSharkSelect.cs | Su inicialización de enlaces y decoraciones de selección también estaba condicionada a TV. Se habilita esa clase de UI en Editor y destinos no Android/iOS, reutilizando m_topControls, ConsoleNavigationFinder y m_sharkHoverActive/DeActive originales. No se cambia la identidad nativa de plataforma. |
| GameStateMachine.cs | Escape también llega como Action2 en el perfil de teclado. El lector hardware-back de Editor/destinos no móviles respeta y registra ahora el consumo compartido antes de ejecutar el evento original, para que la misma pulsación no active Resume. |
| CustomInputCamera.cs | En Editor y destinos no Android/iOS, la identidad consumida de Action2 incluye dispositivo y UpdateTick del control InControl. El reset de un booleano por frame no bastaba: ManagedUpdates (-900) lee el control antes de InControlManager (-462), y podía volver a ver WasPressed de la muestra anterior. Se conserva el evento consumido hasta que cambia esa muestra, sin debounce temporal o nuevo navegador. |
| UIKeyNavigation.cs | MessageBox conservaba enlaces explícitos y startsSelected, pero su Start solo aplicaba ese foco en TV; el mando seguía apuntando detrás del modal. En Editor y destinos no Android/iOS se ejecuta esa inicialización original para los botones ya marcados y con collider habilitado. Sin cambiar enlaces ni callbacks de compra. |
| OptionsIngamePopup.cs | Al salir de Play, OnDisable intentaba obtener InputControlManager después de su destrucción. En destinos no móviles se comprueba su existencia antes de guardar la sensibilidad Tilt. El cierre normal con manager existente conserva la lógica anterior. |

Se añadió **HSWInputRecoveryChecks.cs** bajo Assets/Editor como observador temporal,
sin generar entradas, navegación o acciones de menú. Registra pulsación/liberación,
raycast recibido, eventos NGUI, dispositivo/perfil, ejes, VirtualPad y snapshots.
Menú manual: `HSW Recovery/Capture input snapshot`. La grabación temporal requiere
una bandera privada y tiene límite de diez minutos por Play. La versión final
termina únicamente la grabación, sin detener la partida; se retira la bandera
al terminar. También se registran cambios de estado y cursor/Time.timeScale.

NativeImplementationEditor no contiene contratos de movimiento, botones o
coordenadas. Se comprobó que conserva su hash de la reparación anterior. No se
revirtieron las reparaciones de servicios, catálogo o shaders.

## Alcance compartido solicitado por el propietario

La última instrucción exige reutilizar estas reparaciones al migrar a Vita.
Los cambios de foco, arte y consumo no quedan limitados a UNITY_EDITOR: se
compilan también cuando el destino no es Android/iOS. La simulación mouse→touch,
el cursor libre de Windows, el observador y NativeImplementationEditor conservan
su alcance Editor. No se incorporaron APIs PSP2, nuevos bindings o un navegador.

**VERIFIED:** el ensamblado principal también compila sin UNITY_EDITOR,
sin UNITY_ANDROID y **sin referencia a UnityEditor.dll**. Las ocho clases
mantienen idéntico flujo IL en la compilación Android respecto a la anterior;
sus ocho metas están preservados. No se modificó el Input Manager.

**UNTESTED en Vita:** ejecución física, perfiles/ejes del player PSP2 y servicios
nativos. El perfil antiguo PlayStationVitaPSM no acredita PSP2. La migración
deberá conectar el hardware y sustituir las dependencias Android que aún sean
necesarias; este trabajo prepara la UI común, no un player Vita funcional.

## Soporte original de controles

| Entrada/acción | Implementación encontrada y alcance |
| --- | --- |
| Touch/mouse Editor | Ruta original NGUI de toque simulado; mouse izquierdo. No hover permanente en modo táctil. Los botones pueden mostrar sus estados originales de pulsación. |
| Teclado | HSXKeyboardMouseInputProfile: WASD/flechas → LeftStick; Return/Space → Action1; Escape → Action2. GameStateMachine también comprueba Escape como hardware back, con sus bloqueos originales. |
| Mando físico | 59 perfiles originales listados, 22 de Windows; detección y hotplug InControl. El Xbox conectado se identifica como Controller (XBOX 360 For Windows) y usa InControl.Xbox360WinProfile. |
| Movimiento/boost | GameInputUniversal y Joystick leen LeftStick X/Y y Action1 hacia VirtualPad; PlayerControl copia/mezcla ese pad mediante la lógica original. A corresponde a Action1 en este perfil. No se modificaron física o parámetros. |
| Confirmar/regresar/pausa | CustomInputCamera, ConsoleButtonClick y ConsoleButtonBinding usan acciones originales y consumo por frame. A→Action1, B→Action2. Hay 54 bindings serializados Action2, incluidos cierres, reanudar y **IngameHUD/Butt_pause**. Se conserva B como pausa original; otras ramas permanecen condicionadas a TV. |
| Navegación UI | UICamera usa Horizontal/Vertical; UIKeyNavigation conserva sus enlaces. ConsoleScroll centra el elemento mediante el eje Horizontal. WorldControllerInput y OptionsContentMap también utilizan Direction. |
| D-Pad | Se observó físicamente una muestra derecha DPad=(1,0), Direction=(1,0), LeftStick=(0,0) y VirtualPad=(0,0). No debe confundirse con LeftStick: las rutas NGUI Horizontal/Vertical y GameInputUniversal no agregan automáticamente D-Pad. No se añadió una asignación nueva. |
| Start/pausa | El perfil expone Start y existe InControl.MenuWasPressed. Se registraron seis pulsaciones y seis liberaciones físicas de Start. No se encontró un binding Start de pausa en los consumidores de producción revisados; detectar el botón no acredita que ejecute pausa. No se añadió una asignación nueva. |

InputManager conserva **224 entradas**, incluidas las **200** consultas
`joystick N analog M` que espera InControl: ninguna ausente o con eje/joyNum
incorrecto. No se copió el Input Manager ni los controles de Evolution. Su
documentación solo orientó la revisión de consumo de eventos y rutas NGUI.

## Evidencia y estado de validación

- **VERIFIED:** compilación mcs C#4 del Editor 2017.1.2p4: principal y herramientas
  Editor sin errores; rama Android aislada sin errores. El flujo de instrucciones
  IL de las clases modificadas para Android se contrasta con la compilación
  anterior. Sus metas conservan los bytes; no se cambió el orden de ejecución.
- **VERIFIED en la instancia existente:** mouse abre Opciones, cambia el slider
  de música y abre About mediante NGUI. Se registraron press true, press false y
  un click por cada clic de esas pruebas. El slider cambió de posición; los
  gestos rápidos del automatizador se muestrearon como clicks y no acreditan
  una pulsación mantenida o arrastre continuo físico.
- **VERIFIED:** Xbox detectado y perfil original cargado. Durante la prueba del
  propietario se registraron stick, Action1/Action2 con liberaciones, cambios
  de foco, navegación de pestañas y retorno de los ejes a cero. La entrada
  alcanza VirtualPad. Esto no certifica todas las acciones en gameplay.
- **OWNER-REPORTED:** gameplay, teclado y aspecto visual funcionaban antes de
  esta tarea. En la primera prueba con Xbox respondían los menús, pero el foco
  seguía invisible en Ajustes y después de Play. Esto condujo a la reparación
  de ConsoleObjectDisabler/ConsoleSharkSelect, posterior a aquella prueba.
- **OWNER-REPORTED tras reparar activaciones:** ya aparece el foco; persistía
  la información del selector. Snapshot nativo: BUTT_GroupInfo en Hover, pero
  su target compartido Highlight inactivo. Se amplió la búsqueda desde ancestros
  a los controladores de la misma raíz UI. El censo encuentra **231 targets**
  originales TV conectados por UIButtonColor/UIButton, sin inventar referencias.
- **OWNER-REPORTED tras el último cambio:** el resaltado de Información ya
  aparece y el propietario entró en gameplay. El último problema de foco
  comunicado queda confirmado visualmente por el propietario.
- **VERIFIED:** snapshot y captura del Game View en Hawaii con IngameHUD,
  Pools, audio y escenas Hawaii low/medium/high cargadas. Durante la partida
  el stick y Action1 llegan a VirtualPad, incluyendo retorno a cero y liberación
  de boost. No se registraron errores/excepciones en esa sesión observada.
- **VERIFIED:** Start y Back físicos también llegan a InControl con sus
  liberaciones. En el intervalo de gameplay registrado hubo 89 pares completos
  de Action1, seis de Start y cuatro de Back; no quedaron pulsaciones de esas
  acciones sin liberar en el punto de comprobación.
- **PENDING:** acción de pausa por Start, navegación
  completa, arrastre mantenido y pausa/reanudar. No se
  acredita un resaltado visible para elementos sin un estado visual original.

El propietario observa una demora inicial ocasional al detectar/activar el mando.
InControl comprueba hotplug cada segundo y selecciona el dispositivo activo según
su actividad; además, la carga bloquea temporalmente la entrada. No se midió una
latencia concreta ni se alteraron esos bloqueos para aparentar respuesta inmediata.

**OWNER-REPORTED en la partida posterior:** el tiburón responde al mando, pero
el mouse queda bloqueado, Start no pausa y Escape abre/cierra en una pulsación.
Esto llevó a las correcciones finales de cursor y consumo, y a identificar la
asignación B del HUD. Su regresión manual se registra separadamente; el PASS
anterior de foco no se presenta como PASS de pausa.

**VERIFIED tras corregir cursor/consumo:** Escape alternó OptionsPopupIngame e
Ingame en frames 1626/1652/1667/1700; B lo hizo en 1797/1827. El mouse activó
Butt_pause en 2293 y abrió la pausa en 2294; Resume también produjo su evento
original y retorno a Ingame. Cursor=None, visible=true durante el control de UI.
**OWNER-REPORTED:** esas tres formas de pausa ya funcionan sin apertura/cierre
inmediatos. No se añadió Start ni se cambió el binding B original.

El propietario encontró después el diálogo de compra del mapa sin mando.
Snapshot: MessageBoxPopup activo con foco aún en un botón de OptionsIngame.
El prefab conserva startsSelected=1 y enlaces izquierda/derecha en sus botones
de confirmar/cancelar. Se restauró su inicialización Editor en UIKeyNavigation;
la compilación final pasa. **OWNER-REPORTED PASS:** navegación del diálogo recuperada tras recargar.
No se confirmó ninguna compra mediante automatización ni se modificaron sus
reglas/callbacks.

## Revisión de otras ventanas similares

Auditoría completa de los **56 prefabs** bajo Resources/gui/popups:
**324 nodos**, **111 marcas de foco inicial**, **0 enlaces de navegación rotos**.
**46 prefabs** tienen su destino inicial original configurado y utilizan la
inicialización compartida restaurada. **31 scripts** llaman al MessageBoxPopup
común, por lo que su reparación no está limitada a la compra del mapa.

También se conserva el fallback de UICamera, filtrando en destinos no móviles
los nodos con collider deshabilitado: un modal podía dejar activo el GameObject
del foco anterior mientras desactivaba su collider. No se añadió otro selector.

Casos clasificados sin inventar enlaces:

- PF_Popup_RewardChest y PF_PopupAddon_OptionsIngameOnboarding tienen navegación
  pero no startsSelected. Conservan fallback/configuración del contenedor y
  requieren prueba de sus estados y animaciones específicos.
- PF_Popup_IAPLoading, PF_Popup_Info_Upgrades y PF_Popup_RewardPreview no incluyen
  UIKeyNavigation; los dos últimos tienen ConsoleButtonBinding de cierre.
  No se acredita navegación visual ausente de sus datos originales.
- Otros cinco prefabs son contenido sin ese conjunto de controles o add-ons.

Esta auditoría estática no es una prueba física de todas las ventanas. El detalle
por prefab/clase/enlace queda en Popup_Navigation_Audit.json privado.

Se preservó un error al salir de Play: `The sfx GroupComponent is null`, desde
ForceField.OnDestroy → AudioManager. También apareció un intento de destruir
un Transform de PF_Water_Wake_S al salir. Ocurren en frame 0 al detener la sesión.
**INFERRED:** orden de destrucción en el caso de audio; el Transform requiere
diagnóstico separado. No se silenciaron ni repararon esos sistemas ajenos a UI.
Otro cierre registró una NullReferenceException en OptionsIngamePopup.OnDisable
al obtener InputControlManager ya destruido: ese acceso de UI sí recibió la
comprobación acotada de existencia. Compila; falta repetir ese cierre final en
Editor para acreditar su regresión, sin atribuirle la reparación del Transform.

La primera versión del observador detuvo una sesión al vencer sus diez minutos.
Se reconoció la interferencia y se cambió ese límite a fin de grabación solamente;
la versión final no detiene la partida al vencer el plazo.

Al entregar se retiraron la bandera de grabación y el archivo de comandos.
No quedan pruebas encoladas. Se guardaron checkpoints privados, incluido
InputRepair01_FinalCheckpoint.zip, CRC verificado, con las ocho clases
antes/después, metas, observador y evidencia.
Manifest y recibo de hashes están en la misma carpeta; no se publicaron fuentes.

La primera versión del observador intentaba leer un miembro no público de
UICamera y falló CS1061; se retiró esa lectura y la compilación final pasa.
Una inspección YAML falló por la codificación Windows predeterminada y se
repitió explícitamente como UTF-8. No se cambiaron assets para evitar esos fallos.

Se utilizó la única instancia abierta; Escape detuvo el control remoto durante
la última compilación. No se enviaron más acciones UI; la última validación se
entregó al propietario. Evidencia y copias Before privadas:
`local-work/HSW_Recovery/Reports/InputRepair01`. Proyecto:
`local-work/HSW_Recovery/HSW290_Unity2017_ReadyToOpen`.

Procedencia y herramientas: APK SHA-256
`6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d`, OBB
`c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72`;
DLL originales preservados, Python 3.14.4, dnSpyEx 6.6.0/dnlib, Mono/mcs y APIs
del Editor 2017.1.2p4. Ninguna descarga o investigación externa.

Para cargar la revisión final: fuera de Play, Assets/Refresh (Ctrl+R), permitir
la recompilación y entrar desde SplashLoader. Comprobar
Opciones (los tres sliders), selector de tiburones, A/B, D-Pad/stick, mouse tras
mando y viceversa. Iniciar una partida, verificar boost y pausa/reanudar con
las acciones que realmente estén asignadas. No convertir una respuesta parcial
del mando en una afirmación de navegación completa o futura compatibilidad Vita.
