# AULA 21 - ATIVIDADE EM GRUPO
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Dados para ler SQL
host = "localhost"
user = "root"
password = "root"
database = "bd_aula11"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# TRY 1: COLETANDO E PROCESSANDO DADOS
try:
    os.system("cls")
    # leitura dos dados da tabela de produtos
    tb_base = pd.read_sql("basedp",engine)
    tb_roubo_coletivos = pd.read_sql("basedp_roubo_coletivo",engine)
    
    # Separando, agrupando e filtrando dados
    df_roubo_coletivos = pd.merge(tb_base, tb_roubo_coletivos, on="cod_ocorrencia")
    df_roubo_coletivos = df_roubo_coletivos[(df_roubo_coletivos["ano"]>=2022) & (df_roubo_coletivos["ano"]<=2023)]
    df_roubo_coletivos = df_roubo_coletivos[["aisp","munic","roubo_em_coletivo"]]
    df_roubo_coletivos = df_roubo_coletivos.groupby(["aisp"]).sum(["roubo_em_coletivo"]).reset_index()
    
    # df_roubo_coletivos_final
    print(df_roubo_coletivos)

except Exception as e:
    print(f"Erro {e}")

# TRY 2: EXTRAINDO E ANALISANDO INFORMAÇÕES
try:
    array_roubo = np.array(df_roubo_coletivos["roubo_em_coletivo"])
    
    # Medidas Centrais
    media_roubo = np.mean(array_roubo)
    mediana_roubo = np.median(array_roubo)
    dist_roubo = abs((media_roubo-mediana_roubo)/mediana_roubo)*100

    # Medidas de Posição
    q1 = np.quantile(array_roubo, 0.25)
    q3 = np.quantile(array_roubo, 0.75)
    iqr = q3 - q1
    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    # Medidas de Dispersão
    maximo = np.max(array_roubo)
    minimo = np.min(array_roubo)
    amplitude = maximo - minimo

    # Outliers
    outliers_inferiores = df_roubo_coletivos[df_roubo_coletivos["roubo_em_coletivo"] < limite_inferior]
    outliers_superiores = df_roubo_coletivos[df_roubo_coletivos["roubo_em_coletivo"] > limite_superior]

    # Variancia, Desvio Padrao e Afins
    variancia_roubo = np.var(array_roubo)
    desvio_padrao = np.std(array_roubo)
    dist_var_med = variancia_roubo / (media_roubo ** 2)
    coeficiente_variacao = (desvio_padrao / media_roubo) * 100

    # Assimetria e Curtose
    assimetria = df_roubo_coletivos["roubo_em_coletivo"].skew()
    curtose = df_roubo_coletivos["roubo_em_coletivo"].kurtosis()

except Exception as e:
    print(f"Erro {e}")

# TRY 3: IMPRIMINDO DADOS:
try:
    print("="*30)
    print("\nMEDIDAS DE TENDÊNCIA CENTRAL")
    print(f"Média de roubo em coletivos: {media_roubo}")
    print(f"Mediana de roubo em coletivos: {mediana_roubo}")
    print(f"Distância entre média e mediana: {dist_roubo}%")

    print("\nMEDIDAS DE POSIÇÃO E DISPERSÃO")
    print(f"Mínimo: {minimo}")
    print(f"Limite inferior: {limite_inferior}")
    print(f"Q1: {q1}")
    print(f"Q3: {q3}")
    print(f"IQR: {iqr}")
    print(f"Limite superior: {limite_superior}")
    print(f"Máximo: {maximo}")
    print(f"Amplitude total: {amplitude}")

    if len(outliers_inferiores) == 0:
        print("\nSEM AISPS COM OUTLIERS INFERIORES!")
    else:
        print("\nAISPS COM OUTLIERS INFERIORES:")
        print(outliers_inferiores.sort_values(by="roubo_em_coletivo", ascending=True).to_string())

    if len(outliers_superiores) == 0:
        print("\nSEM AISPS COM OUTLIERS SUPERIORES")
    else:
        print("\nAISPS COM OUTLIERS SUPERIORES:")
        print(outliers_superiores.sort_values(by="roubo_em_coletivo", ascending=False).to_string())
    
    print("\nMEDIDAS DE DISTRIBUIÇÃO")
    print(f"Variância: {variancia_roubo}")
    print(f"Desvio Padrão: {desvio_padrao}")
    print(f"Distância entre a Variância e a Média: {dist_var_med}")
    print(f"Coeficiente de Variação: {coeficiente_variacao}")
    print(f"Assimetria: {assimetria}")
    print(f"Curtose: {curtose}")

except Exception as e:
    print(f"Erro {e}")

# TRY 4: GRAFICO
try:
    plt.subplots(2,2, figsize=(16,7))
    plt.suptitle("Análise de Roubo em Coletivos no RJ", fontsize=20)

    plt.subplot(2,2,1)
    plt.boxplot(array_roubo, vert=False, showmeans=True)
    plt.title("Boxplot dos Dados")

    # Histograma
    plt.subplot(2, 2, 2)
    plt.hist(array_roubo, bins=50, edgecolor="black")
    plt.axvline(media_roubo, color="g", linewidth=1)
    plt.axvline(mediana_roubo, color="y", linewidth=1)
    plt.title("Histograma:")

    # Terceira posição
    plt.subplot(2, 2, 3)
    plt.text(0.5, 0.9, "MEDIDAS DE TENDÊNCIA CENTRAL:", fontsize=12, ha='center')
    plt.text(0.5, 0.8, f'Média: {media_roubo}', fontsize=10, ha='center')
    plt.text(0.5, 0.7, f'Mediana: {mediana_roubo}', fontsize=10, ha='center')
    plt.text(0.5, 0.6, f'Distância: {dist_roubo}', fontsize=10, ha='center')
    plt.text(0.5, 0.4, "AISPS COM NÚMERO MUITO ACIMA DO COMUM:", fontsize=12, ha='center')
    plt.text(0.5, 0.3, f'Duque de Caxias: 1495 roubos', fontsize=10, ha='center')
    plt.text(0.5, 0.2, f'São João de Meriti: 1094 roubos', fontsize=10, ha='center')
    plt.text(1.5, 0.9, "MEDIDAS DE POSIÇÃO E DISPERSÃO:", fontsize=12, ha='center')
    plt.text(1.5, 0.8, f'Mínimo: {minimo}', fontsize=10, ha='center')
    plt.text(1.5, 0.7, f'Limite inferior: {limite_inferior}', fontsize=10, ha='center')
    plt.text(1.5, 0.6, f'Q1: {q1}', fontsize=10, ha='center')
    plt.text(1.5, 0.5, f'Q3: {q3}', fontsize=10, ha='center')
    plt.text(1.5, 0.4, f'IQR: {iqr}', fontsize=10, ha='center')
    plt.text(1.5, 0.3, f'Limite superior: {limite_superior}', fontsize=10, ha='center')
    plt.text(1.5, 0.2, f'Máximo: {maximo}', fontsize=10, ha='center')
    plt.text(1.5, 0.1, f'Amplitude Total: {amplitude}', fontsize=10, ha='center')
    plt.axis("off")

    # Quarta posição
    plt.subplot(2, 2, 4)
    plt.text(0.5, 0.9, 'MEDIDAS DE DISTRIBUIÇÃO:', fontsize=12, ha='center')
    plt.text(0.5, 0.8, f'Assimetria: {assimetria}', fontsize=10, ha='center')
    plt.text(0.5, 0.7, f'Curtose: {curtose}', fontsize=10, ha='center')
    plt.text(0.5, 0.6, f'Variância: {variancia_roubo}', fontsize=10, ha='center')
    plt.text(0.5, 0.5, f'Desvio Padrão: {desvio_padrao}', fontsize=10, ha='center')
    plt.text(0.5, 0.4, f'Distância entre Variância e Média: {dist_var_med}', fontsize=10, ha='center')
    plt.text(0.5, 0.3, f'Coeficiente de Variação: {coeficiente_variacao}', fontsize=10, ha='center')
    plt.axis("off")

    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"Erro {e}")
