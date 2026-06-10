import numpy as np
import matplotlib.pyplot as plt
import os

# ==============================================================================
# PARAMETROS FISICOS DO CASO (Ajuste conforme suas propriedades do fluido)
# ==============================================================================
nu = 1e-5  # Viscosidade cinematica (m^2/s)
rho = 1.0  # Densidade do fluido (kg/m^3)
R = 0.1    # Raio do duto (m) de acordo com o blockMeshDict

# ==============================================================================
# CONFIGURACAO DE PASTAS E FICHEIROS DE ENTRADA
# ==============================================================================
# Caminho exato gerado pelo OpenFOAM v2206
arquivo_dados = "postProcessing/sampleDict0/1000/profile0_p_U_wallShearStress.xy"

# Definicao da pasta onde os graficos serao salvos
pasta_saida = "posprocesspython"

if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

# INSIRA AQUI o valor de wallShearStress (Tau_w) obtido no log do seu terminal
tau_w = 0.0045 

# ==============================================================================
# PROCESSAMENTO DOS DADOS PARA PERFIL ADIMENSIONAL (LOG-LAW)
# ==============================================================================
if os.path.exists(arquivo_dados):
    dados = np.loadtxt(arquivo_dados)
    
    # Coluna 0 eh a coordenada de distancia radial (y)
    dist_y = dados[:, 0]
    
    # CORRECAO: Coluna 2 eh a velocidade Ux real do escoamento (e nao a 4)
    vel_U = dados[:, 2]
    
    # Calculo da velocidade de atrito (u_tau)
    u_tau = np.sqrt(tau_w / rho)
    
    # Adimensionalizacao dos vetores
    y_plus = (dist_y * u_tau) / nu
    u_plus = vel_U / u_tau
    
    # --------------------------------------------------------------------------
    # GRAFICO 1: PERFIL ADIMENSIONAL (u+ vs y+) - SEMI-LOG
    # --------------------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    
    plt.plot(y_plus, u_plus, 'o-', color='blue', label='OpenFOAM - Turbulent Planar')
    
    y_teorico = np.logspace(-1, 3, 100)
    
    subcamada = y_teorico[y_teorico < 10]
    plt.plot(subcamada, subcamada, 'k:', linewidth=2, label='Teorico: u+ = y+')
    
    log_law = (1 / 0.41) * np.log(y_teorico[y_teorico > 10]) + 5.0
    plt.plot(y_teorico[y_teorico > 10], log_law, 'k-', linewidth=2, label='Teorico: Log-Law (k=0.41, B=5.0)')
    
    plt.xscale('log')
    plt.xlim(0.1, 1000)
    plt.ylim(0, 30)
    plt.xlabel('Distancia Adimensional da Parede (y+)', fontsize=12)
    plt.ylabel('Velocidade Adimensional (u+)', fontsize=12)
    plt.title('Perfil Adimensional de Velocidade - Camada Limite (GT1)', fontsize=13)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(loc='best')
    
    caminho_grafico1 = os.path.join(pasta_saida, 'GT1_Planar_LogLaw.png')
    plt.savefig(caminho_grafico1, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Grafico 1 gerado em: {caminho_grafico1}")

    # --------------------------------------------------------------------------
    # GRAFICO 2: PERFIL FISICO VS LEI DE POTENCIA (POWER LAW)
    # --------------------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    
    plt.plot(dist_y, vel_U, 's-', color='red', label='OpenFOAM - Turbulent Planar')
    
    U_max = np.max(vel_U)
    y_eixo = np.linspace(0, R, 100)
    U_power_law = U_max * (1 - y_eixo/R)**(1.0/7.0)
    
    plt.plot(y_eixo, U_power_law, 'k--', linewidth=2, label='Correlacao Empirica: Lei de Potencia (1/7)')
    
    plt.xlim(0, R)
    plt.xlabel('Distancia da Parede y (m)', fontsize=12)
    plt.ylabel('Velocidade Linear U (m/s)', fontsize=12)
    plt.title('Perfil de Velocidade Real vs Lei de Potencia (GT1)', fontsize=13)
    plt.grid(True, ls="--", alpha=0.5)
    plt.legend(loc='best')
    
    caminho_grafico2 = os.path.join(pasta_saida, 'GT1_Planar_PowerLaw.png')
    plt.savefig(caminho_grafico2, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Grafico 2 gerado em: {caminho_grafico2}")

else:
    print("Erro: O ficheiro do OpenFOAM nao foi localizado no caminho indicado.")