## Conclusión

**El resultado en el test (1.092 llamadas, de julio a noviembre de 2010):**

| | Llamadas | Sí conseguidos | Tasa de sí (precision) | Llamadas por sí | Ahorro por sí |
|---|---|---|---|---|---|
| Llamar a todos | 1.092 | 542 de 542 | 49,6 % | 2,01 | — |
| **Modelo** | 1.003 | 519 de 542 (recall 0,958) | 51,7 % | **1,93** | **4,1 %** |

- **Con el modelo, cada sí cuesta 4,1 % menos llamadas (1,93 contra 2,01).** En total son 89 llamadas menos (−8,2 %) a cambio de perder 23 de los 542 sí (−4,2 %). El recall exigido se sostuvo: 0,958 contra el mínimo de 0,95.
- **La validación lo anticipó.** El ahorro medio en validación fue 4,5 % y el test dio 4,1 %.
- **Por qué este modelo.** La logística con C = 1 y `class_weight="balanced"` tiene el mayor ahorro medio (4,5 % ± 1,6 %). Las otras logísticas quedan a menos de 0,2 puntos: el resultado no depende de afinar C. El boosting (3,2 %), el bosque (2,5 %) y el árbol (1,3 %) quedan por debajo, así que se queda la simple.
- **Desbalance.** La tasa de sí del entrenamiento es 44,5 %: ya casi no hay desbalance. `balanced` gana por 0,1 punto, una diferencia que no significa nada.
- **Lo que probamos y no sirvió.** Agregar `month` y `contact_type` no mejora (4,3 % contra 4,5 %). Además, la Entrega 2 las descartó por posible fuga, así que no entran.
- **En qué se apoya.** `poutcome`, el resultado de la campaña anterior, explica casi todo: haber dicho que sí antes es el coeficiente más alto (+0,92). No es fuga, porque se conoce antes de llamar. El resto de las columnas aporta muy poco.
- **El costo de cada punto de recall (sección 4).** Aceptando perder 18 de cada 100 sí (recall 0,80), el ahorro sube a 10 %. La decisión de dónde pararse es de negocio: conviene bajar el recall sólo si un sí vale menos que las llamadas que se ahorran.
- **Aviso honesto.** Este test está contenido en el test que ya miramos en V3, así que no es virgen. El modelo y el umbral se eligieron con validación cruzada, sin mirar el test.
- **Lo que no apareció.** Un modelo que baje mucho más el costo sin perder clientes. Con las columnas que se conocen antes de llamar, el techo está alrededor del 4–5 % de ahorro con recall 0,95.
