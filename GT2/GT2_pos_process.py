import os
import glob
import numpy as np
import matplotlib.pyplot as plt

# =========================================================================
# CONFIGURAÇÕES FÍSICAS DO ESCOAMENTO (Para Cálculos Adimensionais do GT2)
# =========================================================================
NU = 1.5e-5      # Viscosidade cinemática
U_INF = 1.0      # Velocidade da corrente livre [m/s]
X_START = 0.1    # Coordenada x onde a placa plana (sólida) começa [m]

# Define a raiz GT2
dir_base = os.getcwd()

# Pastas alvo para buscar resultados
configuracoes = {
    'RANS': ['KEpsilon_highRE_V1', 'KEpsilon_lowRE_V1', 'KOmegaSST_highRE', 'KOmegaSST_lowRE_V1', 'SA_LRN'],
    'SRS': ['DES_KO_LRN', 'LES-WALE_LRN']
}

arquivo_resumo = os.path.join(dir_base, 'Resumo_Para_Analisar.txt')

# Inicia o arquivo de texto
with open(arquivo_resumo, 'w') as f:
    f.write("=== DADOS EXTRAIDOS DO GT2 PARA ANALISE ===\n\n")

# Varre todas as pastas e extrai os dados
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
        
        # Lê o log.solver do caso específico
        with open(log_path, 'r') as log:
            for linha in log:
                if 'ClockTime =' in linha:
                    try: clock_time = linha.split('ClockTime =')[1].split('s')[0].strip()
                    except: pass
                
                if 'patch bottom y+ :' in linha:
                    try:
                        yplus_max = linha.split('max =')[1].split(',')[0].strip()
                        yplus_avg = linha.split('average =')[1].strip()
                    except: pass
                
                if 'min/max(bottom) =' in linha:
                    try:
                        min_vec = linha.split('=')[1].split('),')[0].replace('(', '').strip()
                        max_vec = linha.split('),')[1].replace('(', '').strip()
                        
                        val_min = abs(float(min_vec.split()[0]))
                        val_max = abs(float(max_vec.split()[0]))
                        tau_w = max(val_min, val_max)
                    except: pass

        with open(arquivo_resumo, 'a') as f:
            f.write(f"[{subpasta}]\n")
            f.write(f"Tau_w: {tau_w}\n")
            f.write(f"Max y+: {yplus_max}\n")
            f.write(f"Avg y+: {yplus_avg}\n")
            f.write(f"ClockTime: {clock_time}s\n")
            f.write("-" * 30 + "\n")

        # =========================================================================
        # GERAÇÃO DE PLOTS (DIMENSIONAIS E ADIMENSIONAIS)
        # =========================================================================
        dir_resultados_master = os.path.join(dir_base, 'Resultados_GT2')
        dir_resultados = os.path.join(dir_resultados_master, f'Resultado_{subpasta}')
        os.makedirs(dir_resultados, exist_ok=True)
        
        arquivos_xy = glob.glob(os.path.join(dir_caso, 'postProcessing', 'sampleDict', '*', '*.xy'))
        
        if arquivos_xy:
            print(f"-> Gerando graficos em: Resultados_GT2/Resultado_{subpasta}/")
            for arq in arquivos_xy:
                nome_campo = os.path.basename(arq).replace('.xy', '')
                
                try:
                    dados = np.loadtxt(arq)
                    
                    if dados.ndim == 2 and dados.shape[0] > 0:
                        is_horizontal = 'profile1' in nome_campo or 'profile3' in nome_campo
                        
                        # --- 1. SEPARAÇÃO INTELIGENTE DE VARIÁVEIS ---
                        if 'U' in nome_campo:
                            val_dados = dados[:, -3] if dados.shape[1] >= 4 else dados[:, 1]
                            label_val = '$U_x$'
                            nome_eixo_val = 'Velocidade Longitudinal $U_x$ [m/s]'
                            cor_linha = 'blue'
                        elif 'wallShearStress' in nome_campo:
                            # Tensão de cisalhamento (módulo do vetor)
                            val_dados = np.sqrt(dados[:, 1]**2 + dados[:, 2]**2 + dados[:, 3]**2) if dados.shape[1] >= 4 else np.abs(dados[:, 1])
                            label_val = r'$\tau_w$'
                            nome_eixo_val = r'Tensão de Cisalhamento $\tau_w$ [m²/s²]'
                            cor_linha = 'orange'
                        else:
                            val_dados = dados[:, 1]
                            label_val = nome_campo
                            nome_eixo_val = f'Grandeza Escalar: {nome_campo}'
                            cor_linha = 'red'

                        # --- 2. GRÁFICO DIMENSIONAL PADRÃO (O que já funcionava) ---
                        plt.figure(figsize=(7, 5))
                        if is_horizontal:
                            distancia_x = dados[:, 0]
                            plt.plot(distancia_x, val_dados, color=cor_linha, linewidth=2, label=label_val)
                            plt.xlabel('Distância ao longo da placa $x$ [m]')
                            plt.ylabel(nome_eixo_val)
                        else:
                            mascara = dados[:, 0] <= 1.0
                            distancia_y = dados[mascara, 0]
                            val_dados_filtrado = val_dados[mascara]
                            ordem = distancia_y.argsort()
                            distancia_y = distancia_y[ordem]
                            val_dados_filtrado = val_dados_filtrado[ordem]
                            
                            plt.plot(val_dados_filtrado, distancia_y, color=cor_linha, linewidth=2, label=label_val)
                            plt.xlabel(nome_eixo_val)
                            plt.ylabel('Distância normal da parede $y$ [m]')

                        plt.title(f'Perfil de {nome_campo} ({subpasta})')
                        plt.grid(True, linestyle='--', alpha=0.5)
                        plt.legend()
                        caminho_salvar = os.path.join(dir_resultados, f'perfil_{nome_campo}.png')
                        plt.savefig(caminho_salvar, dpi=150, bbox_inches='tight')
                        plt.close()

                        # --- 3. GRÁFICOS ADIMENSIONAIS ESPECIAIS (Comparação GT2) ---
                        
                        # 3A. LEI DA PAREDE (u+ vs y+) -> Só para perfis verticais de Velocidade
                        if 'U' in nome_campo and not is_horizontal and tau_w != "N/A" and float(tau_w) > 0:
                            try:
                                u_tau = np.sqrt(float(tau_w))
                                y_plus = (distancia_y * u_tau) / NU
                                u_plus = val_dados_filtrado / u_tau

                                plt.figure(figsize=(7, 5))
                                plt.semilogx(y_plus, u_plus, color='green', linewidth=2, label='Simulação CFD')

                                # Curva Analítica 1: Subcamada Viscosa (u+ = y+)
                                y_lin = np.linspace(0.1, 10, 50)
                                plt.semilogx(y_lin, y_lin, 'r:', linewidth=2, label='Viscous sublayer ($u^+ = y^+$)')

                                # Curva Analítica 2: Log-Law
                                y_log = np.linspace(10, max(y_plus) if max(y_plus) > 10 else 1000, 100)
                                u_log = (1.0 / 0.41) * np.log(y_log) + 5.0
                                plt.semilogx(y_log, u_log, 'k--', linewidth=2, label='Log-law')

                                plt.xlabel('Distância Adimensional $y^+$')
                                plt.ylabel('Velocidade Adimensional $u^+$')
                                plt.title(f'Lei da Parede ($u^+$ vs $y^+$) - {subpasta}')
                                plt.grid(True, which="both", linestyle='--', alpha=0.5)
                                # Limita o eixo Y e X para ficar parecido com o PDF
                                plt.ylim(0, 40)
                                plt.xlim(0.1, max(y_plus) if max(y_plus) > 1000 else 10000)
                                plt.legend()

                                caminho_salvar_lei = os.path.join(dir_resultados, f'adimensional_LeiParede_{nome_campo}.png')
                                plt.savefig(caminho_salvar_lei, dpi=150, bbox_inches='tight')
                                plt.close()
                            except Exception as e:
                                print(f"   [Aviso] Falha ao gerar Lei da Parede para {nome_campo}: {e}")

                        # 3B. COEFICIENTE DE ATRITO (Cf vs x) -> Só para linhas horizontais de Tensão
                        if 'wallShearStress' in nome_campo and is_horizontal:
                            try:
                                # Equação: Cf = tau_w / (0.5 * rho * U^2). (rho=1 em incompressível)
                                cf_num = val_dados / (0.5 * U_INF**2)

                                plt.figure(figsize=(7, 5))
                                plt.plot(distancia_x, cf_num, color='purple', linewidth=2, label='Simulação CFD')

                                # Curva Analítica de Schlichting (para X > inicio da placa)
                                x_placa = distancia_x[distancia_x > X_START] - X_START
                                if len(x_placa) > 0:
                                    x_placa = np.where(x_placa == 0, 1e-6, x_placa) # Evita divisão por zero
                                    rex = (U_INF * x_placa) / NU
                                    cf_analitico = 0.0592 * (rex**-0.2)
                                    
                                    # Plotando a curva teórica alinhada com a placa real
                                    plt.plot(x_placa + X_START, cf_analitico, 'k--', linewidth=2, label='Turbulento Teórico')

                                plt.xlabel('Comprimento do duto $x$ [m]')
                                plt.ylabel(r'Friction coefficient $c_f$')
                                plt.title(f'Coeficiente de Atrito - {subpasta}')
                                plt.grid(True, linestyle='--', alpha=0.5)
                                plt.ylim(0.0, 0.015) # Escala igual ao do PDF
                                plt.legend()

                                caminho_salvar_cf = os.path.join(dir_resultados, f'adimensional_Cf_{nome_campo}.png')
                                plt.savefig(caminho_salvar_cf, dpi=150, bbox_inches='tight')
                                plt.close()
                            except Exception as e:
                                print(f"   [Aviso] Falha ao gerar Cf para {nome_campo}: {e}")
                                
                except Exception as e:
                    print(f"   [Aviso] Falha ao plotar o arquivo {nome_campo}: {e}")