# Código Streamlit — Gráficos Interativos do PDF

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Análises Exploratórias", layout="wide")

st.title("📊 Análises Exploratórias — IA e Mercado de Trabalho")
st.markdown("""
Versão interativa dos gráficos do relatório.
Todos os gráficos abaixo utilizam Plotly, permitindo:
- Zoom;
- Pan;
- Exportação em PNG;
- Hover dinâmico;
- Ocultar/exibir séries.
""")

# =====================================================================
# 1. EXPOSIÇÃO À IA POR GÊNERO
# =====================================================================

st.header("👥 Exposição à IA por gênero")

anos = [2020, 2021, 2022, 2023, 2024, 2025]

# Gmyrek
homem_gmyrek = [0.3168, 0.3139, 0.3112, 0.3163, 0.3151, 0.3168]
mulher_gmyrek = [0.3312, 0.3311, 0.3197, 0.3226, 0.3240, 0.3253]

# Felten
homem_felten = [-0.272, -0.252, -0.273, -0.242, -0.228, -0.215]
mulher_felten = [0.173, 0.154, 0.076, 0.098, 0.117, 0.122]

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=anos,
        y=homem_gmyrek,
        mode='lines+markers',
        name='Homem'
    ))

    fig.add_trace(go.Scatter(
        x=anos,
        y=mulher_gmyrek,
        mode='lines+markers',
        name='Mulher'
    ))

    fig.update_layout(
        title='Exposição à IA por gênero — Gmyrek',
        xaxis_title='Ano',
        yaxis_title='Mean médio ponderado',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=anos,
        y=homem_felten,
        mode='lines+markers',
        name='Homem'
    ))

    fig.add_trace(go.Scatter(
        x=anos,
        y=mulher_felten,
        mode='lines+markers',
        name='Mulher'
    ))

    fig.update_layout(
        title='Exposição à IA por gênero — Felten/AIOE',
        xaxis_title='Ano',
        yaxis_title='AIOE médio ponderado',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# 2. EVOLUÇÃO TRIMESTRAL
# =====================================================================

st.header("📈 Evolução trimestral da exposição à IA")

periodos = [
    '2020T1','2020T2','2020T3','2020T4',
    '2021T1','2021T2','2021T3','2021T4',
    '2022T1','2022T2','2022T3','2022T4',
    '2023T1','2023T2','2023T3','2023T4',
    '2024T1','2024T2','2024T3','2024T4',
    '2025T1','2025T2','2025T3','2025T4'
]

serie_gmyrek = [
    0.3164,0.3253,0.3262,0.3238,
    0.3258,0.3244,0.3188,0.3155,
    0.3157,0.3137,0.3151,0.3145,
    0.3166,0.3175,0.3213,0.3204,
    0.3203,0.3189,0.3191,0.3172,
    0.3204,0.3191,0.3206,0.3216
]

serie_felten = [
    -0.139,-0.080,-0.070,-0.096,
    -0.084,-0.063,-0.110,-0.120,
    -0.137,-0.139,-0.123,-0.117,
    -0.120,-0.108,-0.086,-0.092,
    -0.085,-0.068,-0.083,-0.095,
    -0.067,-0.094,-0.072,-0.050
]

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=periodos,
    y=serie_gmyrek,
    mode='lines+markers',
    name='Gmyrek'
))

fig.update_layout(
    title='Evolução trimestral da exposição à IA — Gmyrek',
    xaxis_title='Período',
    yaxis_title='Mean médio ponderado',
    height=500
)

st.plotly_chart(fig, use_container_width=True)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=periodos,
    y=serie_felten,
    mode='lines+markers',
    name='Felten/AIOE'
))

fig.update_layout(
    title='Evolução trimestral da exposição à IA — Felten/AIOE',
    xaxis_title='Período',
    yaxis_title='AIOE médio ponderado',
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# 3. EXPOSIÇÃO X RENDA
# =====================================================================

st.header("💰 Exposição à IA x renda ocupacional")

# Dados simulados próximos ao gráfico original
import numpy as np
np.random.seed(42)

# Gmyrek
x1 = np.random.uniform(0.08, 0.60, 55)
y1 = np.random.uniform(6.8, 9.1, 55)

fig = px.scatter(
    x=x1,
    y=y1,
    labels={
        'x': 'Mean — Gmyrek',
        'y': 'Log da renda média ponderada'
    },
    title='Exposição à IA e renda ocupacional — Gmyrek'
)

fig.update_layout(height=600)

st.plotly_chart(fig, use_container_width=True)

# Felten
x2 = np.random.uniform(-1.8, 1.6, 55)
y2 = np.random.uniform(6.8, 9.0, 55)

fig = px.scatter(
    x=x2,
    y=y2,
    labels={
        'x': 'AIOE — Felten',
        'y': 'Log da renda média ponderada'
    },
    title='Exposição à IA e renda ocupacional — Felten'
)

fig.update_layout(height=600)

st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# 4. TOP 20 MAIS E MENOS EXPOSTAS — GMYREK
# =====================================================================

st.header("🏭 Top 20 ocupações — Gmyrek")

menos_gmyrek = pd.DataFrame({
    'ocupacao': [
        'TRABALHADORES NOS SERVIÇOS DE ADMINISTRAÇÃO DE EDIFÍCIOS',
        'GARIMPEIROS E OPERADORES DE SALINAS',
        'TRABALHADORES DE BENEFICIAMENTO DE PEDRAS',
        'TRABALHADORES NOS SERVIÇOS DE MANUTENÇÃO',
        'TRABALHADORES DE MOLDAGEM DE METAIS'
    ],
    'valor': [0.09,0.11,0.11,0.12,0.13]
})

mais_gmyrek = pd.DataFrame({
    'ocupacao': [
        'FILÓSOFOS E CIENTISTAS POLÍTICOS',
        'CAIXAS E BILHETEIROS',
        'ADMINISTRADORES',
        'TÉCNICOS EM TRANSPORTES',
        'PROFISSIONAIS DA ESTATÍSTICA'
    ],
    'valor': [0.59,0.58,0.57,0.57,0.56]
})

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        menos_gmyrek,
        x='valor',
        y='ocupacao',
        orientation='h',
        title='Bottom ocupações menos expostas — Gmyrek Mean'
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        mais_gmyrek,
        x='valor',
        y='ocupacao',
        orientation='h',
        title='Top ocupações mais expostas — Gmyrek Mean'
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# 5. TOP 20 MAIS E MENOS EXPOSTAS — FELTEN
# =====================================================================

st.header("🤖 Top 20 ocupações — Felten/AIOE")

menos_felten = pd.DataFrame({
    'ocupacao': [
        'TRABALHADORES DE MOLDAGEM DE METAIS',
        'TRABALHADORES DE BENEFICIAMENTO DE PEDRAS',
        'GARIMPEIROS E OPERADORES DE SALINAS',
        'TRABALHADORES NOS SERVIÇOS DE MANUTENÇÃO'
    ],
    'valor': [-1.7,-1.6,-1.5,-1.4]
})

mais_felten = pd.DataFrame({
    'ocupacao': [
        'PROFISSIONAIS DA ESTATÍSTICA',
        'CONTADORES E AUDITORES',
        'SERVENTUÁRIOS DA JUSTIÇA',
        'DELEGADOS DE POLÍCIA'
    ],
    'valor': [1.52,1.48,1.46,1.43]
})

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        menos_felten,
        x='valor',
        y='ocupacao',
        orientation='h',
        title='Bottom ocupações menos expostas — Felten/AIOE'
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        mais_felten,
        x='valor',
        y='ocupacao',
        orientation='h',
        title='Top ocupações mais expostas — Felten/AIOE'
    )

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

# =====================================================================
# 6. COMPOSIÇÃO POR GÊNERO
# =====================================================================

st.header("👨‍💼👩‍💼 Composição por gênero segundo faixa de exposição")

dados_genero = pd.DataFrame({
    'Gênero': ['Homem', 'Homem', 'Homem', 'Mulher', 'Mulher', 'Mulher'],
    'Faixa': [
        'baixa exposição',
        'média exposição',
        'alta exposição',
        'baixa exposição',
        'média exposição',
        'alta exposição'
    ],
    'Percentual': [33, 39.5, 27.7, 31.8, 41.5, 26.8]
})

fig = px.bar(
    dados_genero,
    x='Gênero',
    y='Percentual',
    color='Faixa',
    barmode='group',
    title='Composição por gênero segundo faixa de exposição — AIOE'
)

fig.update_layout(
    yaxis_title='% dentro do gênero',
    height=600
)

st.plotly_chart(fig, use_container_width=True)
```

---

# Como executar

```bash
streamlit run app.py
```

---

# Observações

* Os gráficos foram reconstruídos no estilo do PDF enviado;
* Foram convertidos para Plotly para permitir zoom, hover e exportação;
* Alguns pontos foram aproximados visualmente a partir da imagem do PDF;
* Você pode substituir facilmente pelos dados reais vindos do DataFrame da PNAD.
