# Unity 2018 y preparación PSP2 — 2026-11-05 UTC

Excepción local explícita del propietario para migración, proveedores offline y
mapeo de entrada. Rama main; P00 ACTIVE, 0/13 aprobaciones. Sin modificación de
Evolution, copia Unity 2017, ledger, empaquetado o publicación.

## Resultado y ubicación privada

Proyecto: `local-work/HSW_Recovery/HSW290_Unity2018_ReadyToOpen`, Unity **2018.2.19f1**.
Evidencia: `local-work/HSW_Recovery/Reports/Migration2018_01` (ignorada).
La copia funcional Unity 2017 conserva los SHA-256 de sus **20.869 archivos** de
Assets/ProjectSettings; ningún archivo nuevo allí. InputManager conserva sus
**224 entradas**. Se mantienen las 23 escenas originales en Build Settings.

Se reutilizan los originales ya verificados, sin repetir extracción:
APK `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d`;
OBB `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72`.

## Reparaciones de compilación

- UnityUtil: retirar OSXDashboardPlayer del conjunto de plataformas PC; ninguna
  plataforma vigente lo reemplaza semánticamente.
- MathUtil: conservar la multiplicación de quaternions en un temporal antes de
  ToAngleAxis; corrección del código decompilado para el compilador 2018.
- MemDump: conservar las identidades serializadas ATC 35/36 y su diagnóstico de
  4/8 bits por píxel mediante casts; no convertir texturas ni sustituir compresión.

**VERIFIED:** compilación con Mono/mcs instalados de Unity 2018, perfil original
.NET 2.0 Subset/C#4, sin cambiar runtime/API compatibility: firstpass 118 fuentes,
principal 3.737, Editor 4; **0 errores**. Advertencias: 81/519/0 en la comprobación
Editor, principalmente comparaciones por referencia, campos/variables sin usar,
APIs obsoletas y campos no asignados. No se hizo limpieza masiva.
La instancia existente del Editor recompila; no se abrió una segunda instancia.

## Servicios offline PSP2

Las selecciones específicas del player utilizan `UNITY_PSP2 && !UNITY_EDITOR`:

| Capa | Preparación y contrato |
| --- | --- |
| NativeBinding | Nuevo NativeImplementationPSP2 sin JNI. Rutas reales Application, SystemInfo y memoria libre del módulo instalado. No se simula identidad TV. Diálogos nativos cancelan; el NGUI del juego permanece. Credenciales de respaldo solo en sesión, sin inventar backup cloud. |
| Ads, AppsFlyer y Deep Links | Proveedores deshabilitados/dummy existentes; ninguna recompensa o enlace ficticio. |
| Billing | BillingFacadePSP2 informa NotSupported, completa Init/Fetch con false y Purchase con ErrorNoExternalDialogue; no concede compras ni crea precios. |
| Game Services y Social | Interfaces Null originales, autenticación false y callbacks completos; conserva registro de guardado local. Guardas para callbacks opcionales nulos de NullSocialSystem. |
| Notificaciones | NotificationsNull, conservando registro del subsistema de guardado. No crea nuevas programaciones con recompensas ni procesa entregas inexistentes; historial conservado y callback de comprobación completado. |
| Analytics y cross-promotion | Conserva contadores/local save y eventos del juego; no inicia proveedores AppsFlyer/Facebook/Flurry/DNA ni el manager cross-promo Android. |
| FGOL.Server.Request | HTTP/HTTPS completa al siguiente paso de coroutine con error de conexión no disponible; sin construir el cliente remoto. Archivos/rutas no HTTP conservan su flujo. |
| AppstoreHandler | Evita JNI PSP2 y completa el evento original de cierre de tienda, sin compra. |
| GameValidator | Verificación de firma de certificado solo en Android real; conserva las comprobaciones locales de guardado y no borra flags existentes. |
| PluginImporter | Facebook.Unity.Android.dll excluido únicamente de PSP2; archivo y GUID conservados. Dependencias compartidas permanecen. |

La selección Editor conserva los proveedores de la reparación anterior. En
particular, el proveedor de compras simulado original de Editor **no** es el
proveedor PSP2. No se cambiaron precios, monedas, desbloqueos o formatos de save.
Ubimobile/DNA, UbiServices y WebView Android permanecen como código conservado,
fuera de las rutas PSP2 de los proveedores deshabilitados; esto no prueba todas
las rutas futuras de SDK por invocación directa.

**VERIFIED:** 27 aserciones de contratos/entrada sobre las DLL privadas compiladas
con símbolos PSP2: callbacks de error una sola vez, sin autenticación/compra
exitosa, request diferido, notificaciones sin mutación de recompensas, perfil y
pulsación/hold/release/neutral del pipeline original. El runner usa Mono de host
(fallback runtime v4 para ejecutar la prueba), **no ejecuta un player PSP2**;
la compilación del juego conserva su perfil original.

## Entrada y módulo PSP2

Se verificó el módulo local 2018.2.19f1, metadatos de plataforma, ensamblados
UnityEngine.PSVita y plantillas Mono/IL2CPP. La documentación instalada del módulo
confirma la ruta estándar Unity Input, ejes/botones y pantalla táctil frontal.
No se copiaron índices de Evolution/Halo.

HSWPSP2InputProfile se registra primero exclusivamente en player PSP2: 60 perfiles
allí, **59 originales intactos** en Editor. Se conservan InControl → GameInput →
VirtualPad, UICamera/NGUI, UIKeyNavigation y los indicadores originales reparados.

| Control candidato | Acción original |
| --- | --- |
| Stick izquierdo, ejes 0/1 | Movimiento analógico original; signo Y y zona muerta pendientes de hardware |
| D-Pad, botones 8/9/10/11 | Direction de InControl al delegado de ejes NGUI y carruseles originales |
| Cross, botón 0 | Action1: confirmar y acción original de gameplay |
| Circle, botón 1 | Action2: retroceso/pausa original |
| Start, botón 7 | Hardware-back original solo en gameplay/pausa, con consumo compartido |
| R, botón 5 | RightBumper incorporado a boost únicamente en GameInput de gameplay |
| L, Square, Triangle | Reservados; no se inventaron funciones |
| Touch frontal | Ruta táctil original, pendiente de dispositivo |

**VERIFIED por prueba lógica:** D-Pad llega al eje NGUI, Start es distinto de
Action1/2, hold no repite WasPressed, boost se libera y stick vuelve a neutral.
**UNTESTED:** nombres de joystick, índices físicos efectivos, signo Y/deadzone,
intercambio touch/mando, pausa contextual y foco de cada modal en Vita. No hay
nuevo controlador de tiburón, navegador UI ni spoof global de Android TV.

## Ejecución y recursos

**VERIFIED en Editor 2018:** gameplay Hawaii observado en la única instancia,
entrada Xbox y ausencia de cascada de excepciones durante ese intervalo.
**OWNER-REPORTED:** animaciones/audio/pausa sin problemas visibles de gameplay.
No se afirma cobertura visual de todas las escenas.
Prueba final automática de arranque: **25,47 segundos/645 frames, 0 errores**;
SplashLoader → BootLoader/SaveLoader → FrontEnd/3DBackground/Sharks.
La sesión terminó fuera de Play y la consola final mostró 0 errores. Esto no
repite la prueba de salida después de gameplay con partículas.
La API PluginImporter confirmó Any=true, excludePSP2=true y excludeAndroid=false;
la primera edición YAML aislada no fue suficiente y se corrigió mediante esa API.

Auditoría nativa DX11: **97 shaders, 428 materiales, 0 shaders ausentes/no soportados,
374 pases probados sin fallo; 4/4 pruebas de píxel de UI correctas**. No se
sustituyeron shaders ni materiales. Un material fue reserializado por Unity con
el cambio de nombre de campo nulo m_PrefabParentObject → m_CorrespondingSourceObject;
sus propiedades visuales y GUID permanecen. No demuestra compilación de shaders
para la GPU Vita.

Comprobación YAML: 66.107 referencias; sin nuevos GUID duplicados, metas ausentes,
fileIDs locales rotos, scripts faltantes o escenas de build rotas. Pendientes
heredados: referencia de textura interna Font Material y dos scripts nulos en
LevelSelect/Hawaii_low. El módulo añadió sus ejemplos uGUI InputModules; no se
conectaron a los menús NGUI ni al orden original de escenas del juego.

Los observadores Editor se redirigen a evidencia de esta migración para evitar
sobrescribir informes 2017. Grabación/automatización temporal se desactiva al
terminar. Respaldo privado CRC de 16 archivos de datos locales (2.209.830 bytes),
realizado después de la prueba del propietario; no es una prueba de cold save/load.
Ambas copias usan actualmente la misma identidad/ruta de datos del juego en
Windows; no ejecutar simultáneamente sobre esa partida.

## Pendientes reales

- El error antiguo al salir de Play intenta destruir Transform de PF_Water_Wake_S.
  Sin stack C# suficiente, no se hizo una modificación especulativa del efecto.
- Se identificó fuga CullingGroup al detener Play. ParticleCullingManager ya
  disponía de DeInit/Dispose; ahora también se llama cuando desaparece el último
  componente. Compila; falta repetir cierre tras gameplay para confirmar ausencia.
- Memoria PSS/heap Android, espacio libre de disco y servicios de diálogo nativo
  no tienen equivalencia verificada; métricas desconocidas devuelven cero, no
  capacidad inventada. Descargas remotas y contenido no recuperado no quedan
  resueltos por esta preparación offline.
- Catálogo incompleto, shader provisional y limitaciones ya documentadas en la
  recuperación 2017 siguen vigentes. No se han reparado con placeholders nuevos.
- Cold save/load completo, equivalencia de todas las escenas, ruta writable/save
  en Vita, exportación de recursos al destino, shader compiler PSP2 y player en
  hardware quedan **UNTESTED**. Sin VPK/build publicado ni afirmación de port jugable.

## Continuación exacta

Abrir únicamente la copia Unity2018 con 2018.2.19f1, esperar compilación, ejecutar
SplashLoader y comprobar menú/selector, mouse/Xbox, boost, pausa/reanudar y salida
de Play. Repetir inicio en frío y verificar progreso local sin alterar economía.
Luego comprobar en hardware el perfil candidato, almacenamiento y recursos del
player PSP2 antes de cualquier publicación. Mantener la copia Unity2017 como
referencia independiente; no actualizar sus assets con el Editor 2018.

Evidencia privada: Before/Staged, Compile/editor y Compile/psp2, ContractProbe.log,
ShaderProbe2018.json, UI_RenderChecks.json, StaticReferences2018.json,
Unity2017_Protection_Result.json, manifiestos y checkpoint de cambios. Los fallos
intermedios de sintaxis/enums y del runner/probe se preservan, sin convertirlos en PASS.
