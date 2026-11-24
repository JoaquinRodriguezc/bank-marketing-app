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
| T6 | S7 | Cierre: README, coherencia con notebook, reparto de explicación | pendiente |

## Log

- L1 (usuario): "Estamos con un proyecto integrador… En la entrega 4 tuvimos que hacer un app para mostrar todo este proceso. El problema es que presentamos y tenemos varias cosas por corregir… Idea un plan para poder mejorar todas estas cosas, y vamos a conversar y llegar a la mejor manera de resolver todos estos problemas."
- L2 (usuario, decisiones): idea extra del profesor incluida; sección nueva del tallo para el techo; CSS + portada renovada (sin reestructura); leer todas las versiones de la Entrega 3 antes de arrancar.
- L3 (usuario): elegir ángulo narrativo "Las dos historias en capas" para la sección del techo.
- L4 (evidencia, análisis descartados, semilla 42, código de la app): dentro de la era vieja CV ahorro 4,1% ± 3,8% (ruido; un shot 10% con recall 0,93); transplant del umbral al test nuevo: 0,4% de ahorro; descartados + calibración en dev: 1.004 llamadas, 519/542, 1,93 llamadas/sí, 3,98%; V4: 1.003, 519/542, 4,08%. AP 0,685 (viejo) vs 0,680 (V4) en el mismo test. El techo ~4% queda demostrado con dos épocas disjuntas de entrenamiento. Script scratch: /tmp/analisis_descartados.py.
- L5 (límite de slice): 412 líneas autoradas en 3 commits (2823cd1, 6b0773e, 1c6c159) al cerrar T3.
- L6 (límite de slice): 535 líneas autoradas en 5 commits al cerrar T5 (último: b182bfb). La forma de entrega al publicar la decide el grupo (push/merge de la rama).
- L7 (corrección del usuario): «Leiste bien las correcciones? ... habia que poner el grafico de el modelo en 0,0. Ahora parece en 0,0 pero los ejes estan mal. Despues, la sección de "Como lo sabemos" de "El modelo" sigue estando completamente congestionada, faltan los graficos que se piden, y el estilo sigue igual de aburrido, faltan graficos, faltan versus, falta la compración de modelos.» → resuelto en 4d301ac: ejes (0,0) de verdad (x 0→1), versus dentro de El modelo, y tres gráficos nuevos en el Cómo lo sabemos (comparación de 12 candidatos, matriz de confusión, coeficientes).
