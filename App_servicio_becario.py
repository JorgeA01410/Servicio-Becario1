import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import *
# Configuración de página
st.set_page_config(page_title="Dashboard de Asesores", layout="wide", page_icon="")

def set_custom_theme():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF;
        }

        [data-testid="stHeader"] {
            background-color: #FFFFFF;
        }

        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
        }
                
        .stButton>button {
            background-color: #0071B9;
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #0071B9;
            color: white;
        }
        .stSelectbox div[data-baseweb="select"] {
            background-color: #FFFFFF;
            border-radius: 10px;
            border: 2px solid #0071B9;
            font-size: 40 px;
        }
        .metric {
            background-color: #FFFFFF;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px #0071B9;
            margin-bottom: 10px;
            color: #0071B9;
            text-align: center;
            border-left: 4px solid #0071B9;
        }
        .header {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            color: #0071B9;
            font-family: 'Arial', sans-serif;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-left: 5px solid #0071B9;
        }
        .stDataFrame {
            border-radius: 10px;
            box-shadow: 0 4px 6px #0071B9;
        }
        .half-moon-container {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100%;
            color: #0071B9;
            box-shadow: 0 4px 6px #0071B9;
            border-top: 3px solid #0071B9;
        }
        .half-moon-title {
            text-align: center;
            margin-bottom: 10px;
            font-weight: light;
            color: #000000;
        }
        .vision-general-del-equipo {
            text-align: center;
            margin-bottom: 10px;
            font-weight: bold;
            color: #000000;
        }
        .performance-text {
            text-align: center;
            margin-top: 10px;
            font-size: 14px;
            color: #000000;
            font-weight: light;
        }
        .progress-container {
            width: 100%;
            margin-top: 15px;
        }
        .progress-label {
            display: flex;
            justify-content: space-between;
            margin-top: 5px;
            font-size: 12px;
            color: #000000;
        }
        .half-moon-chart {
            height: 300px !important;
            margin-bottom: 20px;
        }
        .bar-chart-container {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.06);
            border-top: 4px solid #0071B9;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        h1 {
            color: #0071B9 !important;
            text-align: center;
            background: linear-gradient(to right, #004A7F, #0071B9, #3DB5E6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 10px;
        }
        h2 {
            color: #0071B9 !important;
        }
        h3 {
            color: #0071B9 !important;
        }
        h6,h4 {
            color: #0071B9 !important;
        }
        :root {
            --primary-color: #0071B9;
        }
        *:focus {
            outline: none !important;
        }
        /* contenedor general */
        div[data-baseweb="select"] {
            border: 2px solid #0071B9 !important;
            border-radius: 10px !important;
        }

        /* elemento interno que recibe el focus */
        div[data-baseweb="select"] > div {
            border: none !important;
            box-shadow: none !important;
        }

        /* focus real del selectbox */
        div[data-baseweb="select"] > div:focus,
        div[data-baseweb="select"] > div:focus-visible,
        div[data-baseweb="select"]:focus-within {
            outline: none !important;
            box-shadow: 0 0 0 2px rgba(0,113,185,0.25) !important;
            border-color: #0071B9 !important;
        }        
        </style>
        """, unsafe_allow_html=True)


datos = pd.read_excel("Calificaciones.xlsx",1)
df = datos[datos['Año'] < 2026].iloc[:, [4,8,9,10,11,12,13,14,15,16]]
df2 = datos[datos['Año'] < 2026].iloc[:, [4,8,9,10,11,12,13,14,15,16,17,18]]
set_custom_theme()


# Título con estilo
st.markdown("<h1 style='text-align: center;'>Dashboard de Desempeño de Asesores</h1>", unsafe_allow_html=True)

# ===== GRÁFICOS =====
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='bar-chart-container'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Cantidad de Interacciones por Asesor</h3>", unsafe_allow_html=True)
    # Para tiempo de respuesta, menor es mejor (ordenamos ascendente)

    fig = cantidad_interacciones_asesor(df)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='bar-chart-container'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Heatmap de Desempeño del Equipo</h3>", unsafe_allow_html=True)
    # Para tickets pendientes, menor es mejor (ordenamos ascendente)

    fig = heatmap_equipo(df)
    st.pyplot(fig)




# Sección de selección de agente
asesores = df['Asesor'].unique()
asesores_dict = {}

for asesor in asesores:
    asesores_dict[asesor] = df[df['Asesor'] == asesor]

st.markdown("---")
st.markdown("<h1 style='text-align: center;'> Visualización por Asesor</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:18px; margin-bottom:0px;'>Selecciona un agente para ver sus métricas detalladas:</p>",
    unsafe_allow_html=True
)
asesor_seleccionado = st.selectbox("", asesores)

if asesor_seleccionado:

    # Tarjetas de métricas mejoradas
    st.markdown("---")

    # col1, col2 = st.columns([1, 1])

    # with col1:
    #     st.markdown("<div class='bar-chart-container'></div>", unsafe_allow_html=True)
    #     st.markdown(f"<h3 style='text-align: center;'>Semáforo de desempeño - {asesor_seleccionado}</h3>", unsafe_allow_html=True)
    #     fig = semaforo_bar(asesores_dict[asesor_seleccionado])
    #     st.pyplot(fig)

    
    promedio = df2.groupby("Asesor")["Calificación"].mean()
    # with col2:
    #     st.markdown("<div class='bar-chart-container'>", unsafe_allow_html=True)
    #     st.markdown("<h3 style='text-align:center;'>Calificación Promedio</h3>", unsafe_allow_html=True)
    #     fig, performance = crearluna(promedio[asesor_seleccionado])
    #     st.pyplot(fig, use_container_width=True)

    metricas_resumidas1 = ["Saludo y ánimo","Redacción","Ortografía","Necesidad verdadera (KPI)","Resolver (KPI)"
             ,"Control","Clasificación","Documentación","Resolución","Puntaje","Calificación"]

    df2.columns = ["Asesor"] + metricas_resumidas1
    mean = df2.groupby("Asesor")[metricas_resumidas1].mean()
    std = df2.groupby("Asesor")[metricas_resumidas1].std()
    cv = std / mean

    amenazas = (std > 12) | (cv > 0.15)

    metricas_interes = ["Necesidad verdadera (KPI)", "Resolver (KPI)", "Resolución"]
    metricas_interes_correctas = {
        "Necesidad verdadera (KPI)" : 'Encontrar necesidad verdadera (KPI)',
        "Resolver (KPI)" : 'Resolver y accionar al momento (KPI)',
        "Resolución": 'Confirmar la resolución, ofrecer ayuda adicional, despedida cálida y ofrecer encuesta'
    }

    # Filtra al asesor y selecciona solo esas métricas
    df_asesor = amenazas.loc[asesor_seleccionado, metricas_interes]

    # Mantener solo las métricas que sean True
    metricas_true = df_asesor[df_asesor == True].index.tolist()
    # with col2:
    #     st.markdown("<div class='bar-chart-container'>", unsafe_allow_html=True)
    #     #st.markdown("<h3 style='text-align:center;'>Amenazas</h3>", unsafe_allow_html=True)
    #     if len(metricas_true) == 3:
    #         st.markdown(f"""
    #         <div class='metric'>
    #             <h3>Amenazas</h3>
    #             <h4>{metricas_interes_correctas[metricas_true[0]]}</h4>
    #             <h4>{metricas_interes_correctas[metricas_true[1]]}</h4>
    #             <h4>{metricas_interes_correctas[metricas_true[2]]}</h4>
    #         </div>
    #         """, unsafe_allow_html=True)  
    #     elif len(metricas_true) == 2:
    #         st.markdown(f"""
    #         <div class='metric'>
    #             <h3>Amenazas</h3>
    #             <h4>{metricas_interes_correctas[metricas_true[0]]}</h4>
    #             <h4>{metricas_interes_correctas[metricas_true[1]]}</h4>
    #         </div>
    #         """, unsafe_allow_html=True)
    #     else:
    #         st.markdown(f"""
    #         <div class='metric'>
    #             <h3>Amenazas</h3>
    #             <h4>{metricas_interes_correctas[metricas_true[0]]}</h4>
    #         </div>
    #         """, unsafe_allow_html=True)
# Preparar HTML + CSS
with st.container():
    # Creamos dos columnas: izquierda ancha, derecha estrecha
    col1, col2 = st.columns([2, 1])  # izquierda 2x ancho de derecha

    # Columna izquierda (Semáforo, ocupa dos filas visualmente)
    with col1:
        st.markdown("<div class='bar-chart-container'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center;'>Semáforo de desempeño - {asesor_seleccionado}</h3>", unsafe_allow_html=True)
        fig = semaforo_bar(asesores_dict[asesor_seleccionado])
        st.pyplot(fig)

    # Columna derecha: apilamos dos gráficas
    with col2:
        # Primera fila (Calificación promedio)
        st.markdown("<div class='bar-chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>Calificación Promedio</h3>", unsafe_allow_html=True)
        fig, performance = crearluna(promedio[asesor_seleccionado])
        st.pyplot(fig, use_container_width=True)

        st.markdown("<div class='bar-chart-container'>", unsafe_allow_html=True)  # separación

        # Segunda fila (Amenazas)
        
        df_asesor = amenazas.loc[asesor_seleccionado, metricas_interes]
        metricas_true = df_asesor[df_asesor == True].index.tolist()
        st.markdown("<h3 style='text-align:center;'>Amenazas</h3>", unsafe_allow_html=True)
        if len(metricas_true) > 0:
            metricas_html = "".join([f"<h4 style='text-align:center;'>{metricas_interes_correctas[m]}</h4>" for m in metricas_true])
            #st.markdown("<h3 style='text-align:center;'>Amenazas</h3>", unsafe_allow_html=True)
            st.markdown(metricas_html, unsafe_allow_html=True)