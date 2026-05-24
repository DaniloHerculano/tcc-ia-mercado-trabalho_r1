import streamlit as st
import plotly.express as px
import pandas as pd


def mostrar_evolucao_temporal(df):

    st.title("📈 Evolução Temporal")

    # ============================================================
    # AJUSTE AUTOMÁTICO DE NOMES
    # ============================================================

    cols = {c.lower(): c for c in df.columns}

    col_ano = cols.get("ano")
    col_genero = cols.get("genero")
    col_mean = cols.get("mean")
    col_aioe = cols.get("aioe")

    if not all([col_ano, col_genero, col_mean, col_aioe]):
        st.error("Colunas necessárias não encontradas.")
        st.write(df.columns)
        return

    # ============================================================
    # GRÁFICO 1 — GMYREK
    # ============================================================

    st.subheader("Exposição à IA por gênero — Gmyrek")

    dados_gmyrek = (
        df.groupby([col_ano, col_genero])[col_mean]
        .mean()
        .reset_index()
    )

    fig1 = px.line(
        dados_gmyrek,
        x=col_ano,
        y=col_mean,
        color=col_genero,
        markers=True
    )

    fig1.update_layout(
        height=500,
        xaxis_title="Ano",
        yaxis_title="Mean médio ponderado",
        hovermode="x unified",
        legend_title=""
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ============================================================
    # GRÁFICO 2 — FELTEN
    # ============================================================

    st.subheader("Exposição à IA por gênero — Felten")

    dados_felten = (
        df.groupby([col_ano, col_genero])[col_aioe]
        .mean()
        .reset_index()
    )

    fig2 = px.line(
        dados_felten,
        x=col_ano,
        y=col_aioe,
        color=col_genero,
        markers=True
    )

    fig2.update_layout(
        height=500,
        xaxis_title="Ano",
        yaxis_title="AIOE médio ponderado",
        hovermode="x unified",
        legend_title=""
    )

    st.plotly_chart(fig2, use_container_width=True)
