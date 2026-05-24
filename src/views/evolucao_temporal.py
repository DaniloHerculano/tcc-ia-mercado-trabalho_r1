import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def mostrar_evolucao_temporal(df):

    st.title("📈 Evolução Temporal da Exposição à IA")
    
    st.markdown("""
    Esta seção apresenta a evolução temporal dos indicadores de exposição à Inteligência Artificial
    ao longo dos períodos analisados da PNAD Contínua.
    
    Os gráficos permitem analisar tendências, variações por setor, escolaridade,
    renda e comportamento geral dos indicadores ocupacionais.
    """)

    st.info("""
    💡 Nesta página você pode:
    - Aplicar zoom nos gráficos
    - Filtrar períodos
    - Passar o mouse para visualizar detalhes
    - Exportar gráficos em PNG
    """)

    # ============================================================
    # PREPARAÇÃO DOS DADOS
    # ============================================================

    df = df.copy()

    # Ajuste defensivo caso existam nomes diferentes
    if "ANO" in df.columns:
        df["ano"] = df["ANO"]

    if "TRIMESTRE" in df.columns:
        df["trimestre"] = df["TRIMESTRE"]

    # Cria coluna temporal
    if "ano" in df.columns and "trimestre" in df.columns:
        df["periodo"] = (
            df["ano"].astype(str)
            + " T"
            + df["trimestre"].astype(str)
        )

    # ============================================================
    # FILTROS
    # ============================================================

    st.sidebar.header("🔎 Filtros")

    anos_disponiveis = sorted(df["ano"].dropna().unique())

    anos_selecionados = st.sidebar.multiselect(
        "Selecione os anos",
        anos_disponiveis,
        default=anos_disponiveis
    )

    df_filtrado = df[df["ano"].isin(anos_selecionados)]

    # ============================================================
    # KPIs
    # ============================================================

    st.subheader("📌 Indicadores Gerais")

    col1, col2, col3, col4 = st.columns(4)

    media_aioe = round(df_filtrado["AIOE"].mean(), 3) if "AIOE" in df_filtrado.columns else 0
    media_exposure = round(df_filtrado["Exposure_Mean"].mean(), 3) if "Exposure_Mean" in df_filtrado.columns else 0
    total_ocupacoes = df_filtrado["ocupacao"].nunique() if "ocupacao" in df_filtrado.columns else len(df_filtrado)
    total_registros = len(df_filtrado)

    col1.metric("Média AIOE", media_aioe)
    col2.metric("Média Exposure", media_exposure)
    col3.metric("Ocupações", f"{total_ocupacoes:,}")
    col4.metric("Registros", f"{total_registros:,}")

    st.divider()

    # ============================================================
    # EVOLUÇÃO TEMPORAL AIOE
    # ============================================================

    st.header("📊 Evolução Temporal do Score AIOE")

    if "AIOE" in df_filtrado.columns:

        evolucao_aioe = (
            df_filtrado
            .groupby("periodo", as_index=False)["AIOE"]
            .mean()
        )

        fig1 = px.line(
            evolucao_aioe,
            x="periodo",
            y="AIOE",
            markers=True,
            title="Evolução Média do Score AIOE"
        )

        fig1.update_layout(
            height=500,
            xaxis_title="Período",
            yaxis_title="Média AIOE",
            hovermode="x unified"
        )

        st.plotly_chart(fig1, use_container_width=True)

    # ============================================================
    # EVOLUÇÃO EXPOSURE
    # ============================================================

    st.header("🤖 Evolução do Gradiente de Exposição")

    if "Exposure_Mean" in df_filtrado.columns:

        evolucao_exposure = (
            df_filtrado
            .groupby("periodo", as_index=False)["Exposure_Mean"]
            .mean()
        )

        fig2 = px.line(
            evolucao_exposure,
            x="periodo",
            y="Exposure_Mean",
            markers=True,
            title="Evolução Média da Exposição à IA"
        )

        fig2.update_layout(
            height=500,
            xaxis_title="Período",
            yaxis_title="Exposure Mean",
            hovermode="x unified"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ============================================================
    # COMPARAÇÃO AIOE X EXPOSURE
    # ============================================================

    st.header("⚖️ Comparação entre Indicadores")

    if (
        "AIOE" in df_filtrado.columns
        and "Exposure_Mean" in df_filtrado.columns
    ):

        comparativo = (
            df_filtrado
            .groupby("periodo", as_index=False)
            .agg({
                "AIOE": "mean",
                "Exposure_Mean": "mean"
            })
        )

        fig3 = go.Figure()

        fig3.add_trace(
            go.Scatter(
                x=comparativo["periodo"],
                y=comparativo["AIOE"],
                mode="lines+markers",
                name="AIOE"
            )
        )

        fig3.add_trace(
            go.Scatter(
                x=comparativo["periodo"],
                y=comparativo["Exposure_Mean"],
                mode="lines+markers",
                name="Exposure Mean"
            )
        )

        fig3.update_layout(
            title="Comparação Temporal dos Indicadores",
            height=550,
            xaxis_title="Período",
            yaxis_title="Score Médio",
            hovermode="x unified"
        )

        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ============================================================
    # DISTRIBUIÇÃO TEMPORAL
    # ============================================================

    st.header("📦 Distribuição Temporal dos Scores")

    col5, col6 = st.columns(2)

    with col5:

        if "AIOE" in df_filtrado.columns:

            fig4 = px.box(
                df_filtrado,
                x="ano",
                y="AIOE",
                points="outliers",
                title="Distribuição AIOE por Ano"
            )

            fig4.update_layout(
                height=450,
                xaxis_title="Ano",
                yaxis_title="AIOE"
            )

            st.plotly_chart(fig4, use_container_width=True)

    with col6:

        if "Exposure_Mean" in df_filtrado.columns:

            fig5 = px.box(
                df_filtrado,
                x="ano",
                y="Exposure_Mean",
                points="outliers",
                title="Distribuição Exposure por Ano"
            )

            fig5.update_layout(
                height=450,
                xaxis_title="Ano",
                yaxis_title="Exposure Mean"
            )

            st.plotly_chart(fig5, use_container_width=True)

    st.divider()

    # ============================================================
    # HEATMAP TEMPORAL
    # ============================================================

    st.header("🔥 Heatmap Temporal")

    if (
        "ano" in df_filtrado.columns
        and "trimestre" in df_filtrado.columns
        and "AIOE" in df_filtrado.columns
    ):

        heatmap_data = (
            df_filtrado
            .pivot_table(
                values="AIOE",
                index="ano",
                columns="trimestre",
                aggfunc="mean"
            )
        )

        fig6 = px.imshow(
            heatmap_data,
            text_auto=".2f",
            aspect="auto",
            title="Mapa de Calor - Média AIOE"
        )

        fig6.update_layout(
            height=500
        )

        st.plotly_chart(fig6, use_container_width=True)

    st.divider()

    # ============================================================
    # ANÁLISE ESTATÍSTICA
    # ============================================================

    st.header("📈 Estatísticas Descritivas")

    col7, col8 = st.columns(2)

    with col7:

        if "AIOE" in df_filtrado.columns:

            st.subheader("AIOE")

            st.dataframe(
                df_filtrado["AIOE"].describe().round(3),
                use_container_width=True
            )

    with col8:

        if "Exposure_Mean" in df_filtrado.columns:

            st.subheader("Exposure Mean")

            st.dataframe(
                df_filtrado["Exposure_Mean"].describe().round(3),
                use_container_width=True
            )

    st.divider()

    # ============================================================
    # CONCLUSÃO ANALÍTICA
    # ============================================================

    st.header("🧠 Insights Analíticos")

    st.markdown("""
    - Os gráficos temporais permitem acompanhar a evolução dos indicadores de exposição à IA ao longo do tempo.
    
    - As distribuições ajudam a identificar assimetrias, dispersões e possíveis outliers nos dados ocupacionais.
    
    - A comparação entre AIOE e Exposure Mean auxilia na validação da consistência metodológica entre diferentes métricas internacionais.
    
    - O heatmap temporal facilita a identificação visual de períodos com maior concentração de exposição ocupacional à Inteligência Artificial.
    """)
