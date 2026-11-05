# Recuperación privada de World 2.9.0 / 132 — 2026-11-05 UTC

**READY_TO_OPEN — NOT YET EDITOR VERIFIED.** Proyecto preparado para Unity
**2017.1.2p4**, mediante extracción y comprobaciones estáticas. No se ejecutó
ningún Editor ni se acreditan compilación, importación, shaders o gameplay.

## Autorización y límites

El propietario autorizó expresamente en esta tarea la extracción offline del
APK/OBB, recuperación Mono y assets, reconstrucción de referencias y preparación
del proyecto original sin Unity. Es una excepción preparatoria puntual, no
aprobación de P00/P01 ni de fases posteriores. `PHASE_GATES.json` permanece
intacto: P00 ACTIVE, P01–P12 LOCKED, 0/13 aprobaciones. Se trabajó en `main`, sin
crear ramas, modificar Evolution, usar Unity 2018, preparar PSP2 ni generar VPK.

## Entradas, herramientas y procedimiento

- APK SHA-256: `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d`.
- OBB SHA-256: `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72`.
- Ambos SHA y CRC ZIP: **VERIFIED PASS**. Originales conservados sin modificar.
- Python **3.14.4**, stdlib `zipfile`/`hashlib`; AssetRipper
  **2.0.0+1ac666f47d8e9dedf96afb0b914c70d7656151ea**, ILSpy integrado;
  dnSpyEx **6.6.0**, consola y dnlib. Instalaciones existentes; ninguna descarga.
- Se consultaron inventario y procedimientos de Evolution en modo lectura. Sus
  enlaces locales antiguos apuntaban a otra unidad; se reutilizaron los
  ejecutables reales, sin reparar ni escribir ese repositorio.

Comandos reproducibles desde la raíz World; rutas de entrada y salidas privadas
se sustituyen por sus ubicaciones locales:

```powershell
python tools/check_phase_gates.py
python tools/verify_source_pair.py "<APK>" "<OBB>"
python tools/prepare_private_recovery.py "<APK>" "<OBB>" local-work/HSW_Recovery
```

El último comando exige salida ignorada por Git, preserva todas las entradas,
comprueba rutas/colisiones, concatena partes numéricamente y guarda manifiestos
SHA-256/checkpoints privados. Resultado: **4.735 archivos extraídos**, **3.967
archivos lógicos Data**, **7 grupos / 68 partes**, continuidad/tamaños/hash
verificados, **0 colisiones**. Se preservaron nombres opacos, sidecars y DLL.

AssetRipper se ejecutó desde el directorio privado, con `--headless --port 58065
--log-path Logs/AssetRipper.log`. Su API **local** recibió, en orden,
`POST /Settings/Update`, `/LoadFolder` y `/Export/UnityProject`. Entrada:
`Combined_Unity_Data/Data`, incluyendo `Managed`. Ajustes: TargetVersion
2017.1.2p4, CSharp4, Level2, Hybrid, ShaderExportMode Yaml,
ExportUnreadableAssets activado; los demás valores quedaron registrados.
**VERIFIED:** backend Mono, 23 ensamblados, finalización de 6.381 unidades de
exportación y `Finished post-export`, sin errores registrados por AssetRipper.

Se utilizó dnSpy.Console con `--no-color --no-sln --threads 2 --asm-path
<Managed> -o <privado>` para decompilar ocho bibliotecas externas por separado.
No se recompilaron ensamblados. La exportación íntegra se conservó y se creó una
copia independiente preparada para abrir.

## Resultado verificable

Ruta relativa privada:
`local-work/HSW_Recovery/HSW290_Unity2017_ReadyToOpen/`.

| Contenido | Cantidad verificada |
| --- | ---: |
| Escenas, con orden exportado de BuildSettings y GUID coherentes | 23 |
| Archivos C# dentro del proyecto | 3.849 |
| C# adicional de bibliotecas externas, fuera de Assets | 451 |
| DLL originales preservadas e inventariadas | 23 |
| Bibliotecas externas activas en Assets/Plugins | 8 |
| Prefabs | 1.038 |
| Mallas serializadas | 1.909 |
| AnimationClips | 1.415 |
| AnimatorControllers / OverrideControllers | 40 / 140 |
| Audio OGG | 424 |
| Materiales | 428 |
| Shaders serializados, conservando datos de Android | 96 |
| PNG exportados, antes de añadir StreamingAssets | 442 |
| Archivos de streaming recuperados fuera de Unity Data | 59 |

Las escenas abarcan carga, menús, audio, spawners y Hawaii en tres calidades.
No se interpretan los nombres `levelN` como mundos seleccionables. El conjunto
entregado solo puede contener lo incluido en este par APK/OBB; los datos
descargados posteriormente por Android no se proporcionaron ni verificaron.

Preparación mínima documentada:

- Se conservaron todas las rutas/referencias del exportador. ProjectVersion ya
  indica 2017.1.2p4 y se mantuvieron las configuraciones recuperadas.
- Se omitieron dos atributos AssemblyVersion duplicados al convertir los grupos
  UnityScript a C# dentro de las mismas fases de compilación. No se cambió lógica.
- Dos DLL vacías añadidas por AssetRipper, ausentes de los originales y con solo
  `<Module>`, se conservaron con sus metas en `RecoveryEvidence/ExporterSupport`,
  fuera de Assets. Las ocho bibliotecas del juego permanecen activas.
- Se añadieron 1.356 metas deterministas solo donde no existían: scripts sin
  identidad exportada, carpetas y streaming. Se etiquetan como GUID **nuevos de
  recuperación**, no como GUID originales.
- Se copiaron a StreamingAssets los 59 archivos APK/OBB fuera de `bin/Data`,
  incluidos los atlas japonés/coreano que carga `LanguageInitializer`, sin alterar
  sus bytes. Los recursos Android restantes siguen preservados en la extracción.

## Validación y reparaciones pendientes

`python tools/validate_recovered_unity_project.py <proyecto> --output <JSON privado>`
inspeccionó **66.091 referencias externas**, **27.574 referencias a scripts** y
**10.584 GUID**. Resultado: 0 metas ausentes/huérfanas/inválidas, 0 GUID duplicados,
0 fileID locales o YAML externos ausentes, 0 errores de escenas de BuildSettings
y 0 referencias locales no nulas a scripts sin destino.

Se contrastaron **779 identidades de scripts fuente referenciados** con los
tipos/ensamblados originales mediante el esquema de GUID del exportador. Otras
dos rutas de scripts resuelven a DLL externas. Los GUID del exportador no prueban
la recuperación de los `.meta` originales del desarrollador. Las ocho DLL
exportadas fueron reserializadas por AssetRipper: sus hashes difieren, pero la
comparación dnlib de **3.961 métodos** no detectó métodos añadidos ni diferencias
en firmas/cuerpos comparados. Los 23 binarios originales también se conservan.

**Recuperado pero pendiente de Unity:** todos los assets, código decompilado,
importadores, bibliotecas y configuración. Las 16 referencias UI del prefab de
depuración usan el GUID de la extensión `UnityEngine.UI` del Editor. Se contrastó
con `GUISystem/ivy.xml` local de Unity 5.6, sin ejecutar ese Editor ni copiar su
contenido; su disponibilidad/fileIDs en **2017.1.2p4** siguen pendientes. Las 23
referencias SceneAsset `102900000` son objetos principales implícitos de escenas,
no documentos YAML faltantes. No se prueban fileIDs de subassets binarios.

**Incompleto o pendiente de reparación, preservado sin inventar datos:**

1. Dos MonoBehaviours tienen `m_Script = 0` ya en los datos originales:
   LevelSelect, pathID 3393/GameObject 67; Hawaii_low, pathID 19482/GameObject 2788.
   No hay identidad de clase en esos registros. No se eliminaron componentes.
2. Una referencia de `Font Material` apunta a `Font Texture` sin asset exportado.
   El registro original builtin pathID 10103 tiene dimensiones 0×0, imagen vacía y
   stream vacío. Se conservó evidencia, sin generar textura sustitutiva.
3. Los shaders son datos compilados/serializados Android: no se recuperó fuente
   ShaderLab/Cg original ni se validó su ejecución en escritorio. Se preservó el
   protector de guardado YAML generado por AssetRipper.
4. Los archivos de fuente china/simplificada y taiwanesa referidos por ramas del
   código no están en el par suministrado; su uso real no está probado. Bundles,
   caché descargada y servicios/nativos Android quedan pendientes de comprobar.
5. La decompilación no acredita C# original exacto ni compilación. Excepciones
   presentes en código no se sustituyeron por implementaciones inventadas.

El validador conserva **STATIC_CHECK_ISSUES** por los dos scripts nulos y la
textura referenciada; no se convierte artificialmente en PASS. El estado global
READY_TO_OPEN describe la preparación para inspección en el Editor.

## Conservación y siguiente paso

Todo el material propietario y los reportes detallados permanecen bajo
`local-work/HSW_Recovery/`, ignorado por Git. Allí están extracción completa,
Data combinado, exportación intacta, copia preparada, DLL originales, C# adicional,
manifiestos, evidencia de problemas, logs, copias anteriores de los dos archivos
editados y checkpoint privado de respaldo. Son copias locales en la misma unidad;
no constituyen respaldo externo. La documentación pública no incorpora código o
assets del juego, secretos ni rutas personales.

Respaldo del proyecto preparado: **20.863 archivos**, **189.448.302 bytes**, CRC
ZIP **PASS**, SHA-256
`97f3f10c9f17d8b8881ffbfeb8b5e0be1ed9382868d682d6d660b7b7a708d9c8`.
La comparación con la exportación confirma únicamente los dos atributos
AssemblyVersion editados, las dos DLL vacías/metas trasladadas y las adiciones
documentadas; ningún otro archivo original se perdió o cambió de hash. Los hashes
de ambos contenedores originales se verificaron nuevamente al finalizar.

Para abrir posteriormente:

1. Instalar **Unity 2017.1.2p4**.
2. Abrir como proyecto existente **HSW290_Unity2017_ReadyToOpen**, la carpeta que
   contiene Assets y ProjectSettings. No abrir Combined_Unity_Data.
3. Esperar la importación y conservar el primer Editor.log/Console completo.
4. Revisar compilación e importadores; abrir
   `Assets/Scenes/Loading/SplashLoader.unity`. El orden de las 23 escenas ya está
   en ProjectSettings/EditorBuildSettings.asset.
5. Resolver los fallos reales del Editor antes de acreditar gameplay. Conservar
   la exportación intacta y el respaldo; no actualizar el único proyecto a 2018.

No se aprobaron fases ni se publicó, instaló o probó un port Vita.
