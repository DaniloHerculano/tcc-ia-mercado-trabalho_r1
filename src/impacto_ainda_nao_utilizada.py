# --- CÉLULA DE ANÁLISE DE IMPACTO IA (FELTEN & GMYREK) - V2 ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from google.colab import drive

# 1. Montar Google Drive
drive.mount("/content/drive")

# 2. Configurações de Caminhos
DRIVE_BASE_PATH = "/content/drive/MyDrive/TCC_IA_Mercado_Trabalho_HISTORICO"
PNAD_PATH = os.path.join(DRIVE_BASE_PATH, "pnad_completa_HISTORICO.parquet")
# Tabela enviada pelo usuário
SCORES_IA_PATH = "/content/drive/MyDrive/TCC_IA_Mercado_Trabalho_HISTORICO/tabela_cbo_e5_large_final.xlsx" 

def processar_analise_impacto(pnad_path, scores_path):
    print("Carregando dados da PNAD e Scores de IA...")
    df_pnad = pd.read_parquet(pnad_path)
    df_scores = pd.read_excel(scores_path)
    
    # Ajuste de Colunas baseado na tabela do usuário:
    # CBO_EXTRAIDO -> Coluna de ligação
    # AIOE_SCORE -> O score de exposição de Felten
    
    # Garantir que o CBO seja string com o formato XXXX-XX ou XXXXXX para o cruzamento
    # Na PNAD o CBO costuma vir sem o hífen. Na tabela do usuário tem hífen.
    df_pnad['CBO_JOIN'] = df_pnad['CBO'].astype(str).str.replace('-', '').str.zfill(6)
    df_scores['CBO_JOIN'] = df_scores['CBO_EXTRAIDO'].astype(str).str.replace('-', '').str.zfill(6)
    
    # 3. CRUZAMENTO (Merge)
    print("Cruzando dados...")
    df_final = pd.merge(df_pnad, df_scores[['CBO_JOIN', 'AIOE_SCORE', 'AIOE_MATCH_TITLE', 'CONFIDENCE_SCORE']], on='CBO_JOIN', how='left')
    
    # 4. NORMALIZAÇÃO DO SCORE (Felten costuma variar, vamos normalizar para 0-1 se necessário)
    # Mas aqui vamos usar os percentis para definir alta/baixa exposição
    print("Calculando percentis de exposição...")
    high_threshold = df_final['AIOE_SCORE'].quantile(0.75)
    low_threshold = df_final['AIOE_SCORE'].quantile(0.25)

    # 5. CLASSIFICAÇÃO DE GMYREK (Adaptada)
    def classificar_impacto(row):
        if pd.isna(row['AIOE_SCORE']):
            return 'Não Classificado'
        
        # Lógica de Gmyrek: Alta Exposição + Escolaridade
        # Escolaridade na PNAD (Anos_Estudo) costuma vir como string ou códigos
        # Vamos assumir que '12 anos ou mais' é Ensino Superior/Médio Completo+
        is_high_edu = str(row['Anos_Estudo']) in ['12 anos ou mais', '11 anos']
        
        if row['AIOE_SCORE'] >= high_threshold:
            if is_high_edu:
                return 'Potencial de Aumento (Augmentation)'
            else:
                return 'Risco de Automação (Automation)'
        elif row['AIOE_SCORE'] <= low_threshold:
            return 'Baixa Exposição'
        else:
            return 'Exposição Moderada'

    print("Classificando natureza do impacto...")
    df_final['Impacto_IA'] = df_final.apply(classificar_impacto, axis=1)
    
    # 6. RESULTADOS
    print("\n--- RESULTADOS BRASIL ---")
    dist_impacto = df_final[df_final['AIOE_SCORE'].notnull()]['Impacto_IA'].value_counts(normalize=True) * 100
    print(dist_impacto)
    
    # 7. GRÁFICOS PROFISSIONAIS
    plt.figure(figsize=(12, 7))
    sns.set_style("whitegrid")
    ax = sns.barplot(x=dist_impacto.index, y=dist_impacto.values, palette='magma')
    
    plt.title('Distribuição do Impacto da IA no Emprego Brasileiro (2012-2025)', fontsize=15)
    plt.ylabel('Porcentagem da Força de Trabalho (%)', fontsize=12)
    plt.xlabel('Categoria de Impacto (Metodologia Felten/Gmyrek)', fontsize=12)
    
    # Adicionar rótulos nas barras
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 9), textcoords='offset points')

    plt.tight_layout()
    plt.savefig('analise_impacto_ia_final.png')
    print("\nGráfico salvo como 'analise_impacto_ia_final.png'")
    
    return df_final

# df_final = processar_analise_impacto(PNAD_PATH, SCORES_IA_PATH)