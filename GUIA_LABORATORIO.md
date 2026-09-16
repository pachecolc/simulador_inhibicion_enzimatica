# Guía de laboratorio virtual: Inhibición enzimática

## 1. Datos generales

- **Asignatura sugerida:** Bioquímica / Biofísica / Fisiología para Ciencias de la Salud
- **Práctica:** Cinética de Michaelis-Menten e inhibición enzimática reversible
- **Área temática:** Enzimología y farmacología básica
- **Nivel:** Primeros semestres de Medicina
- **Modalidad:** Laboratorio virtual / análisis computacional
- **Duración estimada:** 90–120 min

## 2. Introducción

La inhibición enzimática permite relacionar una interacción molecular con cambios medibles en la velocidad de una reacción. En esta práctica se estudian cinco condiciones: ausencia de inhibidor, inhibición competitiva, acompetitiva, mixta y no competitiva pura. El estudiante no deberá memorizar una tabla de flechas; deberá inferir el patrón a partir de la curva y de los cambios en **Km** y **Vmax**.

El simulador representa una reacción enzimática sencilla:

\[
E+S\rightleftharpoons ES\rightarrow E+P
\]

y permite observar cómo los estados **E**, **ES**, **EI** y **ESI** modifican el comportamiento cinético.

## 3. Objetivos

### Objetivo general

Analizar cuantitativamente cómo diferentes patrones de inhibición reversible modifican la cinética de Michaelis-Menten y relacionar esos cambios con su interpretación bioquímica y farmacológica.

### Objetivos específicos

1. Calcular y comparar velocidades iniciales para diferentes concentraciones de sustrato.
2. Identificar experimentalmente el significado operacional de Km y Vmax.
3. Determinar cómo cambian Km aparente y Vmax aparente en inhibición competitiva, acompetitiva, mixta y no competitiva pura.
4. Interpretar la influencia relativa de Kic y Kiu en un mecanismo mixto.
5. Comparar predicciones manuales con los resultados del simulador.
6. Relacionar patrones cinéticos ideales con ejemplos farmacológicos introductorios.

## 4. Fundamento teórico

### 4.1 Michaelis-Menten

\[
v_0=\frac{V_{max}[S]}{K_m+[S]}
\]

- **v₀:** velocidad inicial, unidades/min.
- **Vmax:** velocidad máxima, unidades/min.
- **[S]:** concentración de sustrato, mM.
- **Km:** constante de Michaelis, mM.

Cuando `[S] = Km`, la velocidad es `Vmax/2`. Km es un **parámetro cinético** y no debe interpretarse automáticamente como una medida directa de afinidad.

### 4.2 Modelo general de inhibición reversible

\[
\alpha=1+\frac{[I]}{K_{ic}}
\]

\[
\alpha'=1+\frac{[I]}{K_{iu}}
\]

\[
v=\frac{V_{max}[S]}{\alpha K_m+\alpha'[S]}
\]

\[
V_{max,app}=\frac{V_{max}}{\alpha'}
\]

\[
K_{m,app}=\frac{\alpha}{\alpha'}K_m
\]

### 4.3 Patrones esperados

| Mecanismo | Km aparente | Vmax aparente | Idea central |
|---|---:|---:|---|
| Control | = | = | Saturación normal |
| Competitiva | ↑ | = | S e I son funcionalmente excluyentes |
| Acompetitiva | ↓ | ↓ | I se une a ES |
| Mixta | ↑ o ↓ | ↓ | I se une a E y ES con afinidades distintas |
| No competitiva pura | = | ↓ | Caso especial de mixta con Kic = Kiu |

## 5. Supuestos y limitaciones

El modelo se aplica a velocidad inicial y a una cinética de Michaelis-Menten sencilla. No incluye cooperatividad, sistemas multisustrato, tight binding, inhibición por sustrato ni inactivación dependiente del tiempo. Los intervalos de los controles son pedagógicos y no representan valores fisiológicos universales.

## 6. Acceso al laboratorio virtual

- **URL de Streamlit:** ______________________________
- **Repositorio GitHub:** ____________________________

## 7. Guía de uso de la aplicación

1. En la barra lateral seleccione el **mecanismo**.
2. Ajuste `[S]`, `Km` y `Vmax`.
3. Si corresponde, ajuste `[I]` y `Kic`, `Kiu` o `Ki`.
4. Antes de mirar el resultado, escriba una predicción sobre Km aparente, Vmax aparente y velocidad.
5. En **🧪 Simulador**, observe la figura molecular y la curva de Michaelis-Menten.
6. Compare la curva del inhibidor con la curva control.
7. Revise los valores de velocidad, Km aparente, Vmax aparente, α y α′.
8. En **🔬 Experimento**, pulse **Registrar medición**.
9. Repita para todas las condiciones indicadas.
10. Descargue los registros como CSV o Excel.

## 8. Variables experimentales

| Variable | Símbolo | Unidad | Tipo | Rango de la app | Función |
|---|---|---|---|---:|---|
| Concentración de sustrato | [S] | mM | Independiente | 0.1–20 | Modifica la ocupación de la enzima |
| Concentración de inhibidor | [I] | mM | Independiente | 0–10 | Modifica α y/o α′ |
| Km basal | Km | mM | Controlada | 0.1–10 | Parámetro cinético basal |
| Vmax basal | Vmax | unidades/min | Controlada | 10–200 | Capacidad catalítica basal |
| Constante competitiva | Kic | mM | Parámetro | 0.1–10 | Modula unión del inhibidor a E |
| Constante acompetitiva | Kiu | mM | Parámetro | 0.1–10 | Modula unión del inhibidor a ES |
| Constante no competitiva | Ki | mM | Parámetro | 0.1–10 | Se usa con Kic = Kiu |
| Velocidad inicial | v₀ | unidades/min | Dependiente | calculada | Respuesta principal |
| Km aparente | Km,app | mM | Dependiente | calculada | Cambio cinético aparente |
| Vmax aparente | Vmax,app | unidades/min | Dependiente | calculada | Cambio de capacidad máxima |

---

# 9. Experimento 1 — Saturación sin inhibidor

### Pregunta
¿Por qué duplicar indefinidamente [S] no duplica indefinidamente la velocidad?

### Predicción
Antes de simular, dibuje una curva aproximada de `v₀` frente a `[S]` y señale dónde espera encontrar `Vmax/2`.

### Condiciones
- Mecanismo: **Sin inhibidor**
- Km = 2.0 mM
- Vmax = 100 unidades/min
- [S] = 0.5, 1, 2, 5 y 10 mM

### Procedimiento
1. Configure la condición basal.
2. Ajuste [S] a cada valor de la serie.
3. Observe la velocidad y el punto sobre la curva.
4. Pulse **Registrar medición** después de cada valor.
5. Identifique el valor de [S] en el que `v = 50 unidades/min`.

| Ensayo | [S] (mM) | v simulador (unidades/min) | v/Vmax |
|---:|---:|---:|---:|
| 1 | 0.5 | | |
| 2 | 1 | | |
| 3 | 2 | | |
| 4 | 5 | | |
| 5 | 10 | | |

### Cálculo manual
Calcule manualmente `v` para `[S] = 2 mM` y compare.

| Condición | Valor manual | Simulador | Diferencia | % error |
|---|---:|---:|---:|---:|
| [S] = 2 mM | | | | |

---

# 10. Experimento 2 — Inhibición competitiva

### Pregunta
¿Puede un gran exceso de sustrato recuperar la misma velocidad máxima del control?

### Predicción
Indique antes de simular si espera que Km aparente aumente, disminuya o no cambie, y haga lo mismo para Vmax aparente.

### Condiciones
- Mecanismo: **Competitiva**
- Km = 2.0 mM
- Vmax = 100 unidades/min
- Kic = 2.0 mM
- [S] = 2.0 mM
- [I] = 0, 1, 2, 4 y 8 mM

### Procedimiento
1. Mantenga constantes Km, Vmax, Kic y [S].
2. Modifique solo [I].
3. Registre velocidad, Km aparente y Vmax aparente.
4. Luego seleccione [I] = 2 mM y compare [S] = 2, 5, 10 y 20 mM.
5. Observe si la curva inhibida mantiene el mismo techo que el control.

| [I] (mM) | α | Km aparente (mM) | Vmax aparente | v a [S]=2 |
|---:|---:|---:|---:|---:|
| 0 | | | | |
| 1 | | | | |
| 2 | | | | |
| 4 | | | | |
| 8 | | | | |

### Cálculo manual
Para `[I]=2 mM` y `Kic=2 mM`, calcule α, Km aparente y Vmax aparente. Compare con el simulador.

---

# 11. Experimento 3 — Inhibición acompetitiva

### Pregunta
¿Por qué añadir más sustrato no recupera la Vmax basal?

### Condiciones
- Mecanismo: **Acompetitiva**
- Km = 2.0 mM
- Vmax = 100 unidades/min
- Kiu = 2.0 mM
- [S] = 2.0 mM
- [I] = 0, 1, 2, 4 y 8 mM

### Procedimiento
1. Mantenga constantes Km, Vmax, Kiu y [S].
2. Modifique [I].
3. Registre Km aparente y Vmax aparente.
4. Con [I] = 2 mM, aumente [S] hasta 20 mM.
5. Compare el techo de la curva con el control.

| [I] (mM) | α′ | Km aparente (mM) | Vmax aparente | v a [S]=2 |
|---:|---:|---:|---:|---:|
| 0 | | | | |
| 1 | | | | |
| 2 | | | | |
| 4 | | | | |
| 8 | | | | |

---

# 12. Experimento 4 — Inhibición mixta

### Pregunta
¿Cómo cambia Km aparente cuando el inhibidor afecta relativamente más a E o a ES?

### Condiciones comunes
- Km = 2.0 mM
- Vmax = 100 unidades/min
- [S] = 2.0 mM
- [I] = 1.0 mM

### Escenario A
- Kic = 1.0 mM
- Kiu = 2.0 mM

### Escenario B
- Kic = 2.0 mM
- Kiu = 1.0 mM

### Procedimiento
1. Simule el escenario A y registre la medición.
2. Anote α, α′, Km aparente y Vmax aparente.
3. Simule el escenario B.
4. Compare la dirección del cambio de Km.
5. Explique qué estado, E o ES, está siendo relativamente más afectado en cada caso.

| Escenario | Kic | Kiu | α | α′ | Km aparente | Vmax aparente | Interpretación |
|---|---:|---:|---:|---:|---:|---:|---|
| A | 1.0 | 2.0 | | | | | |
| B | 2.0 | 1.0 | | | | | |

---

# 13. Experimento 5 — No competitiva pura

### Pregunta
¿Qué parámetro permanece invariable si el inhibidor afecta E y ES de forma equivalente?

### Condiciones
- Mecanismo: **No competitiva pura**
- Km = 2.0 mM
- Vmax = 100 unidades/min
- Ki = 2.0 mM
- [S] = 2.0 mM
- [I] = 0, 1, 2, 4 y 8 mM

### Procedimiento
1. Mantenga constantes Km, Vmax, Ki y [S].
2. Aumente [I].
3. Registre Km aparente y Vmax aparente.
4. Compruebe si Km cambia.
5. Compare el techo de la curva con el control.

| [I] (mM) | α=α′ | Km aparente (mM) | Vmax aparente | v |
|---:|---:|---:|---:|---:|
| 0 | | | | |
| 1 | | | | |
| 2 | | | | |
| 4 | | | | |
| 8 | | | | |

---

# 14. Experimento 6 — Investigación libre

Diseñe una pregunta que pueda responderse con las variables reales disponibles en la app.

- **Pregunta de investigación:**
- **Hipótesis:**
- **Variable independiente:**
- **Variable dependiente:**
- **Variables controladas:**
- **Mecanismo elegido:**
- **Serie de valores a explorar:**
- **Criterio de interpretación:**

Registre al menos cinco condiciones y exporte el archivo final.

---

## 15. Comparación de mecanismos

Utilice la pestaña **📊 Comparar mecanismos** con `Km = 2 mM`, `Vmax = 100 unidades/min`, `[I] = 2 mM`, `Kic = 1 mM`, `Kiu = 2 mM` y `Ki = 2 mM`.

1. Active las cinco curvas.
2. Identifique cuál conserva Vmax.
3. Identifique cuál conserva Km.
4. Identifique cuál reduce simultáneamente Km y Vmax.
5. Observe cómo la curva mixta depende de la relación entre Kic y Kiu.

## 16. Lineweaver-Burk

Observe la transformación recíproca para al menos dos mecanismos. Utilícela únicamente con finalidad pedagógica. Explique por qué los puntos de baja [S] reciben un peso visual exagerado y por qué un ajuste no lineal de Michaelis-Menten es preferible para estimar parámetros.

## 17. Aplicación biomédica y farmacológica

En la pestaña **💊 Aplicaciones médicas**, revise estatinas, aspirina, metotrexato, AChE y CYP450.

Para cada ejemplo, responda:

1. ¿El ejemplo corresponde directamente al modelo reversible de la app o se presenta como contraste?
2. ¿Qué parámetro cinético del modelo ayuda a explicar el comportamiento idealizado?
3. ¿Qué característica del sistema real impide reducir toda la farmacología a una única categoría cinética?

> No utilice la simulación para diagnosticar pacientes ni para inferir dosis farmacológicas.

## 18. Preguntas de análisis

1. ¿Por qué la velocidad se aproxima a un límite cuando [S] es muy alta?
2. ¿Qué representa operacionalmente Km en una curva de Michaelis-Menten?
3. ¿Por qué Km no debe equipararse automáticamente con afinidad?
4. ¿Qué evidencia gráfica permite distinguir una inhibición competitiva ideal de una no competitiva pura?
5. ¿Por qué la acompetitiva reduce simultáneamente Km y Vmax?
6. En la inhibición mixta, ¿qué indica que α > α′?
7. ¿Qué ocurre con Km aparente si Kic y Kiu son iguales?
8. ¿Por qué más sustrato puede rescatar idealmente la competitiva pero no la acompetitiva?
9. ¿Cómo cambia la velocidad actual cuando se modifica [I] sin cambiar [S]?
10. ¿Qué información se pierde si solo se observa la velocidad en una única concentración de sustrato?
11. ¿Qué diferencia existe entre un patrón cinético de inhibición y un sitio físico de unión?
12. ¿Por qué una representación de Lineweaver-Burk no debe ser el método principal para estimar Km y Vmax?
13. ¿Qué limitación tendría aplicar este modelo directamente a una enzima cooperativa?
14. ¿Por qué la aspirina se presenta en la app como aplicación clínica pero no dentro del modelo reversible principal?
15. ¿Qué ventaja tiene registrar varias condiciones y analizar una curva completa en lugar de memorizar cambios de Km y Vmax?

## 19. Preguntas de pensamiento crítico

1. ¿Qué supuesto del modelo de velocidad inicial podría dejar de cumplirse si el producto se acumula durante mucho tiempo?
2. ¿Cómo diseñaría un experimento real para distinguir inhibición mixta de no competitiva pura?
3. Si un inhibidor farmacológico real muestra dependencia del tiempo, ¿por qué el modelo de equilibrio reversible de esta app podría ser insuficiente?

## 20. Registro y exportación

Después de cada condición pulse **Registrar medición**. Al finalizar descargue preferiblemente:

`Grupo_Apellido_inhibicion_enzimatica.xlsx`

Conserve también el CSV si se requiere análisis adicional.

## 21. Conclusiones

Redacte entre 3 y 5 conclusiones basadas exclusivamente en sus resultados. Cada conclusión debe:

- responder a uno de los objetivos;
- mencionar una tendencia observada;
- relacionar la tendencia con el modelo cinético;
- evitar afirmaciones clínicas que no estén soportadas por la simulación.

## 22. Producto a entregar

1. Guía respondida.
2. Archivo Excel descargado del simulador.
3. Al menos una captura o exportación visual de la comparación de curvas.
4. Cálculos manuales solicitados.
5. Respuestas de análisis.
6. Conclusiones.

## 23. Criterios de evaluación

| Criterio | Peso |
|---|---:|
| Predicciones y diseño experimental | 15 % |
| Registro correcto de datos | 20 % |
| Cálculos y comparación manual-simulador | 20 % |
| Interpretación de curvas y mecanismos | 25 % |
| Preguntas de análisis y pensamiento crítico | 10 % |
| Conclusiones | 10 % |

**Total: 100 %**
