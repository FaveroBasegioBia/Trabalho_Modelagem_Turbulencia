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
# CONFIGURACAO DE PASTAS E ARQUIVOS DE ENTRADA (ESTILO PLANAR)
# ==============================================================================
# Caminho exato do profile1 (1000 pontos) gerado no caso wedge
arquivo_dados = "postProcessing/sampleDict0/1000/profile1_p_U_wallShearStress.xy"

# Definicao da pasta de destino solicitada
pasta_saida = "posprocesspython"

# Cria a pasta automaticamente se ela nao existir
if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

# INSIRA AQUI o valor de wallShearStress (Tau_w) obtido no seu turbulent_wedge
# Verifique o valor maximo de wallShearStress gerado para o caso wedge
tau_w = 0.005295

# ==============================================================================
# PROCESSAMENTO DOS DADOS PARA PERFIL ADIMENSIONAL (LOG-LAW)
# ==============================================================================
if os.path.exists(arquivo_dados):
    dados = np.loadtxt(arquivo_dados)
    
    # Coluna 0 eh a coordenada de distancia radial (y)
    dist_y = dados[:, 0]
    
    # CORRECAO: Coluna 2 eh a velocidade Ux real do escoamento no OpenFOAM v2206
    vel_U = dados[:, 2]
    
    # CORRECAO FISICA: y+ eh medido a partir da PAREDE do duto (R - dist_y)
    dist_parede = R - dist_y
    u_tau = np.sqrt(tau_w / rho)
    
    # Calculo das variaveis adimensionais de camada limite
    y_plus = (dist_parede * u_tau) / nu
    u_plus = vel_U / u_tau
    
    # Filtro para remover o ponto exato da parede e evitar erro de log(0)
    filtro = dist_parede > 1e-6
    y_plus_valido = y_plus[filtro]
    u_plus_valido = u_plus[filtro]
    
    # --------------------------------------------------------------------------
    # GRAFICO 1: PERFIL ADIMENSIONAL (u+ vs y+) - SEMI-LOG
    # --------------------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    
    # Linha solida suave aproveitando os 1000 pontos do profile1
    plt.plot(y_plus_valido, u_plus_valido, '-', color='green', linewidth=2, label='OpenFOAM - Turbulent Wedge')
    
    # Curvas teoricas de referencia (Subcamada viscosa e Lei de Parede)
    y_teorico = np.logspace(-1, 3, 100)
    subcamada = y_teorico[y_teorico < 10]
    plt.plot(subcamada, subcamada, 'k:', linewidth=2, label='Teorico: u+ = y+')
    
    log_law = (1 / 0.41) * np.log(y_teorico[y_teorico > 10]) + 5.0
    plt.plot(y_teorico[y_teorico > 10], log_law, 'k-', linewidth=2, label='Teorico: Log-Law (k=0.41, B=5.0)')
    
    # Formatacao do grafico semi-log conforme o roteiro do trabalho
    plt.xscale('log')
    plt.xlim(0.1, 1000)
    plt.ylim(0, 30)
    plt.xlabel('Distancia Adimensional da Parede (y+)', fontsize=12)
    plt.ylabel('Velocidade Adimensional (u+)', fontsize=12)
    plt.title('Perfil Adimensional de Velocidade - Camada Limite (GT1 Wedge)', fontsize=13)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(loc='best')
    
    caminho_grafico1 = os.path.join(pasta_saida, 'GT1_Wedge_LogLaw.png')
    plt.savefig(caminho_grafico1, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Grafico 1 gerado com sucesso em: {caminho_grafico1}")

    # --------------------------------------------------------------------------
    # GRAFICO 2: PERFIL FISICO VS LEI DE POTENCIA (POWER LAW 1/6)
    # --------------------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    
    # Plotagem da velocidade real extraida da simulacao axissimetrica
    plt.plot(dist_y, vel_U, '-', color='darkcyan', linewidth=2, label='OpenFOAM - Turbulent Wedge')
    
    # Curva de correlacao empirica da Lei de Potencia (Ajustada para o expoente 1/6 do Wedge)
    # U_max calculado direto do ponto de velocidade maxima no centro do duto
    U_max = np.max(vel_U)
    y_eixo = np.linspace(0, R, 100)
    U_power_law = U_max * (1 - y_eixo/R)**(1.0/6.0)
    
    plt.plot(y_eixo, U_power_law, 'k--', linewidth=2, label='Correlacao Empirica: Lei de Potencia (1/6)')
    
    # Formatacao do perfil fisico de velocidades
    plt.xlim(0, R)
    plt.xlabel('Distancia da Parede y (m)', fontsize=12)
    plt.ylabel('Velocidade Linear U (m/s)', fontsize=12)
    plt.title('Perfil de Velocidade Real vs Lei de Potencia (GT1 Wedge)', fontsize=13)
    plt.grid(True, ls="--", alpha=0.5)
    plt.legend(loc='best')
    
    caminho_grafico2 = os.path.join(pasta_saida, 'GT1_Wedge_PowerLaw.png')
    plt.savefig(caminho_grafico2, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Grafico 2 gerado com sucesso em: {caminho_grafico2}")

else:
    print("Erro: O arquivo profile1 do OpenFOAM nao foi localizado. Execute o postProcess primeiro.")