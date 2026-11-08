# SaveLoader: primer render y frontera de carga de partida — 00.07 privado

Continuación del encargo del propietario tras el FAIL físico de los tres modos
00.06 y tres fotos nuevas de B. Investigación/diagnóstico privado exclusivamente
en la copia PSP2 Unity2018.2.19f1 y su caché; sin cambio de fases, rama, Unity2017,
base funcional2018 o Evolution. P00 ACTIVE,0/13 aprobaciones. No hay publicación
ni instalación automática. No se atribuye todavía una causa nativa al cierre.

## Lo que ahora muestran las fotos

**VERIFIED visual:** las tres capturas corresponden a VPK6/00.06 y modoB.

| Foto | Evidencia visible |
| --- | --- |
| 1 | CURRENT STATE SaveLoader; última completada scene BootLoader Single; botón `Avanzar request: screen SaveLoader`. FabricManager.Awake completado; todavía esperando la petición de SaveLoader. La espera de46s es una pausa elegida por el diagnóstico. |
| 2 | `WAIT scene activation screen SaveLoader`; última completada `scene data >=0.9 screen SaveLoader`; botón para avanzar activación. Los datos alcanzan el umbral previo a activación. |
| 3 | Imagen Loading visible; CURRENT/última completada/GFX `DONE first camera CPU submission SaveLoader/Camera`, edad0,1s. No es un recurso llamado SaveCamera ni una prueba de fallo antes de dibujar toda la pantalla. |

Los valores visibles, sin confundir disponibilidad total con bloque mayor libre:

| Foto | LPDDR bytes | CDRAM bytes | PHYSCONT bytes | Managed bytes |
| --- | ---: | ---: | ---: | ---: |
| 1 | 51380224 | 89532064 | 27262976 | 10420224 |
| 2 | 47185920 | 85337760 | 27262976 | 10944512 |
| 3 | 51380224 | 84813472 | 27262976 | 11862016 |

En foto3 equivalen aproximadamente a49/80,9/26MiB libres. No se demuestra OOM ni se
descarta fragmentación. Las tres muestran persistentOK, sin excepción visible y
con FabricManager.Awake PF_Audio_Manager como última marca de audio. Ninguna
muestra petición FrontEnd o reproducción de hsx_mus_frontend. Esto acota lo
fotografiado; no prueba que esas operaciones no ocurrieran después.

**OWNER-REPORTED:** el proceso acaba volviendo a LiveArea en0/A/B.
**INFERRED:** si foto3 corresponde al último instante previo al cierre, el
primer frame de SaveLoader y su entorno inmediato son candidatos prioritarios.
No sabemos si hubo marcas posteriores entre la foto y el cierre. La devolución
de onPostRender es una frontera CPU; no acredita terminación del trabajador
gráfico/GPU ni un frame posterior estable. Tampoco prueba que SaveFacade.Load
ya se haya ejecutado. El contador Update/s visible procede del intervalo previo.

Fotos exactas y hashes se conservan únicamente en Reports/PSP2_VPK07, junto con
VPK06_PhotoEvidence.json. No se recibió un dump o TTY de esa ejecución.

## Prueba siguiente: separar render y carga de partida

00.07 amplía únicamente B. Los modos0/A conservan sus recorridos00.06;
se mantiene audio original activo durante toda la pruebaB. Tras request y
activation de SaveLoader aparecen dos pausas nuevas, independientes de los
valores que pueda retener CURRENT/GFX:

1. **B1 — SaveLoader activado, cámara retenida.** sceneLoaded captura las cámaras
   de esa escena y conserva sus valores enabled antes de deshabilitarlas
   temporalmente. Awake/OnEnable de la escena ya han sucedido. Se deja pendiente
   el retorno del cargador al ScreenTracker: su LoadTracker todavía no se marca
   terminado y OnStateLoaded no habilita la carga de partida. La franja fija
   indica B1 y el botón permite habilitar la cámara. Esperar10–15s antes de pulsar.
2. **B2 — Cámara original habilitada, partida todavía pendiente.** Se restauran
   exactamente los enabled capturados. Continúan pendientes el tracker y la
   carga de partida. Se observa el primer render y muestras acotadas de frames
   CPU; esperar10–15s. Solo el botón siguiente libera el recorrido original.
3. **B3 — Flujo original liberado.** Termina el loader, continúan ScreenRoot,
   eventos, OnStateLoaded, carga de partida y transición originales. No se finge
   resultado de guardado ni se omiten suscriptores. FrontEnd y comunes continúan
   usando los pasos originales de B.

Esta prueba no cambia escenas, atlas, materiales, shaders, geometría, texturas,
AudioClips, importadores, opciones de audio, calidad o player. Cámara y espera
solo cambian temporalmente en modoB, con restauración del estado original.
No se desactiva audio y gráficos simultáneamente. No se modifica Time.timeScale
ni se crean RenderTextures/capturas diagnósticas. El overlay IMGUI sigue activo.

**Límites:** B1 no evita deserialización nativa ni Awake/OnEnable, creación de
mallas, uploads NGUI u operaciones de otras cámaras. Por tanto, fallar en B1 no
descarta todos los recursos gráficos. Llegar a B2 y cerrar al habilitar la cámara
repetidamente, antes de B3, aporta evidencia del recorrido de render con la carga
de partida todavía retenida; no identifica por sí solo shader, buffer o hilo.
Un dump exacto sigue siendo necesario para atribución nativa concluyente.

## Lectura de resultados físicos

| Resultado | Qué permite concluir |
| --- | --- |
| Cierra antes de B1 | Revisar activación/Awake/OnEnable y creación de recursos; no atribuir a la carga de partida por nombre de escena. |
| B1 estable; cierra tras habilitar cámara en B2 | Priorizar primer render y finalización GPU/worker; la llamada original SaveFacade.Load permanece pendiente. |
| B2 estable; cierra después de continuar a B3 | Priorizar ScreenRoot/eventos/save/FrontEnd con los últimos marcadores precisos; la cámara pudo sostener múltiples frames. |
| B1/B2/B3 y menú completos | Resultado sensible a timing/concurrencia; no convertir la espera artificial en reparación permanente. Repetir0 y recuperar log/memoria/dump. |

Preservar foto de franjaB1/B2/B3, CURRENT, última completada, AUDIO/GFX y memoria.
No es necesario volver a memorizar un nombre fugaz. Conservar VPK6 y partidas.

## Validación y entrega

**VERIFIED fuente/Editor:** principal3742fuentes,0errores/514warnings en compilación
PSP2 sin UNITY_EDITOR. Original y B llegan a FrontEnd/3DBackground/Sharks en dos
procesos35s con0errores durantePlay,60/VSync1. En B se comprueba expresamente
que SaveFacade.Load no se llamó durante B1/B2, que la cámara está deshabilitada
en B1 y restaurada en B2, y que B3 libera una única llamada original de carga.
Son fixtures PC con targetPSP2, namespace ficticio y continuación async desde
Splash hacia BootLoader, sin aceptar edad. No ejecutan GXM nativo ni prueban el
flujo legal completo. A mantiene el audio00.06 y no se repite sin cambio de audio.
Fixture fuera de Assets y company/product reales restaurados antes del build.

**VERIFIED único build nativo final:** Succeeded,0errores/596advertencias,
2:59,885; BuildOptions.None,Mono2x,memoriaNone. SELF normal exactoSHA256
`14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`.
58checks startup/save y28contratos diagnósticos pasan;179marcas.23escenas,
480texturas,424HEVAG,140shaders/245passes ConsoleVS/ConsoleFS. Los15blobs
.resource/.resS son idénticos byte a byte a00.06; sin reconversión de audio ni
reimportación correctiva de texturas. No se aplica ExpandBy109MB ni patch nativo.

**VERIFIED paquete privado:**
`local-work/HSW_Recovery/Reports/PSP2_VPK07/HSW_Vita_Test_00.07_HGSKW1178.vpk`,
179.739.564bytes,285entradas; SHA256
`903d447fcaea8f6e123ab4065e7cc710e92ef4abf1ad3bb92abf1bee683ba413`.
CRC y comparación por miembro con la salida nativa PASS; identidadHGSKW1178/00.07,
ATTRIBUTE2=0 y cuota8192KiB. Símbolos exactos preservados en Player/SymbolFiles.

**VERIFIED preservación/reversión:** tres fuentes privadas y dos valores de versión
son los únicos cambios frente a00.06. Assets, metas originales, opciones de audio,
Fabric/helper, input, calidad, limitador, offline y JSON/save mantienen hashes.
Bases2017/2018 funcional y VPK06 preservados; Evolution no se modifica. Manifiestos
Before/After y ZIPs privados; restore_vpk06.py verifica en dry-run la restauración
de4archivos en fuente/caché sin afectar partidas, paquetes o evidencias.

Se conservaron dos rechazos iniciales de revisión automática de autorización.
Tras la autorización expresa del propietario para continuar y comprobar la
cláusula de excepción limitada de PORTING_PLAN/AGENTS, la revisión aceptó el mismo
comando directo. No se cambió el ledger, reglas, rama ni vía de ejecución para
eludir el control. Excepción diagnóstica privada, sin aprobación de fases.

**UNTESTED físico00.07:** B1/B2/B3, primer frame nativo, causa del cierre, menú
original y estabilidad. La compilación y el Editor no demuestran reparación.
Probar B esperando10–15s en B1 y10–15s en B2 antes de continuar, y conservar la
etapa/franja exacta que preceda al cierre. No se afirma que el problema sea ya
la cámara o la partida.


## Resultado físico posterior — B1 estable, B2 cierra

**OWNER-REPORTED 2026-11-07:** B1 muestra Loading y permanece normal unos20s.
Al pulsar para pasar aB2 se congela y vuelve aLiveArea tras unossegundos;B3 no
se alcanza. No se recibió nuevo log/foto/dump. **FAIL físico00.07 enB2.**
El código y la fixture mantienen la carga original de partida pendiente enB2;
esto prioriza el recorrido de cámara/render sin atribuir todavía un recurso o
stacknativo. Loadingvisible enB1 no demuestra que SaveLoader/Camera estuviera
renderizando: Splash también usa esa imagen. La comparación siguienteR0/R1/R2
está en [la prueba de cámara00.08](PSP2_SAVELOADER_CAMERA_VPK08_2026-11-07.md).
