import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Parametros Fisicos do Caso Laminar
R = 0.1             # Raio do duto (m)
U_max_teorico = 2.0 # Velocidade maxima teorica no centro (m/s)

pasta_saida = "posprocesspython"
if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

# Busca automaticamente o arquivo .xy gerado pelo OpenFOAM na pasta 1000
pasta_amostra = "postProcessing/sampleDict0/1000"
arquivo_dados = None

if os.path.exists(pasta_amostra):
    arquivos_xy = glob.glob(os.path.join(pasta_amostra, "*.xy"))
    if arquivos_xy:
        arquivo_dados = arquivos_xy[0] 

# Se existir o arquivo, faz a leitura e plota o grafico
if arquivo_dados and os.path.exists(arquivo_dados):
    try:
        dados = np.loadtxt(arquivo_dados)
        
        # O eixo de raio (r) costuma ser a primeira coluna (indice 0)
        r_sim = dados[:, 0]
        
        # A velocidade (U) no eixo X costuma ser a coluna 2 ou 1.
        try:
            u_sim = dados[:, 2] 
        except IndexError:
            u_sim = dados[:, 1]
        
        # ==========================================
        # PLOT DA VALIDAÇÃO DO PERFIL LAMINAR
        # ==========================================
        plt.figure(figsize=(10, 6))
        
        # Plot da Simulação (OpenFOAM) - Usando pontos roxos (como no seu Gnuplot original)
        plt.plot(r_sim, u_sim, 'o', color='purple', markersize=5, label='OpenFOAM - Laminar solution')
        
        # Plot da Solução Analítica (Equação da Parábola de Hagen-Poiseuille)
        r_teorico = np.linspace(0, R, 100)
        u_teorico = U_max_teorico * (1 - (r_teorico/R)**2)
        plt.plot(r_teorico, u_teorico, '-', color='lightseagreen', linewidth=1.5, label='Analytical solution')
        
        # Formatacao do Grafico
        plt.xlim(0, R)
        plt.ylim(0, U_max_teorico * 1.05)
        plt.xlabel('Radius (m)', fontsize=12)
        plt.ylabel('Radial velocity (m/s)', fontsize=12)
        plt.title('Laminar profile at outlet (GT1 Validation)', fontsize=13)
        plt.grid(True, ls=":", alpha=0.7)
        plt.legend(loc='best')
        
        # Salvamento
        caminho_grafico = os.path.join(pasta_saida, 'GT1_Laminar_Validation.png')
        plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Grafico Laminar gerado com sucesso: {caminho_grafico}")

    except Exception as e:
        print(f"Erro ao processar os dados laminares: {e}")
else:
    print(f"Aviso: Arquivo de amostra (.xy) nao encontrado na pasta {pasta_amostra}.")