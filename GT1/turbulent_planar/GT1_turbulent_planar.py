import numpy as np
import matplotlib.pyplot as plt
import os

nu = 1e-5  
rho = 1.0  
R = 0.1    

arquivo_dados = "postProcessing/sampleDict0/1000/profile1_p_U_wallShearStress.xy"
pasta_saida = "posprocesspython"

if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

with open("valor_tau_w.txt", "r") as f:
    tau_w = float(f.read().strip())

if os.path.exists(arquivo_dados):
    dados = np.loadtxt(arquivo_dados)
    
    dist_y = dados[:, 0]
    vel_U = dados[:, 2]
    
    # CORRECAO FISICA: y+ eh medido a partir da PAREDE (R - dist_y)
    dist_parede = R - dist_y
    u_tau = np.sqrt(tau_w / rho)
    
    y_plus = (dist_parede * u_tau) / nu
    u_plus = vel_U / u_tau
    
    # Removemos o ponto exato da parede (onde dist=0) para nao dar erro no log(0)
    filtro = dist_parede > 1e-6
    y_plus_valido = y_plus[filtro]
    u_plus_valido = u_plus[filtro]
    
    # PERFIL ADIMENSIONAL (u+ vs y+) - SEMI-LOG
    plt.figure(figsize=(10, 6))
    
    # Linha solida ao inves de pontos ('-') para ficar suave com 1000 dados
    plt.plot(y_plus_valido, u_plus_valido, '-', color='blue', linewidth=2, label='OpenFOAM - Turbulent Planar')
    
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
    print(f"Grafico 1 gerado: {caminho_grafico1}")

    # PERFIL FISICO VS LEI DE POTENCIA (POWER LAW)
    plt.figure(figsize=(10, 6))
    
    plt.plot(dist_y, vel_U, '-', color='red', linewidth=2, label='OpenFOAM - Turbulent Planar')
    
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
    print(f"Grafico 2 gerado: {caminho_grafico2}")

else:
    print("Erro: O ficheiro nao foi encontrado.")