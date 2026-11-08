import modelado_v3 as m3
from build_app import num, pct, INICIO, tabla_html
import pandas as pd

CSS = """
:root{--tinta:#1a1a1a;--gris:#555;--suave:#f4f5f6;--linea:#dcdfe3;--acento:#0072B2;--copa:#8a4b0f;--fondo:#fff}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:16px}
body{margin:0;background:var(--fondo);color:var(--tinta);font:18px/1.55 "Segoe UI",Helvetica,Arial,sans-serif}
nav{position:fixed;top:0;left:0;bottom:0;width:230px;padding:28px 18px;border-right:1px solid var(--linea);background:#fafbfc;overflow-y:auto}
nav .marca{font-size:13px;color:var(--gris);margin:0 0 22px}
nav h3{font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin:22px 0 6px;padding-left:12px}
nav .tallo h3{color:var(--acento)} nav .copa h3{color:var(--copa)}
nav ol{list-style:none;margin:0;padding:0 0 0 12px}
nav .tallo ol{border-left:3px solid var(--acento)} nav .copa ol{border-left:3px solid var(--copa)}
nav li a{display:block;padding:5px 0 5px 12px;color:var(--tinta);text-decoration:none;font-size:15px;line-height:1.3}
nav li a:hover,nav li a.activo{color:var(--acento);font-weight:600}
nav .copa li a:hover,nav .copa li a.activo{color:var(--copa)}
main{margin-left:230px;padding:0 48px 80px}
section{max-width:980px;margin:0 auto;padding:56px 0 24px;border-bottom:1px solid var(--linea)}
section:last-of-type{border-bottom:none}
.etapa{font-size:13px;letter-spacing:.08em;text-transform:uppercase;font-weight:600;margin:0 0 6px}
.etapa.tallo{color:var(--acento)} .etapa.copa{color:var(--copa)}
h1{font-size:40px;line-height:1.15;margin:0 0 18px;max-width:24ch}
h2{font-size:28px;line-height:1.25;margin:0 0 14px;max-width:46ch}
p,li{max-width:74ch}
.lead{font-size:21px;color:var(--gris);max-width:64ch}
.oracion{font-size:24px;line-height:1.4;border-left:5px solid var(--acento);padding:4px 0 4px 20px;margin:26px 0 34px;max-width:54ch}
.nums{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:10px 0 18px}
.num{background:var(--suave);border-radius:8px;padding:18px 20px}
.num span{display:block;font-size:44px;font-weight:700;line-height:1.1;color:var(--acento)}
.num p{margin:6px 0 0;font-size:15.5px;color:var(--gris)}
.grafico{margin:22px 0 10px;overflow-x:auto}
.nota{font-size:15px;color:var(--gris)}
details{background:var(--suave);border-radius:8px;padding:0 20px;margin:18px 0}
details[open]{padding-bottom:12px}
summary{cursor:pointer;font-weight:600;padding:14px 0;color:var(--acento)}
details h4{margin:16px 0 6px;font-size:17px}
details p,details li{font-size:16px}
.tabla{overflow-x:auto;margin:8px 0 14px}
table{border-collapse:collapse;font-size:15px;background:#fff}
th,td{border:1px solid var(--linea);padding:6px 10px;text-align:left;vertical-align:top}
th{background:#eef1f4;font-weight:600}
code{font-size:.9em;background:#eef1f4;padding:1px 5px;border-radius:4px}
.vega-bindings:empty{display:none}
.vega-bindings{display:flex;flex-wrap:wrap;gap:8px 22px;margin:14px 0 0;font-size:15px;padding:12px 16px;background:var(--suave);border-radius:8px}
.vega-bind{display:flex;align-items:center;gap:6px}
.vega-bind-name{font-weight:600}
.vega-bind select{font-size:15px;padding:4px 6px;max-width:330px}
.vega-bind-radio label{margin-right:10px}
.probar{display:grid;grid-template-columns:minmax(0,1fr) 480px;gap:24px;align-items:start}
.entradas{display:grid;grid-template-columns:1fr;gap:10px}
fieldset{border:1px solid var(--linea);border-radius:8px;padding:6px 12px 10px;margin:0}
legend{font-weight:600;font-size:14px;color:var(--gris);padding:0 4px}
.slot .vega-bind{margin:4px 0}
.slot .vega-bind label{display:grid;grid-template-columns:170px minmax(80px,1fr) 64px;align-items:center;gap:8px;font-size:14.5px}
.slot .vega-bind-name{font-weight:500}
.slot input[type=range]{width:100%;margin:0;accent-color:var(--copa)}
.slot select{font-size:14.5px;padding:3px 6px}
.slot .vega-bind-radio{display:flex;gap:10px;align-items:center}
.fijo{position:sticky;top:16px}
footer{max-width:980px;margin:0 auto;padding:30px 0;color:var(--gris);font-size:14px}
@media (max-width:1150px){.probar{grid-template-columns:1fr}.fijo{position:static}}
@media (max-width:860px){nav{display:none}main{margin-left:0;padding:0 16px 60px}.nums{grid-template-columns:1fr}h1{font-size:32px}}
"""

JS = """
const OPC = {actions: false, renderer: "svg",
  formatLocale: {decimal: ",", thousands: ".", grouping: [3], currency: ["", " €"], percent: " %"},
  timeFormatLocale: {dateTime: "%A, %e de %B de %Y, %X", date: "%d/%m/%Y", time: "%H:%M:%S", periods: ["AM", "PM"],
    days: ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"], shortDays: ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"],
    months: ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    shortMonths: ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]}};
window.vistas = {};
window.listo = Promise.all(Object.entries(SPECS).map(([id, s]) =>
  vegaEmbed("#" + id, s, OPC).then(r => { window.vistas[id] = r.view; })));
const enlaces = [...document.querySelectorAll("nav a")];
const obs = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting)
  enlaces.forEach(a => a.classList.toggle("activo", a.getAttribute("href") === "#" + e.target.id)); }), {rootMargin: "-40% 0px -55% 0px"});
document.querySelectorAll("section").forEach(s => obs.observe(s));
"""


def pasos_filtrado(df, r):
    antes = df[df.contact_date < INICIO]
    reciente = r["reciente"]
    corte = r["corte"]
    filas = [
        ("Dataset completo", num(len(df)), pct(df.si.mean(), 1), "Todos los contactos de las campañas, de mayo de 2008 a noviembre de 2010."),
        ("Desde junio de 2009", num(len(reciente)), pct(reciente.si.mean(), 1),
         f"Se dejan afuera los {num(len(antes))} contactos anteriores ({pct(antes.si.mean(), 1)} de sí): la tasa de sí cambió con el tiempo, y el período reciente es el que se parece al uso actual."),
        ("Entrenamiento (80 % más viejo)", num(corte), pct(reciente.si.iloc[:corte].mean(), 1),
         "Todo lo que se elige —modelo, C, pesos y umbral— se elige acá, con validación cruzada temporal."),
        ("Test (20 % más nuevo)", num(len(reciente) - corte), pct(reciente.si.iloc[corte:].mean(), 1),
         "Se separa por fecha y se mira una sola vez, con el modelo y el umbral ya fijos."),
    ]
    return pd.DataFrame(filas, columns=["Paso", "Contactos", "Tasa de sí", "Qué se hizo"])


def folds(r):
    rec = r["reciente"]
    filas = []
    for i, (tr, va) in enumerate(r["cortes"], 1):
        filas.append((i, num(len(tr)), f"{rec.contact_date.iloc[va[0]]:%d/%m/%Y} – {rec.contact_date.iloc[va[-1]]:%d/%m/%Y}",
                      num(len(va)), pct(rec.si.iloc[va].mean(), 1)))
    return pd.DataFrame(filas, columns=["Pedazo", "Entrena con", "Valida", "Contactos validados", "Tasa de sí validada"])


def armar(df, r, pm, specs, h, sha, tablas):
    t = m3.medir(r["y_te"], r["p_te"], r["umbral"])
    todos = len(r["y_te"]) / r["y_te"].sum()
    ahorro = 1 - t["llamadas_por_si"] / todos
    menos = len(r["y_te"]) - t["llamadas"]
    perdidos = t["si_totales"] - t["si_conseguidos"]
    e = r["eleccion"]
    hasta = df.contact_date.max()
    oracion = (f"Con lo que el banco sabe antes de llamar, el modelo consigue el {pct(t['recall'])} de los sí con "
               f"{num(menos)} llamadas menos, y cada sí cuesta {num(t['llamadas_por_si'], 2)} llamadas en vez de {num(todos, 2)}.")
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>¿A quién conviene llamar?</title>
<script src="https://cdn.jsdelivr.net/npm/vega@6.4.0"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-lite@6.4.1"></script>
<script src="https://cdn.jsdelivr.net/npm/vega-embed@7.3.0"></script>
<style>{CSS}</style></head>
<body>
<nav>
  <p class="marca">Ciencia de Datos · UTN FRM · 2026<br>Proyecto Integrador · Grupo 5K09-04</p>
  <div class="tallo"><h3>La historia</h3><ol>
    <li><a href="#portada" class="activo">El proyecto</a></li>
    <li><a href="#datos">Los datos</a></li>
    <li><a href="#hallazgos">Lo que encontramos</a></li>
    <li><a href="#modelo">El modelo</a></li></ol></div>
  <div class="copa"><h3>Tu turno</h3><ol>
    <li><a href="#explora">Explorá los clientes</a></li>
    <li><a href="#proba">Probá el modelo</a></li></ol></div>
</nav>
<main>

<section id="portada">
  <p class="etapa tallo">El proyecto</p>
  <h1>¿A quién conviene llamar para que cada depósito cueste menos llamadas?</h1>
  <p class="lead">Un banco portugués llamó a sus clientes para ofrecerles un depósito a plazo. Cada llamada cuesta tiempo de un operador.
  La pregunta es si, con lo que el banco ya sabe de un cliente antes de llamarlo, se puede dejar de llamar a algunos
  sin perder a los que iban a decir que sí.</p>
  <p class="oracion">{oracion}</p>
  <div class="nums">
    <div class="num"><span>{num(t['llamadas_por_si'], 2)}</span><p>llamadas por cada sí en el test, contra {num(todos, 2)} si se llama a todos</p></div>
    <div class="num"><span>{pct(t['recall'])}</span><p>de los {num(t['si_totales'])} sí del test, conseguidos: se escapan {num(perdidos)}</p></div>
    <div class="num"><span>−{pct(menos / len(r['y_te']))}</span><p>de llamadas: {num(t['llamadas'])} en vez de {num(len(r['y_te']))}</p></div>
  </div>
  <p class="nota">Medido sobre los {num(len(r['y_te']))} contactos más recientes (julio a noviembre de 2010) del dataset Bank Marketing,
  que el modelo no vio. La mejora es modesta, y la aplicación cuenta por qué.</p>
</section>

<section id="datos">
  <p class="etapa tallo">Los datos</p>
  <h2>La tasa de sí cambió con el tiempo: {pct(df[df.contact_date < INICIO].si.mean())} en las campañas viejas, {pct(r['reciente'].si.mean())} en las recientes</h2>
  <p>Arriba, qué parte de los contactos de cada mes terminó en un depósito; abajo, cuántos contactos hubo. En 2008 el banco hacía
  miles de llamadas por mes y muy pocos aceptaban. Desde mediados de 2009 llamó a mucha menos gente y casi la mitad dijo que sí.
  El modelo se entrena y se prueba en el período sombreado, que es el que se parece al uso actual.</p>
  <div class="grafico" id="g-datos"></div>
  <details><summary>Cómo lo sabemos</summary>
    <h4>De dónde salen</h4>
    <p>Del dataset <b>Bank Marketing</b> de UCI (Moro, Cortez y Rita, 2014), versión <code>bank-full</code>: {num(len(df))} contactos
    de las campañas de telemarketing de un banco portugués, de mayo de 2008 a noviembre de 2010. El pipeline del grupo lo deja como
    <code>datos/_bank_marketing_silver.csv</code> (SHA256 <code>{sha[:16]}…</code>), que es lo que lee <code>build_app.py</code>.</p>
    <p>El archivo no trae el año: viene ordenado en el tiempo, así que la fecha se reconstruye con el mes y el día, sumando un año cada vez que el mes vuelve atrás.</p>
    <h4>Qué es una fila</h4>
    <p>Un contacto de campaña con un cliente (<code>contact_id</code>), con los datos del cliente y del último contacto. La respuesta es
    <code>y</code>: si contrató el depósito. Como las filas son una secuencia en el tiempo, los pedazos de la validación se arman por fecha, nunca al azar.</p>
    <h4>Qué se filtró y qué quedó</h4>
    {tabla_html(pasos_filtrado(df, r))}
    <h4>Qué columnas quedan afuera por fuga</h4>
    <p><code>duration</code>, la duración de la llamada: se conoce recién cuando la llamada termina, y una llamada de cero segundos siempre es un no.
    Por precaución también quedan afuera <code>campaign</code>, <code>contact</code>, <code>day</code> y <code>month</code>: el dataset no
    permite asegurar que se conozcan antes de decidir a quién llamar.</p>
    <p>No son fuga, pero tampoco entran: <code>marital</code>, porque la hipótesis de que los casados aceptan menos se refutó en el análisis
    (lift 1,28, una diferencia que no alcanza el corte), y <code>default</code>, porque sólo el 1,8 % de los clientes tiene una deuda impaga.</p>
  </details>
</section>

<section id="hallazgos">
  <p class="etapa tallo">Lo que encontramos</p>
  <h2>Quien ya dijo que sí en la campaña anterior vuelve a decir que sí {num(h['lift_exito'], 1)} veces más que el promedio</h2>
  <p>Cada barra es la tasa de sí de los clientes según cómo terminó el contacto de la campaña anterior; la línea punteada es el promedio
  de todos. De los {num(h['n_exito'])} clientes con un éxito previo, el {pct(h['exito'])} volvió a aceptar. La gran mayoría no tuvo
  contacto previo, y ahí la tasa queda por debajo del promedio: para ellos el banco sabe muy poco.</p>
  <div class="grafico" id="g-hallazgo"></div>
  <details><summary>Cómo lo sabemos</summary>
    <p>Los números de esta sección son los del análisis exploratorio (Entrega 2), sobre los {num(len(df))} contactos del dataset.
    Una hipótesis se sostiene si el <i>lift</i> —la tasa del grupo dividida por la tasa de todos— llega a 3,33, el corte que fijamos antes de mirar.</p>
    <h4>Una que se sostuvo: el éxito previo vale más que el perfil</h4>
    <p>Tasa de sí con éxito previo: {pct(h['exito'], 1)}, contra {pct(h['media'], 1)} de todos. Lift {num(h['lift_exito'], 2)}, por encima del corte:
    se sostiene, y el resultado anterior entra al modelo.</p>
    <h4>Una que no: no hay una ocupación que se lleve los sí</h4>
    <p>La ocupación con más sí en proporción es estudiante: {pct(h['estudiante'], 1)} de {num(h['n_est'])} contactos. Lift {num(h['lift_est'], 2)},
    por debajo del corte: hay sobrerrepresentación, pero no alcanza el tamaño que fijamos. La ocupación entra al modelo, pero no decide sola.</p>
    <h4>Cómo se construyó el gráfico</h4>
    <p>Datos: un contacto por fila. Transformación: se agrupa por el resultado de la campaña anterior y se calcula la proporción de sí
    (los que no tuvieron contacto previo forman su propio grupo). Quedan fuera del gráfico los 5 contactos con contacto previo pero resultado desconocido: con 5 casos, su tasa no dice nada. Marca: barras, porque es una magnitud y el eje arranca en 0. Mapeo:
    la tasa a la posición horizontal; el rótulo muestra también cuántos clientes hay en cada grupo, porque los tamaños son muy distintos.</p>
  </details>
</section>

<section id="modelo">
  <p class="etapa tallo">El modelo</p>
  <h2>El modelo baja el costo de cada sí un {pct(ahorro, 1)} y deja escapar menos de 5 de cada 100 clientes</h2>
  <p>La línea muestra, en el test, cuántas llamadas cuesta cada sí según cuántos sí se exige conseguir; la línea gris es llamar a todos.
  Cuanto más a la derecha, menos clientes se escapan y más se acerca al costo de llamar a todos. El punto es el umbral que se eligió
  antes de mirar el test: exige al menos el 95 % de los sí.</p>
  <div class="grafico" id="g-modelo"></div>
  <details><summary>Cómo lo sabemos</summary>
    <h4>La métrica y por qué</h4>
    <p>El banco quiere que cada depósito le cueste la menor cantidad de llamadas posible, sin perder a los que iban a decir que sí.
    Por eso se fija un mínimo de recall —conseguir al menos el {pct(m3.RECALL_MIN)} de los sí— y, con eso fijo, se busca la mayor
    precision, que se lee como <b>llamadas por cada sí = 1 / precision</b>. No se usa F1: mezcla las dos cosas en un número que no se lee en llamadas.</p>
    <h4>El piso</h4>
    <p>Llamar a todos (<code>DummyClassifier</code>): consigue el 100 % de los sí y su precision es la tasa de sí. En el test cuesta {num(todos, 2)} llamadas por sí.
    Como la tasa de sí cambia entre períodos, los modelos se comparan por el <b>ahorro</b>: cuánto bajan las llamadas por sí respecto de llamar a todos en el mismo período.</p>
    <h4>La validación</h4>
    <p>Validación cruzada temporal (<code>TimeSeriesSplit</code>, 5 pedazos) sobre el entrenamiento: cada pedazo se entrena con el pasado y se valida con lo que viene después,
    como se va a usar el modelo. Imputar, escalar y codificar van adentro del pipeline, así que se ajustan dentro de cada pedazo.</p>
    {tabla_html(folds(r))}
    <h4>La comparación completa</h4>
    <p>Ahorro medio ± desvío en los 5 pedazos, con recall ≥ 0,95. Regla fijada de antemano: si un modelo más complejo no le gana a la logística por más que el
    desvío, se queda la logística, que además es la que se puede llevar a esta página. Ninguno le gana.</p>
    {tablas['comparacion']}
    <h4>El ajuste del elegido</h4>
    <p>La grilla de C (0,1; 1; 10; 100) con pesos iguales y balanceados está en la tabla. Todas las logísticas quedan a menos de un desvío entre sí: el resultado no depende de afinar C.
    Se queda la de mayor ahorro, C = {num(r['params']['C'])} con pesos {'balanceados' if r['params']['class_weight'] else 'iguales'}: {pct(e.ahorro_media, 1)} ± {pct(e.ahorro_desvio, 1)}.
    El umbral se fija en el pedazo más reciente, el que más se parece al test: {num(r['umbral'], 4)}.</p>
    <h4>El resultado en el test</h4>
    <p>{num(t['llamadas'])} llamadas en vez de {num(len(r['y_te']))}, {num(t['si_conseguidos'])} de {num(t['si_totales'])} sí (recall {num(t['recall'], 3)}):
    {num(t['llamadas_por_si'], 2)} llamadas por sí contra {num(todos, 2)}, un ahorro de {pct(ahorro, 1)}. La validación había anticipado {pct(e.ahorro_media, 1)}.</p>
    <h4>Dónde se equivoca</h4>
    <p>Para no perder sí, el modelo llama a casi todos: la mayoría de sus errores son llamadas a quien dice que no.</p>
    {tablas['confusion']}
    <h4>En qué se apoya</h4>
    <p>Los coeficientes de la logística, sobre columnas estandarizadas. El que más pesa es haber dicho que sí en la campaña anterior: es lo que mostró el análisis,
    y no es fuga, porque se conoce antes de llamar.</p>
    {tablas['coef']}
  </details>
</section>

<section id="explora">
  <p class="etapa copa">Tu turno · Explorá</p>
  <h2>Los clientes, según la probabilidad de sí que les da el modelo</h2>
  <p>Cada punto es un contacto; a la derecha de la línea punteada, el modelo dice que hay que llamarlo. En rojo, los sí que se escapan.
  Empezá por el panorama, después achicá con los menús o mové el umbral, y pasá el mouse por un cliente para ver sus datos y qué dijo el modelo.</p>
  <div class="grafico" id="g-explora"></div>
  <p class="nota">Cada contacto lo predice un modelo que no lo vio: los del entrenamiento salen de la validación cruzada, y los del test, del modelo final.
  Los primeros {num(r['cortes'][0][0].size)} contactos del entrenamiento no tienen predicción, porque ningún pedazo los valida.</p>
</section>

<section id="proba">
  <p class="etapa copa">Tu turno · Probá el modelo</p>
  <h2>Armá un cliente y mirá si el modelo lo llamaría</h2>
  <p>La probabilidad se calcula dentro de la página con los coeficientes de la logística entrenada: nada se reentrena. Los deslizadores van del mínimo
  al máximo que vio el entrenamiento y los menús sólo ofrecen categorías que el modelo conoce, así que no se puede cargar un valor que nunca vio.</p>
  <div class="probar">
    <div class="entradas">
      <fieldset><legend>El cliente</legend>
        <div class="slot" id="d-edad"></div><div class="slot" id="d-ocupacion"></div><div class="slot" id="d-educacion"></div></fieldset>
      <fieldset><legend>Su situación con el banco</legend>
        <div class="slot" id="d-saldo"></div><div class="slot" id="d-hipoteca"></div><div class="slot" id="d-prestamo"></div></fieldset>
      <fieldset><legend>La campaña anterior</legend>
        <div class="slot" id="d-previos"></div><div class="slot" id="d-dias"></div><div class="slot" id="d-anterior"></div></fieldset>
    </div>
    <div class="fijo"><div class="grafico" id="g-proba"></div>
    <p class="nota">Valores de partida: la mediana del entrenamiento. Con 0 contactos anteriores, el cliente cuenta como «sin contacto previo».
    El umbral es el mismo que en el test: {num(r['umbral'], 4)}.</p></div>
  </div>
</section>

<footer>Ciencia de Datos · UTN FRM · 2026 · Grupo 5K09-04 · Datos: Bank Marketing (UCI, bank-full), contactos hasta el {hasta:%d/%m/%Y}.
Generado con <code>build_app.py</code>.</footer>
</main>
<script>
const SPECS = {specs};
{JS}
</script>
</body></html>
"""
