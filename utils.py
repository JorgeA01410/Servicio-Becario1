import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Wedge

metricas_resumidas = ["Saludo y ánimo","Redacción","Ortografía","Necesidad verdadera (KPI)","Resolver (KPI)"
            ,"Control","Clasificación","Documentación","Resolución"]

def cantidad_interacciones_asesor(df):
    agente_counts = df['Asesor'].value_counts()

    fig, ax = plt.subplots(figsize=(14,7))

    bars = ax.bar(
        agente_counts.index,
        agente_counts.values,
        color='#0071B9',
        edgecolor='none'
    )

    # títulos
    ##ax.set_title('Cantidad de Interacciones por Asesor', fontsize=16, fontweight='bold')
    ax.set_xlabel('Asesor', fontsize=12)
    ax.set_ylabel('Cantidad de Interacciones', fontsize=12)

    # rotación de etiquetas
    ax.set_xticklabels(agente_counts.index, rotation=40, ha='right')

    # grid suave
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    # quitar bordes innecesarios
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # mostrar valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom',
            fontsize=10
        )

    fig.tight_layout()

    return fig


def heatmap_equipo(df):
    df.columns = ["Asesor"] + metricas_resumidas

    max_scores = df[metricas_resumidas].max()
    pivot = (df.groupby("Asesor")[metricas_resumidas].mean() / max_scores) * 100

    fig, ax = plt.subplots(figsize=(12,6))

    cmap = LinearSegmentedColormap.from_list(
        "custom_blue",
        ["#0071B9", "#FFFFFF"]
    )

    im = ax.imshow(pivot, aspect="auto", cmap=cmap, vmin=0, vmax=100)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Desempeño (%)")

    ax.set_xticks(range(len(metricas_resumidas)))
    ax.set_xticklabels(metricas_resumidas, rotation=40, ha="right")

    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)

    ##ax.set_title("Heatmap de Desempeño del Equipo", fontsize=16, fontweight="bold")

    for i in range(len(pivot.index)):
        for j in range(len(metricas_resumidas)):
            value = pivot.iloc[i, j]
            ax.text(j, i, f"{value:.0f}%", ha="center", va="center", fontsize=9)

    plt.tight_layout()
    return fig

def semaforo_bar(df):
    df.columns = ["Asesor"] + metricas_resumidas

    # Normalización a porcentaje
    data = (df[metricas_resumidas].mean() / df[metricas_resumidas].max()) * 100

    # Ordenar para mejor visualización
    data = data.sort_values()

    # Colores tipo semáforo más profesionales
    colores = []
    for v in data:
        if v >= 90:
            colores.append("#2ECC71")   # verde suave
        elif v >= 70:
            colores.append("#F1C40F")   # amarillo
        else:
            colores.append("#E74C3C")   # rojo

    fig, ax = plt.subplots(figsize=(10,6))

    bars = ax.barh(
        data.index,
        data.values,
        color=colores,
        edgecolor="black",
        linewidth=0.6
    )

    ax.set_xlim(0,100)

    ax.set_xlabel("Puntaje (%)", fontsize=11)
    ax.set_ylabel("Métrica", fontsize=11)

    # Grid suave
    #ax.grid(axis='x', linestyle='--', alpha=0.4)

    # Quitar bordes innecesarios
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Mostrar valor en cada barra
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 1,
            bar.get_y() + bar.get_height()/2,
            f"{width:.1f}",
            va='center',
            fontsize=10
        )

    plt.tight_layout()

    return fig

def crearluna(promedio):
    fig, ax = plt.subplots(figsize=(6, 4))  # Más alto
 
    if promedio >= 90:  
        color = '#2ECC71'  # Verde
        performance = "Excelente"
    elif promedio >= 70:  
        color = '#F1C40F'  # Amarillo
        performance = "Bueno"
    else:
        color = '#E74C3C'  # Rojo
        performance = "Necesita mejorar"

    # Borde exterior
    borde = Wedge(
        (0.5,0.15),
        0.45,
        0,
        180,
        width=0.25,
        facecolor="none",
        edgecolor="black",
        linewidth=1.5
    )
    ax.add_patch(borde)

    # Fondo (gris claro)
    wedge_bg = Wedge(
        (0.5, 0.15),
        0.45,
        0,
        180,
        width=0.25,
        color="#DDEBF4",
        edgecolor="black",
        linewidth=0.8
    )
    ax.add_patch(wedge_bg)

    # Porcentaje (color)
    angulo = 180 * (promedio / 100)

    wedge_fill = Wedge(
        (0.5, 0.15),
        0.45,
        0,
        angulo,
        width=0.25,
        color=color,
        edgecolor="black",
        linewidth=0.8
    )
    ax.add_patch(wedge_fill)

    # Texto central
    ax.text(0.5, 0.15, f"{promedio:.1f}", ha='center', va='center', fontsize=20, fontweight='bold', color=color)


    #ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.7)
    ax.axis('off')
    plt.tight_layout()

    return fig, performance