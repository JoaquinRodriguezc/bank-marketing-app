import modelado_v3 as m3
from build_app import num, pct, INICIO, tabla_html
import pandas as pd

MESES = "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split()


def fecha_larga(ts):
    return f"{MESES[ts.month - 1]} de {ts.year}"


CSS = """
:root{--tinta:#141310;--tinta-2:#3d3831;--gris:#6b6459;--suave:#f4f1ea;--linea:#e4dfd5;--acento:#0072B2;--acento-suave:#eff4f9;--copa:#8a4b0f;--fondo:#faf9f6;--serif:Georgia,"Times New Roman",serif}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:16px}
body{margin:0;background:var(--fondo);color:var(--tinta);font:18px/1.55 "Segoe UI",Helvetica,Arial,sans-serif}
nav{position:fixed;top:0;left:0;bottom:0;width:230px;padding:28px 18px;border-right:1px solid var(--linea);background:#fafbfc;overflow-y:auto}
nav .marca{font-family:var(--serif);font-size:13.5px;color:var(--gris);margin:0 0 22px}
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
h1{font-family:var(--serif);font-weight:400;letter-spacing:-.01em;font-size:44px;line-height:1.14;margin:0 0 18px;max-width:24ch}
h2{font-family:var(--serif);font-weight:400;letter-spacing:-.01em;font-size:30px;line-height:1.22;margin:0 0 14px;max-width:46ch}
p,li{max-width:74ch}
.lead{font-size:22px;line-height:1.5;color:#3f4750;max-width:66ch}
.oracion{font-family:var(--serif);font-size:25px;line-height:1.42;border-left:4px solid var(--acento);padding:6px 0 6px 24px;margin:26px 0 34px;max-width:54ch}
.nums{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:10px 0 18px}
.nums.dos{grid-template-columns:repeat(2,1fr)}
#portada{margin-top:26px;padding:46px 40px 26px;border:1px solid var(--linea);border-top:4px solid var(--acento);border-radius:14px;background:linear-gradient(180deg,#f7f9fb 0%,#fff 72%)}
#portada h1{margin-bottom:20px}
.nums.versus{grid-template-columns:1fr auto 1fr;gap:16px;align-items:center;margin:4px 0 22px}
.nums.versus .num{background:#fff;padding:20px 22px;border-radius:10px}
.nums.versus .num.hoy{border:1px dashed #c3c9d0}
.nums.versus .num.conmodelo{border:2px solid var(--acento);background:#eff6fb}
.nums.versus .num span{font-size:46px}
.nums.versus .num.hoy span{color:var(--gris)}
.nums.versus .rotulo{margin:0;font-size:12.5px;letter-spacing:.09em;text-transform:uppercase;font-weight:700;color:var(--gris)}
.nums.versus .conmodelo .rotulo{color:var(--acento)}
.nums.versus .num p:not(.rotulo){margin:4px 0 0;font-size:15px;color:var(--gris)}
.nums.versus .flecha{font-size:32px;font-weight:700;line-height:1;color:var(--acento);justify-self:center}
main h3{font-family:var(--serif);font-weight:400;font-size:23px;margin:30px 0 10px}
h2 b{color:var(--acento);font-weight:400}
.capitulo{float:right;font-family:var(--serif);font-size:15px;color:var(--gris);border:1px solid var(--linea);border-radius:999px;padding:6px 14px}
.entradilla{font-size:16.5px;color:var(--tinta-2);max-width:64ch}
.paso .entradilla{margin:12px 0 0}
.figura{margin:34px 0 0;background:#fff;border:1px solid var(--linea);border-radius:14px;padding:24px 24px 14px}
.figura .titulo-f{font-family:var(--serif);font-size:17.5px;margin:0 0 14px;color:var(--tinta)}
.figura .titulo-f em{color:var(--gris)}
.figura figcaption{font-size:13.5px;color:var(--gris);margin:10px 0 0;border-top:1px solid var(--linea);padding-top:10px;max-width:74ch}
.aparte{margin:26px 0 0;background:var(--suave);border-left:4px solid var(--gris);border-radius:0 12px 12px 0;padding:18px 22px;font-size:15.5px;color:var(--tinta-2);max-width:74ch}
.morgue{margin:52px 0 0}
.rotulo-m{font-size:11.5px;letter-spacing:.15em;text-transform:uppercase;font-weight:700;color:var(--gris);display:flex;align-items:center;gap:12px;margin:0 0 14px}
.rotulo-m::after{content:"";flex:1;border-top:1px solid var(--linea)}
.morgue ul{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:0;margin:24px 0 0}
.morgue li{border:1px solid var(--linea);border-radius:12px;background:#fff;padding:16px 18px}
.morgue li .h{font-family:var(--serif);font-size:17px;color:var(--tinta-2);margin:0 0 4px}
.morgue li .v{font-size:13.5px;color:var(--gris);line-height:1.5;margin:0}
.morgue li .v b{color:var(--tinta-2)}
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
fieldset{border:1px solid var(--linea);border-radius:12px;padding:8px 14px 12px;margin:0 0 12px;background:#fff}
legend{font-weight:600;font-size:12.5px;color:var(--copa);text-transform:uppercase;letter-spacing:.06em;padding:0 6px}
.slot .vega-bind{margin:4px 0}
.slot .vega-bind label{display:grid;grid-template-columns:170px minmax(80px,1fr) 64px;align-items:center;gap:8px;font-size:14.5px}
.slot .vega-bind-name{font-weight:500}
.slot input[type=range]{width:100%;margin:0;accent-color:var(--copa)}
.slot select{font-size:14.5px;padding:3px 6px}
.slot .vega-bind-radio{display:flex;gap:10px;align-items:center}
.fijo{position:sticky;top:16px;border:1px solid var(--linea);border-radius:14px;background:#fff;padding:16px 16px 10px}
footer{max-width:980px;margin:0 auto;padding:30px 0;color:var(--gris);font-size:14px}
@media (max-width:1150px){.probar{grid-template-columns:1fr}.fijo{position:static}}
.paso{margin:44px 0 0}
.rotulo-paso{font-size:11.5px;letter-spacing:.15em;text-transform:uppercase;font-weight:700;color:var(--gris);display:flex;align-items:center;gap:12px;margin:0}
.rotulo-paso::after{content:"";flex:1;border-top:1px solid var(--linea)}
.paso.resultado .rotulo-paso{color:var(--acento)}
.duelo{display:grid;grid-template-columns:1fr auto 1fr;gap:18px;align-items:stretch;margin-top:16px}
.duelo .lado{border-radius:12px;padding:22px 24px}
.duelo .hoy{background:#fff;border:1px dashed #c3c9d0}
.duelo .nuevo{background:#fff;border:1px solid var(--linea)}
.duelo .modelo{background:var(--acento-suave);border:2px solid var(--acento)}
.duelo .rotulo{font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;color:var(--gris);margin:0 0 10px}
.duelo .modelo .rotulo{color:var(--acento)}
.duelo .cifra{font-family:var(--serif);font-size:58px;line-height:1;font-weight:400;color:var(--tinta-2)}
.duelo .modelo .cifra{color:var(--acento)}
.duelo .detalle{font-size:14.5px;color:var(--gris);margin:10px 0 0;max-width:28ch}
.duelo .flecha{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;min-width:86px}
.duelo .delta{font-size:12px;font-weight:700;color:var(--acento);background:#fff;border:1px solid var(--acento);border-radius:999px;padding:4px 12px}
.duelo .punta{font-size:26px;color:var(--acento)}
.duelo .nota-f{font-size:11.5px;color:var(--gris);text-align:center;max-width:18ch;margin:0}
.remate{font-family:var(--serif);font-size:19px;color:var(--tinta-2);margin:18px 0 0;max-width:54ch}
.remate b{color:var(--acento);font-weight:400}
.pie-portada{margin-top:36px;border-top:3px double var(--linea);padding-top:14px}
.pasos-tu{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:26px 0 0}
.paso-chip{display:flex;align-items:center;gap:10px;border:1px solid var(--linea);border-radius:999px;
  background:#fff;padding:10px 16px;font-size:14px;color:var(--tinta-2);margin:0}
.paso-chip b{width:24px;height:24px;border-radius:999px;background:var(--copa);color:#fff;
  display:flex;align-items:center;justify-content:center;font-size:13px;flex:none}
.carta{margin:38px 0 0}
.rotulo-c{font-size:11.5px;letter-spacing:.15em;text-transform:uppercase;font-weight:700;color:var(--gris);
  display:flex;align-items:center;gap:12px;margin:0 0 14px}
.rotulo-c::after{content:"";flex:1;border-top:1px solid var(--linea)}
.carta ul{list-style:none;display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;padding:0;margin:0}
.carta li{border:1px solid var(--linea);border-radius:12px;background:#fff;padding:18px 18px 16px}
.carta li .falta{font-family:var(--serif);font-size:18px;color:var(--tinta);margin:0 0 6px}
.carta li .hoy{font-size:13.5px;color:var(--gris);line-height:1.5;margin:0}
.carta li .hoy b{color:var(--tinta-2)}
@media (max-width:860px){.pasos-tu{grid-template-columns:1fr}.carta ul{grid-template-columns:1fr}.morgue ul{grid-template-columns:1fr}.duelo{grid-template-columns:1fr}.duelo .flecha{flex-direction:row;min-height:64px}
nav{display:none}main{margin-left:0;padding:0 16px 60px}.nums{grid-template-columns:1fr}h1{font-size:32px}
#portada{padding:28px 20px 18px;border-radius:12px}.nums.versus{grid-template-columns:1fr}.nums.versus .flecha{transform:rotate(90deg)}}
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
    d = r["descartados"]
    may09 = df[df.contact_date.dt.strftime("%Y-%m").eq("2009-05")]
    n_may, tasa_may = len(may09), float(may09.si.mean())
    hasta = df.contact_date.max()
    oracion = (f"Con lo que el banco ya sabe antes de llamar, el modelo hace que cada sí cueste un {pct(ahorro)} menos "
               f"llamadas y deja escapar {num(perdidos)} de los {num(t['si_totales'])} clientes que igual iban a decir que sí "
               f"— y esa es toda la distancia que estos datos permiten recorrer.")
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
    <li><a href="#modelo">El modelo</a></li>
    <li><a href="#techo">Por qué no más</a></li></ol></div>
  <div class="copa"><h3>Tu turno</h3><ol>
    <li><a href="#explora">Explorá los clientes</a></li>
    <li><a href="#proba">Probá el modelo</a></li></ol></div>
</nav>
<main>

<section id="portada">
  <p class="etapa tallo">El proyecto</p>
  <h1>¿A quién conviene llamar para que cada depósito cueste menos llamadas?</h1>
  <p class="lead">Un banco portugués llamó a sus clientes para ofrecerles un depósito a plazo.
  Son las campañas de telemarketing del dataset público Bank Marketing (UCI, <i>bank-full</i>): {num(len(df))} contactos
  entre {fecha_larga(df.contact_date.min())} y {fecha_larga(hasta)}.
  Cada llamada le cuesta minutos de operador al banco, y las llamadas son justamente lo que este proyecto intenta bajar.
  Antes de mostrar nuestro resultado, conviene conocer al rival.</p>
  <div class="paso">
    <p class="rotulo-paso">Primero · contra quién competimos</p>
    <div class="duelo">
      <div class="lado hoy">
        <p class="rotulo">2008 · el banco llamaba a todos</p>
        <p class="cifra">{pct(float(df[df.contact_date < INICIO].si.mean()), 1)}</p>
        <p class="detalle">de sí, con miles de llamadas por mes a casi toda la base de clientes.</p>
      </div>
      <div class="flecha">
        <span class="punta" aria-hidden="true">──▶</span>
        <p class="nota-f">el banco aprende y cambia de estrategia</p>
      </div>
      <div class="lado nuevo">
        <p class="rotulo">Desde 2009 · elige a quién llamar</p>
        <p class="cifra">{pct(float(r['reciente'].si.mean()), 1)}</p>
        <p class="detalle">de sí, llamando a una lista mucho más chica de clientes elegidos.</p>
      </div>
    </div>
    <p class="remate">Nuestro rival no es el azar: es <b>la lista que el banco ya elige</b> — un piso que sus expertos
    construyeron con el tiempo. La pregunta del proyecto es si todavía se le puede ganar algo.</p>
  </div>
  <div class="paso resultado">
    <p class="rotulo-paso">Después · lo que hace el modelo</p>
    <div class="duelo">
      <div class="lado hoy">
        <p class="rotulo">Banco hoy</p>
        <p class="cifra">{num(todos, 2)}</p>
        <p class="detalle">llamadas por cada sí: {num(len(r['y_te']))} llamadas para conseguir los {num(t['si_totales'])} sí de su lista.</p>
      </div>
      <div class="flecha">
        <span class="delta">−{pct(ahorro, 0)}</span>
        <span class="punta" aria-hidden="true">──▶</span>
        <p class="nota-f">{num(menos)} llamadas menos, {num(perdidos)} sí que se escapan</p>
      </div>
      <div class="lado modelo">
        <p class="rotulo">Con el modelo</p>
        <p class="cifra">{num(t['llamadas_por_si'], 2)}</p>
        <p class="detalle">llamadas por cada sí: {num(t['llamadas'])} llamadas y {num(t['si_conseguidos'])} de los {num(t['si_totales'])} sí conseguidos.</p>
      </div>
    </div>
  </div>
  <p class="oracion">{oracion}</p>
  <p class="nota pie-portada">Medido sobre los {num(len(r['y_te']))} contactos más recientes (julio a noviembre de 2010), que el modelo no vio.
  Las secciones siguientes cuentan cómo se llega a estas cifras y por qué no se pueden estirar mucho más: entrená con la época
  que entrenes, el techo es el mismo.</p>
</section>

<section id="datos">
  <p class="etapa tallo">Los datos</p>
  <p class="capitulo">Capítulo 02</p>
  <h2>La tasa de sí cambió con el tiempo: <b>{pct(df[df.contact_date < INICIO].si.mean())}</b> en las campañas viejas, <b>{pct(r['reciente'].si.mean())}</b> en las recientes</h2>
  <p class="entradilla">Arriba, qué parte de los contactos de cada mes terminó en un depósito; abajo, cuántos contactos hubo. En 2008 el banco hacía
  miles de llamadas por mes y muy pocos aceptaban. Desde mediados de 2009 llamó a mucha menos gente y casi la mitad dijo que sí.
  El modelo se entrena y se prueba en el período sombreado, que es el que se parece al uso actual.</p>
  <figure class="figura">
    <p class="titulo-f">La tasa de sí, mes a mes <em>· y el salto de la estrategia del banco</em></p>
    <div class="grafico" id="g-datos"></div>
    <figcaption>Los dos paneles se leen juntos: cuando las barras de abajo se achican, la línea de arriba se dispara. No es un cambio
    de los clientes — es un cambio de estrategia del banco, que pasó de llamar a casi todos a llamar a una lista elegida.
    Esa lista es el rival del modelo.</figcaption>
  </figure>
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
  <p class="capitulo">Capítulo 03</p>
  <h2>Quien ya dijo que sí en la campaña anterior vuelve a decir que sí <b>{num(h['lift_exito'], 1)} veces</b> más que el promedio</h2>
  <p class="entradilla">La lista elegida que presentamos en los datos no es magia: se apoya en el historial de campañas. Cuando el banco
  pasó de llamar a casi todos a elegir a quién llamar, lo que más aprovechó fue justamente el pasado de cada cliente:</p>
  <div class="duelo">
    <div class="lado hoy">
      <p class="rotulo">2008 · llamaba a casi todos</p>
      <p class="cifra">{pct(h['hist_viejos'], 1)}</p>
      <p class="detalle">de los contactados tenía una campaña anterior: casi todo el pasado por escribir.</p>
    </div>
    <div class="flecha">
      <span class="punta" aria-hidden="true">──▶</span>
      <p class="nota-f">la lista nueva se arma sobre el historial</p>
    </div>
    <div class="lado nuevo">
      <p class="rotulo">Desde 2009 · la lista elegida</p>
      <p class="cifra">{pct(h['hist_rec'], 1)}</p>
      <p class="detalle">de los contactados ya había sido llamada antes por el banco.</p>
    </div>
  </div>
  <p class="entradilla">Cada barra es un grupo de clientes, agrupados por cómo terminó su <b>último contacto de la campaña anterior</b>.
  La barra mide la <b>tasa de sí</b> de ese grupo —de cada 100 clientes que llegan con ese mismo pasado, cuántos aceptaron esta vez—,
  y el rótulo del costado dice cuántos hay, porque los grupos no pesan lo mismo. La línea punteada es el promedio de todos,
  {pct(h['media'], 1)}: lo que queda a su derecha le va mejor que al cliente promedio.</p>
  <figure class="figura">
    <p class="titulo-f">La tasa de sí según el contacto anterior <em>· Éxito, Fracaso, Otro o ninguno</em></p>
    <div class="grafico" id="g-hallazgo"></div>
    <figcaption>El hallazgo que sostiene al modelo: el pasado del cliente manda más que su perfil. De los {num(h['n_sin'])}
    clientes que nunca fueron contactados acepta apenas el {pct(h['sin'], 1)}: de ellos, el banco sabe muy poco.</figcaption>
  </figure>
  <div class="morgue">
    <p class="rotulo-m">Lo que probamos y no llegó · el corte de lift era 3,33</p>
    <figure class="figura">
      <p class="titulo-f">El lift de cada hipótesis <em>· y el corte que fijamos antes de mirar</em></p>
      <div class="grafico" id="g-lift"></div>
      <figcaption>La única que cruzó el corte es la que sostiene al modelo. Las demás existen en el promedio,
      pero no distinguen cliente por cliente — por eso no entran.</figcaption>
    </figure>
    <ul>
      <li><p class="h">Los estudiantes aceptan más</p>
        <p class="v">{pct(h['estudiante'], 1)} de sí, lift <b>{num(h['lift_est'], 2)}</b> — pero sobre {num(h['n_est'])} contactos,
        el {pct(h['n_est'] / len(df), 1)} del dataset: el volumen no alcanza y la tasa se mueve mucho entre períodos.</p></li>
      <li><p class="h">Los casados aceptan menos</p>
        <p class="v">Solteros lift <b>1,28</b>, casados <b>0,87</b> (η² 0,004, resultado de la Entrega 2) — existe en el promedio
        pero no distingue cliente por cliente.</p></li>
      <li><p class="h">Insistir con llamadas separa</p>
        <p class="v">Separación <b>0,27 → 0,29 → 0,24</b> (Entrega 2) — inconclusa, y cuenta la llamada en curso:
        <code>campaign</code> queda afuera del modelo.</p></li>
      <li><p class="h">El mes y el día</p>
        <p class="v">El mes explica mucho (η² 6,8&nbsp;%) pero no se puede asegurar que se conozcan antes de llamar:
        <b>fuga posible</b>, no falta de señal.</p></li>
    </ul>
  </div>
  <details><summary>Cómo lo sabemos · el detalle de cada hipótesis</summary>
    <p>Los números del gráfico y de estos párrafos salen del mismo CSV que usa el modelo y se calculan al generar la página; los de las
    hipótesis descartadas son resultados del análisis exploratorio (Entrega 2), sobre los {num(len(df))} contactos del dataset, y se citan
    como tales. Una hipótesis se sostiene si el <i>lift</i> —la tasa del grupo dividida por la tasa de todos— llega a 3,33, el corte que
    fijamos antes de mirar.</p>
    <h4>Una que se sostuvo: el éxito previo vale más que el perfil</h4>
    <p>Tasa de sí con éxito previo: {pct(h['exito'], 1)}, contra {pct(h['media'], 1)} de todos. Lift {num(h['lift_exito'], 2)}, por encima del corte:
    se sostiene, y el resultado anterior entra al modelo.</p>
    <h4>Una que no: no hay una ocupación que se lleve los sí</h4>
    <p>La ocupación con más sí en proporción es estudiante: {pct(h['estudiante'], 1)} de {num(h['n_est'])} contactos, el {pct(h['n_est'] / len(df), 1)}
    del dataset. Lift {num(h['lift_est'], 2)}, por debajo del corte: hay sobrerrepresentación, pero no alcanza el tamaño que fijamos, y con un
    volumen tan chico la tasa se mueve mucho de un período a otro. La ocupación entra al modelo, pero no decide sola.</p>
    <h4>Otra que no: los casados aceptan menos</h4>
    <p>La idea era razonable —un hogar con más obligaciones dice que no más seguido— y la dirección aparece: los solteros llegan a un lift de
    1,28 y los casados quedan en 0,87, con el estado civil explicando menos del 0,5 % de la variación (η² 0,004). Pero 1,28 no llega a 3,33,
    así que la hipótesis quedó refutada en la Entrega 2: es una diferencia de tres puntos sobre una base de doce, que existe en el promedio
    y no distingue a un cliente de otro. El estado civil se conoce antes de llamar, pero no entra al modelo.</p>
    <h4>Otra que quedó inconclusa: insistir con llamadas</h4>
    <p>Si al cliente que va a decir que sí no hace falta llamarlo diez veces, la cantidad de llamadas de la campaña (<code>campaign</code>)
    debería separar a los que aceptan. Separa, y en la dirección esperada, pero no lo suficiente: separación 0,266, que sube a 0,291 al pasarla
    a logaritmo y vuelve a 0,239 al partir a los clientes con historial, siempre en la zona intermedia y nunca en la que decide. Quedó
    <i>inconclusa</i> y como candidata débil en la Entrega 2. Además cuenta la llamada en curso, así que usarla honestamente pide restarle uno
    y el dataset no permite reconstruir ese momento: <code>campaign</code> queda afuera del modelo.</p>
    <h4>Dos que no llegaron a ser hipótesis: el mes y el día</h4>
    <p>Con <code>month</code> y <code>day</code> no hay un resultado fallido sino un problema anterior: el dataset mezcla el calendario de la
    campaña con la fecha en que se hizo cada llamada, así que no se puede asegurar que se conozcan al decidir a quién llamar. El mes, además,
    es de las columnas que más explican el sí (η² 6,8 % en la Entrega 2): duele sacarlo, y por eso conviene decirlo. Quedan afuera por fuga
    posible, no por falta de señal, y probar sumar el mes y el canal de contacto al modelo no mejoró el ahorro (nota de la versión V4).</p>
    <h4>Cómo se construyó el gráfico</h4>
    <p>Datos: un contacto por fila. Transformación: se agrupa por el resultado de la campaña anterior —<code>poutcome</code> limpio, con
    «Otro» = <code>other</code>, «Fracaso» = <code>failure</code>, «Éxito» = <code>success</code> y «Sin contacto previo» para quien nunca fue
    contactado— y se calcula la proporción de sí de cada grupo. Quedan fuera del gráfico los {num(h['n_desc'])} contactos con contacto previo
    y resultado desconocido: con {num(h['n_desc'])} casos, su tasa no dice nada. Marca: barras, porque es una magnitud y el eje arranca en 0.
    Mapeo: la tasa a la posición horizontal; el rótulo muestra también cuántos clientes hay en cada grupo, porque los tamaños son muy distintos.</p>
  </details>
</section>

<section id="modelo">
  <p class="etapa tallo">El modelo</p>
  <p class="capitulo">Capítulo 04</p>
  <h2>El modelo baja el costo de cada sí un <b>{pct(ahorro, 1)}</b> y deja escapar menos de 5 de cada 100 clientes</h2>
  <p class="entradilla">El rival no es llamar a los {num(len(df))} clientes del dataset, sino la lista a la que el banco ya llama —
  la que su estrategia elige desde 2009. En el test esa lista convierte a la mitad de los que llama: es un rival duro. Contra eso:</p>
  <div class="duelo">
    <div class="lado hoy">
      <p class="rotulo">Llamar a toda la lista</p>
      <p class="cifra">{num(todos, 2)}</p>
      <p class="detalle">llamadas por cada sí: {num(len(r['y_te']))} llamadas para los {num(t['si_totales'])} sí.</p>
    </div>
    <div class="flecha">
      <span class="delta">−{pct(ahorro, 0)}</span>
      <span class="punta" aria-hidden="true">──▶</span>
      <p class="nota-f">{num(menos)} llamadas menos, {num(perdidos)} sí que se escapan</p>
    </div>
    <div class="lado modelo">
      <p class="rotulo">Con el modelo</p>
      <p class="cifra">{num(t['llamadas_por_si'], 2)}</p>
      <p class="detalle">llamadas por cada sí: {num(t['llamadas'])} llamadas, {num(t['si_conseguidos'])} de {num(t['si_totales'])} sí ({pct(t['recall'], 0)}).</p>
    </div>
  </div>
  <div class="paso">
    <p class="rotulo-paso">Acto 1 · Cómo se llegó: cuatro familias contra el piso</p>
    <p class="entradilla">Ninguna familia le gana a la logística por más de un desvío — y la logística, además, es la que se puede
    llevar a esta página. La regla se fijó antes de mirar el test.</p>
    <figure class="figura">
      <p class="titulo-f">Ahorro de llamadas por sí, por familia <em>· la misma validación temporal para todas</em></p>
      <div class="grafico" id="g-familias"></div>
      <figcaption>La regla de selección se fijó de antemano: si un modelo más complejo no le gana a la logística por más de un
      desvío, se queda la logística. Ninguno le ganó.</figcaption>
    </figure>
  </div>
  <div class="paso resultado">
    <p class="rotulo-paso">Acto 2 · El resultado, medido una sola vez en el test</p>
    <p class="entradilla">La curva arranca en (0, 0): cuánto cuesta cada sí según cuántos sí se exige conseguir, desde exigirle
    poquísimos hasta no perder ninguno. El punto es el umbral fijado antes de mirar el test: exige al menos el
    {pct(m3.RECALL_MIN, 0)} de los sí. La distancia a la línea gris es el ahorro real.</p>
    <figure class="figura">
      <p class="titulo-f">Llamadas por cada sí <em>· según cuántos sí se exige conseguir</em></p>
      <div class="grafico" id="g-modelo"></div>
      <figcaption>Del tamaño que es: entre el punto azul y la línea gris cabe todo el ahorro — {num(menos)} llamadas menos de
      {num(len(r['y_te']))} a cambio de {num(perdidos)} sí de {num(t['si_totales'])}. Aceptando perder más sí el ahorro crecería;
      dónde pararse es decisión del negocio, no del modelo.</figcaption>
    </figure>
  </div>
  <div class="paso">
    <p class="rotulo-paso">Acto 3 · La radiografía del modelo</p>
    <figure class="figura">
      <p class="titulo-f">Dónde se equivoca <em>· la matriz del test, con los colores de Explorá</em></p>
      <div class="grafico" id="g-confusion"></div>
      <figcaption>Para no perder sí, el modelo llama a casi todos: su error típico es una llamada a quien dice que no.
      Los sí que se escapan son {num(perdidos)} — el costo en clientes de las {num(menos)} llamadas ahorradas.</figcaption>
    </figure>
    <figure class="figura">
      <p class="titulo-f">En qué se apoya <em>· los coeficientes de mayor magnitud</em></p>
      <div class="grafico" id="g-coef"></div>
      <figcaption>El coeficiente que más empuja hacia el sí es haber dicho sí en la campaña anterior: es exactamente el hallazgo
      del capítulo 03. No es fuga: se conoce antes de llamar.</figcaption>
    </figure>
  </div>
  <details><summary>Cómo lo sabemos</summary>
    <h4>La métrica y por qué</h4>
    <p>El banco quiere que cada depósito le cueste la menor cantidad de llamadas posible, sin perder a los que iban a decir que sí.
    Por eso se fija un mínimo de recall —conseguir al menos el {pct(m3.RECALL_MIN)} de los sí— y, con eso fijo, se busca la mayor
    precision, que se lee como <b>llamadas por cada sí = 1 / precision</b>. No se usa F1: mezcla las dos cosas en un número que no se lee en llamadas.</p>
    <h4>El piso: la estrategia del banco</h4>
    <p>El piso no es llamar a todos los clientes del banco: es llamar a toda la lista que el banco ya decidió llamar, la lista del operador,
    elegida campaña a campaña desde 2009 (<code>DummyClassifier</code> sobre esa lista). Llamarla entera consigue el 100 % de los sí y cuesta
    {num(todos, 2)} llamadas por sí en el test. Como la tasa de sí cambia entre períodos, los modelos se comparan por el <b>ahorro</b>:
    cuánto bajan las llamadas por sí respecto de esa lista en el mismo período.</p>
    <h4>Las correcciones que llevaron a este modelo</h4>
    <p>V1 entrenaba con las campañas viejas y sus números no se podían leer: la tasa de sí cambia de época y las validaciones al azar
    daban números más lindos que falsos. V3 fijó la métrica de negocio y el umbral por pedazo. V4 sacó mayo de 2009: {num(n_may)} llamadas
    con {pct(tasa_may, 1)} de sí, la cola del régimen viejo que quedaba en el corte; sin ese mes, el ahorro de validación sube en los
    cuatro pedazos (1,5 % → 5,0 %).</p>
    <h4>Las versiones que hubo antes, y por qué el modelo es lo que es</h4>
    <p>Cada punto es una versión medida en su propio test: cuántos sí consigue (horizontal) contra cuánto ahorra por sí
    (vertical). Las viejas sólo ahorraban dejando clientes escaparse; la vigente fija primero el compromiso — no perder más de
    5 de cada 100 sí — y recién ahí mide el ahorro.</p>
    <div class="grafico" id="g-versiones"></div>
    <p>V1 mezclaba épocas: entrenada con las campañas viejas y medida con f1, ahorraba un 18,6 % por sí en su test — pero
    perdiendo 23 de cada 100 clientes que iban a aceptar, con una validación (f1 0,158 ± 0,092) que no anticipaba nada.
    V6 probó si la era vieja escondía una estrategia: su mejor ahorro interno es ruido (4,8 % ± 1,7 % en validación, la
    rayita vertical) y su único test decente (19,1 %) vuelve a caer en el mismo vicio — ahorra perdiendo 17 de cada 100 sí.
    V4, la vigente, mide 4,1 % con la validación anticipándolo (4,5 % ± 1,6 %). <b>No cambiamos el modelo: cambiamos la
    pregunta.</b></p>
    <p class="nota">Los números de V1 y V6 son los documentados en los notebooks de la Entrega 3 (V1 con umbral 0,5 y pesos
    balanceados, sobre su test de 9.043 contactos; V6 sobre su test interno de 7.234); los de V4 los computa esta página al
    generarla.</p>
    <h4>La validación</h4>
    <p>Validación cruzada temporal (<code>TimeSeriesSplit</code>, 5 pedazos) sobre el entrenamiento: cada pedazo se entrena con el pasado y se valida con lo que viene después,
    como se va a usar el modelo. Imputar, escalar y codificar van adentro del pipeline, así que se ajustan dentro de cada pedazo.</p>
    {tabla_html(folds(r))}
    <h4>La comparación completa</h4>
    <p>Cada punto es un candidato —las cuatro familias y cada combinación de C y pesos—, con su desvío, todos medidos igual: la misma validación
    temporal y el mismo recall mínimo. La regla se fijó de antemano: si un modelo más complejo no le gana a la logística por más que el desvío,
    se queda la logística, que además es la que se puede llevar a esta página. Ninguno le gana.</p>
    <div class="grafico" id="g-comparacion"></div>
    {tablas['comparacion']}
    <h4>El ajuste del elegido</h4>
    <p>La grilla de C (0,1; 1; 10; 100) con pesos iguales y balanceados está en la tabla. Todas las logísticas quedan a menos de un desvío entre sí: el resultado no depende de afinar C.
    Se queda la de mayor ahorro, C = {num(r['params']['C'])} con pesos {'balanceados' if r['params']['class_weight'] else 'iguales'}: {pct(e.ahorro_media, 1)} ± {pct(e.ahorro_desvio, 1)}.
    El umbral se fija en el pedazo más reciente, el que más se parece al test: {num(r['umbral'], 4)}.</p>
    <h4>El resultado en el test</h4>
    <p>{num(t['llamadas'])} llamadas en vez de {num(len(r['y_te']))}, {num(t['si_conseguidos'])} de {num(t['si_totales'])} sí (recall {num(t['recall'], 3)}):
    {num(t['llamadas_por_si'], 2)} llamadas por sí contra {num(todos, 2)}, un ahorro de {pct(ahorro, 1)}. La validación había anticipado {pct(e.ahorro_media, 1)}.</p>
  </details>
</section>

<section id="techo">
  <p class="etapa tallo">El techo</p>
  <p class="capitulo">Capítulo 05</p>
  <h2>El techo es <b>{pct(ahorro, 1)}</b> — y es de los datos, no del modelo</h2>
  <p class="entradilla">Entrená con la época que entrenes, la misma logística llega al mismo lugar. Para romper el techo no hace
  falta un modelo mejor: hace falta <b>otra información</b>. Esta es la demostración, y la carta de lo que falta.</p>
  <figure class="figura">
    <p class="titulo-f">Ahorro de llamadas por sí, según con qué época se entrenó <em>· la misma logística, el mismo test</em></p>
    <div class="grafico" id="g-techo"></div>
    <figcaption>Dos épocas de entrenamiento, el mismo techo. La roja muestra por qué la estrategia del banco no salió de los
    datos viejos: la señal del cliente siempre estuvo, pero su umbral no viaja entre regímenes.</figcaption>
  </figure>
  <div class="carta">
    <p class="rotulo-c">La carta de lo que falta · para romper el techo habría que recolectar</p>
    <ul>
      <li>
        <p class="falta">Cuánto vale el cliente</p>
        <p class="hoy">Ingresos, productos contratados, antigüedad. Hoy sólo hay <b>edad, ocupación y saldo</b> — nada que diga
        si a este cliente le conviene un plazo fijo.</p>
      </li>
      <li>
        <p class="falta">Un historial de campañas de verdad</p>
        <p class="hoy">En los viejos casi nadie tenía contacto previo, y el resultado anterior casi siempre es <b>«Otro» o
        desconocido</b>. La señal que más pesa es justamente la que menos registrada está.</p>
      </li>
      <li>
        <p class="falta">Contexto que no sea fuga</p>
        <p class="hoy">El mes explica mucho (η² 6,8&nbsp;%) pero no se puede asegurar que se conozca antes de llamar:
        <b>queda afuera por fuga posible</b>, no por falta de señal.</p>
      </li>
    </ul>
  </div>
  <details><summary>Cómo lo sabemos · qué se hizo, la era vieja por adentro y el empate del ranking</summary>
    <h4>Qué se hizo</h4>
    <p>La misma logística y el mismo pipeline del modelo de esta app, entrenados sólo con los {num(d['n'])} contactos que la app descarta
    ({d['desde']:%d/%m/%Y} – {d['hasta']:%d/%m/%Y}, {pct(d['tasa'], 1)} de sí), con el umbral fijado igual que en el modelo: el mejor con
    recall ≥ {pct(m3.RECALL_MIN)} en el pedazo más reciente de su propia validación temporal.</p>
    <h4>Adentro de la era vieja tampoco hay nada estable</h4>
    <p>Validación cruzada temporal dentro de los viejos: ahorro de {pct(d['cv_media'], 1)} ± {pct(d['cv_desvio'], 1)} — el desvío se come la media.
    En su test interno ({num(d['n_int'])} contactos) el ahorro llega a {pct(d['ahorro_int'], 1)}, pero el recall cae a {num(d['t_int']['recall'], 2)}:
    el compromiso de {pct(m3.RECALL_MIN)} de sí conseguidos no se sostiene en esa época, donde el banco llamaba a casi todos.</p>
    <h4>El empate del ranking</h4>
    <p>Sobre el mismo test, el modelo viejo ordena igual que el reciente: AP {num(d['ap_viejo'], 3)} contra {num(d['ap_rec'], 3)},
    contra una tasa base de {pct(float(r['y_te'].mean()), 1)}. Lo que no viaja entre épocas es el umbral: la tasa de sí pasa de {pct(d['tasa'], 1)}
    en los viejos a {pct(float(r['y_te'].mean()), 1)} en el test, y las probabilidades quedan en otra escala.</p>
    <p class="nota">Honestidad: el test de esta app ya fue mirado en versiones anteriores del proyecto. El umbral de esta sección se calibró sólo
    con el entrenamiento reciente, sin mirar el test.</p>
  </details>
</section>

<section id="explora">
  <p class="etapa copa">Tu turno · Explorá</p>
  <p class="capitulo">Tu turno · 01</p>
  <h2>Los clientes, según la probabilidad de sí que les da el modelo</h2>
  <p class="entradilla">Cada punto es un contacto; a la derecha de la línea punteada, el modelo dice que hay que llamarlo. En rojo,
  los sí que se escapan. La vertical la elegís vos con el menú «Eje vertical»; el eje horizontal es siempre la probabilidad de sí
  según el modelo.</p>
  <div class="pasos-tu">
    <p class="paso-chip"><b>1</b> achicá el universo con los menús</p>
    <p class="paso-chip"><b>2</b> mové el umbral y mirá cómo cambia la lista</p>
    <p class="paso-chip"><b>3</b> pasá el mouse por un cliente para verlo entero</p>
  </div>
  <figure class="figura">
    <p class="titulo-f">El panorama, con filtros <em>· cada punto lleva la probabilidad del modelo y su resultado real</em></p>
    <div class="grafico" id="g-explora"></div>
    <figcaption>Cada contacto lo predice un modelo que no lo vio: los del entrenamiento salen de la validación cruzada, y los del
    test, del modelo final. Los primeros {num(r['cortes'][0][0].size)} contactos del entrenamiento no tienen predicción, porque
    ningún pedazo los valida. El monto exacto en euros aparece al pasar el mouse.</figcaption>
  </figure>
</section>

<section id="proba">
  <p class="etapa copa">Tu turno · Probá el modelo</p>
  <p class="capitulo">Tu turno · 02</p>
  <h2>Armá un cliente y mirá si el modelo lo llamaría</h2>
  <p class="entradilla">La probabilidad se calcula dentro de la página con los coeficientes de la logística entrenada: nada se
  reentrena. Los deslizadores van del mínimo al máximo que vio el entrenamiento y los menús sólo ofrecen categorías que el modelo
  conoce, así que no se puede cargar un valor que nunca vio.</p>
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
  <p class="nota pie-portada"><b>Probalo vos:</b> subí la edad a 70 o cambiá el resultado anterior a Fracaso, y mirá cómo cae la
  probabilidad. Después de probar un caso raro, volvé a la sección de arriba y buscalo en el panorama.</p>
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
