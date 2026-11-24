# Mejoras Entrega 4 — correcciones del profesor

Feature: aplicar las correcciones del profesor a la app de la Entrega 4 (copa de martini, HTML+Altair, GitHub Pages). Fuente: `../correcciones_y_recomendaciones_del_profesor.md` y la conversación con el grupo.

## Specs

- S1: Reenfocar la narrativa: "El objetivo de un proyecto de ciencia de datos no es 'inflar un numerito', sino responder preguntas con evidencia." No esconder el ahorro chico (~4%): la app debe convencer de que ese es el máximo posible dados los límites del dataset, y "bardear a los datos": exponer qué limitaciones impiden bajar más el piso de llamadas y qué habría que recolectar.
- S2: Intro más vistosa + cajas comparativas "versus" (1,93 llamadas por sí vs 2,1) + más contexto (banco portugués, llamadas de operador).
- S3: Explicar el gráfico de `poutcome` y qué es "OTRO"; etiqueta del eje Y ("Resultado del contacto previo"); sumar hipótesis que no funcionaron (ej. estudiantes 28,7% con volumen ínfimo).
- S4: Sección El modelo: reducir texto, sumar gráficos; pensar cada sección como póster; gráfico de ahorro desde (0,0); número concreto de ahorro; mostrar el proceso (modelos probados, umbral recall mínimo 0,95, justificación); aclarar contra qué se compite (estrategia del banco como piso alto, no "llamar a todos" en bruto).
- S5: Copa: aclarar qué es "Saldo"; si hay tiempo, selector de variable del eje Y.
- S6: Idea extra del profesor: replicar el análisis de umbral sobre los datos descartados para investigar si la estrategia del banco surgió de ahí. Decisión del grupo: incluirla como sección nueva del tallo «Por qué no se puede ahorrar más», con ángulo narrativo "dos historias en capas" (título afirma el techo; subsección «¿la estrategia surgió de los viejos?» con transplant vs calibración como mini-versus).
- S7: Los gráficos siguen siendo Altair; colores/categorías/escalas consistentes; lo que muestra la app coincide con el notebook; repo regenerable con `python build_app.py`.

## Tasks

| ID | Spec | Trabajo | Commit |
|---|---|---|---|
| T1 | S6 | Sección nueva del tallo «Por qué no se puede ahorrar más»: análisis de descartados dentro de `build_app.py`, gráfico de ahorro por época de entrenamiento, subsección transplant-vs-calibración, «Cómo lo sabemos» | 2823cd1 |
| T2 | S4 | Revamp de El modelo: gráfico de familias (ahorro ± desvío), curva recall vs llamadas con 0,95 y 0,80, ahorro desde (0,0), número protagonista (89 llamadas menos de 1.092 por 23 de 542 sí), baseline = estrategia del banco | 6b0773e |
| T3 | S3 | Hallazgos: qué es OTRO, etiqueta eje Y, hipótesis fallidas | 1c6c159 |
| T4 | S2 | Portada/intro: oración honesta, caja versus, contexto, CSS renovado | e904795 |
| T5 | S5 | Copa: aclarar Saldo; selector eje Y verificado y con guard | b182bfb |
| T6 | S7 | Cierre: README, coherencia con notebook, reparto de explicación | d6230df |
| T7 | S2+ | Restilo editorial elegido por el grupo («revista de datos», paleta Okabe-Ito, nav lateral, aire): portada con cadena de dos versus (artboard 04 aprobado) implementada en plantilla.py; faltan las demás secciones | 1755166 |

## Log

- L1 (usuario): "Estamos con un proyecto integrador… En la entrega 4 tuvimos que hacer un app para mostrar todo este proceso. El problema es que presentamos y tenemos varias cosas por corregir… Idea un plan para poder mejorar todas estas cosas, y vamos a conversar y llegar a la mejor manera de resolver todos estos problemas."
- L2 (usuario, decisiones): idea extra del profesor incluida; sección nueva del tallo para el techo; CSS + portada renovada (sin reestructura); leer todas las versiones de la Entrega 3 antes de arrancar.
- L3 (usuario): elegir ángulo narrativo "Las dos historias en capas" para la sección del techo.
- L4 (evidencia, análisis descartados, semilla 42, código de la app): dentro de la era vieja CV ahorro 4,1% ± 3,8% (ruido; un shot 10% con recall 0,93); transplant del umbral al test nuevo: 0,4% de ahorro; descartados + calibración en dev: 1.004 llamadas, 519/542, 1,93 llamadas/sí, 3,98%; V4: 1.003, 519/542, 4,08%. AP 0,685 (viejo) vs 0,680 (V4) en el mismo test. El techo ~4% queda demostrado con dos épocas disjuntas de entrenamiento. Script scratch: /tmp/analisis_descartados.py.
- L5 (límite de slice): 412 líneas autoradas en 3 commits (2823cd1, 6b0773e, 1c6c159) al cerrar T3.
- L6 (límite de slice): 535 líneas autoradas en 5 commits al cerrar T5 (último: b182bfb). La forma de entrega al publicar la decide el grupo (push/merge de la rama).
- L7 (corrección del usuario): «Leiste bien las correcciones? ... habia que poner el grafico de el modelo en 0,0. Ahora parece en 0,0 pero los ejes estan mal. Despues, la sección de "Como lo sabemos" de "El modelo" sigue estando completamente congestionada, faltan los graficos que se piden, y el estilo sigue igual de aburrido, faltan graficos, faltan versus, falta la compración de modelos.» → resuelto en 4d301ac: ejes (0,0) de verdad (x 0→1), versus dentro de El modelo, y tres gráficos nuevos en el Cómo lo sabemos (comparación de 12 candidatos, matriz de confusión, coeficientes).
- L8 (estilo visual): el grupo eligió personalidad «revista de datos», paleta Okabe-Ito intacta en los gráficos, nav lateral y ritmo editorial con aire. Diseño de la portada en design/portada-revista/ (3 artboards: apertura editorial, cifras protagonistas, gancho del régimen). Pendiente: elegir dirección y aplicarla sección por sección a plantilla.py.
- L9 (handoff de diseño): implementado design/portada-revista/04-cadena-versus.html (elegido por el grupo: cadena de dos versus — banco vs su pasado 7,1→45,5 %, luego banco hoy vs modelo 2,01→1,93). Base editorial global: papel #faf9f6, serif en títulos, hairlines. Artboards 01-03 quedan como alternativas. Pendiente por sección: datos, hallazgos, modelo, techo, copa.
- L10 (handoff de diseño): implementado design/datos-revista/01-salto-senhalado.html (capítulo 02, figura enmarcada con epígrafe, anotación del salto dentro del g-datos real de Altair, rangos por época computados de los datos). Artboards 02-03 quedan como alternativas. Pendiente: secciones hallazgos, modelo, techo y copa.

## Pendiente (lista de seguimiento, retomar acá)

Restilo editorial sección por sección (personalidad «revista de datos» aprobada; base global ya aplicada: papel, serif, hairlines; gráficos en Okabe-Ito):

- [ ] Sección «Lo que encontramos»: vestimenta editorial (figura enmarcada + epígrafe como en datos). Decisión de contenido pendiente: conectar el hallazgo con «qué sabe el banco de su lista» (el 49 % de la lista tiene contacto previo, y el historial es lo que más pesa en el modelo).
- [ ] Sección «El modelo»: vestimenta editorial (el contenido ya está corregido; falta el estilo: nums/versus, figura enmarcada del gráfico de ahorro, capítulo 04).
- [ ] Sección «Por qué no más»: vestimenta editorial (capítulo 05).
- [ ] Copa «Explorá» y «Probá el modelo»: vestimenta editorial (fondo papel ya global; revisar los bindings de Vega a la nueva paleta).
- [ ] Verificación en navegador real: nadie vio la página renderizada todavía (solo verificación estructural). Abrir index.html o `python -m http.server` y revisar sección por sección.

Publicación y defensa (decisiones del grupo):

- [ ] Publicar: push de `mejoras-entrega4` + merge a `main` para que GitHub Pages sirva la versión nueva; probar desde otra computadora (lo exige la consigna).
- [ ] Reparto de la defensa oral (nota individual): cada gráfico con un dueño que lo sepa leer componente por componente.
- [ ] Preparar el cruce V6-vs-techo: el informe V6 dice «lift máximo 1,24× desde los datos viejos» (aplica al umbral transplantado); la sección del techo muestra el empate con calibración (3,98 % vs 4,08 %). La diferencia es transplantar vs calibrar el umbral — pregunta probable de la devolución.

Estado: 16 commits en `mejoras-entrega4`, rama local (nunca pusheada). El test del build imprime idéntico en cada regeneración: umbral 0,354462 · 1.003 llamadas · 519/542 sí.
