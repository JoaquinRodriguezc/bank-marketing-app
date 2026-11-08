import json
import sys
from pathlib import Path
import nbformat as nbf

destino = Path(sys.argv[1])
conclusion = Path(sys.argv[2]).read_text() if len(sys.argv) > 2 else "## Conclusión\n\n(pendiente)"

M = nbf.v4.new_markdown_cell
C = nbf.v4.new_code_cell

celdas = [
M("""# V4 · Modelado con la métrica del negocio

**Qué cambió desde la defensa de la Entrega 3.** El docente nos marcó que el F1 no responde la pregunta del proyecto. El banco no quiere un equilibrio abstracto entre precision y recall: quiere **llamar sólo a quienes van a decir que sí**, sin que se escape casi ninguno, y que cada "sí" le cueste la menor cantidad de llamadas posible.

| Decisión | V2 (defensa) | V4 (este notebook) |
|---|---|---|
| Métrica | F1 con umbral elegido | **Precision con recall ≥ 0,95**, leída como **llamadas por cada sí = 1 / precision** |
| Piso | Dummy y siempre-yes | **Llamar a todos**: recall 1, precision = tasa de sí |
| Datos | 80 % viejo para entrenar, 20 % reciente reservado | **Llamadas desde junio de 2009**, partidas 80/20 por tiempo |

- **Por qué precision y recall separados.** Fijamos cuánto recall exigimos (que se escape como mucho 1 de cada 20 "sí") y, con eso fijo, buscamos el modelo que más sube la precision. Un F1 o un F-beta mezclaría las dos cosas en un número que no se lee en llamadas.
- **Por qué 0,95 y no 1.** Con recall = 1 el umbral queda en el puntaje del "sí" peor puntuado, que es un solo cliente. Ese umbral cambia mucho de un período a otro y en el test casi nunca se sostiene. Igual mostramos la curva completa entre 0,80 y 1,0.
- **Por qué sólo las llamadas desde junio de 2009.** La tasa de sí cambia muchísimo en el tiempo, y las llamadas recientes son las que se parecen al uso actual.
- **Aviso sobre el test.** Una versión anterior (V3) ya se midió sobre un test que contiene a este. Este test no es virgen: el modelo y el umbral se eligieron con validación cruzada, pero el número del test hay que leerlo sabiendo eso.
- **No tenemos el monto depositado**, así que el costo se mide en llamadas, no en pesos.

Para correrlo (también en Colab) tienen que estar en la misma carpeta `_bank_marketing_silver.csv`, `modelado_v3.py`, `modelado_v2_e2.py` y `transformadores.py`. Las versiones exactas están en `requirements_v3.txt`."""),
C("""import platform, hashlib, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import confusion_matrix, classification_report, make_scorer
from sklearn.inspection import permutation_importance
import joblib
from transformadores import COLUMNAS_ENTRADA
import modelado_v3 as m3
SEED = 42
np.random.seed(SEED)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 180)
warnings.filterwarnings("ignore", message="Skipping features without any observed values.*", category=UserWarning)
print({"python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__,
       "sklearn": sklearn.__version__, "seed": SEED, "recall_min": m3.RECALL_MIN})"""),
M("""## 1. Datos

Se deriva la fecha de cada contacto, se ordena por tiempo y se toman las llamadas desde junio de 2009. Esas filas se parten por tiempo: el 80 % más viejo es el entrenamiento, donde se hace la validación cruzada, y el 20 % más nuevo es el test, que se mira **una sola vez** al final."""),
C("""archivo = Path("_bank_marketing_silver.csv")
print("SHA256 CSV:", hashlib.sha256(archivo.read_bytes()).hexdigest())
df = pd.read_csv(archivo).rename(columns={"contact": "contact_type", "y": "deposit_subscribed"})
meses = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
num_mes = df["month"].str.lower().map(meses)
assert num_mes.notna().all(), "Mes desconocido"
anios, anio, anterior = [], 2008, 4
for mes in num_mes:
    if mes < anterior:
        anio += 1
    anios.append(anio)
    anterior = mes
df["contact_date"] = pd.to_datetime(pd.DataFrame({"year": anios, "month": num_mes, "day": df["day"]}))
df = df.sort_values(["contact_date", "contact_id"], kind="stable").reset_index(drop=True)
assert df["deposit_subscribed"].isin(["yes", "no"]).all()
columnas = COLUMNAS_ENTRADA + ["previous"]
reciente = df[df.contact_date >= "2009-06-01"].reset_index(drop=True)
assert len(reciente) == 5459
corte2 = int(len(reciente) * 0.8)
X_tr, X_te = reciente.iloc[:corte2][columnas], reciente.iloc[corte2:][columnas]
y_tr = reciente.iloc[:corte2]["deposit_subscribed"].eq("yes").astype(int)
y_te = reciente.iloc[corte2:]["deposit_subscribed"].eq("yes").astype(int)
cortes = list(TimeSeriesSplit(n_splits=5).split(X_tr))

si = df["deposit_subscribed"].eq("yes")
display(pd.DataFrame([
    {"tramo": "dataset completo", "filas": len(df), "desde": df.contact_date.min().date(), "hasta": df.contact_date.max().date(), "tasa_si": si.mean()},
    {"tramo": "antes de junio 2009 (no se usa)", "filas": int((df.contact_date < "2009-06-01").sum()), "desde": df.contact_date.min().date(), "hasta": df.contact_date[df.contact_date < "2009-06-01"].max().date(), "tasa_si": si[df.contact_date < "2009-06-01"].mean()},
    {"tramo": "desde junio 2009 (se usa)", "filas": len(reciente), "desde": reciente.contact_date.iloc[0].date(), "hasta": reciente.contact_date.iloc[-1].date(), "tasa_si": reciente.deposit_subscribed.eq("yes").mean()},
    {"tramo": "  entrenamiento (80 %)", "filas": len(X_tr), "desde": reciente.contact_date.iloc[0].date(), "hasta": reciente.contact_date.iloc[corte2-1].date(), "tasa_si": y_tr.mean()},
]).assign(llamadas_por_si=lambda t: 1 / t.tasa_si).round(4))
print("Test reservado:", len(X_te), "filas, desde", reciente.contact_date.iloc[corte2].date(), "— su tasa de sí se mira recién en la sección 5.")
display(pd.DataFrame([{"fold": i, "n_entrena": len(tr), "n_valida": len(va),
    "valida_desde": reciente.contact_date.iloc[va[0]].date(), "valida_hasta": reciente.contact_date.iloc[va[-1]].date(),
    "tasa_si_valida": y_tr.iloc[va].mean()} for i, (tr, va) in enumerate(cortes, 1)]).round(3))"""),
M("""## 2. Cómo se lee la métrica

Para cada modelo y cada fold de validación:

1. El modelo ordena a los clientes del fold por probabilidad de decir que sí.
2. Se baja el umbral hasta conseguir al menos el 95 % de los "sí" del fold (recall ≥ 0,95) y se toma el umbral con mejor precision.
3. Se reporta la **precision** (tasa de sí entre los llamados) y las **llamadas por sí** (1 / precision).

**Aclaración honesta:** en la validación cruzada el umbral se elige mirando el mismo fold que se mide. Sirve para **comparar modelos entre sí** en igualdad de condiciones, pero es optimista. En el test el umbral se fija **antes** de mirar (sección 5).

**La tasa de sí cambia bastante entre el primer y el último fold** (ver la tabla de la sección 1). Por eso la precision promedio tiene un desvío enorme que no habla del modelo sino del período. Para comparar modelos usamos el **ahorro**: cuánto bajan las llamadas por sí respecto de llamar a todos en ese mismo fold (`1 − tasa_si / precision`). Dentro de cada fold, el ahorro ordena igual que la precision.

El **piso** es `DummyClassifier(strategy="prior")`: le da el mismo puntaje a todos, así que para tener recall ≥ 0,95 tiene que llamar a todos. Precision = tasa de sí, ahorro = 0."""),
M("""## 3. Comparación de modelos

Las columnas son las del conjunto conservador de la Entrega 2 (`e2_deudas`): sin `duration` (fuga), y sin `campaign`, `contact`, `day` ni `month`, porque no está acreditado que se conozcan antes de la llamada. Todo va adentro del pipeline (derivar columnas → imputar → escalar / one-hot → modelo).

- **Logística**: C ∈ {0,1; 1; 10; 100} × `class_weight` ∈ {ninguno, balanced}. Es la referencia.
- **Árbol, bosque y boosting**: una configuración regularizada cada uno, con las mismas columnas y la misma validación.
- **Ablación**: la misma logística (C = 10) con las mismas columnas más `month` y `contact_type`, para mostrar el número con y sin esas dos columnas."""),
C("""candidatos = [("piso", "e2_deudas", {})]
candidatos += [("logistica", "e2_deudas", dict(C=C, class_weight=w)) for C in (0.1, 1.0, 10.0, 100.0) for w in (None, "balanced")]
candidatos += [
    ("arbol", "e2_deudas", dict(max_depth=4, min_samples_leaf=50)),
    ("bosque", "e2_deudas", dict(max_depth=8, min_samples_leaf=20)),
    ("boosting", "e2_deudas", dict(learning_rate=0.05, max_iter=200, max_leaf_nodes=7, min_samples_leaf=50)),
    ("logistica", "e2_deudas_mes_contacto", dict(C=10.0, class_weight=None)),
]
tabla, por_fold = m3.buscar(candidatos, X_tr, y_tr, cortes)
print("Tabla completa, ordenada por ahorro medio (validación cruzada temporal, 5 folds):")
display(tabla.sort_values("ahorro_media", ascending=False).round(4))
print("Ahorro por fold (filas = fold, columnas = candidato):")
display(por_fold.pivot(index="fold", columns="candidato", values="ahorro_llamadas").round(4))
tabla.to_csv("v4_busqueda_completa.csv", index=False)
por_fold.to_csv("v4_por_fold.csv", index=False)"""),
M("""### Elección

Regla de parsimonia de la consigna: se toma el candidato con mayor ahorro medio, salvo que sea más complejo que la mejor logística y le gane por menos que el desvío de la logística. En ese caso se queda la logística. La ablación con `month` y `contact_type` **no compite**: incluye columnas que la Entrega 2 descartó por posible fuga, así que sólo se informa como evidencia."""),
C("""elegible = tabla[tabla.modo.eq("e2_deudas")]
eleccion = m3.elegir(elegible)
familia, modo, params = candidatos[int(eleccion.candidato)]
display(eleccion.to_frame().T)
print("Modelo elegido:", familia, modo, params)
ref = elegible[elegible.familia.ne("piso")].sort_values("ahorro_media", ascending=False)
print("Diferencia con el segundo:", round(ref.ahorro_media.iloc[0] - ref.ahorro_media.iloc[1], 5))
abl = tabla[tabla.modo.eq("e2_deudas_mes_contacto")].iloc[0]
print(f"Ablación con month y contact_type: ahorro {abl.ahorro_media:.4f} ± {abl.ahorro_desvio:.4f} contra {eleccion.ahorro_media:.4f} ± {eleccion.ahorro_desvio:.4f} sin ellas.")
display(por_fold[por_fold.candidato.eq(int(eleccion.candidato))].round(4))"""),
M("""## 4. Cuántos "sí" estamos dispuestos a perder

Esta tabla responde la pregunta del docente: **cuántas llamadas al pedo aceptamos con tal de que no se escape nadie**. Para el modelo elegido se repite la validación con distintos recall mínimos. Llamar a todos es la referencia: siempre consigue el 100 % de los sí."""),
C("""curva = []
for r in (0.80, 0.85, 0.90, 0.95, 1.00):
    d = m3.evaluar(familia, modo, params, X_tr, y_tr, cortes, recall_min=r)
    curva.append({"recall_min": r, "si_perdidos_de_100": round(100 * (1 - d.recall.mean()), 1),
                  "precision_media": d.precision.mean(), "llamadas_por_si_media": d.llamadas_por_si.mean(),
                  "ahorro_media": d.ahorro_llamadas.mean(), "ahorro_desvio": d.ahorro_llamadas.std(ddof=0),
                  "ahorro_fold5": d.ahorro_llamadas.iloc[-1]})
curva = pd.DataFrame(curva)
piso = por_fold[por_fold.familia.eq("piso")]
print(f"Llamar a todos: {piso.llamadas_por_si.mean():.3f} llamadas por sí en promedio de los folds; {piso.llamadas_por_si.iloc[-1]:.3f} en el fold 5.")
display(curva.round(4))
curva.to_csv("v4_curva_recall.csv", index=False)
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(curva.recall_min, 100 * curva.ahorro_media, marker="o", label="modelo elegido (media de folds)")
ax.plot(curva.recall_min, 100 * curva.ahorro_fold5, marker="s", linestyle="--", label="modelo elegido (fold 5, el más reciente)")
ax.axhline(0, color="gray", label="llamar a todos")
ax.set_xlabel("recall mínimo exigido")
ax.set_ylabel("% menos llamadas por sí que llamar a todos")
ax.set_title("Cuánto ahorra el modelo según cuántos sí aceptamos perder")
ax.legend()
plt.show()"""),
M("""## 5. Test: una sola vez

El umbral se fija **antes** de mirar el test: es el umbral que logró recall ≥ 0,95 en el **fold 5**, el período más reciente del entrenamiento y el que más se parece al test. Así se imita el uso: se calibra con lo último que se vio. Después el modelo se entrena con todo el entrenamiento y se aplica una sola vez al test. El recall que salga se informa tal como sale, aunque no sea 0,95."""),
C("""umbral = float(eleccion.umbral_fold5)
final = m3.construir(familia, modo, **params).fit(X_tr, y_tr)
p_te = final.predict_proba(X_te)[:, 1]
yt = y_te.to_numpy()
resultado = pd.DataFrame([
    {"estrategia": "llamar a todos", **m3.medir(yt, p_te, -np.inf)},
    {"estrategia": f"modelo, umbral {umbral:.4f}", **m3.medir(yt, p_te, umbral)},
]).set_index("estrategia")
resultado["llamadas_ahorradas"] = resultado.llamadas.iloc[0] - resultado.llamadas
resultado["si_perdidos"] = resultado.si_totales - resultado.si_conseguidos
resultado["ahorro_llamadas_por_si"] = 1 - resultado.llamadas_por_si / resultado.llamadas_por_si.iloc[0]
display(resultado.round(4))
pred = (p_te >= umbral).astype(int)
cm = confusion_matrix(yt, pred)
etiquetas = dict(index=["real no", "real sí"], columns=["no llamar", "llamar"])
print("Matriz de confusión (cantidades):"); display(pd.DataFrame(cm, **etiquetas))
print("Normalizada por fila (de cada clase real, qué hizo el modelo):"); display(pd.DataFrame(cm / cm.sum(1, keepdims=True), **etiquetas).round(3))
print("Normalizada por columna (de cada decisión, qué había):"); display(pd.DataFrame(cm / cm.sum(0, keepdims=True), **etiquetas).round(3))
print(classification_report(yt, pred, target_names=["no", "sí"], digits=3))
resultado.to_csv("v4_test.csv")"""),
M("""## 6. En qué se apoya el modelo

Importancia por permutación sobre el test: cuánto empeora el ordenamiento (average precision) al mezclar cada columna de entrada. Se muestran sólo las columnas que el pipeline usa."""),
C("""imp = permutation_importance(final, X_te, y_te, scoring="average_precision", n_repeats=20, random_state=SEED)
importancia = pd.DataFrame({"columna": X_te.columns, "media": imp.importances_mean, "desvio": imp.importances_std})
importancia = importancia[importancia.media.abs() > 1e-9].sort_values("media", ascending=False)
display(importancia.round(4))
modelo = final.named_steps["modelo"]
if hasattr(modelo, "coef_"):
    nombres = final.named_steps["preparar"].get_feature_names_out()
    coef = pd.Series(modelo.coef_[0], index=nombres).sort_values(key=abs, ascending=False)
    print("Coeficientes de la logística (escala estandarizada), los 12 de mayor módulo:")
    display(coef.head(12).round(3).to_frame("coeficiente"))
joblib.dump(final, "modelo_final_v4.joblib")
print("Guardado modelo_final_v4.joblib. Umbral:", round(umbral, 6))"""),
M(conclusion),
]

nb = nbf.v4.new_notebook()
nb.cells = celdas
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
nbf.write(nb, destino)
print("escrito", destino, len(celdas), "celdas")
