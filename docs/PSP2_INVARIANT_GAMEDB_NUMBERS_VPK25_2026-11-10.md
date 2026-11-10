# Lectura numérica de GameDB — VPK privado 25

## Resultado físico de 24

**OWNER-REPORTED:**el nivel abre,pero modelos gigantes,HUD sobredimensionado y muerte inmediata impiden jugar. Ocurre solo dentro del nivel,menú/carga normales. **FAIL jugabilidad24.** Los logs superan el fatal anterior,fila37 y cuatro pools/spawner/jugador/callbacks;no se repite el fatal de1024trampolines en esa captura. Esto no acredita estabilidad prolongada ni todas las funciones.

## Defecto demostrado

El lector `FGOL.ThirdParty.MiniJSON.Json.Parser.ParseNumber` usa las sobrecargas TryParse dependientes de CurrentCulture. Con separador decimal de coma,un punto JSON puede interpretarse como separador de miles. El formato con coma se observa en los logs deVita;el nombre exacto de la cultura se registrará en25. La DLL **exacta** de24,reproducida localmente bajo es-ES,lee0.5→5 y1.25→125. El mismo problema se reproduce en es-CO.

Con el archivo cifrado original,sin modificar su contenido,se comparó la lectura invariable con la española: **2345 de19656 valores numéricos difieren**,mismos108grupos JSON/3407registros;el importador completa109tipos. Ejemplos reales:

| Dato original | Correcto | Lectura defectuosa |
| --- | --- | --- |
| Sardine,defaultSize |1.15|115|
| BlackTip,sizeMetresMin |3.65|365|
| BlackTip,minHealthBarSize |0.09|9|
| BlackTip,healthDrainRate |1.7|17|
| BlackTip,healthDrainAmpPerSecond |0.005|5|
| PlayerGreatWhite,cameraFrameWidthModifier |1.2|12|

Estos datos justifican una reparación de interpretación:explican magnitudes incorrectas en modelos,HUD y daño. **VERIFIED:**defecto del parser y valores afectados. **INFERRED hasta próxima prueba física:**que esta corrección resuelva por completo los tres síntomas observados.

## Corrección mínima

Solo con UNITY_PSP2,ParseNumber usa NumberStyles.Integer/Float y CultureInfo.InvariantCulture;el escritor numérico también usa proveedor invariable. Se reconoce notación científica válida;no hay tokens con exponente sin punto en el GameDB original inspeccionado,por lo que ese caso adicional no altera sus valores. Se conserva el comportamiento previo de retorno ante TryParse fallido;no se ocultan excepciones del juego.

La cultura del hilo se mantiene intacta. No se ajustan cámaras,FOV,escalas de modelos,rectángulos del HUD,estadísticas,reglas de salud,tiempos,guardados o datos para compensar el error. Se leen correctamente los números del recurso original. La desactivación temporal de GameCamera pertenece al flujo original de intro/spawn y tiene rutas de reactivación;se conserva. Los métodos de cámara/control/salud/carga siguen idénticos a24.

Se agregan únicamente observaciones acotadas:NUMERIC_FORMAT al arrancar,NUMERIC_GAMEPLAY al detectar jugador y sesión iniciada,con cultura,valores originales seleccionados,salud,escala,cámara y resolución. Se usan el UDP y respaldo existentes,sin ventanas o botones nuevos. Se conservan60cap/VSync1,Mono2x,BuildOptions.None,memoriaenum3 y reserva4096trampolines de24;sin cambiar presupuestos32filas/2ms.

## Validación

**VERIFIED local:**los19656números,tipos,claves y orden del árbol original coinciden en Invariant,en-US,es-ES,es-CO,fr-FR,de-DE,ar-SA,lectura string/TextReader,escritura numérica y cultura del llamador intacta. La DLL final25 repite contratos numéricos en siete culturas. Sin UNITY_PSP2,los28métodos de JSON conservan exactamente el IL original24.

**VERIFIED Editor es-ES:**todos los3407registros importados y16847campos numéricos escalares coinciden con el JSON original;109tipos,GameDB/callbacks completos. Guardado nuevo/sobrescritura/errores/recuperación/payload grande/copia diferencial pasan. Flujo original FrontEnd→Hawaii_low→pools/spawner/jugador/sesión,0errores del juego;tras ocho segundos el jugador sigue vivo. El snapshot al inicio muestra salud70/70 y valores Float32 equivalentes a tamaño3.65,amp0.005,barra0.09.5607paquetes completos consecutivos,un único error intencional de autoprueba del logger.

La prueba usa GameView640x480;no valida proyección visual960x544 deVita. ScreenCapture en batch no produjo archivo;no se declara verificación visual por captura. Fixture configura el componente original de carga y no valida cada interacción UI o controles físicos.

**VERIFIED build:**result=Succeeded errors=0 warnings=492 bytes=270205322 duration=00:02:58.6057485. Único build nativo,58contratos generales+110diagnósticos,325marcadores;28tipos protegidos de gameplay/cámara/salud/codec/GameDB/IA con IL y campos exactos a24.49archivos serializados,15bancos y23escenas preservados;auditorías424HEVAG/480texturas/140shaders reutilizadas,sin conversiones. SELF y runtimeMono intactos;tabla nativa4096verificada. Ocho archivos existentes modificados,cero nuevos;settings solo dos versiones24→25,fuente/cache exactas y rollback24dry-run validado.

**Fallos de herramientas conservados:**primer comando de probe /out sin token de ruta;dos errores C# por using FGOL.Utilities ausente;comparador AOT apuntó inicialmente a23 y rechazó1024vs4096. Se corrigieron argumentos/namespace/ruta,las verificaciones estrictas pasan;sin reconstrucciones nativas repetidas ni cambios adicionales al player.

## Entrega y siguiente ejecución física

`HSW_Vita_Test_00.25_HGSKW1178.vpk`: 179916751bytes,288entradas,SHA256:

```text
6462882b8df583440cda708ece39706dde459c0a821b475d3d7780273b7dfbe2
```

CRC/hash/espejo,siete símbolos exactos y símbolos del plugin verificados. Mantener VPK25_ExactSymbols.zip,VPK25_NativePluginSymbols.zip y manifiestos junto al paquete exacto. VPK24/anteriores preservados;sin ramas,fases,publicación o alteraciones Evolution/2017.

Cerrar24,instalar00.25 y repetir con la partida actual. Comprobar proporciones del nivel/HUD,movimiento y salud al empezar. Mantener receptorUDP18194 activo. Conservar logPC y vita_live.log,vita_live_watch.log,vita_mono_native.log,vita_native_exit.log de ux0:data/HSW_Vita;conservar nuevo dump con símbolos25 si aparece. No borrar ni reiniciar progreso.

**Estado:corrección funcional del parser demostrada localmente;proporciones,control,muerte inicial y estabilidad25 pendientes de validación física.**
# Resultado físico posterior de VPK 25

El propietario confirmó proporciones normales de modelos y HUD y controles que responden entre pausas. Inicialmente hubo pausas al comer, usar turbo y moverse; después esas acciones funcionaron sin las pausas intermitentes. La recarga del nivel mejoró dentro del mismo proceso. Los valores numéricos originales quedaron confirmados por telemetría es-ES. Rendimiento reportado: aproximadamente 20 FPS en menú y menos de 15 en gameplay; sin medición GPU independiente. La correlación entre fluidez y corte del diagnóstico detallado, y la caché caliente, se investigan en el [informe de VPK 26](PSP2_LIGHTWEIGHT_LOGGING_FPS_VPK26_2026-11-10.md). Esto actualiza el estado físico pendiente de la entrega original sin atribuir estabilidad prolongada ni rendimiento suficiente.
