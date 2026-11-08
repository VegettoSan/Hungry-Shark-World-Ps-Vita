# SaveLoader B3 y salida de audio — diagnóstico privado 00.09

Encargo privado vigente del propietario; excepción limitada autorizada, sin
modificación de fases, ledger, ramas o publicación. Solo copia PSP2 privada2018;
Evolution es referencia de lectura. Unity2018.2.19f1, BuildOptions.None, Mono2x,
expansión de memoria None y límite60/VSync1.

## Evidencia física que cambia la prioridad

**OWNER-REPORTED 00.08:** R1 y R2 mantienen B2 estable. Ambos cierran después de
continuar B3. No oyó sonidos en ninguna prueba. No hay nuevo log, dump ni foto.
R0 no está informado. Esto sustituye la inferencia de que 00.08 falla al habilitar
la cámara; no modifica el informe histórico 00.07. Causa nativa sin demostrar.

B3 devolvía el control al tracker original; después se ejecutaban ScreenRoot,
OnStateLoaded y SaveFacade.Load/transición. La marca antigua de SaveLoader/Camera
no basta para identificar la operación fatal. Las fronteras existentes registran
suscriptores, GameDB, carga local, solicitud de FrontEnd y escenas comunes, con
memoria libre y escritura AutoFlush. No se asume que C# sin excepción excluya
un fallo nativo. No existe dump reciente para resolver con símbolos de00.08.

## Cambios temporales exclusivos de PSP2

- **B3a:** pausa cuando estado/pantalla están listos, antes de mutar los flags de
  carga o llamar a SaveFacade.Load. Botón explícito libera la llamada original
  una sola vez. Modo Original permanece sin pausa. No se acepta consentimiento,
  simula guardado ni omite escenas.
- **T en B1/B2:** PCM440Hz,44100Hz mono,1s; clip sintético temporal, SetData,
  asignación y Play de AudioSource directo. Solo la sonda y su clip son destruidos.
- **M en B1/B2:** localiza el AudioClip original hsx_mus_frontend ya referenciado
  por BootLoader. LoadAudioData/asignación/Play3s/Stop. No se destruye ni descarga
  el clip original. HEVAG real del player debe verificarse otra vez al empaquetar.
- Registra listeners activos, volumen/pausa global solo lectura, frecuencia de
  salida, volúmenes music/sfx de AudioManager, loadState, isPlaying y DSPdelta.
  Play retornado/isPlaying no son prueba de audibilidad física. Los botones de
  avance se bloquean solo mientras dura esta prueba para no mezclar operaciones.

La prueba T usa un array temporal de176400bytes más el clip; no crea texturas,
render textures, GC forzado ni preferencias persistentes. Es una carga diagnóstica
acotada. B conserva Fabric/audio original. No convertir clips ni copiar la
expansión de memoria de Evolution sin evidencia.

## Comparación de audio existente

World: menú HEVAG Streaming estéreo22050Hz,103,38458s, preloadfalse. Evolution:
HEVAG Streaming estéreo44100Hz,112s, preloadtrue. DSP/BGM comparables, controladores
Fabric/AudioManager frente a SoundController distintos. Esos valores no prueban
incompatibilidad; el silencio antes de FrontEnd no demuestra fallo de su música.
Los auditores previos de424clips/480texturas/140shaders se reutilizan.

## Validación y fallos reales

Compilación manual principal3742fuentes PSP2: **VERIFIED** 0errores/514warnings.
El primer intento falla CS0009 por metadatos inválidos en TMP de Library; se
preserva el resultado fallido. Cecil detecta6DLL derivados inválidos y se apartan
con respaldo. El scan MZ inicial no detectaba ese daño; no se presenta como
validación suficiente. Otro intento de referencia con espacios falló CS2001;
se corrigió el quoting, sin tocar fuentes del juego. Cache Assets/Fabric.meta se
recupera byteexacto desde la copia privada autoritativa.

Al arrancar Unity detecta además cabecera inválida de Library/assetDatabase3 y
reconstruye automáticamente el índice/importación. No se borró Library ni se
solicitó una conversión masiva. Los fallos de caché del PC no se atribuyen al
cierre físico.

**VERIFIED Editor:** dos procesos45s, Original y B/R2, namespaces ficticios;
FrontEnd +3DBackground +Sharks,0errores durantePlay,60/VSync1. B1/B2 retienen
SaveFacade.Load; B3a lo retiene2s y al liberar ocurre exactamenteuna llamada.
PCM y música original:Loaded,isPlayingTrue,DSPdelta0,256/0,235s;1listeneractivo,
volume1,pausedfalse,output48000Hz. Ambos limpian su AudioSource sin destruir
originales. La música Fabric original se programa al activarFrontEnd. Es Editor
PC,targetPSP2; no prueba de GXM/HEVAG/audibilidad física. BootstrapasyncBootLoader
solo fixture,no aceptaciónedad. Ajustes reales restaurados y fixture retirada.

**VERIFIED único build09:**Succeeded0errores/596warnings,03:16,5926139;
BuildOptions.None/Mono2x,memoriaNone. SELF normal exactoSHA256
`14e028be4fce1992aa8a3cbde030c7a094a1e0bc49af8f6767bc58c0266a75ad`.
58checksstartup/save +41diagnósticos,196marcas.23escenas/424HEVAG/480texturas/
140shaders245passes PSP2 ConsoleVS/ConsoleFS. No reconversióncorrectiva deaudio
ni texturas; auditor nativo confirma0importsoverride/reimportadicionales.

**FAIL de verificadores/IO preservados:**primer auditor de bases aborta por
assert deigualdad sinretener archivo. Relectura explícita completa2017(20870)
y2018(20887) coincide con todoslos hashes históricos,sin modificación de bases.
Auditores dehash paralelos quedan esperandoIO,se detienen solo susPIDidentificados
y se resuelve conpasadas secuenciales; no condición eliminada. Trasregeneración
Unity reserializa7PluginImporter(soloGUID/Anyenabledpreservados yWSAdisabled)
yPresetManagerempty aYAML. Primer checksource/cacheFAIL detecta8diferencias;
archivadas,se restaura caché desde bytes privados originales. Presetbinario
original se decodifica como8bytescero deobjeto:hideflags0,listavacía. Fullscan
finalsource/cachePASS. Ningún plugin/código del player cambió por esa restauración.

El comparador de15blobs exigeigualdadtotal yFAIL. Se conserva:12/15exactos,
**los4bancos.resource deaudio exactos a08**;3resS cambian trasregenerar caché.
Comparaciónpornombre/dimensiones/mips/formato/tamaño/SHA de **cada uno de480payloads
comprimidos** da multiconjunto exacto08/09. Se demuestra contenido de texturas
preservado aunque difiere disposición/bytesdelcontenedor; no se copiaresS deotro
player ni se afirma15/15. TexturePayloadComparison yNativeResourceBlobs privados.

Copiasdearchivo playerC→E esperanIO. StopsoloPIDrecolector; untemporalcambia antes
decomprobarlo,assertpreservado; renombrado posterior devuelveWinError32/archivoenuso.
Seconserva Player parcial yno se usaparaempaquetar. La propuesta de enlaces de
bancos no llega a ejecutarse por esefallo depreparación; no se sustituyeronbancos.
El empaquetador lee directamente elplayercompletoC yaauditado, creaVPKindependiente,
luego Copy-Item guarda espejopermanenteE conSHA exacto. Símbolos09 exactos5archivos
enZIP36.422.675bytes,CRC yhashporarchivo; espejoE verificado. No nuevo build,
parcheSELF/AOTni recuperación deSDK antigua. CopyIOFailure.json registra límites.

**VERIFIED paquete permanente:**
`local-work/HSW_Recovery/Reports/PSP2_VPK09/HSW_Vita_Test_00.09_HGSKW1178.vpk`,
179.740.208bytes/285entradas,SHA256
`64521f291992963485fa6c091450729ab90aee3128c4fa58ae7f78c2c01664fb`.
CRC ycada miembrocomparado conmanifest;HGSKW1178/00.09,ATTRIBUTE2=0,cuota8192KiB.
Símbolos:VPK09_ExactSymbols.zip+VPK09_SymbolManifest.json exactos alAOT09.

**VERIFIED preservación/reversión:**solo4fuentesprivadas y2versiones cambiadas
frente08;assets/metas originales,Fabric/helper,savecodec,controles,FPS/offline
intactos. Fuentes/caché byteexactas después de restaurarreserialización. Bases
2017/2018 hashesexactos;VPK08conservaSHA. Before/After manifests/ZIP yrollbackdryrun
5archivosPASS. Sinledger,ramas,aprobaciónfases,publicaciónni cambiosEvolution.
Playerparcial no es artefacto válido; usarVPKyZIPsímbolos independientes.

**UNTESTED físico09:**causanativa,menúVita,audibilidad,memoria duranteB3b yestabilidad.
Sinreparación afirmada hasta prueba física.

## Protocolo físico

Cada prueba requiere reiniciar el proceso. Primero B/R2 hasta B1: probar T,
anotar sonido/status. En otro arranque B/R2/B1 probar M. No avanzar al menú en
esos ensayos de audio. Tercer arranque sin pulsar T/M: B/R2 -> B2, esperar -> B3;
ver si aparece B3a y se mantiene estable, luego liberar carga original y registrar
CURRENT/Last completed/AUDIO/GFX/memoria antes del cierre. Una foto del resultado
estable de T/M evita depender de leer la pantalla durante una congelación.

Sin prueba física00.09, sin reparación del cierre ni llegada al menú Vita afirmada.
Evidencia privada: local-work/HSW_Recovery/Reports/PSP2_VPK09.

## Pregunta del propietario: OBB omitido durante el build

**VERIFIED estático09:** el OBB se incorporó a la recuperaciónAPK+OBB (23escenas,
level1..22 procedentesOBB); elplayer nativo incluye23escenas enordenoriginal.
Se inspecciona el índiceResources real de09:1071clavesúnicas. De528rutas delcatálogo,
477están incluidas y51ausentes, exactamente las mismas51ya ausentesenelproyecto
recuperado según auditoríahistórica. **0omisiones adicionales delcatálogo enelbuild**.
GameDB/gameDB.gdb estáindexado ysuTextAsset de1928000bytes tieneSHA idéntico aloriginal
privado:0e9177d0de3ff3105e9af6cff0f1f56804fd2dca8f66fccc20d3770e78496127.

PSP2 prioriza escenasintegradas cuandoCanStreamedLevelBeLoadedtrue; no necesita
unOBBAndroid externo para esas escenas. GetOrLoadAssetBundle retornanullenPSP2,
ylaúnicaruta llamante observadaes cargaescenasconfallbackintegrado. Bdiagnóstico
usaLoadSceneAsync deescenasintegradas directamente. GameDB usaResources.Load.

Esto descarta la omisióncompleta delOBB yno muestra exclusiónnueva deesas477rutas.
**No prueba completitud absoluta de datos originales**:las51rutas incluyen comida
yvariantesdetiburón,algunasFrontEnd; puedenrequeririnvestigarrecuperaciónocontenido
adicional,nodebeninventarseni ignorarse. No se ha demostradoquesolicitarlasprovoque
elcierre. Loaders09yaregistranBEFORE/DONEresource yHSW_RESOURCE_MISSING;B3a separa
pantallapreparada deSaveFacade.Load ypermiteobteneresa evidencia física.
No se cambia elVPKni se haceotrobuildporestapregunta. Evidencia:OBB_Inclusion_Audit.json,
NativeResources09.json ycatálogo528histórico. Comparador auditaestasrutas,no toda
referencia dinámica posible.
