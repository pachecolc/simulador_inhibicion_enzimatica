# Simulador interactivo de inhibición enzimática

Aplicación educativa en **Python + Streamlit + Plotly** para estudiantes de primeros semestres de Medicina. Permite explorar la cinética de Michaelis-Menten y comparar los patrones clásicos de inhibición reversible mediante una secuencia de predicción, simulación, observación, registro e interpretación.

## Objetivo

Relacionar los estados moleculares **E, ES, EI y ESI** con cambios cuantitativos en la velocidad inicial, **Km aparente** y **Vmax aparente**, y conectar esos cambios con ejemplos biomédicos y farmacológicos.

## Fundamento científico

Modelo basal de Michaelis-Menten:

\[
v_0=\frac{V_{max}[S]}{K_m+[S]}
\]

Marco general de inhibición reversible:

\[
\alpha=1+\frac{[I]}{K_{ic}},\qquad
\alpha'=1+\frac{[I]}{K_{iu}}
\]

\[
v=\frac{V_{max}[S]}{\alpha K_m+\alpha'[S]}
\]

\[
V_{max,app}=\frac{V_{max}}{\alpha'},\qquad
K_{m,app}=\frac{\alpha}{\alpha'}K_m
\]

La inhibición no competitiva pura se implementa como el caso particular de inhibición mixta en el que `Kic = Kiu = Ki`, por lo que `alpha = alpha_prime`, `Km_app = Km` y `Vmax_app` disminuye.

## Tipos de inhibición incluidos

| Mecanismo | Unión simplificada | Km aparente | Vmax aparente | ¿Exceso de S rescata? |
|---|---|---:|---:|---|
| Sin inhibidor | E + S ⇌ ES | = | = | No aplica |
| Competitiva | I se une a E; S e I son excluyentes | ↑ | = | Sí, idealmente |
| Acompetitiva | I se une a ES | ↓ | ↓ | No |
| Mixta | I se une a E y ES con afinidades distintas | ↑ o ↓ | ↓ | No completamente |
| No competitiva pura | I afecta E y ES de modo equivalente | = | ↓ | No |

> **Nota:** Km es un parámetro cinético. No debe interpretarse automáticamente como una medida directa de afinidad.

## Variables

| Variable | Unidad | Rango pedagógico en la app |
|---|---|---:|
| [S] | mM | 0.1–20 |
| [I] | mM | 0–10 |
| Km | mM | 0.1–10 |
| Vmax | unidades/min | 10–200 |
| Kic | mM | 0.1–10 |
| Kiu | mM | 0.1–10 |
| Ki | mM | 0.1–10 |

Estos rangos son **pedagógicos** y no se presentan como intervalos fisiológicos universales.

## Funciones educativas

- Curvas interactivas de Michaelis-Menten con control e inhibidor.
- Figura molecular que cambia con el mecanismo seleccionado.
- Visualización de Km, Vmax, Km aparente, Vmax aparente, α y α′.
- Interpretación automática basada en reglas matemáticas.
- Comparación simultánea de mecanismos.
- Representación pedagógica de Lineweaver-Burk con advertencia sobre sus limitaciones.
- Modo de predicción y comprobación.
- Registro de múltiples mediciones mediante `st.session_state`.
- Exportación a CSV y Excel.
- Actividades guiadas y aplicaciones médicas.

## Estructura del proyecto

```text
simulador_inhibicion_enzimatica/
├── app.py
├── models/
│   ├── __init__.py
│   └── kinetics.py
├── utils/
│   ├── __init__.py
│   ├── assets.py
│   ├── export.py
│   └── plotting.py
├── assets/
│   ├── 01_sin_inhibidor.png
│   ├── 02_competitiva.png
│   ├── 03_acompetitiva.png
│   ├── 04_mixta.png
│   └── 05_no_competitiva.png
├── ANALISIS_DISENO.md
├── GUIA_LABORATORIO.md
├── GUIA_ESTUDIANTE.md
├── VALIDACION.md
├── validate_model.py
├── requirements.txt
├── README.md
└── .gitignore
```

El modelo científico está separado de la interfaz para facilitar mantenimiento y reutilización.

## Instalación local

Requiere Python 3.10 o superior.

```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\\Scripts\\activate      # Windows
pip install -r requirements.txt
```

## Ejecución local

Desde la carpeta del proyecto:

```bash
streamlit run app.py
```

## Validación científica

Ejecute:

```bash
python validate_model.py
```

Se verifican cinco casos de referencia: condición basal, competitiva, acompetitiva, no competitiva pura y mixta.

## Despliegue en Streamlit Community Cloud

1. Cree un repositorio en GitHub y suba el contenido de esta carpeta.
2. Confirme que `requirements.txt`, `app.py`, `models/`, `utils/` y `assets/` estén en el repositorio.
3. En Streamlit Community Cloud seleccione:
   - **Repository:** su repositorio de GitHub
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Despliegue la aplicación.
5. Coloque la URL pública resultante en `GUIA_LABORATORIO.md`.

## Uso para estudiantes

1. Seleccione un mecanismo.
2. Formule una predicción sobre Km, Vmax y velocidad.
3. Modifique [S], [I] y las constantes de inhibición pertinentes.
4. Observe simultáneamente la figura molecular y la curva cinética.
5. Registre la medición en la pestaña **🔬 Experimento**.
6. Repita varias condiciones y compare.
7. Descargue los datos en CSV o Excel.
8. Interprete los resultados con la guía de laboratorio.

## Limitaciones del modelo

La aplicación trabaja con velocidad inicial y los patrones clásicos de Michaelis-Menten. No pretende describir de forma general:

- cooperatividad y enzimas alostéricas sigmoides;
- sistemas multisustrato complejos;
- tight binding;
- inhibición por exceso de sustrato;
- unión lenta y residence time;
- inactivación irreversible o dependiente del tiempo;
- ecuaciones cinéticas específicas de sistemas farmacológicos reales.

La pestaña de Lineweaver-Burk es histórica y pedagógica; para estimar parámetros se prefieren ajustes no lineales.

## Fuentes principales

El simulador fue diseñado a partir del informe académico suministrado por el usuario, que integra cinética enzimática, farmacología y estrategias pedagógicas. Entre las referencias citadas en dicho informe se encuentran:

1. Cornish-Bowden A. *Current IUBMB recommendations on enzyme nomenclature and kinetics*. Perspectives in Science. 2014;1:74-87.
2. Srinivasan B. *A guide to the Michaelis-Menten equation: steady state and beyond*. FEBS Journal. 2022.
3. Johnson KA. *A century of enzyme kinetic analysis, 1913-2013*.
4. Istvan ES, Deisenhofer J. *Structural mechanism for statin inhibition of HMG-CoA reductase*. Science. 2001.
5. Deodhar M, et al. *Mechanisms of CYP450 Inhibition*. Pharmaceutics. 2020;12:846.
6. Colovic MB, et al. *Acetylcholinesterase inhibitors: pharmacology and toxicology*. Current Neuropharmacology. 2013.
7. Lineweaver H, Burk D. *The Determination of Enzyme Dissociation Constants*. J Am Chem Soc. 1934;56:658-666.
