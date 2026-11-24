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
| T1 | S6 | Sección nueva del tallo «Por qué no se puede ahorrar más»: análisis de descartados dentro de `build_app.py`, gráfico de ahorro por época de entrenamiento, subsección transplant-vs-calibración, «Cómo lo sabemos» | pendiente |
| T2 | S4 | Revamp de El modelo: gráfico de familias (ahorro ± desvío), curva recall vs llamadas con 0,95 y 0,80, ahorro desde (0,0), número protagonista (89 llamadas menos de 1.092 por 23 de 542 sí), baseline = estrategia del banco | pendiente |
| T3 | S3 | Hallazgos: qué es OTRO, etiqueta eje Y, hipótesis fallidas | pendiente |
| T4 | S2 | Portada/intro: oración central honesta, tres números, caja versus, contexto, CSS renovado | pendiente |
| T5 | S5 | Copa: aclarar Saldo; selector eje Y si hay tiempo | pendiente |
| T6 | S7 | Cierre: README, coherencia con notebook, reparto de explicación | pendiente |

## Log

- L1 (usuario): "Estamos con un proyecto integrador… En la entrega 4 tuvimos que hacer un app para mostrar todo este proceso. El problema es que presentamos y tenemos varias cosas por corregir… Idea un plan para poder mejorar todas estas cosas, y vamos a conversar y llegar a la mejor manera de resolver todos estos problemas."
- L2 (usuario, decisiones): idea extra del profesor incluida; sección nueva del tallo para el techo; CSS + portada renovada (sin reestructura); leer todas las versiones de la Entrega 3 antes de arrancar.
- L3 (usuario): elegir ángulo narrativo "Las dos historias en capas" para la sección del techo.
- L4 (evidencia, análisis descartados, semilla 42, código de la app): dentro de la era vieja CV ahorro 4,1% ± 3,8% (ruido; un shot 10% con recall 0,93); transplant del umbral al test nuevo: 0,4% de ahorro; descartados + calibración en dev: 1.004 llamadas, 519/542, 1,93 llamadas/sí, 3,98%; V4: 1.003, 519/542, 4,08%. AP 0,685 (viejo) vs 0,680 (V4) en el mismo test. El techo ~4% queda demostrado con dos épocas disjuntas de entrenamiento. Script scratch: /tmp/analisis_descartados.py.
