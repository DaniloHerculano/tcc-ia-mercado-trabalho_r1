import plotly.express as px


# ==========================================
# BAR CHART
# ==========================================

def grafico_barra(
    df,
    x,
    y,
    color,
    titulo
):

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        title=titulo
    )

    return fig


# ==========================================
# PIE CHART
# ==========================================

def grafico_pizza(
    df,
    names,
    values,
    titulo
):

    fig = px.pie(
        df,
        names=names,
        values=values,
        title=titulo
    )

    return fig


# ==========================================
# LINE CHART
# ==========================================

def grafico_linha(
    df,
    x,
    y,
    titulo
):

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=titulo
    )

    return fig


# ==========================================
# HISTOGRAMA
# ==========================================

def grafico_histograma(
    df,
    coluna,
    titulo
):

    fig = px.histogram(
        df,
        x=coluna,
        nbins=30,
        title=titulo
    )

    return fig