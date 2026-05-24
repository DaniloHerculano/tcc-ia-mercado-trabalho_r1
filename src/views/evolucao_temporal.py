import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def mostrar_evolucao_temporal(df):

    st.title("📈 Evolução Temporal da Exposição à IA")

    st.markdown("""
    Nesta seção são apresentados os gráficos temporais e comparativos
    relacionados à exposição das ocupações brasileiras à Inteligência Artificial,
    utilizando os indicadores de Gmyrek e Felten/AIOE.
    """)

    # ============================================================
    # AJUSTE DAS COLUNAS
    # ============================================================

    df = df.copy()

    # Ajuste automático para evitar KeyError
    colunas = [c.lower() for c in df.columns]
    mapa = dict(zip(colunas, df.columns))

    # tenta identificar colunas
    col_ano = mapa.get("ano")
    col_trim = mapa.get("trimestre")
    col_genero = mapa.get("genero")
    col_mean = mapa.get("mean")
    col_aioe = mapa.get("aioe")
    col_renda = mapa.get("log_renda")

    # Debug opcional
    # st.write(df.columns)

    # ============================================================
    # CRIA PERÍODO
    # ============================================================

    if col_ano and col_trim:
        df["periodo"] = (
            df[col_ano].astype(str)
            + "T"
            + df[col_trim].astype(str)
        )

    # ============================================================
    # GRÁFICOS POR GÊNERO
    # ============================================================

    st.header("👥 Exposição à IA por gênero")

    col1, col2 = st.columns(2)

    with col1:

        if all([col_ano, col_genero, col_mean]):

            dados_genero_mean = (
                df.groupby([col_ano, col_genero])[col_mean]
                .mean()
                .reset_index()
            )

            fig1 = px.line(
                dados_genero_mean,
                x=col_ano,
                y=col_mean,
                color=col_genero,
                markers=True,
                title="Exposição à IA por gênero — Gmyrek"
            )

            fig1.update_layout(
                xaxis_title="Ano",
                yaxis_title="Mean médio ponderado",
                height=450,
                hovermode="x unified"
            )

            st.plotly_chart(fig1, use_container_width=True)

    with col2:

        if all([col_ano, col_genero, col_aioe]):

            dados_genero_aioe = (
                df.groupby([col_ano, col_genero])[col_aioe]
                .mean()
                .reset_index()
            )

            fig2 = px.line(
                dados_genero_aioe,
                x=col_ano,
                y=col_aioe,
                color=col_genero,
                markers=True,
                title="Exposição à IA por gênero — Felten"
            )

            fig2.update_layout(
                xaxis_title="Ano",
                yaxis_title="AIOE médio ponderado",
                height=450,
                hovermode="x unified"
            )

            st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ============================================================
    # EVOLUÇÃO TRIMESTRAL
    # ============================================================

    st.header("📊 Evolução trimestral da exposição à IA")

    col3, col4 = st.columns(2)

    with col3:

        if "periodo" in df.columns and col_mean:

            evolucao_mean = (
                df.groupby("periodo")[col_mean]
                .mean()
                .reset_index()
            )

            fig3 = px.line(
                evolucao_mean,
                x="periodo",
                y=col_mean,
                markers=True,
                title="Evolução trimestral da exposição à IA — Gmyrek"
            )

            fig3.update_layout(
                xaxis_title="Período",
                yaxis_title="Mean médio ponderado",
                height=450
            )

            st.plotly_chart(fig3, use_container_width=True)

    with col4:

        if "periodo" in df.columns and col_aioe:

            evolucao_aioe = (
                df.groupby("periodo")[col_aioe]
                .mean()
                .reset_index()
            )

            fig4 = px.line(
                evolucao_aioe,
                x="periodo",
                y=col_aioe,
                markers=True,
                title="Evolução trimestral da exposição à IA — Felten/AIOE"
            )

            fig4.update_layout(
                xaxis_title="Período",
                yaxis_title="AIOE médio ponderado",
                height=450
            )

            st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # ============================================================
    # RENDA X IA
    # ============================================================

    st.header("💰 Exposição à IA e renda ocupacional")

    col5, col6 = st.columns(2)

    with col5:

        if all([col_mean, col_renda]):

            fig5 = px.scatter(
                df,
                x=col_mean,
                y=col_renda,
                opacity=0.7,
                title="Exposição à IA e renda ocupacional — Gmyrek"
            )

            fig5.update_layout(
                xaxis_title="Mean — Gmyrek",
                yaxis_title="Log da renda média ponderada",
                height=500
            )

            st.plotly_chart(fig5, use_container_width=True)

    with col6:

        if all([col_aioe, col_renda]):

            fig6 = px.scatter(
                df,
                x=col_aioe,
                y=col_renda,
                opacity=0.7,
                title="Exposição à IA e renda ocupacional — Felten"
            )

            fig6.update_layout(
                xaxis_title="AIOE — Felten",
                yaxis_title="Log da renda média ponderada",
                height=500
            )

            st.plotly_chart(fig6, use_container_width=True)

    st.divider()

    # ============================================================
    # TOP 20 MAIS EXPOSTAS
    # ============================================================

    st.header("🏆 Ocupações mais expostas à IA")

    col_ocup = None

    for c in df.columns:
        if "ocup" in c.lower():
            col_ocup = c
            break

    if col_ocup and col_mean:

        top20 = (
            df.groupby(col_ocup)[col_mean]
            .mean()
            .reset_index()
            .sort_values(col_mean, ascending=False)
            .head(20)
        )

        fig7 = px.bar(
            top20.sort_values(col_mean),
            x=col_mean,
            y=col_ocup,
            orientation="h",
            title="Top 20 ocupações mais expostas — Gmyrek Mean"
        )

        fig7.update_layout(
            xaxis_title="Gmyrek Mean",
            yaxis_title="",
            height=700
        )

        st.plotly_chart(fig7, use_container_width=True)

    st.divider()

    # ============================================================
    # BOTTOM 20 MENOS EXPOSTAS
    # ============================================================

    st.header("🛡️ Ocupações menos expostas à IA")

    if col_ocup and col_aioe:

        bottom20 = (
            df.groupby(col_ocup)[col_aioe]
            .mean()
            .reset_index()
            .sort_values(col_aioe, ascending=True)
            .head(20)
        )

        fig8 = px.bar(
            bottom20.sort_values(col_aioe),
            x=col_aioe,
            y=col_ocup,
            orientation="h",
            title="Bottom 20 ocupações menos expostas — Felten/AIOE"
        )

        fig8.update_layout(
            xaxis_title="Felten/AIOE",
            yaxis_title="",
            height=700
        )

        st.plotly_chart(fig8, use_container_width=True)
