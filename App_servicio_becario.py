import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import *

# ─── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Asesores",
    layout="wide",
    page_icon="2",
    initial_sidebar_state="expanded",
)

# ─── CSS global ────────────────────────────────────────────────────────────────
def set_custom_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --blue-900: #002F5F;
        --blue-700: #0055A5;
        --blue-500: #0071B9;
        --blue-300: #3DB5E6;
        --blue-100: #D6EEF8;
        --blue-50:  #EEF7FC;
        --neutral-900: #0F1923;
        --neutral-600: #4A5568;
        --neutral-300: #CBD5E0;
        --neutral-100: #F7FAFC;
        --white: #FFFFFF;
        --green:  #27AE60;
        --yellow: #F39C12;
        --red:    #E74C3C;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 20px;
        --shadow-md: 0 4px 12px rgba(0,71,185,.10);
    }

    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stHeader"], .main {
        background-color: var(--neutral-100) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--blue-900) 0%, var(--blue-700) 100%) !important;
        border-right: none !important;
    }
    [data-testid="stSidebar"] * { color: var(--white) !important; }
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background: rgba(255,255,255,.12) !important;
        border: 1px solid rgba(255,255,255,.25) !important;
        border-radius: var(--radius-sm) !important;
    }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.2) !important; }

    h1 { font-size: 1.9rem !important; font-weight: 700 !important;
         color: var(--blue-900) !important; letter-spacing: -.5px; }
    h2 { font-size: 1.3rem !important; font-weight: 600 !important;
         color: var(--blue-700) !important; }
    h3 { font-size: 1.05rem !important; font-weight: 600 !important;
         color: var(--blue-900) !important; }

    .kpi-card {
        background: var(--white);
        border-radius: var(--radius-md);
        padding: 18px 20px;
        box-shadow: var(--shadow-md);
        border-top: 3px solid var(--blue-500);
        margin-bottom: 4px;
    }
    .kpi-label {
        font-size: .75rem; font-weight: 600;
        letter-spacing: .06em; text-transform: uppercase;
        color: var(--neutral-600); margin-bottom: 4px;
    }
    .kpi-value { font-size: 2rem; font-weight: 700;
                 color: var(--blue-900); line-height: 1.1; }
    .kpi-sub   { font-size: .8rem; color: var(--neutral-600); margin-top: 4px; }
    .kpi-badge {
        display: inline-block; font-size: .7rem; font-weight: 600;
        padding: 2px 8px; border-radius: 99px; margin-top: 6px;
    }
    .kpi-badge.green  { background:#E8F8F0; color:var(--green); }
    .kpi-badge.yellow { background:#FEF9E7; color:var(--yellow);}
    .kpi-badge.red    { background:#FDEDEC; color:var(--red);   }

    .section-card {
        background: var(--white);
        border-radius: var(--radius-lg);
        padding: 24px 28px;
        box-shadow: var(--shadow-md);
        margin-bottom: 24px;
    }
    .section-title {
        font-size: 1rem; font-weight: 600; color: var(--blue-900);
        margin-bottom: 16px; padding-bottom: 10px;
        border-bottom: 1px solid var(--blue-100);
    }

    .amenaza-pill {
        display: flex; align-items: center; gap: 10px;
        background: #FDEDEC; border-left: 4px solid var(--red);
        border-radius: var(--radius-sm); padding: 10px 14px;
        margin-bottom: 8px; font-size: .85rem;
        color: #922B21; font-weight: 500;
    }

    .custom-divider { border: none; border-top: 1px solid var(--neutral-300); margin: 28px 0; }

    div[data-baseweb="input"] { background-color: var(--white) !important; border: 2px solid var(--blue-300) !important; border-radius: var(--radius-sm) !important; }
    div[data-baseweb="input"] input { background-color: var(--white) !important; color: var(--neutral-900) !important; }
    div[data-baseweb="input"] button { background-color: var(--white) !important; border: none !important; color: var(--neutral-600) !important; }
    div[data-baseweb="select"] { border: 2px solid var(--blue-300) !important; border-radius: var(--radius-sm) !important; background-color: var(--white) !important; }
    div[data-baseweb="select"] > div { border: none !important; box-shadow: none !important; background-color: var(--white) !important; }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] p { color: #0F1923 !important; font-weight: 500 !important; }
    [role="listbox"] { background-color: #FFFFFF !important; }
    [role="option"] { background-color: #FFFFFF !important; color: #0F1923 !important; }
    [role="option"]:hover, [aria-selected="true"] { background-color: #EEF7FC !important; color: #002F5F !important; }

    .stButton > button {
        background: var(--blue-500) !important; color: var(--white) !important;
        border-radius: var(--radius-sm) !important; border: none !important;
        font-weight: 600 !important; padding: 8px 20px !important;
    }
    .stButton > button:hover { background: var(--blue-700) !important; }

    #MainMenu, footer { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }
    </style>
    """, unsafe_allow_html=True)


# ─── Data ──────────────────────────────────────────────────────────────────────
ASESORES_INACTIVOS = [
    "Alberto Gonzalez Carballo",
    "Angela Patricia Gonzalez Torres",
    "Elisa Esperanza Rodriguez Sanchez",
    "Juan Andres Aguilar Garcia",
    "Sandra Ofelia Gómez Urbina",
    "Sergio Armenta Sánchez",
    "Zaira Judith Pérez Arizpe",
]

@st.cache_data
def load_data():
    datos = pd.read_excel("Calificaciones.xlsx", 1)
    datos = datos[datos['Año'] < 2026]
    datos = datos[~datos.iloc[:, 4].isin(ASESORES_INACTIVOS)]
    # Periodo académico Ago-Jul
    def get_periodo_acad(row):
        if row['Mes'] >= 8:
            return f"Ago {int(row['Año'])} – Jul {int(row['Año']) + 1}"
        else:
            return f"Ago {int(row['Año']) - 1} – Jul {int(row['Año'])}"
    datos['periodo_acad'] = datos.apply(get_periodo_acad, axis=1)
    df        = datos.iloc[:, [4, 8, 9, 10, 11, 12, 13, 14, 15, 16]]
    df2       = datos.iloc[:, [4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]]
    df_tiempo = datos.iloc[:, [0, 1, 2, 4, 17, 18]]
    df_texto  = datos.iloc[:, [4, 5, 19]]
    periodos  = datos['periodo_acad']
    return df, df2, df_tiempo, df_texto, periodos

df_raw, df2_raw, df_tiempo_raw, df_texto_raw, periodos_serie = load_data()

metricas_resumidas1 = [
    "Saludo y ánimo", "Redacción", "Ortografía",
    "Necesidad verdadera (KPI)", "Resolver (KPI)",
    "Control", "Clasificación", "Documentación",
    "Resolución", "Puntaje", "Calificación"
]
metricas_interes = ["Necesidad verdadera (KPI)", "Resolver (KPI)", "Resolución"]
metricas_interes_correctas = {
    "Necesidad verdadera (KPI)": "Encontrar necesidad verdadera (KPI)",
    "Resolver (KPI)": "Resolver y accionar al momento (KPI)",
    "Resolución": "Confirmar resolución y despedida cálida",
}
periodos_disponibles = sorted(periodos_serie.unique(), key=lambda p: int(p.split()[1]))

set_custom_theme()

# ═══════════════════════════════════════════════════════════════════════════════
# AUTENTICACIÓN
# ═══════════════════════════════════════════════════════════════════════════════
def login_screen():
    col_c, col_form, col_d = st.columns([1, 1.2, 1])
    with col_form:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("https://atencionremota.tec.mx/sites/g/files/vgjovo2371/files/inline-images/tecservices%20color%20%281%29.png", width=200)
        st.markdown("<h2 style='color:#002F5F; margin-top:16px;'>Acceso al Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#4A5568; margin-bottom:24px;'>Ingresa tu contraseña para continuar.</p>", unsafe_allow_html=True)
        password = st.text_input("Contraseña", type="password", placeholder="••••••••")
        if st.button("Ingresar", use_container_width=True):
            passwords = st.secrets.get("passwords", {})
            if password == passwords.get("admin", ""):
                st.session_state.autenticado = True
                st.session_state.es_admin = True
                st.session_state.asesor_login = None
                st.rerun()
            else:
                match = next((nombre for nombre, pwd in passwords.items() if nombre != "admin" and password == pwd), None)
                if match:
                    st.session_state.autenticado = True
                    st.session_state.es_admin = False
                    st.session_state.asesor_login = match
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta.")

if not st.session_state.get("autenticado", False):
    login_screen()
    st.stop()

es_admin      = st.session_state.get("es_admin", False)
asesor_login  = st.session_state.get("asesor_login", None)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image("https://atencionremota.tec.mx/sites/g/files/vgjovo2371/files/inline-images/tecservices%20color%20%281%29.png",  use_container_width=False, width=200)
    st.markdown("## Dashboard")
    st.markdown("**Desempeño de Asesores**")
    st.markdown("<hr>", unsafe_allow_html=True)

    if es_admin:
        vista = st.radio(
            "Navegación",
            ["Vision General", "Por Asesor"],
            label_visibility="collapsed",
        )
    else:
        vista = "Por Asesor"
        st.markdown("**Vista:** Por Asesor", unsafe_allow_html=False)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    usuario_label = "Admin" if es_admin else asesor_login
    st.markdown(f"<p style='font-size:.8rem; color:rgba(255,255,255,.7);'>Sesión: {usuario_label}</p>", unsafe_allow_html=True)
    if st.button("Cerrar sesión", use_container_width=True):
        for key in ["autenticado", "es_admin", "asesor_login"]:
            st.session_state.pop(key, None)
        st.rerun()


# ─── Helper: aplicar filtro de periodo ────────────────────────────────────────
def aplicar_filtro(periodo_sel):
    mask = periodos_serie.notna() if periodo_sel == "Histórico" else periodos_serie == periodo_sel
    df        = df_raw[mask].copy()
    df2       = df2_raw[mask].copy()
    df_tiempo = df_tiempo_raw[mask].copy()
    df_texto  = df_texto_raw[mask].copy()

    df2.columns       = ["Asesor"] + metricas_resumidas1
    df_tiempo.columns = ["Periodo", "Mes", "Año", "Asesor", "Puntaje", "Calificación"]
    df_texto.columns  = ["Asesor", "Interaccion", "Comentarios"]

    asesores             = df['Asesor'].unique()
    asesores_dict        = {a: df[df['Asesor'] == a] for a in asesores}
    asesores_tiempo_dict = {a: df_tiempo[df_tiempo['Asesor'] == a] for a in asesores}
    asesores_texto_dict  = {a: df_texto[df_texto['Asesor'] == a][["Interaccion", "Comentarios"]] for a in asesores}

    promedio_global         = df2.groupby("Asesor")["Calificación"].mean()
    promedio_global_puntaje = df2.groupby("Asesor")["Puntaje"].mean()
    std_df   = df2.groupby("Asesor")[metricas_resumidas1].std()
    cv_df    = std_df / df2.groupby("Asesor")[metricas_resumidas1].mean()
    amenazas = (std_df > 12) | (cv_df > 0.15)

    return (df, df2, df_tiempo, df_texto, asesores, asesores_dict,
            asesores_tiempo_dict, asesores_texto_dict,
            promedio_global, promedio_global_puntaje, amenazas)

# ═══════════════════════════════════════════════════════════════════════════════
# VISTA GENERAL
# ═══════════════════════════════════════════════════════════════════════════════
if "Vision General" in vista:

    h1, col_periodo = st.columns([3, 1])
    with h1:
        st.markdown("<h1>Visión General del Equipo</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#4A5568; margin-top:-8px; margin-bottom:24px;'>"
            "Resumen de desempeño de todos los asesores.</p>",
            unsafe_allow_html=True,
        )
    with col_periodo:
        st.markdown("<br>", unsafe_allow_html=True)
        periodo_sel = st.selectbox(
            "Periodo",
            ["Histórico"] + list(reversed(periodos_disponibles)),
            key="periodo_general",
        )

    (df, df2, df_tiempo, df_texto, asesores, asesores_dict,
     asesores_tiempo_dict, asesores_texto_dict,
     promedio_global, promedio_global_puntaje, amenazas) = aplicar_filtro(periodo_sel)

    # ── KPI Cards ──────────────────────────────────────────────────────────────
    total_interacciones = len(df)
    total_asesores      = df['Asesor'].nunique()
    cal_promedio        = df2["Calificación"].mean()
    mejor_asesor        = promedio_global.idxmax()
    mejor_cal           = promedio_global.max()

    if cal_promedio > 89:   badge_clase, badge_txt = "green",  "Excelente"
    elif cal_promedio >= 70: badge_clase, badge_txt = "yellow", "Bueno"
    else:                    badge_clase, badge_txt = "red",    "Necesita mejorar"

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>Interacciones</div>
            <div class='kpi-value'>{total_interacciones:,}</div>
            <div class='kpi-sub'>Total registradas</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>Asesores</div>
            <div class='kpi-value'>{total_asesores}</div>
            <div class='kpi-sub'>Totales</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>Calificación Promedio</div>
            <div class='kpi-value'>{cal_promedio:.1f}</div>
            <span class='kpi-badge {badge_clase}'>{badge_txt}</span>
        </div>""", unsafe_allow_html=True)


    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    # ── Gráficas ───────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("<div class='section-card'><div class='section-title'>Interacciones por Asesor</div>", unsafe_allow_html=True)
        chart = cantidad_interacciones_asesor(df)
        st.altair_chart(chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-card'><div class='section-title'>Heatmap de Desempeño</div>", unsafe_allow_html=True)
        chart = heatmap_equipo(df)
        st.altair_chart(chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# VISTA POR ASESOR
# ═══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown("<h1>Desempeño por Asesor</h1>", unsafe_allow_html=True)

    # Listado completo de asesores (sin filtrar por periodo)
    all_asesores = sorted(df_raw['Asesor'].unique())

    if es_admin:
        col_asesor, col_periodo = st.columns([2, 1])
        with col_asesor:
            asesor = st.selectbox(
                "Asesor",
                options=[""] + all_asesores,
                key="asesor_sel",
            )
        with col_periodo:
            periodo_sel = st.selectbox(
                "Periodo",
                ["Histórico"] + list(reversed(periodos_disponibles)),
                key="periodo_asesor",
            )
        if not asesor:
            st.stop()
    else:
        asesor = asesor_login
        periodo_sel = st.selectbox(
            "Periodo",
            ["Histórico"] + list(reversed(periodos_disponibles)),
            key="periodo_asesor",
        )

    (df, df2, df_tiempo, df_texto, asesores, asesores_dict,
     asesores_tiempo_dict, asesores_texto_dict,
     promedio_global, promedio_global_puntaje, amenazas) = aplicar_filtro(periodo_sel)

    if asesor not in asesores:
        st.markdown(
            f"<div style='background:#FEF9E7; border-left:4px solid #F39C12; border-radius:8px; "
            f"padding:12px 16px; color:#7D6608; font-weight:500;'>"
            f"No hay datos para <strong>{asesor}</strong> en el periodo <strong>{periodo_sel}</strong>.</div>",
            unsafe_allow_html=True,
        )
        st.stop()

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

    cal_asesor  = promedio_global[asesor]
    punt_asesor = promedio_global_puntaje[asesor]
    n_inter     = len(asesores_dict[asesor])
    df_amenazas = amenazas.loc[asesor, metricas_interes]
    n_amenazas  = int(df_amenazas.sum())

    if punt_asesor >= 90:   badge_clase, badge_txt = "green",  "Excelente"
    elif punt_asesor >= 70: badge_clase, badge_txt = "yellow", "Bueno"
    else:                  badge_clase, badge_txt = "red",    "Necesita mejorar"

    if n_amenazas == 0:   am_clase, am_txt = "green",  "Sin amenazas"
    elif n_amenazas == 1: am_clase, am_txt = "yellow", "1 amenaza"
    else:                 am_clase, am_txt = "red",    f"{n_amenazas} amenazas"

    ka, kb, kc = st.columns(3)
    with ka:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>Interacciones</div>
            <div class='kpi-value'>{n_inter}</div>
            <div class='kpi-sub'>Registradas para este asesor</div>
        </div>""", unsafe_allow_html=True)
    with kb:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>Puntaje</div>
            <div class='kpi-value'>{punt_asesor:.1f}</div>
            <span class='kpi-badge {badge_clase}'>{badge_txt}</span>
        </div>""", unsafe_allow_html=True)
    with kc:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-label'>Alertas KPI</div>
            <div class='kpi-value'>{n_amenazas}</div>
            <span class='kpi-badge {am_clase}'>{am_txt}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3], gap="large")

    with col1:
        st.markdown("<div class='section-card'><div class='section-title'>Calificación Promedio</div>", unsafe_allow_html=True)
        fig, performance = crearluna(promedio_global[asesor])
        st.pyplot(fig, use_container_width=True)
        st.markdown(
            f"<p style='text-align:center; font-weight:600; color:#0055A5; margin-top:4px;'>{performance}</p>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-card'><div class='section-title'>Análisis FODA</div>", unsafe_allow_html=True)
        chart = foda_cuadrantes(asesores_dict[asesor], df_amenazas)
        st.altair_chart(chart, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'><div class='section-title'>Tendencia en el Tiempo</div>", unsafe_allow_html=True)
    chart = tendencia_asesor(asesores_tiempo_dict[asesor])
    st.altair_chart(chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'><div class='section-title'>Resumen de Fortalezas y Areas de Oportunidad</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#4A5568; font-size:.85rem; margin-top:-8px; margin-bottom:16px;'>Oraciones más representativas extraídas de los comentarios de evaluación.</p>", unsafe_allow_html=True)
    oraciones = resumen_comentarios(asesores_texto_dict[asesor])
    if not oraciones:
        st.markdown("<p style='color:#4A5568; font-style:italic;'>Sin comentarios registrados para este asesor.</p>", unsafe_allow_html=True)
    else:
        for i, (oracion, fuentes) in enumerate(oraciones, 1):
            fuentes_html = " ".join(
                f"<span style='display:inline-block; font-size:.7rem; font-weight:600; "
                f"padding:2px 8px; border-radius:99px; background:#D6EEF8; color:#0055A5; margin-right:4px;'>{f}</span>"
                for f in fuentes
            )
            st.markdown(f"""
            <div style='display:flex; align-items:flex-start; gap:12px; margin-bottom:14px;'>
                <div style='min-width:24px; height:24px; border-radius:50%; background:#0071B9;
                            color:white; font-size:.75rem; font-weight:700; flex-shrink:0;
                            display:flex; align-items:center; justify-content:center;'>{i}</div>
                <div>
                    <p style='margin:0 0 4px 0; color:#0F1923; font-size:.9rem; line-height:1.55;'>{oracion}</p>
                    <div>{fuentes_html}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Comparativa con periodo anterior ───────────────────────────────────────
    st.markdown("<div class='section-card'><div class='section-title'>Comparativa con Periodo Anterior</div>", unsafe_allow_html=True)

    idx_actual = periodos_disponibles.index(periodo_sel) if periodo_sel != "Histórico" else -1

    if periodo_sel == "Histórico" or idx_actual == 0:
        st.markdown("<p style='color:#4A5568; font-style:italic;'>Selecciona un periodo específico (no el primero) para ver la comparativa con el anterior.</p>", unsafe_allow_html=True)
    else:
        periodo_anterior = periodos_disponibles[idx_actual - 1]
        (_, df2_ant, _, _, _, _, _, _, _, _, _) = aplicar_filtro(periodo_anterior)

        metricas_comp = ["Saludo y ánimo", "Redacción", "Ortografía",
                         "Necesidad verdadera (KPI)", "Resolver (KPI)",
                         "Control", "Clasificación", "Documentación",
                         "Resolución", "Puntaje", "Calificación"]

        delta_data, chart_comp = comparativa_periodos(
            df2, df2_ant, asesor, periodo_sel, periodo_anterior, metricas_comp
        )

        # Cards delta para Puntaje y Calificación
        kpi_metricas = ["Puntaje", "Calificación"]
        cols_kpi = st.columns(2)
        for col, item in zip(cols_kpi, [d for d in delta_data if d["metrica"] in kpi_metricas]):
            if item["delta"] is None:
                delta_html = "<span class='kpi-badge yellow'>Sin dato anterior</span>"
            elif item["delta"] > 0:
                delta_html = f"<span class='kpi-badge green'>▲ {item['delta']:+.1f}</span>"
            elif item["delta"] < 0:
                delta_html = f"<span class='kpi-badge red'>▼ {item['delta']:+.1f}</span>"
            else:
                delta_html = "<span class='kpi-badge yellow'>= Sin cambio</span>"
            with col:
                st.markdown(f"""<div class='kpi-card'>
                    <div class='kpi-label'>{item['metrica']}</div>
                    <div class='kpi-value'>{item['actual'] if item['actual'] is not None else '—'}</div>
                    <div class='kpi-sub'>Anterior: {item['anterior'] if item['anterior'] is not None else '—'} &nbsp;·&nbsp; {periodo_anterior}</div>
                    {delta_html}
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.altair_chart(chart_comp, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
