import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# define a raiz GT2
dir_base = os.getcwd()

# pastas alvo para buscar resultados
configuracoes = {
    'RANS': ['KEpsilon_highRE_V1', 'KEpsilon_lowRE_V1', 'KOmegaSST_highRE', 'KOmegaSST_lowRE_V1', 'SA_LRN'],
    'SRS': ['DES_KO_LRN', 'LES-WALE_LRN']
}

arquivo_resumo = os.path.join(dir_base, 'Resumo_Para_Analisar.txt')

# inicia o arquivo de texto
with open(arquivo_resumo, 'w') as f:
    f.write("=== DADOS EXTRAIDOS DO GT2 PARA ANALISE ===\n\n")

# varre todas as pastas e extrai os dados
for pasta_mae, subpastas in configuracoes.items():
    for subpasta in subpastas:
        dir_caso = os.path.join(dir_base, pasta_mae, subpasta)
        log_path = os.path.join(dir_caso, 'log.solver')
        
        if not os.path.exists(log_path):
            continue
        
        tau_w = "N/A"
        yplus_max = "N/A"
        yplus_avg = "N/A"
        clock_time = "N/A"
        
        # le o log.solver do caso especifico
        with open(log_path, 'r') as log:
            for linha in log:
                # captura o tempo de execucao
                if 'ClockTime =' in linha:
                    try: clock_time = linha.split('ClockTime =')[1].split('s')[0].strip()
                    except: pass
                
                # captura y+ do patch bottom
                if 'patch bottom y+ :' in linha:
                    try:
                        yplus_max = linha.split('max =')[1].split(',')[0].strip()
                        yplus_avg = linha.split('average =')[1].strip()
                    except: pass
                
                # captura atrito na parede bottom quebrando o vetor
                if 'min/max(bottom) =' in linha:
                    try:
                        min_vec = linha.split('=')[1].split('),')[0].replace('(', '').strip()
                        max_vec = linha.split('),')[1].replace('(', '').strip()
                        
                        val_min = abs(float(min_vec.split()[0]))
                        val_max = abs(float(max_vec.split()[0]))
                        tau_w = max(val_min, val_max)
                    except: pass

        # adiciona os valores no resumo txt
        with open(arquivo_resumo, 'a') as f:
            f.write(f"[{subpasta}]\n")
            f.write(f"Tau_w: {tau_w}\n")
            f.write(f"Max y+: {yplus_max}\n")
            f.write(f"Avg y+: {yplus_avg}\n")
            f.write(f"ClockTime: {clock_time}s\n")
            f.write("-" * 30 + "\n")

# =========================================================================
        # MODIFICADO: GERAÇÃO DE PLOTS E PASTAS NA RAIZ DO SCRIPT
        # =========================================================================
        # Caminho da pasta mestre centralizada na raiz do script
        dir_resultados_master = os.path.join(dir_base, 'Resultados_GT2')
        
        # Cria a subpasta específica para o modelo: Resultado_nome_modelo
        dir_resultados = os.path.join(dir_resultados_master, f'Resultado_{subpasta}')
        os.makedirs(dir_resultados, exist_ok=True)
        
        # Procura arquivos .xy extraidos pelo sampleDict (postProcessing/sampleDict/<tempo>/*.xy)
        arquivos_xy = glob.glob(os.path.join(dir_caso, 'postProcessing', 'sampleDict', '*', '*.xy'))
        
        if arquivos_xy:
            print(f"-> Gerando graficos em: Resultados_GT2/Resultado_{subpasta}/")
            for arq in arquivos_xy:
                nome_campo = os.path.basename(arq).replace('.xy', '')
                
                try:
                    # Carrega a tabela de dados
                    dados = np.loadtxt(arq)
                    
                    if dados.ndim == 2 and dados.shape[0] > 0:
                        
                        # =======================================================
                        # CORREÇÃO DO BUG DO MATPLOTLIB
                        # 1. Ordena os dados baseados na coordenada Y (coluna 0)
                        dados = dados[dados[:, 0].argsort()]
                        # 2. Corta os "zeros" do infinito (limita até o topo da malha y=1.0)
                        dados = dados[dados[:, 0] <= 1.0]
                        plt.figure(figsize=(7, 5))
                        
                        # Tratamento inteligente para achar Ux independente de como o OpenFOAM salvou
                        if 'U' in nome_campo:
                            # Se o arquivo tem muitas colunas, o vetor U (Ux, Uy, Uz) ocupa as ultimas 3 posicoes
                            if dados.shape[1] >= 4:
                                ux_dados = dados[:, -3] # Pega a antepenultima coluna (Ux)
                            else:
                                ux_dados = dados[:, 1]  # Pega a coluna 1 se o arquivo for exclusivo do U
                                
                            plt.plot(ux_dados, dados[:, 0], color='blue', linewidth=2, label='$U_x$')
                            plt.xlabel('Velocidade Longitudinal $U_x$ [m/s]')
                        else:
                            # Tratamento para as outras variaveis (p, k, omega, nut)
                            plt.plot(dados[:, 1], dados[:, 0], color='red', linewidth=2, label=nome_campo)
                            plt.xlabel(f'Grandeza Escalar: {nome_campo}')
                            
                        plt.ylabel('Distancia normal da parede $y$ [m]')
                        plt.title(f'Perfil de {nome_campo} ({subpasta})')
                        plt.grid(True, linestyle='--', alpha=0.5)
                        plt.legend()
                        
                        # Salva o plot na nova estrutura centralizada
                        caminho_salvar = os.path.join(dir_resultados, f'perfil_{nome_campo}.png')
                        plt.savefig(caminho_salvar, dpi=150, bbox_inches='tight')
                        plt.close()
                except Exception as e:
                    print(f"   [Aviso] Falha ao plotar o arquivo {nome_campo}: {e}")