from pathlib import Path
import pandas as pd
import streamlit as st
from models.kinetics import MECHANISMS, evaluate_condition, mixed_tendency
from utils.assets import mechanism_image_path, optional_asset
from utils.export import dataframe_to_csv_bytes, dataframe_to_excel_bytes
from utils.plotting import michaelis_plot, comparison_plot, comparison_table, lineweaver_burk_plot

st.set_page_config(page_title="Simulador de inhibición enzimática", page_icon="🧬", layout="wide")
st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1500px;}
[data-testid="stSidebar"] {background: #f7f9fb;}
.small-note {font-size: 0.88rem; color: #5c6770;}
.mechanism-box {padding: .8rem 1rem; border: 1px solid #d9e2ec; border-radius: 10px; background: #f9fbfd;}
</style>
""", unsafe_allow_html=True)

MECH_INFO = {
    "Sin inhibidor": {
        "scheme": "E + S ⇌ ES → E + P",
        "concept": "En ausencia de inhibidor, la velocidad aumenta con [S] hasta aproximarse a Vmax por saturación enzimática.",
    },
    "Competitiva": {
        "scheme": "E + S ⇌ ES   |   E + I ⇌ EI",
        "concept": "Sustrato e inhibidor son funcionalmente excluyentes. Vmax se conserva y Km aparente aumenta. En el modelo ideal, un exceso de sustrato puede superar el efecto.",
    },
    "Acompetitiva": {
        "scheme": "E + S ⇌ ES   |   ES + I ⇌ ESI",
        "concept": "El inhibidor se une al complejo ES. Vmax y Km aparentes disminuyen en la misma proporción en el caso ideal; aumentar [S] no recupera la Vmax original.",
    },
    "Mixta": {
        "scheme": "E + I ⇌ EI   |   ES + I ⇌ ESI",
        "concept": "El inhibidor puede unirse a E y ES con afinidades diferentes. Vmax disminuye; Km puede aumentar o disminuir según Kic y Kiu.",
    },
    "No competitiva pura": {
        "scheme": "E + I ⇌ EI   |   ES + I ⇌ ESI   |   Kic = Kiu = Ki",
        "concept": "Es un caso particular de inhibición mixta. E y ES son afectados de forma equivalente: Km permanece constante y Vmax disminuye.",
    },
}

GUIDED = {
    "1. Saturación sin inhibidor": "Seleccione **Sin inhibidor**, fije Km = 2 mM y Vmax = 100 unidades/min. Explore [S] = 0.5, 1, 2, 5 y 10 mM. Registre cada medición y observe cómo la velocidad se aproxima a Vmax.",
    "2. Inhibición competitiva": "Seleccione **Competitiva**, fije Km = 2 mM, Vmax = 100 unidades/min y Kic = 2 mM. Mantenga [S] y aumente [I]. Después eleve mucho [S] y examine si la velocidad se aproxima al mismo Vmax del control.",
    "3. Inhibición acompetitiva": "Seleccione **Acompetitiva**, fije Km = 2 mM, Vmax = 100 unidades/min y Kiu = 2 mM. Aumente [I] y registre Km aparente y Vmax aparente. Compruebe que elevar [S] no restaura la Vmax basal.",
    "4. Inhibición mixta": "Seleccione **Mixta**. Compare primero Kic < Kiu y después Kic > Kiu manteniendo constantes [I], Km y Vmax. Observe el cambio de dirección de Km aparente y el descenso de Vmax aparente.",
    "5. No competitiva pura": "Seleccione **No competitiva pura**, fije Ki = 2 mM y aumente [I]. Compruebe que Km se mantiene mientras Vmax aparente disminuye.",
}


def header():
    left, right = st.columns([5, 1])
    with left:
        st.title("SIMULADOR INTERACTIVO DE INHIBICIÓN ENZIMÁTICA")
        st.subheader("Cinética de Michaelis-Menten para estudiantes de Medicina")
        st.write("Explora cómo diferentes mecanismos de inhibición modifican la velocidad enzimática, Km y Vmax.")
    with right:
        logo = optional_asset("logo_serendipia.png")
        if logo:
            st.image(str(logo), use_container_width=True)
        else:
            st.caption("Logo del proyecto no disponible.")


def current_interpretation(r):
    if r.mechanism == "Sin inhibidor":
        return "La condición es basal. Al aumentar [S], la velocidad se aproxima asintóticamente a Vmax; cuando [S] = Km, v = Vmax/2."
    if r.mechanism == "Competitiva":
        return f"El inhibidor eleva Km aparente de {r.Km:.2f} a {r.Km_app:.2f} mM sin modificar Vmax. La curva se desplaza hacia la derecha."
    if r.mechanism == "Acompetitiva":
        return f"Km y Vmax disminuyen simultáneamente: Km aparente = {r.Km_app:.2f} mM y Vmax aparente = {r.Vmax_app:.2f} unidades/min."
    if r.mechanism == "No competitiva pura":
        return f"Vmax disminuye a {r.Vmax_app:.2f} unidades/min mientras Km permanece en {r.Km_app:.2f} mM."
    tendency = mixed_tendency(r.alpha, r.alpha_p)
    if r.alpha > r.alpha_p:
        detail = "Km aumenta: el componente competitivo es relativamente mayor (mayor perturbación de E libre)."
    elif r.alpha < r.alpha_p:
        detail = "Km disminuye: el componente acompetitivo es relativamente mayor (mayor perturbación de ES)."
    else:
        detail = "Km cambia muy poco: el comportamiento se aproxima al caso no competitivo puro."
    return f"Vmax disminuye. En esta configuración hay **{tendency}**. {detail}"


def show_equations(r):
    st.latex(r"v_0=\frac{V_{max}[S]}{K_m+[S]}")
    if r.mechanism != "Sin inhibidor":
        st.latex(r"\alpha=1+\frac{[I]}{K_{ic}}\qquad \alpha'=1+\frac{[I]}{K_{iu}}")
        st.latex(r"v=\frac{V_{max}[S]}{\alpha K_m+\alpha'[S]}")
        st.latex(r"V_{max,app}=\frac{V_{max}}{\alpha'}\qquad K_{m,app}=\frac{\alpha}{\alpha'}K_m")
    if r.mechanism == "Competitiva":
        st.latex(r"\alpha=1+[I]/K_{ic},\quad \alpha'=1\Rightarrow V_{max,app}=V_{max},\ K_{m,app}=\alpha K_m")
    elif r.mechanism == "Acompetitiva":
        st.latex(r"\alpha=1,\quad \alpha'=1+[I]/K_{iu}\Rightarrow V_{max,app}=V_{max}/\alpha',\ K_{m,app}=K_m/\alpha'")
    elif r.mechanism == "No competitiva pura":
        st.latex(r"K_{ic}=K_{iu}=K_i\Rightarrow \alpha=\alpha',\ K_{m,app}=K_m,\ V_{max,app}=V_{max}/\alpha")


header()

if "measurements" not in st.session_state:
    st.session_state.measurements = []

with st.sidebar:
    st.header("Controles experimentales")
    mechanism = st.selectbox("Mecanismo", MECHANISMS, index=0)
    S = st.slider("[S] concentración de sustrato (mM)", 0.1, 20.0, 2.0, 0.1)
    Km = st.slider("Km basal (mM)", 0.1, 10.0, 2.0, 0.1)
    Vmax = st.slider("Vmax basal (unidades/min)", 10.0, 200.0, 100.0, 1.0)
    I, Kic, Kiu, Ki = 0.0, 2.0, 2.0, 2.0
    if mechanism != "Sin inhibidor":
        I = st.slider("[I] concentración de inhibidor (mM)", 0.0, 10.0, 2.0, 0.1)
    if mechanism == "Competitiva":
        Kic = st.slider("Kic (mM)", 0.1, 10.0, 2.0, 0.1)
    elif mechanism == "Acompetitiva":
        Kiu = st.slider("Kiu (mM)", 0.1, 10.0, 2.0, 0.1)
    elif mechanism == "Mixta":
        Kic = st.slider("Kic (mM)", 0.1, 10.0, 1.0, 0.1)
        Kiu = st.slider("Kiu (mM)", 0.1, 10.0, 2.0, 0.1)
    elif mechanism == "No competitiva pura":
        Ki = st.slider("Ki = Kic = Kiu (mM)", 0.1, 10.0, 2.0, 0.1)
    show_refs = st.checkbox("Mostrar líneas de referencia", value=True)
    st.divider()
    st.caption("Los rangos son valores pedagógicos para explorar el modelo; no representan intervalos fisiológicos universales.")

result = evaluate_condition(mechanism, S, Vmax, Km, I=I, Kic=Kic, Kiu=Kiu, Ki=Ki)

tab_sim, tab_concepts, tab_compare, tab_lb, tab_learn, tab_exp, tab_med = st.tabs([
    "🧪 Simulador", "📚 Conceptos", "📊 Comparar mecanismos", "📈 Lineweaver-Burk",
    "🧠 Aprende", "🔬 Experimento", "💊 Aplicaciones médicas"
])

with tab_sim:
    left, right = st.columns([1, 1.3])
    with left:
        st.subheader(mechanism)
        image = mechanism_image_path(mechanism)
        if image:
            st.image(str(image), use_container_width=True)
        else:
            st.info("Imagen no disponible.")
        st.markdown(f"**Esquema:** `{MECH_INFO[mechanism]['scheme']}`")
        st.write(MECH_INFO[mechanism]["concept"])
    with right:
        st.plotly_chart(michaelis_plot(result, show_references=show_refs, s_max=20), use_container_width=True)

    st.subheader("Resultados principales")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Velocidad actual", f"{result.velocity:.2f} unidades/min")
    c2.metric("Km basal", f"{result.Km:.2f} mM")
    c3.metric("Km aparente", f"{result.Km_app:.2f} mM", delta=f"{result.Km_app-result.Km:+.2f} mM" if mechanism != "Sin inhibidor" else None)
    c4.metric("Vmax basal", f"{result.Vmax:.1f} unidades/min")
    c5.metric("Vmax aparente", f"{result.Vmax_app:.2f} unidades/min", delta=f"{result.Vmax_app-result.Vmax:+.2f}" if mechanism != "Sin inhibidor" else None)
    if mechanism != "Sin inhibidor":
        a1, a2 = st.columns(2)
        a1.metric("α", f"{result.alpha:.3f}")
        a2.metric("α′", f"{result.alpha_p:.3f}")

    st.subheader("¿Qué está ocurriendo?")
    st.info(current_interpretation(result))
    with st.expander("📐 Ver ecuaciones"):
        show_equations(result)
        st.caption("Cuando [S] = Km en la condición basal, v = Vmax/2.")

with tab_concepts:
    st.header("Conceptos básicos")
    concepts = {
        "Enzima": "Catalizador biológico que acelera una reacción sin consumirse estequiométricamente en cada ciclo.",
        "Sustrato": "Molécula sobre la que actúa la enzima dentro del mecanismo considerado.",
        "Sitio activo": "Región funcional donde se reconocen sustratos y ocurre la catálisis; su descripción estructural no debe confundirse con el patrón cinético de inhibición.",
        "Complejo ES": "Estado enzima-sustrato cuya formación es central para interpretar la velocidad inicial y los mecanismos de inhibición.",
        "Velocidad inicial": "Velocidad medida al comienzo de la reacción, cuando la acumulación de producto todavía es pequeña.",
        "Saturación": "Régimen en el que elevar más [S] produce incrementos cada vez menores de velocidad y v se aproxima a Vmax.",
        "Km": "Parámetro cinético con unidades de concentración. En Michaelis-Menten, [S]=Km implica v=Vmax/2.",
        "Vmax": "Velocidad límite del sistema cuando la enzima se aproxima a saturación; depende de la cantidad de enzima funcional y de kcat.",
        "Inhibidor": "Molécula que reduce la actividad observada por interacción con uno o más estados del sistema enzimático.",
        "Inhibición vs regulación": "La regulación enzimática es un concepto más amplio; no toda regulación corresponde a uno de los patrones clásicos de inhibición reversible.",
    }
    for title, text in concepts.items():
        with st.expander(title, expanded=title in ("Km", "Vmax")):
            st.write(text)
    st.warning("**Km no debe interpretarse automáticamente como una medida directa de afinidad.** Es un parámetro cinético compuesto; solo bajo condiciones particulares puede aproximarse a una constante de disociación.")
    with st.expander("⚠️ Errores frecuentes"):
        st.markdown("""
- ❌ **Km es siempre afinidad.** ✅ Km es un parámetro cinético.
- ❌ **Competitivo = mismo sitio físico.** ✅ La definición ideal es operacional: S e I son mutuamente excluyentes.
- ❌ **Todo inhibidor disminuye Vmax.** ✅ La competitiva clásica conserva Vmax.
- ❌ **Todo inhibidor aumenta Km.** ✅ La acompetitiva disminuye Km; la mixta puede moverlo en ambas direcciones.
- ❌ **Mixta y no competitiva son exactamente iguales.** ✅ La no competitiva pura es un caso particular de mixta.
- ❌ **Más sustrato siempre vence al inhibidor.** ✅ Solo rescata idealmente el patrón competitivo.
- ❌ **Todo inhibidor alostérico es no competitivo.** ✅ Alosterismo y patrón cinético son conceptos distintos.
""")

with tab_compare:
    st.header("Comparar mecanismos")
    st.write("Superpone curvas bajo un conjunto común de parámetros para reconocer patrones cinéticos.")
    with st.expander("Parámetros de comparación", expanded=True):
        p1, p2, p3, p4 = st.columns(4)
        comp_I = p1.slider("[I] común (mM)", 0.0, 10.0, 2.0, 0.1, key="comp_I")
        comp_Kic = p2.slider("Kic competitiva/mixta (mM)", 0.1, 10.0, 1.0, 0.1, key="comp_Kic")
        comp_Kiu = p3.slider("Kiu acompetitiva/mixta (mM)", 0.1, 10.0, 2.0, 0.1, key="comp_Kiu")
        comp_Ki = p4.slider("Ki no competitiva (mM)", 0.1, 10.0, 2.0, 0.1, key="comp_Ki")
    checks = st.columns(5)
    selected = []
    for i, m in enumerate(MECHANISMS):
        label = "Control" if m == "Sin inhibidor" else m.replace(" pura", "")
        if checks[i].checkbox(label, value=True, key=f"cmp_{i}"):
            selected.append(m)
    if selected:
        st.plotly_chart(comparison_plot(selected, Vmax, Km, comp_I, comp_Kic, comp_Kiu, comp_Ki), use_container_width=True)
        df_cmp = pd.DataFrame(comparison_table(selected, Vmax, Km, comp_I, comp_Kic, comp_Kiu, comp_Ki))
        st.dataframe(df_cmp, hide_index=True, use_container_width=True)
    else:
        st.info("Seleccione al menos un mecanismo.")

with tab_lb:
    st.header("Lineweaver-Burk")
    st.plotly_chart(lineweaver_burk_plot(result), use_container_width=True)
    st.latex(r"\frac{1}{v}=\frac{\alpha K_m}{V_{max}}\frac{1}{[S]}+\frac{\alpha'}{V_{max}}")
    st.warning("Esta representación tiene valor histórico y pedagógico. La transformación recíproca amplifica el error de los puntos a bajas concentraciones de sustrato. Para estimar parámetros cinéticos se prefieren ajustes no lineales.")

with tab_learn:
    st.header("Predice antes de observar")
    quiz = st.selectbox("Mecanismo para el ejercicio", ["Competitiva", "Acompetitiva", "Mixta", "No competitiva pura"], key="quiz_mech")
    if quiz == "Mixta":
        st.info("Escenario de la pregunta: [I] = 1 mM, Kic = 1 mM y Kiu = 2 mM. Por tanto, α = 2 y α′ = 1.5.")
    q1, q2 = st.columns(2)
    pred_km = q1.radio("¿Qué ocurre con Km aparente?", ["Aumenta", "Disminuye", "No cambia"], key="pred_km", horizontal=True)
    pred_vmax = q2.radio("¿Qué ocurre con Vmax aparente?", ["Aumenta", "Disminuye", "No cambia"], key="pred_vmax", horizontal=True)
    answers = {
        "Competitiva": ("Aumenta", "No cambia", "El sustrato y el inhibidor son excluyentes; el mismo Vmax puede alcanzarse idealmente con [S] muy alta."),
        "Acompetitiva": ("Disminuye", "Disminuye", "El inhibidor se une a ES; Km y Vmax aparentes disminuyen en el patrón ideal."),
        "Mixta": ("Aumenta", "Disminuye", "Con α > α′ en este escenario, Km aparente aumenta y Vmax aparente disminuye."),
        "No competitiva pura": ("No cambia", "Disminuye", "Cuando α = α′, Km se conserva y Vmax disminuye."),
    }
    if st.button("Comprobar predicción", type="primary"):
        akm, av, explanation = answers[quiz]
        if pred_km == akm and pred_vmax == av:
            st.success("Predicción correcta. " + explanation)
        else:
            st.error(f"Revise la predicción. Para este caso: Km **{akm.lower()}** y Vmax **{av.lower()}**. {explanation}")

with tab_exp:
    st.header("Experimento virtual y registro de datos")
    st.write("La condición activa se configura con los controles de la barra lateral. Antes de registrar, formule una predicción y después contraste con la curva y los parámetros aparentes.")
    scenario = st.selectbox("Actividad guiada", list(GUIDED), key="guided")
    st.info(GUIDED[scenario])
    s1, s2, s3 = st.columns(3)
    s1.metric("Condición", mechanism)
    s2.metric("[S]", f"{S:.2f} mM")
    s3.metric("Velocidad", f"{result.velocity:.2f} unidades/min")

    if st.button("Registrar medición", type="primary"):
        row = {
            "Experimento": len(st.session_state.measurements) + 1,
            "Mecanismo": mechanism,
            "[S] (mM)": round(S, 4),
            "[I] (mM)": round(result.I, 4),
            "Km basal (mM)": round(result.Km, 4),
            "Vmax basal (unidades/min)": round(result.Vmax, 4),
            "Kic (mM)": None if result.Kic is None else round(result.Kic, 4),
            "Kiu (mM)": None if result.Kiu is None else round(result.Kiu, 4),
            "Ki (mM)": None if result.Ki is None else round(result.Ki, 4),
            "alpha": round(result.alpha, 5),
            "alpha_prime": round(result.alpha_p, 5),
            "Km aparente (mM)": round(result.Km_app, 5),
            "Vmax aparente (unidades/min)": round(result.Vmax_app, 5),
            "Velocidad (unidades/min)": round(result.velocity, 5),
        }
        st.session_state.measurements.append(row)
        st.success("Medición registrada.")

    if st.button("Borrar todas las mediciones"):
        st.session_state.measurements = []
        st.success("Se borraron las mediciones de la sesión.")

    if st.session_state.measurements:
        df = pd.DataFrame(st.session_state.measurements)
        st.dataframe(df, hide_index=True, use_container_width=True)
        d1, d2 = st.columns(2)
        d1.download_button("Descargar CSV", dataframe_to_csv_bytes(df), "datos_inhibicion_enzimatica.csv", "text/csv", use_container_width=True)
        d2.download_button("Descargar Excel", dataframe_to_excel_bytes(df), "datos_inhibicion_enzimatica.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    else:
        st.caption("Todavía no hay mediciones registradas.")

with tab_med:
    st.header("Aplicaciones médicas y farmacológicas")
    st.info("Los sistemas farmacológicos reales pueden ser más complejos que los cuatro modelos cinéticos introductorios.")
    st.markdown("""
**Estatinas — HMG-CoA reductasa.** Son un ejemplo docente útil de componente competitivo respecto a HMG-CoA y disminuyen la síntesis de colesterol. El patrón aparente puede depender del sustrato o cofactor analizado.

**Aspirina — ciclooxigenasa (COX).** Produce inactivación covalente irreversible. Es clínicamente importante, pero **no pertenece** al modelo reversible interactivo principal de esta app.

**Metotrexato — dihidrofolato reductasa (DHFR).** Ejemplo clásico de competencia frente a dihidrofolato, con disminución de la regeneración de tetrahidrofolato.

**Acetilcolinesterasa (AChE).** Diferentes fármacos o tóxicos pueden producir mecanismos reversibles, pseudoirreversibles o covalentes persistentes; una misma diana no implica un único patrón cinético.

**CYP450.** Puede mostrar inhibición competitiva, mixta, reversible, quasiirreversible o dependiente del mecanismo y del tiempo; es un buen puente hacia interacciones farmacológicas reales.
""")

st.divider()
st.caption("Modelo educativo: velocidad inicial, cinética de Michaelis-Menten y patrones clásicos de inhibición reversible. No modela cooperatividad, sistemas multisustrato, tight binding, inhibición por sustrato ni inactivación dependiente del tiempo.")
