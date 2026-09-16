# Validación científica y técnica

La validación se ejecutó con `python validate_model.py` usando los casos del material de referencia (`Vmax = 100 unidades/min`, `Km = 2 mM`).

| Caso | Entradas | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| 1. Control | S=2 | v=50 | v=50 | OK |
| 2. Competitiva | alpha=2, alpha'=1 | Km_app=4; Vmax_app=100 | Km_app=4; Vmax_app=100 | OK |
| 3. Acompetitiva | alpha=1, alpha'=2 | Km_app=1; Vmax_app=50 | Km_app=1; Vmax_app=50 | OK |
| 4. No competitiva pura | alpha=2, alpha'=2 | Km_app=2; Vmax_app=50 | Km_app=2; Vmax_app=50 | OK |
| 5. Mixta | alpha=2, alpha'=1.5 | Km_app≈2.6667; Vmax_app≈66.6667 | Km_app=2.66667; Vmax_app=66.6667 | OK |

También se verificó programáticamente:

- creación de las curvas de Michaelis-Menten;
- creación de la comparación de cinco mecanismos;
- creación de Lineweaver-Burk sin usar `[S]=0`;
- existencia de las cinco imágenes renombradas dentro de `assets/`;
- exportación a CSV;
- exportación a Excel mediante `openpyxl`;
- compilación sintáctica de todos los archivos Python.

## Validaciones de dominio

El modelo rechaza concentraciones negativas y parámetros no físicos como `Km <= 0`, `Vmax <= 0`, `Kic <= 0`, `Kiu <= 0` o `Ki <= 0`.

## Verificación local

```bash
python validate_model.py
python -m py_compile app.py models/kinetics.py utils/assets.py utils/export.py utils/plotting.py
```

> El entorno de construcción utilizado para esta entrega no tenía Streamlit instalado, por lo que no se levantó el servidor web localmente. La sintaxis, el modelo, Plotly, Pandas, OpenPyXL, las imágenes y las exportaciones sí fueron verificados. Streamlit está declarado en `requirements.txt` para instalación automática local o en Streamlit Community Cloud.
