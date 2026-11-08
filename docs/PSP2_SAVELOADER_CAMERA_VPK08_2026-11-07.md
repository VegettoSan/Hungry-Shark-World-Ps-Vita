# SaveLoader B2: cámara, borrado y contenido — diagnóstico privado 00.08

Continuación privada autorizada por el propietario, sin aprobar ni cambiar fases.
Solo copia PSP2 Unity2018.2.19f1 y su caché; conservar BuildOptions.None, Mono2x,
memoriaNone,60/VSync1, todos los recursos, offline, guardado y controles.
No se publica/instala automáticamente ni se modifica Unity2017, base2018 o Evolution.

## Resultado físico nuevo y alcance

**OWNER-REPORTED físico00.07:** B1 muestra Loading, permanece normal unos20s sin
congelarse/cerrarse; al avanzar a B2 se congela y vuelve a LiveArea pocos segundos
después. B3 no se alcanzó. Sin foto/log/dump nuevo de00.07.

**VERIFIED código/fixture anterior:** duranteB1/B2 el retorno del loader a
ScreenTracker permanece retenido y la llamada original SaveFacade.Load todavía
no se ha ejecutado. B2 restaura Camera.enabled; AudioListener y Fabric siguen
igual que en B1. **INFERRED:** el disparador depende del recorrido habilitado al
activar la cámara, antes de cargar la partida; priorizar dibujo, materiales y
buffers/clear nativos. No es un stack GXM ni demuestra qué recurso falla.
La música de FrontEnd y la carga original de partida no deben atribuirse a este
ensayo sin evidencia de que se liberó B3.

Loading visible en B1 no demuestra render continuo de SaveLoader/Camera: la misma
imagen FE_Loading_Hawaii también es dependencia de SplashLoader; puede quedar un
frame previo o dibujarse desde otra cámara. La sonda deshabilita las cámaras de
SaveLoader, no todos los gráficos del proceso. Una fotografía no distingue esas
posibilidades.

## Diferencia concreta encontrada

Comparación textual de los componentes Camera de SplashLoader y SaveLoader:
salvo el fileID del propietario, la única diferencia serializada es clearFlags.
Ambas tienen near=-10/far=10, ortográfica, profundidad4, máscaraUI32, viewport
completo, renderingPath heredado, HDR0, allowMSAA1 y targetTexture nula.

| Cámara | clearFlags | Significado |
| --- | --- | --- |
| SplashLoader/Camera | 3 | Depth: borrar profundidad, conservar color. |
| SaveLoader/Camera | 2 | SolidColor: borrar color/profundidad. |

Splash además tiene AntiClearBufferCamera, con clearFlags2, máscara0 y el script
ClearCamera que persiste ese objeto. Por ello no se afirma que todo borrado de
color sea incompatible con PSP2. Se prueba la combinación de la cámara concreta,
su contenido y el orden de cámaras. El nivel de calidad0 observado tiene AA0;
allowMSAA1 no basta para afirmar MSAA activo o cambiar sus ajustes.

SaveLoader referencia MAT_Atlas_GUI, MAT_Atlas_Main, Unlit/Transparent Colored,
FE_Loading_Hawaii, TEX_Atlas_GUI/Main y su LightingData. No se encontró un nuevo
formato incompatible que justifique reconvertir texturas/shaders masivamente.

## Tres perfiles en un solo paquete

En modoB, request/activation y las pausasB1/B2/B3 continúan como00.07. **En B1**
se elige uno de los tres botones R0/R1/R2 antes de habilitar la cámara. No se
cambia perfil duranteB2; cada comparación requiere reiniciar el proceso.
El audio original permanece activo en los tres perfiles.

| Perfil | Único cambio frente a la cámara original habilitada | Pregunta |
| --- | --- | --- |
| R0 Original | Ninguno. | Control equivalente al B2 que falló en00.07. |
| R1 Sin objetos | cullingMask=0; clearFlags SolidColor y demás propiedades originales. | ¿Cierra incluso sin que esta cámara dibuje objetos/NGUI? |
| R2 Depth + UI original | clearFlags=Depth; máscara y contenido originales. | ¿Evita el fallo usando el borrado que tiene la cámara principal de Splash? |

Las máscaras/clearFlags/enabled originales se capturan antes del ensayo y se
restauran al descargar la escena o destruir la sonda. DuranteB2/B3 se conserva
el perfil elegido para no mezclar una segunda modificación al liberar la carga.
Se aplica solo a cámaras SaveLoader y solo enB; no se guardan preferencias.
Los modos0/A conservan sus rutas; R2 es un ensayo, no una corrección permanente.

R1 no evita deserialización, uploads de mallas u otras cámaras/IMGUI, y no es una
prueba global sin gráficos. Su ausencia de UI tampoco prueba que falten recursos:
es el efecto esperado de máscara0 en esa cámara. R2 no prueba fidelidad de un
frame completo solo por no cerrar; hay que observar que la imagen original se
dibuja bien. No se borran atlas, prefabs, música, escenas ni consentimientos.

## Cómo interpretar la comparación

- R1 también cierra enB2: priorizar cámara/clear/contexto/buffers y otras tareas
  concurrentes; no atribuirlo todavía al shader de un widget concreto.
- R1 estable yR0 falla: el contenido dibujado por la cámara pasa a ser candidato
  principal; siguiente aislamiento por drawcall/material, con recursos originales.
- R2 estable yR0 falla: el cambio de clearFlags es candidato localizado; confirmar
  múltiples reinicios, imagen fiel y llegada al menú antes de adoptarlo como parche.
- R2 falla yR1 estable: priorizar geometría/atlas/shader o actualización NGUI, sin
  descartar aún interacción de buffers/estado entre draws.
- Cambia al esperar: considerar timing/concurrencia; no convertir una pausa en
  arreglo permanente ni afirmar que hubo OOM solo por memoria libre total.

Probar primeroR1 enB, esperar10–20s enB1, habilitar cámara y esperar10–20s enB2.
Reiniciar y repetirR2. Conservar R0 como control si se necesita repetir el fallo.
Si B2 permanece estable, continuarB3 y pasosFrontEnd/comunes sin saltar su flujo.
Anotar perfil y última franja/operación si vuelve a cerrar; guardar dump exacto
de00.08 si se genera. Símbolos de00.07 no identifican el AOT00.08.

## Validación y entrega

**VERIFIED compilación/Editor:** principal3742fuentes PSP2 sin UNITY_EDITOR,
0errores/514warnings. Tres procesos35s, Original/R1/R2, namespaces ficticios,
FrontEnd+3DBackground+Sharks,0errores durantePlay,60/VSync1. R1 comprueba máscara0
y SolidColor;R2 máscara32 y Depth. B1/B2 no llaman SaveFacade.Load y B3 libera una
única llamada original. Son pruebas PCbatch con targetPSP2, sin renderGXM nativo;
continuación async desde Splash sin aceptar edad, no validación del flujo legal.
Fixture fuera deAssets y company/product reales restaurados antes del build.

**FAIL de fixture conservado:** la preparación inicial generó un getterCase
recursivo; executeMethod terminó con excepción antes del Play previsto. Se
archivó el log y se corrigió el runner. El intento de detenerlo no encontró una
única instancia pendiente y no detuvo ningún proceso. No fue un fallo Vita ni
se presentó como sesión de juego válida. Las tres sesiones finales son posteriores.

**VERIFIED único build final PSP2:** Succeeded,0errores/596advertencias,
2:57,079,BuildOptions.None/Mono2x,memoriaNone. SELF normal exactoSHA256
`14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`.
58checksstartup/save+32contratos diagnósticos,181marcas.23escenas,480texturas,
424HEVAG,140shaders/245passes PSP2 ConsoleVS/ConsoleFS;15blobs.resource/resS
idénticos byte a byte a00.07. No reconversión de audio ni importación masiva.

**FAIL de integridad de archivos de trabajo/salida, detectado antes de entregar:**
el auditor de fuentes se quedó esperando IO en el sandbox; se detuvo solo su
proceso identificado y se repitió la comprobación local. ProjectSettings.asset
tenía17638bytes cero tanto en caché como en copia privada. Se conservaron los
archivos dañados y se recuperaron desde Before_VPK08.zip conSHA de manifiesto,
cambiando únicamente bundleVersion/psp2AppVersion07→08. No se atribuye una causa
a Unity, al juego o al almacenamiento sin evidencia adicional.

El empaquetador también rechazó un templateXML inválido. La auditoría completa
detectó32salidas copiadas llenas de ceros: plantilla común LiveArea, imágenes
StreamingAssets sin cambios, dos símbolos de soporteSDK y configuración de host.
Se archivaron esos bytes, se recuperaron los recursos desdeAssets originales y
los archivosSDK/plantilla invariables desde la salida07 con hashes fijados por
sus manifiestos. La configuraciónhost queda fuera del VPK. SELF nativo y AOT08
no se reemplazaron ni se parchearon; el player conserva company/product/version
correctos. Después se compararon **todos** los StreamingAssets, sce_module y
sce_sys salvoparam.sfo con07: idénticos. Fabric/helper exactos. No quedan archivos
completamente cero en las dos salidas. Los únicos miembros runtime diferentes
frente a07 son cuatro contenedores serializados, Assembly-CSharp, AOT y SFO.
Estos fallos locales de00.08 no se presentan como causa del cierre físico00.07.

**VERIFIED paquete final después de la recuperación:**
`local-work/HSW_Recovery/Reports/PSP2_VPK08/HSW_Vita_Test_00.08_HGSKW1178.vpk`,
179.778.925bytes/285entradas,SHA256
`c46fba7726f12d9701bf8d3bf47a1ff2dd8a066a8ce3d0d7beec587eca169e54`.
CRC y cada miembro comparados con salida verificada, solo adaptación SFO de
identidad al empaquetar. HGSKW1178/00.08,ATTRIBUTE2=0,cuota8192KiB.
Símbolos exactos deAOT08 preservados; manifiesto regenerado tras recuperar los
dos símbolosSDK invariantes. Los soportes recuperados no son códigoAOT del juego.

**VERIFIED preservación y reversión:** solo3fuentes privadas y2valores de versión
frente a07; assets/metas/audio/Fabric/input/calidad/FPS/offline/save exactos.
Bases2017/2018 funcional verificadas durante preparación; VPK07 conservaSHA.
Manifiestos/ZIPBefore/After y restore_vpk07.py:dry-run de4archivos PASS. Las
configuraciones recuperadas coinciden entre fuente/caché con los2cambios previstos.
Sin modificación de ledger, ramas, paquetes anteriores o publicación.

**UNTESTED físico00.08:** estabilidad deR1/R2, fidelidad deR2, causa nativa exacta,
menú y gameplay originales. No se declara reparación. Probar R1 yR2 en arranques
separados y registrar si B2 se mantiene estable antes de liberar B3.
