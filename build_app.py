import ast
import hashlib
import json
import warnings
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import TimeSeriesSplit

import modelado_v3 as m3
from transformadores import COLUMNAS_ENTRADA

warnings.filterwarnings("ignore", message="Skipping features without any observed values.*", category=UserWarning)
alt.data_transformers.disable_max_rows()

RAIZ = Path(__file__).parent
CSV = RAIZ / "datos" / "_bank_marketing_silver.csv"
SALIDA = RAIZ / "index.html"
SEED = 42
INICIO = "2009-06-01"
COLUMNAS = COLUMNAS_ENTRADA + ["previous"]

AZUL, NARANJA, ROJO, GRIS = "#0072B2", "#E69F00", "#D55E00", "#9a9a9a"
CATEGORIAS = ["Llamado y dijo sí", "Llamado y dijo no", "No llamado, pero decía sí", "No llamado y decía no"]
COLORES = [AZUL, NARANJA, ROJO, "#c9c9c9"]

OCUPACION = {"admin.": "Administrativo", "blue-collar": "Obrero", "entrepreneur": "Emprendedor",
             "housemaid": "Empleada doméstica", "management": "Gerencial", "retired": "Jubilado",
             "self-employed": "Cuentapropista", "services": "Servicios", "student": "Estudiante",
             "technician": "Técnico", "unemployed": "Desempleado", "desconocido": "Desconocida"}
EDUCACION = {"primary": "Primaria", "secondary": "Secundaria", "tertiary": "Terciaria", "desconocido": "Desconocida"}
ANTERIOR = {"success": "Éxito", "failure": "Fracaso", "other": "Otro", "sin_historial": "Sin contacto previo",
            "desconocido_con_historial": "Desconocido (con contacto previo)"}
SI_NO = {"yes": "Sí", "no": "No"}
NOMBRES_NUM = {"age": "Edad", "balance_signed_log": "Saldo (log con signo)", "previous_log": "Contactos anteriores (log)",
               "tiene_historial": "Tuvo contacto previo", "dias_desde_contacto": "Días desde el contacto anterior",
               "saldo_por_hipoteca": "Saldo × hipoteca", "saldo_por_prestamo": "Saldo × préstamo",
               "missingindicator_dias_desde_contacto": "Sin contacto previo (indicador)"}
NOMBRES_CAT = {"job": ("Ocupación", OCUPACION), "education": ("Educación", EDUCACION), "housing": ("Hipoteca", SI_NO),
               "loan": ("Préstamo", SI_NO), "poutcome_limpio": ("Resultado anterior", ANTERIOR)}

CONFIG = dict(font="Segoe UI, Helvetica, Arial, sans-serif")


def num(x, dec=0):
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(x, dec=0):
    return num(100 * x, dec) + " %"


def tema(chart):
    return (chart.configure(**CONFIG).configure_view(stroke=None)
            .configure_axis(labelFontSize=13, titleFontSize=13, titleFontWeight="normal", labelColor="#555",
                            titleColor="#555", gridColor="#ececec", domainColor="#bbb", tickColor="#bbb")
            .configure_legend(labelFontSize=13, titleFontSize=13, titleColor="#555")
            .configure_title(fontSize=15, anchor="start", color="#1a1a1a"))


def cargar():
    df = pd.read_csv(CSV).rename(columns={"contact": "contact_type", "y": "deposit_subscribed"})
    meses = {m: i for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split(), 1)}
    num_mes = df["month"].str.lower().map(meses)
    assert num_mes.notna().all()
    anios, anio, anterior = [], 2008, 4
    for mes in num_mes:
        anio += mes < anterior
        anios.append(anio)
        anterior = mes
    df["contact_date"] = pd.to_datetime(pd.DataFrame({"year": anios, "month": num_mes, "day": df["day"]}))
    df = df.sort_values(["contact_date", "contact_id"], kind="stable").reset_index(drop=True)
    df["si"] = df["deposit_subscribed"].eq("yes").astype(int)
    return df


def modelar(df):
    reciente = df[df.contact_date >= INICIO].reset_index(drop=True)
    corte = int(len(reciente) * 0.8)
    X, y = reciente[COLUMNAS], reciente["si"]
    X_tr, X_te, y_tr, y_te = X.iloc[:corte], X.iloc[corte:], y.iloc[:corte], y.iloc[corte:]
    cortes = list(TimeSeriesSplit(n_splits=5).split(X_tr))
    candidatos = [("piso", "e2_deudas", {})]
    candidatos += [("logistica", "e2_deudas", dict(C=C, class_weight=w)) for C in (0.1, 1.0, 10.0, 100.0) for w in (None, "balanced")]
    candidatos += [("arbol", "e2_deudas", dict(max_depth=4, min_samples_leaf=50)),
                   ("bosque", "e2_deudas", dict(max_depth=8, min_samples_leaf=20)),
                   ("boosting", "e2_deudas", dict(learning_rate=0.05, max_iter=200, max_leaf_nodes=7, min_samples_leaf=50))]
    tabla, por_fold = m3.buscar(candidatos, X_tr, y_tr, cortes)
    eleccion = m3.elegir(tabla)
    familia, modo, params = candidatos[int(eleccion.candidato)]
    final = m3.construir(familia, modo, **params).fit(X_tr, y_tr)
    umbral = float(eleccion.umbral_fold5)
    p_te = final.predict_proba(X_te)[:, 1]
    oof = np.full(len(X_tr), np.nan)
    for tr, va in cortes:
        oof[va] = m3.construir(familia, modo, **params).fit(X_tr.iloc[tr], y_tr.iloc[tr]).predict_proba(X_tr.iloc[va])[:, 1]
    reciente["prob"] = np.concatenate([oof, p_te])
    reciente["parte"] = ["Entrenamiento (validación cruzada)"] * corte + ["Test"] * (len(reciente) - corte)
    return dict(reciente=reciente, corte=corte, tabla=tabla, por_fold=por_fold, eleccion=eleccion, final=final,
                umbral=umbral, params=params, X_tr=X_tr, X_te=X_te, y_te=y_te.to_numpy(), p_te=p_te, cortes=cortes)


def pasos_del_modelo(final):
    prep = final.named_steps["preparar"]
    nombres = list(prep.get_feature_names_out())
    num_pipe = prep.named_transformers_["num"]
    cat_pipe = prep.named_transformers_["cat"]
    num_cols = list(prep.transformers_[0][2])
    cat_cols = list(prep.transformers_[1][2])
    coef = final.named_steps["modelo"].coef_[0]
    return dict(nombres=nombres, coef=coef, b=float(final.named_steps["modelo"].intercept_[0]),
                mediana=dict(zip(num_cols, num_pipe.named_steps["imputar"].statistics_)),
                media=num_pipe.named_steps["escalar"].mean_, escala=num_pipe.named_steps["escalar"].scale_,
                num_cols=num_cols, cat_cols=cat_cols, categorias=cat_pipe.named_steps["onehot"].categories_)


JS_NUM = {
    "age": "edad",
    "balance_signed_log": "(saldo < 0 ? -1 : 1) * log(1 + abs(saldo))",
    "previous_log": "log(1 + previos)",
    "tiene_historial": "(previos > 0 ? 1 : 0)",
    "dias_desde_contacto": "(previos > 0 ? dias : {mediana})",
    "saldo_por_hipoteca": "(hipoteca == 'yes' ? (saldo < 0 ? -1 : 1) * log(1 + abs(saldo)) : 0)",
    "saldo_por_prestamo": "(prestamo == 'yes' ? (saldo < 0 ? -1 : 1) * log(1 + abs(saldo)) : 0)",
    "missingindicator_dias_desde_contacto": "(previos > 0 ? 0 : 1)",
}
JS_CAT = {"job": "ocupacion", "education": "educacion", "housing": "hipoteca", "loan": "prestamo",
          "poutcome_limpio": "(previos > 0 ? anterior : 'sin_historial')"}


def expresion_logit(pm):
    partes = [repr(pm["b"])]
    n_num = len(pm["media"])
    for i in range(n_num):
        nombre = pm["nombres"][i].split("__", 1)[1]
        x = JS_NUM[nombre].format(mediana=repr(float(pm["mediana"].get("dias_desde_contacto", 0))))
        partes.append(f"{float(pm['coef'][i])!r} * ({x} - {float(pm['media'][i])!r}) / {float(pm['escala'][i])!r}")
    i = n_num
    for col, cats in zip(pm["cat_cols"], pm["categorias"]):
        ramas = " : ".join(f"{JS_CAT[col]} == {json.dumps(str(c))} ? {float(pm['coef'][i + k])!r}" for k, c in enumerate(cats))
        partes.append(f"({ramas} : 0)")
        i += len(cats)
    return " + ".join(partes)


def logit_python(pm, filas):
    hist = filas["previous"].to_numpy() > 0
    saldo = filas["balance"].to_numpy().astype(float)
    bsl = np.sign(saldo) * np.log1p(np.abs(saldo))
    valores = {"age": filas["age"].to_numpy(), "balance_signed_log": bsl, "previous_log": np.log1p(filas["previous"].to_numpy()),
               "tiene_historial": hist.astype(float), "dias_desde_contacto": np.where(hist, filas["pdays"], pm["mediana"]["dias_desde_contacto"]),
               "saldo_por_hipoteca": bsl * filas["housing"].eq("yes").to_numpy(), "saldo_por_prestamo": bsl * filas["loan"].eq("yes").to_numpy(),
               "missingindicator_dias_desde_contacto": (~hist).astype(float)}
    z = np.full(len(filas), pm["b"])
    n_num = len(pm["media"])
    for i in range(n_num):
        z += pm["coef"][i] * (valores[pm["nombres"][i].split("__", 1)[1]] - pm["media"][i]) / pm["escala"][i]
    crudos = {"job": filas["job"].fillna("desconocido"), "education": filas["education"].fillna("desconocido"),
              "housing": filas["housing"], "loan": filas["loan"], "poutcome_limpio": poutcome_limpio(filas)}
    i = n_num
    for col, cats in zip(pm["cat_cols"], pm["categorias"]):
        for k, c in enumerate(cats):
            z += pm["coef"][i + k] * crudos[col].eq(c).to_numpy()
        i += len(cats)
    return z


def poutcome_limpio(filas):
    sin = np.where(filas["pdays"].eq(-1), "sin_historial", "desconocido_con_historial")
    return filas["poutcome"].fillna(pd.Series(sin, index=filas.index))


def grafico_datos(df):
    mensual = (df.assign(mes=df.contact_date.dt.to_period("M").dt.to_timestamp())
               .groupby("mes").agg(llamadas=("si", "size"), tasa=("si", "mean")).reset_index())
    mensual["mes_txt"] = mensual.mes.dt.strftime("%m/%Y")
    base = alt.Chart(mensual).encode(x=alt.X("mes:T", title=None, axis=alt.Axis(format="%b %Y", labelAngle=0, tickCount=10)))
    zona = alt.Chart(pd.DataFrame({"desde": [pd.Timestamp(INICIO)], "hasta": [mensual.mes.max() + pd.offsets.MonthEnd(1)]}))
    sombra = zona.mark_rect(color="#eef4f8").encode(x="desde:T", x2="hasta:T")
    rotulo = zona.mark_text(align="left", dx=6, dy=-4, baseline="bottom", color=AZUL, fontSize=13).encode(
        x="desde:T", y=alt.value(14), text=alt.value("Período que usa el modelo"))
    tooltip = [alt.Tooltip("mes_txt:N", title="Mes"), alt.Tooltip("llamadas:Q", title="Llamadas", format=",d"),
               alt.Tooltip("tasa:Q", title="Tasa de sí", format=".1%")]
    tasa = base.mark_line(color=AZUL, point=alt.OverlayMarkDef(color=AZUL, size=40)).encode(
        y=alt.Y("tasa:Q", title="Tasa de sí", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 0.7])), tooltip=tooltip)
    llamadas = base.mark_bar(color=GRIS, width=8).encode(y=alt.Y("llamadas:Q", title="Llamadas en el mes"), tooltip=tooltip)
    arriba = alt.layer(sombra, rotulo, tasa).properties(width=760, height=230)
    abajo = alt.layer(sombra, llamadas).properties(width=760, height=130)
    return tema(alt.vconcat(arriba, abajo, spacing=8).resolve_scale(x="shared"))


def tasa_por_anterior(df):
    t = df.assign(anterior=poutcome_limpio(df).map(ANTERIOR)).groupby("anterior").agg(n=("si", "size"), tasa=("si", "mean")).reset_index()
    return t.sort_values("tasa", ascending=False)


def grafico_hallazgo(df):
    t = tasa_por_anterior(df)
    t = t[t.n >= 30]
    t["rotulo"] = t.apply(lambda r: f"{pct(r.tasa)} de {num(r.n)}", axis=1)
    orden = t.anterior.tolist()
    y = alt.Y("anterior:N", sort=orden, title=None)
    barras = alt.Chart(t).mark_bar(color=AZUL, height=26).encode(
        y=y, x=alt.X("tasa:Q", title="Tasa de sí", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 0.75])),
        tooltip=[alt.Tooltip("anterior:N", title="Resultado anterior"), alt.Tooltip("n:Q", title="Clientes", format=",d"),
                 alt.Tooltip("tasa:Q", title="Tasa de sí", format=".1%")])
    texto = alt.Chart(t).mark_text(align="left", dx=6, fontSize=13, color="#1a1a1a").encode(y=y, x="tasa:Q", text="rotulo:N")
    media = df.si.mean()
    regla = alt.Chart(pd.DataFrame({"m": [media]})).mark_rule(color="#1a1a1a", strokeDash=[4, 3]).encode(x="m:Q")
    nota = alt.Chart(pd.DataFrame({"m": [media]})).mark_text(align="left", dx=4, dy=-112, fontSize=12.5, color="#1a1a1a").encode(
        x="m:Q", text=alt.value(f"Promedio de todos: {pct(media, 1)}"))
    return tema(alt.layer(barras, texto, regla, nota).properties(width=700, height=230))


def curva_test(y, p):
    filas = []
    for u in np.unique(p):
        llamar = p >= u
        tp = int((llamar & (y == 1)).sum())
        filas.append(dict(umbral=u, recall=tp / y.sum(), llamadas_por_si=llamar.sum() / max(tp, 1), llamadas=int(llamar.sum())))
    c = pd.DataFrame(filas)
    return c[c.recall >= 0.8].sort_values("recall")


def grafico_modelo(r):
    c = curva_test(r["y_te"], r["p_te"])
    elegido = m3.medir(r["y_te"], r["p_te"], r["umbral"])
    todos = len(r["y_te"]) / r["y_te"].sum()
    escala_x = alt.Scale(domain=[0.8, 1])
    x = alt.X("recall:Q", title="Sí conseguidos (de cada 100 que había)", axis=alt.Axis(format="%"), scale=escala_x)
    y = alt.Y("llamadas_por_si:Q", title="Llamadas por cada sí", scale=alt.Scale(zero=False))
    linea = alt.Chart(c).mark_line(color=AZUL, interpolate="step-after", clip=True).encode(
        x=x, y=y, tooltip=[alt.Tooltip("recall:Q", title="Sí conseguidos", format=".1%"),
                           alt.Tooltip("llamadas_por_si:Q", title="Llamadas por sí", format=".2f"),
                           alt.Tooltip("llamadas:Q", title="Llamadas", format=",d")])
    ref = pd.DataFrame({"y": [todos], "t": [f"Llamar a todos: {num(todos, 2)} llamadas por sí"]})
    regla = alt.Chart(ref).mark_rule(color=GRIS, strokeDash=[5, 4]).encode(y="y:Q")
    regla_t = alt.Chart(ref).mark_text(align="left", x=6, dy=-8, fontSize=13, color="#555").encode(y="y:Q", text="t:N")
    punto_df = pd.DataFrame({"recall": [elegido["recall"]], "llamadas_por_si": [elegido["llamadas_por_si"]],
                             "t": [f"Umbral elegido: {num(elegido['llamadas_por_si'], 2)} llamadas por sí, {pct(elegido['recall'], 1)} de los sí"]})
    punto = alt.Chart(punto_df).mark_point(color=AZUL, filled=True, size=140).encode(x=alt.X("recall:Q", scale=escala_x), y="llamadas_por_si:Q")
    punto_t = alt.Chart(punto_df).mark_text(align="right", dx=-10, dy=-14, fontSize=13, color=AZUL, fontWeight="bold").encode(
        x=alt.X("recall:Q", scale=escala_x), y="llamadas_por_si:Q", text="t:N")
    minimo = pd.DataFrame({"x": [m3.RECALL_MIN]})
    req = alt.Chart(minimo).mark_rule(color="#1a1a1a", strokeDash=[2, 3]).encode(x=alt.X("x:Q", scale=escala_x))
    req_t = alt.Chart(minimo).mark_text(align="right", dx=-4, y=12, fontSize=12.5, color="#1a1a1a").encode(
        x=alt.X("x:Q", scale=escala_x), text=alt.value("mínimo exigido: 95 %"))
    return tema(alt.layer(regla, regla_t, req, req_t, linea, punto, punto_t).properties(width=720, height=320))


def datos_explora(r):
    d = r["reciente"].dropna(subset=["prob"]).copy()
    saldo = d.balance.astype(float)
    out = pd.DataFrame({
        "Fecha": d.contact_date.dt.strftime("%d/%m/%Y"),
        "Edad": d.age, "Saldo (log con signo)": np.round(np.sign(saldo) * np.log1p(np.abs(saldo)), 3),
        "Contactos anteriores": d.previous, "saldo": d.balance,
        "ocupacion": d.job.fillna("desconocido").map(OCUPACION), "educacion": d.education.fillna("desconocido").map(EDUCACION),
        "hipoteca": d.housing.map(SI_NO), "prestamo": d.loan.map(SI_NO), "anterior": poutcome_limpio(d).map(ANTERIOR),
        "prob": np.round(d.prob, 4), "real": np.where(d.si == 1, "Sí", "No"), "parte": d.parte,
    })
    rng = np.random.default_rng(SEED)
    out["jy"] = np.round(rng.uniform(-0.4, 0.4, len(out)), 3)
    return out


def grafico_explora(r):
    d = datos_explora(r)
    umbral = alt.param(name="umbral", value=round(r["umbral"], 4),
                       bind=alt.binding_range(min=0.05, max=0.9, step=0.005, name="Umbral para llamar "))
    ocup = alt.param(name="ocup_sel", value="Todas", bind=alt.binding_select(options=["Todas"] + sorted(d.ocupacion.unique()), name="Ocupación "))
    ant = alt.param(name="ant_sel", value="Todos", bind=alt.binding_select(options=["Todos"] + sorted(d.anterior.unique()), name="Resultado anterior "))
    eje = alt.param(name="eje_y", value="Edad", bind=alt.binding_select(options=["Edad", "Saldo (log con signo)", "Contactos anteriores"], name="Eje vertical "))
    parte = alt.param(name="parte_sel", value="Todas", bind=alt.binding_radio(options=["Todas", "Entrenamiento (validación cruzada)", "Test"], name="Llamadas "))
    filtro = ("(ocup_sel == 'Todas' || datum.ocupacion == ocup_sel) && (ant_sel == 'Todos' || datum.anterior == ant_sel)"
              " && (parte_sel == 'Todas' || datum.parte == parte_sel)")
    categoria = ("datum.prob >= umbral ? (datum.real == 'Sí' ? 'Llamado y dijo sí' : 'Llamado y dijo no')"
                 " : (datum.real == 'Sí' ? 'No llamado, pero decía sí' : 'No llamado y decía no')")
    base = alt.Chart(d).transform_calculate(en_filtro=filtro, categoria=categoria, llamar="datum.prob >= umbral ? 1 : 0",
                                            exito="datum.real == 'Sí' ? 1 : 0")
    resumen_txt = ("datum.n == 0 ? 'Ningún cliente cumple el filtro' : format(datum.n, ',d') + ' clientes · el modelo llama a '"
                   " + format(datum.llamadas, ',d') + ' y consigue ' + format(datum.tp, ',d') + ' de ' + format(datum.sis, ',d') + ' sí ('"
                   " + format(datum.sis ? datum.tp / datum.sis : 0, '.0%') + ') · ' + (datum.tp ? format(datum.llamadas / datum.tp, '.2f') : '—')"
                   " + ' llamadas por sí, contra ' + (datum.sis ? format(datum.n / datum.sis, '.2f') : '—') + ' si llama a todos'")
    resumen = base.transform_filter("datum.en_filtro").transform_calculate(tp="datum.llamar * datum.exito").transform_aggregate(
        n="count()", llamadas="sum(llamar)", tp="sum(tp)", sis="sum(exito)").transform_calculate(t=resumen_txt).mark_text(
        align="left", fontSize=15, fontWeight="bold", color="#1a1a1a").encode(x=alt.value(0), y=alt.value(10), text="t:N").properties(width=760, height=20)
    tooltip = [alt.Tooltip("Fecha:N"), alt.Tooltip("Edad:Q"), alt.Tooltip("ocupacion:N", title="Ocupación"),
               alt.Tooltip("educacion:N", title="Educación"), alt.Tooltip("saldo:Q", title="Saldo (€)", format=",d"),
               alt.Tooltip("hipoteca:N", title="Hipoteca"), alt.Tooltip("prestamo:N", title="Préstamo"),
               alt.Tooltip("Contactos anteriores:Q"), alt.Tooltip("anterior:N", title="Resultado anterior"),
               alt.Tooltip("prob:Q", title="Probabilidad de sí (modelo)", format=".1%"),
               alt.Tooltip("categoria:N", title="Decisión y resultado"), alt.Tooltip("parte:N", title="Predicho en")]
    color = alt.condition("datum.en_filtro", alt.Color("categoria:N", title="Decisión del modelo y resultado real",
                          scale=alt.Scale(domain=CATEGORIAS, range=COLORES), legend=alt.Legend(orient="bottom", columns=2, titleLimit=0, labelLimit=0)), alt.value("#eeeeee"))
    puntos = base.transform_calculate(yv="datum[eje_y] + datum.jy", orden="datum.en_filtro ? 1 : 0").mark_circle(size=22).encode(
        x=alt.X("prob:Q", title="Probabilidad de sí según el modelo", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1])),
        y=alt.Y("yv:Q", title=None, scale=alt.Scale(zero=False, nice=False)), color=color,
        opacity=alt.condition("datum.en_filtro", alt.value(0.8), alt.value(0.4)), order="orden:Q", tooltip=tooltip)
    regla_df = pd.DataFrame({"k": [0]})
    regla = alt.Chart(regla_df).transform_calculate(u="umbral").mark_rule(color="#1a1a1a", strokeDash=[5, 4], size=1.5).encode(x="u:Q")
    regla_t = alt.Chart(regla_df).transform_calculate(u="umbral", t="'llama desde acá →'").mark_text(
        align="left", dx=4, y=8, fontSize=12.5, color="#1a1a1a").encode(x="u:Q", text="t:N")
    eje_t = alt.Chart(regla_df).mark_text(align="left", baseline="bottom", fontSize=13, color="#555", text=alt.expr("'↑ ' + eje_y")).encode(
        x=alt.value(0), y=alt.value(-6))
    principal = alt.layer(puntos, regla, regla_t, eje_t).properties(width=760, height=430)
    chart = alt.vconcat(resumen, principal, spacing=14).add_params(umbral, ocup, ant, eje, parte)
    return tema(chart)


def grafico_proba(r, pm, rango):
    params = [
        alt.param(name="edad", value=int(rango["edad"][2]), bind=alt.binding_range(min=rango["edad"][0], max=rango["edad"][1], step=1, name="Edad", element="#d-edad")),
        alt.param(name="ocupacion", value="management", bind=alt.binding_select(options=list(OCUPACION), labels=list(OCUPACION.values()), name="Ocupación", element="#d-ocupacion")),
        alt.param(name="educacion", value="secondary", bind=alt.binding_select(options=list(EDUCACION), labels=list(EDUCACION.values()), name="Educación", element="#d-educacion")),
        alt.param(name="hipoteca", value="no", bind=alt.binding_select(options=["yes", "no"], labels=["Sí", "No"], name="Hipoteca", element="#d-hipoteca")),
        alt.param(name="prestamo", value="no", bind=alt.binding_select(options=["yes", "no"], labels=["Sí", "No"], name="Préstamo", element="#d-prestamo")),
        alt.param(name="saldo", value=int(rango["saldo"][2]), bind=alt.binding_range(min=rango["saldo"][0], max=rango["saldo"][1], step=10, name="Saldo (€)", element="#d-saldo")),
        alt.param(name="previos", value=0, bind=alt.binding_range(min=0, max=rango["previos"][1], step=1, name="Contactos anteriores", element="#d-previos")),
        alt.param(name="dias", value=int(rango["dias"][2]), bind=alt.binding_range(min=rango["dias"][0], max=rango["dias"][1], step=1, name="Días desde el anterior", element="#d-dias")),
        alt.param(name="anterior", value="success", bind=alt.binding_select(
            options=["success", "failure", "other", "desconocido_con_historial"],
            labels=[ANTERIOR[k] for k in ["success", "failure", "other", "desconocido_con_historial"]], name="Resultado anterior", element="#d-anterior")),
    ]
    umbral = round(r["umbral"], 4)
    base = alt.Chart(pd.DataFrame({"k": [0]})).transform_calculate(z=expresion_logit(pm)).transform_calculate(
        p="1 / (1 + exp(-datum.z))").transform_calculate(
        decision=f"datum.p >= {umbral} ? 'Llamar' : 'No llamar'",
        t="format(datum.p, '.1%') + ' de probabilidad de sí → ' + datum.decision",
        nota="previos == 0 ? 'Sin contacto previo: los días y el resultado anterior no se usan' : ''")
    x = alt.X("p:Q", title=None, axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1]))
    fondo = alt.Chart(pd.DataFrame({"a": [0], "b": [1]})).mark_bar(color="#eef1f4", height=46).encode(x="a:Q", x2="b:Q")
    barra = base.mark_bar(height=46).encode(x=x, color=alt.Color("decision:N", scale=alt.Scale(domain=["Llamar", "No llamar"], range=[AZUL, GRIS]), legend=None))
    regla = alt.Chart(pd.DataFrame({"u": [umbral]})).mark_rule(color="#1a1a1a", strokeDash=[5, 4], size=2).encode(x="u:Q")
    regla_t = alt.Chart(pd.DataFrame({"u": [umbral]})).mark_text(align="left", dx=4, y=-14, fontSize=12.5, color="#1a1a1a").encode(
        x="u:Q", text=alt.value(f"umbral {pct(umbral, 1)}"))
    texto = base.mark_text(align="left", fontSize=18, fontWeight="bold", color="#1a1a1a").encode(x=alt.value(0), y=alt.value(-52), text="t:N")
    nota = base.mark_text(align="left", fontSize=13, color="#555").encode(x=alt.value(0), y=alt.value(84), text="nota:N")
    chart = alt.layer(fondo, barra, regla, regla_t, texto, nota).properties(width=420, height=46, padding={"top": 70, "bottom": 40, "left": 10, "right": 20})
    return tema(chart.add_params(*params))


def rangos(r):
    X = r["X_tr"]
    con = X[X.previous > 0]
    return {"edad": (int(X.age.min()), int(X.age.max()), int(X.age.median())),
            "saldo": (int(X.balance.min()), int(X.balance.max()), int(X.balance.median())),
            "previos": (0, int(X.previous.max())), "dias": (int(con.pdays.min()), int(con.pdays.max()), int(con.pdays.median()))}


def tabla_html(df):
    cab = "".join(f"<th>{c}</th>" for c in df.columns)
    filas = "".join("<tr>" + "".join(f"<td>{v}</td>" for v in fila) + "</tr>" for fila in df.itertuples(index=False))
    return f'<div class="tabla"><table><thead><tr>{cab}</tr></thead><tbody>{filas}</tbody></table></div>'


NOMBRE_FAMILIA = {"piso": "Piso (llamar a todos)", "logistica": "Regresión logística", "arbol": "Árbol de decisión",
                  "bosque": "Bosque aleatorio", "boosting": "HistGradientBoosting"}


def texto_params(fila):
    if fila.familia != "logistica":
        return "—"
    p = ast.literal_eval(fila.params)
    return f"C = {num(p['C'], 1) if p['C'] < 1 else num(p['C'])}, pesos {'balanceados' if p['class_weight'] else 'iguales'}"


def tabla_comparacion(tabla, cand):
    t = tabla.copy()
    t["Modelo"] = t.familia.map(NOMBRE_FAMILIA)
    t["Ajuste"] = t.apply(texto_params, axis=1)
    t["Ahorro de llamadas por sí"] = t.apply(lambda f: f"{pct(f.ahorro_media, 1)} ± {pct(f.ahorro_desvio, 1)}", axis=1)
    t["Precision"] = t.apply(lambda f: f"{num(f.precision_media, 3)} ± {num(f.precision_desvio, 3)}", axis=1)
    t["Recall"] = t.recall_media.map(lambda v: num(v, 3))
    t = t.sort_values("ahorro_media", ascending=False)
    t["Modelo"] = np.where(t.candidato == cand, "<b>" + t.Modelo + " (elegido)</b>", t.Modelo)
    return t[["Modelo", "Ajuste", "Ahorro de llamadas por sí", "Precision", "Recall"]]


def tabla_confusion(r):
    pred = (r["p_te"] >= r["umbral"]).astype(int)
    cm = confusion_matrix(r["y_te"], pred)
    fila = cm / cm.sum(1, keepdims=True)
    col = cm / cm.sum(0, keepdims=True)
    reales = ["Dijo no", "Dijo sí"]
    return pd.DataFrame({"Real \\ Decisión": reales,
                         "No llamar": [f"{num(cm[i, 0])} · {pct(fila[i, 0])} de la fila · {pct(col[i, 0])} de la columna" for i in range(2)],
                         "Llamar": [f"{num(cm[i, 1])} · {pct(fila[i, 1])} de la fila · {pct(col[i, 1])} de la columna" for i in range(2)]})


def nombre_coef(nombre, pm):
    tipo, resto = nombre.split("__", 1)
    if tipo == "num":
        return NOMBRES_NUM.get(resto, resto)
    for col, (etiqueta, mapa) in NOMBRES_CAT.items():
        if resto.startswith(col + "_"):
            valor = resto[len(col) + 1:]
            return f"{etiqueta}: {mapa.get(valor, valor)}"
    return resto


def tabla_coeficientes(pm):
    s = pd.Series(pm["coef"], index=[nombre_coef(n, pm) for n in pm["nombres"]]).sort_values()
    contra = [f"{k} ({num(v, 2)})" for k, v in s.head(5).items()]
    favor = [f"{k} ({num(v, 2)})" for k, v in s.tail(5)[::-1].items()]
    return pd.DataFrame({"Empujan hacia el sí": favor, "Empujan hacia el no": contra})


def hipotesis(df):
    t = tasa_por_anterior(df).set_index("anterior")
    media = df.si.mean()
    estudiante = df[df.job.eq("student")].si.mean()
    return dict(media=media, exito=t.loc["Éxito", "tasa"], n_exito=int(t.loc["Éxito", "n"]), lift_exito=t.loc["Éxito", "tasa"] / media,
                sin=t.loc["Sin contacto previo", "tasa"], estudiante=estudiante, lift_est=estudiante / media,
                n_est=int(df.job.eq("student").sum()))


def specs_json(graficos):
    return json.dumps({k: v.to_dict() for k, v in graficos.items()}, ensure_ascii=False)


def verificar(r, pm):
    z = logit_python(pm, r["X_te"])
    p = 1 / (1 + np.exp(-z))
    dif = np.abs(p - r["p_te"]).max()
    assert dif < 1e-9, dif
    return dif


def construir():
    df = cargar()
    r = modelar(df)
    pm = pasos_del_modelo(r["final"])
    verificar(r, pm)
    rango = rangos(r)
    graficos = {"g-datos": grafico_datos(df), "g-hallazgo": grafico_hallazgo(df), "g-modelo": grafico_modelo(r),
                "g-explora": grafico_explora(r), "g-proba": grafico_proba(r, pm, rango)}
    html = pagina(df, r, pm, graficos)
    SALIDA.write_text(html, encoding="utf-8")
    return r


def pagina(df, r, pm, graficos):
    from plantilla import armar
    return armar(df=df, r=r, pm=pm, specs=specs_json(graficos), h=hipotesis(df),
                 sha=hashlib.sha256(CSV.read_bytes()).hexdigest(), tablas=dict(
                     comparacion=tabla_html(tabla_comparacion(r["tabla"], int(r["eleccion"].candidato))),
                     confusion=tabla_html(tabla_confusion(r)), coef=tabla_html(tabla_coeficientes(pm))))


if __name__ == "__main__":
    r = construir()
    medida = m3.medir(r["y_te"], r["p_te"], r["umbral"])
    print("Umbral:", round(r["umbral"], 6), "| test:", {k: round(v, 4) for k, v in medida.items()})
    print("Escrito", SALIDA)
