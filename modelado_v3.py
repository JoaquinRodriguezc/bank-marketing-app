"""V3: precision con recall mínimo fijo, sobre el último 20 % temporal."""
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.base import BaseEstimator, TransformerMixin
from modelado_v2_e2 import construir as construir_v2, VariablesE2

RECALL_MIN = 0.95

FAMILIAS = {
    "piso": lambda p: DummyClassifier(strategy="prior"),
    "logistica": lambda p: LogisticRegression(max_iter=3000, random_state=42, **p),
    "arbol": lambda p: DecisionTreeClassifier(random_state=42, **p),
    "bosque": lambda p: RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1, **p),
    "boosting": lambda p: HistGradientBoostingClassifier(early_stopping=False, random_state=42, **p),
}


class ConMesYContacto(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return VariablesE2("e2_deudas").transform(X).assign(
            month=X["month"], contact_type=X["contact_type"].fillna("unknown"))


def construir(familia, modo="e2_deudas", **params):
    base = construir_v2(dict(familia="logistica", modo="e2_deudas"))
    pasos = base.steps[:-1]
    if modo == "e2_deudas_mes_contacto":
        pasos[0] = ("derivar", ConMesYContacto())
    elif modo != "e2_deudas":
        raise ValueError(modo)
    return Pipeline(pasos + [("modelo", FAMILIAS[familia](params))])


def precision_con_recall(y, p, recall_min=RECALL_MIN):
    precision, recall, umbrales = precision_recall_curve(y, p)
    ok = recall[:-1] >= recall_min
    i = np.flatnonzero(ok)[np.argmax(precision[:-1][ok])]
    return precision[i], recall[i], umbrales[i]


def medir(y, p, umbral):
    llamar = p >= umbral
    tp = int((llamar & (y == 1)).sum())
    return dict(llamadas=int(llamar.sum()), si_conseguidos=tp, si_totales=int(y.sum()),
                precision=float(tp / max(llamar.sum(), 1)), recall=float(tp / y.sum()),
                llamadas_por_si=float(llamar.sum() / max(tp, 1)))


def evaluar(familia, modo, params, X, y, cortes, recall_min=RECALL_MIN):
    filas = []
    for fold, (tr, va) in enumerate(cortes, 1):
        p = construir(familia, modo, **params).fit(X.iloc[tr], y.iloc[tr]).predict_proba(X.iloc[va])[:, 1]
        yv = y.iloc[va].to_numpy()
        prec, rec, umbral = precision_con_recall(yv, p, recall_min)
        filas.append(dict(fold=fold, tasa_si=float(yv.mean()), precision=float(prec), recall=float(rec),
                          umbral=float(umbral), llamadas_por_si=float(1 / prec),
                          ahorro_llamadas=float(1 - yv.mean() / prec), ap=float(average_precision_score(yv, p))))
    return pd.DataFrame(filas)


def resumir(familia, modo, params, d):
    return {k: (float(v) if isinstance(v, np.floating) else v) for k, v in dict(familia=familia, modo=modo, params=str(params),
                precision_media=d.precision.mean(), precision_desvio=d.precision.std(ddof=0),
                ahorro_media=d.ahorro_llamadas.mean(), ahorro_desvio=d.ahorro_llamadas.std(ddof=0),
                llamadas_por_si_media=d.llamadas_por_si.mean(), recall_media=d.recall.mean(),
                umbral_fold5=d.umbral.iloc[-1], ap_media=d.ap.mean()).items()}


def buscar(candidatos, X, y, cortes, recall_min=RECALL_MIN):
    resumen, detalle = [], []
    for i, (familia, modo, params) in enumerate(candidatos):
        d = evaluar(familia, modo, params, X, y, cortes, recall_min)
        detalle.append(d.assign(candidato=i, familia=familia, modo=modo, params=str(params)))
        resumen.append(dict(candidato=i, **resumir(familia, modo, params, d)))
    return pd.DataFrame(resumen), pd.concat(detalle, ignore_index=True)


def elegir(tabla):
    modelos = tabla[tabla.familia.ne("piso")].sort_values("ahorro_media", ascending=False)
    mejor = modelos.iloc[0]
    simple = modelos[modelos.familia.eq("logistica")].iloc[0]
    return simple if mejor.ahorro_media - simple.ahorro_media <= simple.ahorro_desvio else mejor
