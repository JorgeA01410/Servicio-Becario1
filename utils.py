import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import numpy as np
import altair as alt

# ─── Paleta corporativa ────────────────────────────────────────────────────────
BLUE_900    = "#002F5F"
BLUE_700    = "#0055A5"
BLUE_500    = "#0071B9"
BLUE_300    = "#3DB5E6"
BLUE_100    = "#D6EEF8"
BLUE_50     = "#EEF7FC"
NEUTRAL_600 = "#4A5568"
NEUTRAL_300 = "#CBD5E0"
GREEN       = "#27AE60"
YELLOW      = "#F39C12"
RED         = "#E74C3C"
WHITE       = "#FFFFFF"

metricas_resumidas = [
    "Saludo y ánimo", "Redacción", "Ortografía",
    "Necesidad verdadera (KPI)", "Resolver (KPI)",
    "Control", "Clasificación", "Documentación", "Resolución"
]

# ─── Tema base Altair ──────────────────────────────────────────────────────────
_base_config = dict(
    background=WHITE,
    axis=alt.AxisConfig(
        labelColor=NEUTRAL_600,
        titleColor=NEUTRAL_600,
        gridColor=NEUTRAL_300,
        domainColor=NEUTRAL_300,
        tickColor=NEUTRAL_300,
        labelFontSize=11,
        titleFontSize=12,
    ),
    legend=alt.LegendConfig(
        labelColor=NEUTRAL_600,
        titleColor=NEUTRAL_600,
        labelFontSize=11,
    ),
    view=alt.ViewConfig(stroke="transparent"),
)


# ─── 1. Cantidad de interacciones por asesor ──────────────────────────────────
def cantidad_interacciones_asesor(df):
    counts = df['Asesor'].value_counts().reset_index()
    counts.columns = ["Asesor", "count"]
    avg = counts["count"].mean()

    # Pre-ordenar en pandas y usar lista explicita — unica forma confiable en capas
    counts = counts.sort_values("count", ascending=False).reset_index(drop=True)
    orden_asesores = counts["Asesor"].tolist()

    base = alt.Chart(counts)

    bars = base.mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4).encode(
        x=alt.X("Asesor:N",
                sort=orden_asesores,
                title="Asesor",
                axis=alt.Axis(labelAngle=-35)),
        y=alt.Y("count:Q",
                title="Cantidad de Interacciones",
                axis=alt.Axis(grid=True)),
        color=alt.Color("count:Q",
                        scale=alt.Scale(range=[BLUE_100, BLUE_900]),
                        legend=None),
        tooltip=[
            alt.Tooltip("Asesor:N", title="Asesor"),
            alt.Tooltip("count:Q",  title="Interacciones"),
        ],
    )

    text = base.mark_text(
        align="center", baseline="bottom", dy=-4,
        fontSize=11, fontWeight=600, color=BLUE_900
    ).encode(
        x=alt.X("Asesor:N", sort=orden_asesores),
        y=alt.Y("count:Q"),
        text=alt.Text("count:Q", format="d"),
    )

    avg_line = (
        alt.Chart(pd.DataFrame({"avg": [avg]}))
        .mark_rule(color=BLUE_300, strokeDash=[5, 3], strokeWidth=1.5)
        .encode(y="avg:Q")
    )

    chart = (
        (bars + text + avg_line)
        .properties(height=320)
        .configure(**_base_config)
    )
    return chart


# ─── 2. Heatmap de desempeño del equipo ───────────────────────────────────────
def heatmap_equipo(df):
    df = df.copy()
    df.columns = ["Asesor"] + metricas_resumidas

    max_scores = df[metricas_resumidas].max()
    pivot = (df.groupby("Asesor")[metricas_resumidas].mean() / max_scores) * 100

    # Pre-ordenar asesores por promedio descendente → Altair los recibe ya ordenados
    orden_asesores = pivot.mean(axis=1).sort_values(ascending=True).index.tolist()

    long_df = (
        pivot.reset_index()
        .melt(id_vars="Asesor", var_name="Métrica", value_name="Puntaje")
    )
    long_df["Puntaje"] = long_df["Puntaje"].round(1)

    heatmap = (
        alt.Chart(long_df)
        .mark_rect()
        .encode(
            x=alt.X("Métrica:N",
                    sort=metricas_resumidas,
                    axis=alt.Axis(labelAngle=-35, labelLimit=160)),
            y=alt.Y("Asesor:N",
                    title="Asesor",
                    sort=orden_asesores),
            color=alt.Color(
                "Puntaje:Q",
                scale=alt.Scale(
                    domain=[0, 100],
                    range=[BLUE_700, BLUE_50],  # bajo=azul oscuro, alto=blanco
                ),
                legend=alt.Legend(title="Desempeño (%)", gradientLength=120),
            ),
            tooltip=[
                alt.Tooltip("Asesor:N",  title="Asesor"),
                alt.Tooltip("Métrica:N", title="Métrica"),
                alt.Tooltip("Puntaje:Q", title="Puntaje (%)", format=".1f"),
            ],
        )
    )

    text = (
        alt.Chart(long_df)
        .mark_text(fontSize=10, fontWeight=500)
        .encode(
            x=alt.X("Métrica:N", sort=metricas_resumidas),
            y=alt.Y("Asesor:N",
                    sort=orden_asesores),
            text=alt.Text("Puntaje:Q", format=".0f"),
            color=alt.condition(
                alt.datum.Puntaje > 65,
                alt.value(BLUE_900),
                alt.value(WHITE),
            ),
        )
    )

    chart = (
        (heatmap + text)
        .properties(height=max(180, pivot.shape[0] * 42))
        .configure(**_base_config)
    )
    return chart


# ─── 3. Semáforo de desempeño ─────────────────────────────────────────────────
def semaforo_bar(df):
    df = df.copy()
    df.columns = ["Asesor"] + metricas_resumidas

    data = (df[metricas_resumidas].mean() / df[metricas_resumidas].max()) * 100
    semaforo_df = data.reset_index()
    semaforo_df.columns = ["Métrica", "Puntaje"]
    semaforo_df["Puntaje"] = semaforo_df["Puntaje"].round(1)

    def categoria(v):
        if v >= 90:   return "Excelente (≥ 90%)"
        elif v >= 70: return "Bueno (70–89%)"
        else:         return "Mejorar (< 70%)"

    semaforo_df["Categoría"] = semaforo_df["Puntaje"].apply(categoria)

    # Pre-ordenar descendente → lista explícita para Altair (barras horizontales: menor arriba = mayor al fondo)
    orden_metricas = semaforo_df.sort_values("Puntaje", ascending=True)["Métrica"].tolist()

    color_scale = alt.Scale(
        domain=["Excelente (≥ 90%)", "Bueno (70–89%)", "Mejorar (< 70%)"],
        range=[GREEN, YELLOW, RED],
    )

    # Franjas de fondo para zonas
    zonas = pd.DataFrame([
        {"x1": 0,  "x2": 70,  "zona": "Mejorar (< 70%)"},
        {"x1": 70, "x2": 90,  "zona": "Bueno (70–89%)"},
        {"x1": 90, "x2": 105, "zona": "Excelente (≥ 90%)"},
    ])

    fondo = (
        alt.Chart(zonas)
        .mark_rect(opacity=0.06)
        .encode(
            x=alt.X("x1:Q", scale=alt.Scale(domain=[0, 105])),
            x2="x2:Q",
            color=alt.Color("zona:N", scale=color_scale, legend=None),
        )
    )

    barras = (
        alt.Chart(semaforo_df)
        .mark_bar(height=18, cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            y=alt.Y("Métrica:N",
                    sort=orden_metricas,
                    axis=alt.Axis(labelLimit=200)),
            x=alt.X("Puntaje:Q",
                    scale=alt.Scale(domain=[0, 105]),
                    title="Puntaje (%)"),
            color=alt.Color("Categoría:N",
                            scale=color_scale,
                            legend=alt.Legend(title="Categoría", orient="bottom")),
            tooltip=[
                alt.Tooltip("Métrica:N",   title="Métrica"),
                alt.Tooltip("Puntaje:Q",   title="Puntaje (%)", format=".1f"),
                alt.Tooltip("Categoría:N", title="Categoría"),
            ],
        )
    )

    texto = barras.mark_text(
        align="left", dx=4, fontSize=10, fontWeight=600
    ).encode(
        text=alt.Text("Puntaje:Q", format=".1f"),
        color=alt.value(BLUE_900),
    )

    umbrales = pd.DataFrame([{"x": 70, "label": "70%"}, {"x": 90, "label": "90%"}])
    lineas = (
        alt.Chart(umbrales)
        .mark_rule(strokeDash=[4, 3], strokeWidth=1.4, opacity=0.8)
        .encode(
            x="x:Q",
            color=alt.Color("label:N",
                            scale=alt.Scale(
                                domain=["70%", "90%"],
                                range=[RED, GREEN]
                            ),
                            legend=None),
        )
    )

    chart = (
        (fondo + barras + texto + lineas)
        .properties(height=320)
        .configure(**_base_config)
    )
    return chart


# ─── 4. Medidor semicircular (luna) — matplotlib ──────────────────────────────
def crearluna(promedio):
    if promedio >= 89.9:
        color = GREEN
        performance = "Excelente"
    elif promedio >= 70:
        color = YELLOW
        performance = "Bueno"
    else:
        color = RED
        performance = "Necesita mejorar"

    fig, ax = plt.subplots(figsize=(5, 3.2))
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.65)

    cx, cy, r, w = 0.5, 0.12, 0.42, 0.22

    # Marcas de escala
    for pct in [0, 25, 50, 75, 100]:
        angle_rad = np.radians(180 - pct * 180 / 100)
        x_out = cx + (r + 0.04) * np.cos(angle_rad)
        y_out = cy + (r + 0.04) * np.sin(angle_rad)
        ax.text(x_out, y_out, str(pct), ha="center", va="center",
                fontsize=7, color=NEUTRAL_600, fontweight="500")

    ax.add_patch(Wedge((cx, cy), r, 0, 180, width=w,
                       facecolor=BLUE_50, edgecolor=NEUTRAL_300, linewidth=1))

    angulo = 180 * (min(promedio, 100) / 100)
    ax.add_patch(Wedge((cx, cy), r, 0, angulo, width=w,
                       facecolor=color, edgecolor="none", alpha=0.9))

    ax.add_patch(Wedge((cx, cy), r, 0, 180, width=w,
                       facecolor="none", edgecolor=NEUTRAL_300, linewidth=1.2))

    needle_angle = np.radians(angulo)
    needle_r = r - w / 2
    ax.annotate("",
        xy=(cx + needle_r * np.cos(needle_angle),
            cy + needle_r * np.sin(needle_angle)),
        xytext=(cx, cy),
        arrowprops=dict(arrowstyle="-|>", color=BLUE_900, lw=2, mutation_scale=12),
    )
    ax.plot(cx, cy, "o", color=BLUE_900, markersize=7, zorder=10)

    ax.text(cx, cy + 0.13, f"{promedio:.1f}", ha="center", va="center",
            fontsize=22, fontweight="700", color=BLUE_900)
    ax.text(cx, cy + 0.07, performance, ha="center", va="center",
            fontsize=9.5, fontweight="600", color=color)

    fig.tight_layout(pad=0.5)
    return fig, performance

# ─── 5. FODA visual en cuadrantes ─────────────────────────────────────────────
def foda_cuadrantes(df_asesor, amenazas_asesor):
    df_asesor = df_asesor.copy()
    df_asesor.columns = ["Asesor"] + metricas_resumidas

    data = (df_asesor[metricas_resumidas].mean() / df_asesor[metricas_resumidas].max()) * 100
    puntajes = data.reset_index()
    puntajes.columns = ["Metrica", "Puntaje"]
    puntajes["Puntaje"] = puntajes["Puntaje"].round(1)

    def asignar_cuadrante(v):
        if v >= 90:   return "Fortalezas"
        elif v >= 70: return "Oportunidades"
        else:         return "Debilidades"

    puntajes["Cuadrante"] = puntajes["Puntaje"].apply(asignar_cuadrante)

    metricas_amenaza = amenazas_asesor[amenazas_asesor].index.tolist()
    amenaza_df = pd.DataFrame({
        "Metrica":    metricas_amenaza,
        "Puntaje":    [round(float(data.get(m, 0)), 1) for m in metricas_amenaza],
        "Cuadrante":  ["Amenazas"] * len(metricas_amenaza),
    })

    puntajes_filtrado = puntajes[~puntajes["Metrica"].isin(metricas_amenaza)]
    foda_df = pd.concat([puntajes_filtrado, amenaza_df], ignore_index=True)

    # Agregar columna de color por cuadrante
    color_map = {
        "Fortalezas":    "#27AE60",
        "Oportunidades": "#F39C12",
        "Debilidades":   "#E74C3C",
        "Amenazas":      "#8E44AD",
    }
    foda_df["Color"] = foda_df["Cuadrante"].map(color_map)
    foda_df["CuadranteN"] = foda_df["Cuadrante"].map({
        "Fortalezas": 0, "Oportunidades": 1, "Debilidades": 2, "Amenazas": 3
    })

    orden_cuadrantes = ["Fortalezas", "Oportunidades", "Debilidades", "Amenazas"]
    charts = []

    for cuad in orden_cuadrantes:
        subset = foda_df[foda_df["Cuadrante"] == cuad].sort_values("Puntaje", ascending=False).reset_index(drop=True)
        color  = color_map[cuad]
        n      = len(subset)
        titulo = f"{cuad}  ({n})"

        if subset.empty:
            placeholder = pd.DataFrame({"Metrica": ["Sin elementos en este cuadrante"], "Puntaje": [0]})
            chart = (
                alt.Chart(placeholder)
                .mark_text(color=NEUTRAL_600, fontSize=11, fontStyle="italic", align="left")
                .encode(
                    y=alt.Y("Metrica:N", axis=alt.Axis(title=None, ticks=False, domain=False)),
                    text="Metrica:N",
                )
                .properties(height=60, title=alt.Title(titulo, color=color, fontSize=13, fontWeight=700))
            )
        else:
            base = alt.Chart(subset)
            orden = subset["Metrica"].tolist()

            bars = base.mark_bar(
                cornerRadiusTopRight=4, cornerRadiusBottomRight=4,
                color=color, opacity=0.85,
            ).encode(
                y=alt.Y("Metrica:N",
                        sort=orden,
                        axis=alt.Axis(labelLimit=200, labelFontSize=11,
                                      ticks=False, domain=False, title=None)),
                x=alt.X("Puntaje:Q",
                        scale=alt.Scale(domain=[0, 105]),
                        axis=alt.Axis(grid=True, tickCount=4, title="Puntaje (%)", titleFontSize=10)),
                tooltip=[
                    alt.Tooltip("Metrica:N", title="Métrica"),
                    alt.Tooltip("Puntaje:Q", title="Puntaje (%)", format=".1f"),
                ],
            )

            labels = base.mark_text(
                align="left", dx=4, fontSize=10, fontWeight=600, color=color
            ).encode(
                y=alt.Y("Metrica:N", sort=orden),
                x=alt.X("Puntaje:Q"),
                text=alt.Text("Puntaje:Q", format=".1f"),
            )

            chart = (
                (bars + labels)
                .properties(
                    height=max(70, n * 38),
                    title=alt.Title(titulo, color=color, fontSize=13, fontWeight=700),
                )
            )

        charts.append(chart)

    # 2x2 grid — sin background en subchart
    row1 = alt.hconcat(charts[0], charts[1], spacing=20)
    row2 = alt.hconcat(charts[2], charts[3], spacing=20)
    final = alt.vconcat(row1, row2, spacing=20).configure(
        background=WHITE,
        view=alt.ViewConfig(stroke="transparent"),
        axis=alt.AxisConfig(
            labelColor=NEUTRAL_600, titleColor=NEUTRAL_600,
            gridColor=NEUTRAL_300, domainColor=NEUTRAL_300,
            tickColor=NEUTRAL_300, labelFontSize=11, titleFontSize=11,
        ),
        title=alt.TitleConfig(anchor="start", fontSize=13),
    )
    return final


# ─── 6. Tendencia en el tiempo por asesor ─────────────────────────────────────
def tendencia_asesor(df2_asesor):
    """
    Recibe el slice de df2 filtrado por asesor (incluye Mes, Año, Puntaje, Calificación).
    Agrupa por Mes+Año y grafica la evolución de Puntaje y Calificación.
    """
    df = df2_asesor.copy()

    # Construir fecha a partir de Mes y Año (columnas índice 1 y 2 del Excel original)
    # df2_asesor ya viene con columnas renombradas: ["Asesor", métricas..., "Puntaje", "Calificación"]
    # Mes y Año están en el DataFrame original — se pasan como columnas extra
    df["Fecha"] = pd.to_datetime(
        df["Año"].astype(str) + "-" + df["Mes"].astype(str).str.zfill(2) + "-01"
    )
    df["FechaLabel"] = df["Fecha"].dt.strftime("%b %Y")

    resumen = (
        df.groupby("Fecha")[["Puntaje", "Calificación"]]
        .mean()
        .round(1)
        .reset_index()
    )
    resumen["FechaLabel"] = resumen["Fecha"].dt.strftime("%b %Y")
    resumen = resumen.sort_values("Fecha")

    # Formato largo para Altair
    long_df = resumen.melt(
        id_vars=["Fecha", "FechaLabel"],
        value_vars=["Puntaje", "Calificación"],
        var_name="Métrica",
        value_name="Valor",
    )

    color_scale = alt.Scale(
        domain=["Puntaje", "Calificación"],
        range=[BLUE_500, GREEN],
    )

    orden_fechas = resumen["FechaLabel"].tolist()

    lineas = (
        alt.Chart(long_df)
        .mark_line(strokeWidth=2.5, point=alt.OverlayMarkDef(size=60, filled=True))
        .encode(
            x=alt.X("FechaLabel:N",
                    sort=orden_fechas,
                    title="Mes",
                    axis=alt.Axis(labelAngle=-35)),
            y=alt.Y("Valor:Q",
                    scale=alt.Scale(domain=[0, 105]),
                    title="Promedio",
                    axis=alt.Axis(grid=True)),
            color=alt.Color("Métrica:N",
                            scale=color_scale,
                            legend=alt.Legend(
                                title="Métrica",
                                #orient="bottom",
                                direction="horizontal",
                                titleAnchor="middle",
                            )),
            tooltip=[
                alt.Tooltip("FechaLabel:N", title="Mes"),
                alt.Tooltip("Métrica:N",    title="Métrica"),
                alt.Tooltip("Valor:Q",      title="Promedio", format=".1f"),
            ],
        )
    )

    # Líneas de referencia 70 y 90 — solo línea con tooltip, sin etiquetas flotantes
    '''
    refs = pd.DataFrame([
        {"ref": 70, "label": "Mínimo (70)"},
        {"ref": 90, "label": "Objetivo (90)"},
    ])
    ref_lines = (
        alt.Chart(refs)
        .mark_rule(strokeDash=[4, 3], strokeWidth=1.4, opacity=0.7)
        .encode(
            y="ref:Q",
            color=alt.Color("label:N",
                            scale=alt.Scale(
                                domain=["Mínimo (70)", "Objetivo (90)"],
                                range=[RED, GREEN],
                            ),
                            legend=alt.Legend(
                                title="Referencia",
                                orient="bottom",
                                direction="horizontal",
                                titleAnchor="middle",
                            )),
            tooltip=[
                alt.Tooltip("label:N", title="Referencia"),
                alt.Tooltip("ref:Q",   title="Valor"),
            ],
        )
    )
    '''

    chart = (
        (lineas)  # + ref_lines)
        .properties(height=320)
        .configure(**_base_config)
    )
    return chart


# ─── 7. Resumen de comentarios con PLN (sumy) ────────────────────────────────
def resumen_comentarios(textos_serie, n_oraciones=5):
    """
    Recibe una Serie de pandas con textos libres.
    Usa sumy (LSA) para extraer las oraciones mas representativas.
    Devuelve una lista de strings con el resumen.
    """
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.utils import get_stop_words

    def normalizar(texto):
        t = texto.strip()
        if t and t[-1] not in ".!?":
            t += "."
        return t

    texto_completo = " ".join(
        normalizar(t) for t in textos_serie.dropna().astype(str).tolist()
    ).strip()

    if not texto_completo:
        return []

    try:
        parser    = PlaintextParser.from_string(texto_completo, Tokenizer("spanish"))
        stemmer   = Stemmer("spanish")
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words("spanish")

        oraciones = summarizer(parser.document, n_oraciones)
        return [str(o) for o in oraciones]
    except Exception:
        # Fallback: devolver primeras n oraciones si sumy falla
        import re
        todas = re.split(r"(?<=[.!?])\s+", texto_completo)
        return [o.strip() for o in todas[:n_oraciones] if o.strip()]
