"""Transformador propio del proyecto Bank Marketing (Entrega 3).

Vive en un archivo aparte (y no adentro del notebook) para que el pipeline guardado con
joblib se pueda volver a cargar desde la app de la Entrega 4: joblib guarda el *nombre* de la
clase, no su código, así que la app tiene que poder hacer `from transformadores import DerivarColumnas`.
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# las columnas crudas que el pipeline espera recibir (las mismas que va a mandar la app)
COLUMNAS_ENTRADA = ["age", "job", "marital", "education", "default", "balance", "housing", "loan",
                    "contact_type", "day", "month", "campaign", "pdays", "poutcome"]

ESTUDIANTE_O_JUBILADO = ["student", "retired"]


class DerivarColumnas(BaseEstimator, TransformerMixin):
    '''Arma las columnas que decidió la Entrega 2, a partir de las crudas.

    - poutcome: nulo -> "nunca_contactado" (no es un dato faltante, es un hecho).
    - contact_type: nulo -> "unknown".
    - pdays se parte en tiene_historial (0/1) y dias_desde_contacto (NaN sin historial;
      la imputación y el indicador los pone el paso preparar, que viene después).
    - campaign -> campaign_previas_log = log1p(campaign - 1): sólo los contactos ANTERIORES
      a la llamada actual, que son los que se conocen al decidir a quién llamar.
    - job: one-hot (lo hace preparar) o una sola columna es_estudiante_o_jubilado.

    Cada usar_* permite medir "con vs sin" sin tocar el resto del pipeline.
    No aprende nada de los datos: fit no guarda nada, así que no puede filtrar información del test.
    '''

    def __init__(self, usar_campaign=True, usar_mes=True, usar_dia=True, usar_historial=True,
                 job_como="onehot"):
        self.usar_campaign = usar_campaign
        self.usar_mes = usar_mes
        self.usar_dia = usar_dia
        self.usar_historial = usar_historial
        self.job_como = job_como

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X["poutcome"] = X["poutcome"].fillna("nunca_contactado")
        X["contact_type"] = X["contact_type"].fillna("unknown")

        if self.usar_historial:
            X["tiene_historial"] = (X["pdays"] != -1).astype(int)
            X["dias_desde_contacto"] = X["pdays"].where(X["pdays"] != -1, np.nan).astype(float)

        if self.usar_campaign:
            X["campaign_previas_log"] = np.log1p(X["campaign"] - 1)

        if self.job_como == "estudiante_o_jubilado":
            X["es_estudiante_o_jubilado"] = X["job"].isin(ESTUDIANTE_O_JUBILADO).astype(int)
            X = X.drop(columns="job")

        afuera = ["pdays", "campaign"]
        if not self.usar_mes:
            afuera.append("month")
        if not self.usar_dia:
            afuera.append("day")
        return X.drop(columns=afuera)
