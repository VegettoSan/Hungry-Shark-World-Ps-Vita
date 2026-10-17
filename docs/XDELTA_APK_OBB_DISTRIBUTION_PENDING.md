# Pendiente P12 — Extractor de datos APK + OBB y evaluación de xdelta3

**Fecha:** 2026-10-17 · **Estado:** DISEÑO / PENDIENTE, **NO IMPLEMENTADO NI PROBADO**.
**Prioridad actual:** estabilizar Hungry Shark Evolution; este archivo solo deja preparada la investigación de distribución para Hungry Shark World. **P00 sigue ACTIVE; P01–P12 permanecen LOCKED.** No constituye autorización para desarrollar P12 ni aprobación de fases.

## Objetivo de experiencia final (hipótesis)

Que una persona con **sus propios archivos originales de Hungry Shark World Android 2.9.0 (versionCode 132)** pueda indicar al extractor de Windows el APK **Y** el OBB correspondiente. Si en el futuro existe un port PSP2 verificado, el extractor aplicaría una receta/parche validado, comprobaría los archivos generados y prepararía una carpeta/ZIP para copiarlos a la ruta PSP2 realmente probada, sin exigir al usuario un Unity Editor o el módulo PSP2.

**No basta prometer «solo el APK»**: en esta versión los datos fuente están divididos entre ambos archivos; si el usuario solo tiene el APK, el programa deberá explicar que **falta el OBB**, no generar una instalación incompleta, asumir que cualquier OBB es compatible ni descargar contenido no autorizado. Se puede estudiar admitir un XAPK/paquete con APK+OBB, **si** se valida que contiene exactamente los archivos esperados. Las dependencias adicionales descargadas/cachés del juego original están aún por investigar.

## Datos verificados de la referencia World

| Archivo | Tamaño comprimido | SHA-256 exigido por la referencia |
| --- | ---: | --- |
| APK 2.9.0 (132), `com.ubisoft.hungrysharkworld` | 27,378,446 bytes | `6bf41929985b556e6729f3696a02d687da119b04ced1c5cb13590f4ce69fab9d` |
| `main.132.com.ubisoft.hungrysharkworld.obb` | 92,431,553 bytes | `c35c6daf1514977fdba2101ea994fcbb244f0a757a74b908c1dc3c6203847d72` |

Ambos son contenedores ZIP. El APK contiene `assets/bin/Data/Managed/`, `level0` y fragmentos de `sharedassets0.assets`; el OBB aporta `level1`–`level22` y otros recursos/fragmentos. En la inspección estática constan **7 grupos `.splitN` / 68 partes** en conjunto. Es imprescindible reconstruir esas secuencias en orden numérico y preservar todas las referencias antes de evaluar qué datos puede leer la salida PSP2. Véanse [auditoría](TECHNICAL_AUDIT.md), [método de recuperación](DATA_EXTRACTION_AND_LAYOUT.md) y [lecciones de Evolution](EVOLUTION_TRANSFER_NOTES_2026-10-17.md). Estos son **datos Android**, no un pack Vita probado.

## Lo demostrado por otros ports (referencia, no compatibilidad World)

- [Predators PS Vita](https://github.com/AJ170/Predators-PSVita-Port): su README indica que el usuario facilita **el OBB original** y aplica `PredatorsData.xdelta` para reconstruir `PredatorsData.zip`; usa un VPK «stub».
- [Pocket Mortys PS Vita](https://github.com/celticg/AS-Pocket-Mortys-vita): el usuario facilita **su APK exacto** y usa `PocketMortysData.xdelta` para reconstruir `PocketMortysData.zip`; también usa stub VPK.
- [xdelta3](https://github.com/jmacd/xdelta/blob/main/site/docs/commandline.md) aplica diferencias binarias de **una fuente por invocación** (`-s SOURCE`) a un objetivo preexistente. No transforma formatos de texturas, shaders, escenas Unity o código Android en PSP2 por sí mismo. El autor del port debe preparar **primero** una salida PSP2 jugable.

**Importante en World:** un único `xdelta3 -d -s` no toma simultáneamente el APK y el OBB como fuentes independientes. No copiar sin cambios los comandos de Predators o Evolution. Se evaluarán estas **alternativas aún sin benchmark ni decisión final**:

1. **Preferente para investigar — normalizar ambos inputs localmente:** el extractor verifica APK + OBB y construye un *archivo fuente combinado determinista* (o una representación canónica de sus datos) con manifiesto fijo. Después `xdelta3` usa ese **único** archivo combinado como SOURCE y reconstruye un **ZIP PSP2 objetivo ya probado**. El diseño de concatenación/normalización, sus bytes exactos, espacio temporal, coste y ventaja en tamaño deben demostrarse; no se ha creado tal archivo ni parche.
2. **OBB como SOURCE + verificar APK aparte:** podría imitar Predators para el grueso de los datos, pero no reutiliza por delta los bytes que existen solo en el APK y puede aumentar sustancialmente el parche. **No sirve como prueba** de que el APK se aprovechó.
3. **Varios parches o transformaciones por archivo:** teóricamente posible; requiere decidir y documentar qué parte del objetivo deriva de cada archivo y validar dependencias cruzadas.
4. **Extractor/conversor reproducible sin xdelta:** considerar solo cuando haya una ruta real para generar contenido PSP2 compatible; **descomprimir ZIP Android no es convertir un build Unity al destino**.

Si el objetivo PSP2 tiene poca similitud con el APK/OBB comprimidos, **xdelta puede ser casi tan grande como la salida**. Comparar tamaño, memoria y tiempo con extracción normalizada, y fijar versión/compilación de xdelta por compatibilidad. No afirmar ahorro de espacio antes de medir.

## Contrato previsto del extractor (para decidir tras P08–P11; construir y liberar únicamente en P12 aprobado)

1. **Entrada:** APK y OBB elegidos por la persona, sin obtenerlos del repositorio. Verificar nombres lógicos/package/versionCode **y SHA-256 de ambos**, integridad ZIP, presencia de los recursos esperados; rechazar pareja incorrecta, parcialmente descargada, modificada o de versión distinta. La versión **3.0.2** no es intercambiable. Si se quieren aceptar hashes alternativos oficiales, deberán tener pruebas y receta independientes.
2. **Receta:** manifiesto versionado que especifique dos hashes fuente, versión y hash de la herramienta xdelta, estrategia fuente (combinada/OBB/otra), hash del parche, hash del ZIP final, lista de archivos, destinos y versión del VPK que los carga. Archivos y procesos temporales **en PC**, reproducibles y recuperables en caso de error.
3. **Salida:** construir en carpeta temporal nueva, comprobar hash del ZIP reconstruido y hashes de sus miembros, tamaños, dependencias, rutas relativas seguras, archivo ZIP completo y espacio libre. No aceptar rutas `../`, rutas absolutas, enlaces peligrosos ni sobrescribir silenciosamente instaladores; solo publicar resultado después de validarlo.
4. **Instalación:** distinguir el **VPK/stub PSP2** de los **datos preparados**, verificar ubicación exacta en el VPK y acceso desde la Vita; `ux0:app/HGSKW1178/` es la ubicación planeada, **no prueba** de que toda la salida vaya a `Media/`. Nunca sustituir `eboot.bin`, `sce_sys` ni archivos Unity PSP2 por contenidos Android. Guardados en ubicación de escritura verificada y separados de datos instalados.
5. **Pruebas de usuario:** Windows limpio, APK incorrecto, OBB incorrecto/ausente, archivos corruptos, permisos/espacio, reejecución del extractor, instalación limpia, actualización/reinstalación y guardados conservados. Confirmar apertura, niveles, audio, texturas, partidas y salida/reentrada en **PS Vita física** con el conjunto generado.
6. **Distribución y derechos:** no añadir al repositorio APK/OBB originales, datos extraídos, DLL/código propietario ni SDK restringido. **Que el resultado se publique como delta no lo convierte automáticamente en libre de derechos**: un patch puede incluir bytes originales del objetivo. Revisar derechos de redistribución del VPK, parche y herramientas antes de un release.

## Cuándo retomar este pendiente

- **P00 actual:** mantener diseño y fuentes. No preparar instalador ni xdelta real; esta nota no cambia [PHASE_GATES](PHASE_GATES.json).
- **P01 autorizado:** auditar recuperación conjunta y posibles datos descargados fuera del OBB. Congelar hashes de archivos originales y rastrear procedencia.
- **P07–P08 autorizados:** medir layout real de VPK y rutas que Unity PSP2 carga; decidir qué datos admiten separación del stub.
- **P09–P11 autorizados:** estabilizar, probar en Vita y congelar el **ZIP objetivo** con hashes y manifiesto (primero runtime correcto, después delta).
- **P12 autorizado:** prototipar alternativas, generar xdelta a partir de datos fuente verificables, ensayar extracción e instalación con un PC limpio, documentar el paso a paso y revisar aspectos legales. No dar por completado P12 únicamente por producir un ZIP válido.

**Criterio de aceptación futuro:** una persona proporciona ambos archivos exactos, la herramienta produce determinísticamente un pack verificado y ese pack reproduce en Vita física el contenido jugable validado sin instalar Unity; las partes publicables tienen revisión de derechos. Hasta entonces, estado **PENDIENTE / NO PROBADO**.
