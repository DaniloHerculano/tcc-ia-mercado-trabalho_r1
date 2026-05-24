import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def mostrar_evolucao_temporal(df):

    st.title("📈 Evolução Temporal da Exposição à IA")

    st.markdown("""
    Esta página apresenta os gráficos temporais utilizados no TCC para análise da evolução
    da exposição das ocupações brasileiras à Inteligência Artificial.
    
    Todos os gráficos abaixo foram recriados utilizando Plotly para permitir:
    
    - Zoom
    - Hover interativo
    - Download em PNG
    - Navegação dinâmica
    """)

    # ============================================================
    # MAPEAMENTO AUTOMÁTICO DAS COLUNAS
    # ============================================================

    cols = {c.lower(): c for c in df.columns}

    def localizar_coluna(lista_nomes):
        for nome in lista_nomes:
            if nome.lower() in cols:
                return cols[nome.lower()]
        return None

    col_ano = localizar_coluna([
        "ano",
        "ANO"
    ])

    col_trimestre = localizar_coluna([
        "trimestre",
        "TRIMESTRE"
    ])

    col_genero = localizar_coluna([
        "genero",
        "sexo",
        "Genero",
        "Sexo"
    ])

    col_mean = localizar_coluna([
        "mean",
        "Mean",
        "exposure_mean"
    ])

    col_sd = localizar_coluna([
        "sd",
        "SD",
        "exposure_sd"
    ])

    col_aioe = localizar_coluna([
        "aioe",
        "AIOE"
    ])

    col_renda = localizar_coluna([
        "log_renda",
        "renda",
        "media_renda"
    ])

    col_escolaridade = localizar_coluna([
        "escolaridade",
        "grau_instrucao",
        "nivel_instrucao"
    ])

    col_setor = localizar_coluna([
        "setor",
        "setor_economico",
        "atividade"
    ])

    col_ocupacao = localizar_coluna([
        "ocupacao",
        "descricao_ocupacao",
        "titulo_ocupacao"
    ])

    # ============================================================
    # DEBUG OPCIONAL
    # ============================================================

    # st.write(df.columns)

    # ============================================================
    # CRIA COLUNA TEMPORAL
    # ============================================================

    if col_ano and col_trimestre:

        df["periodo"] = (
            df[col_ano].astype(str)
            + " T"
            + df[col_trimestre].astype(str)
        )

    # ============================================================
    # FILTRO
    # ============================================================

    st.sidebar.header("🔎 Filtros")

    if col_ano:

        anos = sorted(df[col_ano].dropna().unique())

        anos_selecionados = st.sidebar.multiselect(
            "Ano",
            anos,
            default=anos
        )

        df = df[df[col_ano].isin(anos_selecionados)]

    # ============================================================
    # GRÁFICO 1
    # EXPOSIÇÃO POR GÊNERO — GMYREK
    # ============================================================

    st.header("👥 Exposição à IA por gênero — Gmyrek")

    if all([col_ano, col_genero, col_mean]):

        dados_g1 = (
            df.groupby([col_ano, col_genero])[col_mean]
            .mean()
            .reset_index()
        )

        fig1 = px.line(
            dados_g1,
            x=col_ano,
            y=col_mean,
            color=col_genero,
            markers=True
        )

        fig1.update_layout(
            xaxis_title="Ano",
            yaxis_title="Mean médio ponderado",
            height=500,
            hovermode="x unified"
        )

        st.plotly_chart(fig1, use_container_width=True)

    # ============================================================
    # GRÁFICO 2
    # EXPOSIÇÃO POR GÊNERO — FELTEN
    # ============================================================

    st.header("👥 Exposição à IA por gênero — Felten")

    if all([col_ano, col_genero, col_aioe]):

        dados_g2 = (
            df.groupby([col_ano, col_genero])[col_aioe]
            .mean()
            .reset_index()
        )

        fig2 = px.line(
            dados_g2,
            x=col_ano,
            y=col_aioe,
            color=col_genero,
            markers=True
        )

        fig2.update_layout(
            xaxis_title="Ano",
            yaxis_title="AIOE médio ponderado",
            height=500,
            hovermode="x unified"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ============================================================
    # GRÁFICO 3
    # EVOLUÇÃO TEMPORAL — GMYREK
    # ============================================================

    st.header("📈 Evolução temporal da exposição — Gmyrek")

    if "periodo" in df.columns and col_mean:

        dados_g3 = (
            df.groupby("periodo")[col_mean]
            .mean()
            .reset_index()
        )

        fig3 = px.line(
            dados_g3,
            x="periodo",
            y=col_mean,
            markers=True
        )

        fig3.update_layout(
            xaxis_title="Período",
            yaxis_title="Mean médio",
            height=500
        )

        st.plotly_chart(fig3, use_container_width=True)

    # ============================================================
    # GRÁFICO 4
    # EVOLUÇÃO TEMPORAL — AIOE
    # ============================================================

    st.header("📈 Evolução temporal da exposição — Felten/AIOE")

    if "periodo" in df.columns and col_aioe:

        dados_g4 = (
            df.groupby("periodo")[col_aioe]
            .mean()
            .reset_index()
        )

        fig4 = px.line(
            dados_g4,
            x="periodo",
            y=col_aioe,
            markers=True
        )

        fig4.update_layout(
            xaxis_title="Período",
            yaxis_title="AIOE médio",
            height=500
        )

        st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # ============================================================
    # GRÁFICO 5
    # IA X RENDA
    # ============================================================

    st.header("💰 Relação entre exposição à IA e renda")

    col1, col2 = st.columns(2)

    with col1:

        if all([col_mean, col_renda]):

            fig5 = px.scatter(
                df,
                x=col_mean,
                y=col_renda,
                opacity=0.5,
                trendline="ols"
            )

            fig5.update_layout(
                title="Gmyrek Mean x Renda",
                xaxis_title="Mean",
                yaxis_title="Renda",
                height=500
            )

            st.plotly_chart(fig5, use_container_width=True)

    with col2:

        if all([col_aioe, col_renda]):

            fig6 = px.scatter(
                df,
                x=col_aioe,
                y=col_renda,
                opacity=0.5,
                trendline="ols"
            )

            fig6.update_layout(
                title="AIOE x Renda",
                xaxis_title="AIOE",
                yaxis_title="Renda",
                height=500
            )

            st.plotly_chart(fig6, use_container_width=True)

    st.divider()

    # ============================================================
    # GRÁFICO 6
    # TOP OCUPAÇÕES MAIS EXPOSTAS
    # ============================================================

    st.header("🏆 Ocupações com maior exposição à IA")

    if all([col_ocupacao, col_mean]):

        top_ocupacoes = (
            df.groupby(col_ocupacao)[col_mean]
            .mean()
            .reset_index()
            .sort_values(col_mean, ascending=False)
            .head(15)
        )

        fig7 = px.bar(
            top_ocupacoes.sort_values(col_mean),
            x=col_mean,
            y=col_ocupacao,
            orientation="h",
            text=col_mean
        )

        fig7.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig7.update_layout(
            xaxis_title="Mean",
            yaxis_title="",
            height=700
        )

        st.plotly_chart(fig7, use_container_width=True)

    # ============================================================
    # GRÁFICO 7
    # SETORES ECONÔMICOS
    # ============================================================

    st.header("🏭 Exposição média à IA por setor econômico")

    if all([col_setor, col_mean]):

        dados_setor = (
            df.groupby(col_setor)[col_mean]
            .mean()
            .reset_index()
            .sort_values(col_mean, ascending=False)
        )

        fig8 = px.bar(
            dados_setor,
            x=col_mean,
            y=col_setor,
            orientation="h",
            text=col_mean
        )

        fig8.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig8.update_layout(
            xaxis_title="Mean médio",
            yaxis_title="",
            height=700
        )

        st.plotly_chart(fig8, use_container_width=True)

    st.divider()

    # ============================================================
    # GRÁFICO 8
    # HEATMAP DE CORRELAÇÃO
    # ============================================================

    st.header("🔥 Correlação entre indicadores")

    colunas_corr = []

    if col_aioe:
        colunas_corr.append(col_aioe)

    if col_mean:
        colunas_corr.append(col_mean)

    if col_sd:
        colunas_corr.append(col_sd)

    if col_renda:
        colunas_corr.append(col_renda)

    if len(colunas_corr) >= 2:

        corr = df[colunas_corr].corr()

        fig9 = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1
        )

        fig9.update_layout(
            height=600
        )

        st.plotly_chart(fig9, use_container_width=True)
