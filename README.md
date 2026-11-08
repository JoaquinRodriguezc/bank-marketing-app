# ¿A quién conviene llamar? · Bank Marketing

Proyecto integrador de Ciencia de Datos (UTN FRM, 2026), grupo 5K09-04.

La aplicación cuenta el proyecto entero y deja usarlo: `index.html` es una sola página que se publica con GitHub Pages.

## Cómo se regenera la aplicación

Con Python 3.12:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python build_app.py
```

`build_app.py` hace todo de punta a punta, con la semilla 42:

1. Lee `datos/_bank_marketing_silver.csv`, el CSV que produce el pipeline.
2. Reconstruye la fecha de cada contacto, toma los contactos desde junio de 2009 y los parte 80/20 por tiempo.
3. Repite la comparación de modelos de la Entrega 3 con validación cruzada temporal, elige el modelo y fija el umbral.
4. Comprueba que la fórmula que viaja a la página da la misma probabilidad que el modelo de scikit-learn en todo el test.
5. Arma los gráficos con Altair y escribe `index.html`.

Si los datos cambian, se reemplaza el CSV y se vuelve a correr `python build_app.py`.

## Cómo se publica

En GitHub: *Settings → Pages → Deploy from a branch → `main` / `(root)`*. La página queda en `https://<usuario>.github.io/<repositorio>/`.

La página usa Vega, Vega-Lite y Vega-Embed desde jsDelivr, así que necesita conexión a internet.

## Qué hay en el repositorio

| Archivo | Qué es |
|---|---|
| `build_app.py` | Construye la aplicación: datos, modelo y gráficos. |
| `plantilla.py` | El texto y el HTML de la página. |
| `modelado_v3.py`, `modelado_v2_e2.py`, `transformadores.py` | El pipeline del modelo (columnas, preparación, familias, métrica). |
| `datos/_bank_marketing_silver.csv` | Los datos que produce el pipeline (Bank Marketing de UCI, `bank-full`). |
| `notebooks/Entrega_2_Bank_Marketing_desde_cero.ipynb` | El análisis exploratorio (Entrega 2). |
| `notebooks/v4.ipynb` | El modelado (Entrega 3, versión corregida). Se regenera con `crear_v4.py`. |
| `index.html` | La aplicación generada. |

Para correr `notebooks/v4.ipynb`, tienen que estar en la misma carpeta el CSV y los tres `.py` del modelo.

## Qué coincide con el notebook

El modelo, el umbral y el resultado en el test son los de `notebooks/v4.ipynb`: logística con C = 1 y pesos balanceados, umbral 0,3545, y en el test 1.003 llamadas, 519 de 542 sí, 1,93 llamadas por sí contra 2,01 de llamar a todos.
