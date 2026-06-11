import os
import subprocess
import shutil

dir_base = os.getcwd()

# Matriz de Testes Expandida
configuracoes = {
    'laminar': [{'modelo': 'Padrao', 'intensidade': 'N/A', 'sufixo': 'Padrao'}],
    'turbulent_planar': [{'modelo': 'Padrao', 'intensidade': 'N/A', 'sufixo': 'Padrao'}], 
    'turbulent_wedge': [
        {'modelo': 'kEpsilon', 'intensidade': '0.05', 'sufixo': 'kEps_5pct'},
        {'modelo': 'kEpsilon', 'intensidade': '0.10', 'sufixo': 'kEps_10pct'},
        {'modelo': 'kOmegaSST', 'intensidade': '0.05', 'sufixo': 'SST_5pct'},
        {'modelo': 'kOmegaSST', 'intensidade': '0.10', 'sufixo': 'SST_10pct'},
        {'modelo': 'SpalartAllmaras', 'intensidade': '0.05', 'sufixo': 'SA_5pct'}
    ]
}

arquivo_resumo = os.path.join(dir_base, 'Resumo_Para_Analisar.txt')

with open(arquivo_resumo, 'w') as f:
    f.write("=== DADOS EXTRAIDOS DO GT1 PARA ANALISE ===\n\n")

for caso, testes in configuracoes.items():
    dir_caso = os.path.join(dir_base, caso)
    
    if not os.path.exists(dir_caso):
        continue

    os.chdir(dir_caso)
    
    for teste in testes:
        modelo_atual = teste['modelo']
        intensidade_atual = teste['intensidade']
        sufixo_atual = teste['sufixo']
        
        print(f"\n{'='*60}")
        print(f"Processando: CASO [{caso}] | MODELO [{modelo_atual}] | INTENS. [{intensidade_atual}]")
        print(f"{'='*60}")

        arq_config = 'constant/turbulenceProperties'
        arq_k = '0/k'
        
        # === 1. PROTEÇÃO DO SETUP FÍSICO (Modelos) ===
        if caso == 'laminar':
            with open(arq_config, 'w') as f:
                f.write("FoamFile { version 2.0; format ascii; class dictionary; location \"constant\"; object turbulenceProperties; }\n")
                f.write("simulationType  laminar;\n")
        elif modelo_atual != 'Padrao':
            with open(arq_config, 'w') as f:
                f.write("FoamFile { version 2.0; format ascii; class dictionary; location \"constant\"; object turbulenceProperties; }\n")
                f.write("simulationType  RAS;\n")
                f.write("RAS\n{\n")
                f.write(f"    RASModel        {modelo_atual};\n")
                f.write("    turbulence      on;\n")
                f.write("    printCoeffs     on;\n")
                f.write("}\n")
                
            # === 2. PROTEÇÃO DO SETUP FÍSICO (Intensidade) ===
            # Altera a condicao de contorno de entrada da energia turbulenta
            if os.path.exists(arq_k) and intensidade_atual != 'N/A':
                with open(arq_k, 'r') as f: linhas_k = f.readlines()
                with open(arq_k, 'w') as f:
                    for linha in linhas_k:
                        if 'intensity' in linha:
                            f.write(f"        intensity       {intensidade_atual};\n")
                        else:
                            f.write(linha)

        # === EXECUTA A SIMULAÇÃO ===
        subprocess.run(['sh', 'run_all.sh'])

        # --- Extração de Dados ---
        tau_w_real = None 
        yplus_max = "N/A"
        yplus_avg = "N/A"
        clock_time = "N/A"
        
        # Leitura direta e exata do log.solver
        if os.path.exists('log.solver'):
            with open('log.solver', 'r') as log:
                conteudo = log.readlines()
                for linha in conteudo:
                    if 'patch top y+ :' in linha:
                        try:
                            yplus_max = linha.split('max =')[1].split(',')[0].strip()
                            yplus_avg = linha.split('average =')[1].strip()
                        except: pass
                    if 'ClockTime =' in linha:
                        try: clock_time = linha.split('ClockTime =')[1].split('s')[0].strip()
                        except: pass
                    
                    if 'min/max(top)' in linha:
                        try:
                            vetor_saida = linha.split('), (')[1]
                            tau_w_real = abs(float(vetor_saida.split()[0]))
                        except: pass
        
        # Salva-vidas
        if tau_w_real is None:
            tau_w_real = 0.001
            print(f"\n[ALERTA CRÍTICO]: OpenFOAM falhou no modelo {modelo_atual}.")
        
        # Salva o valor para o plot Python ler
        with open("valor_tau_w.txt", "w") as f: f.write(str(tau_w_real))

        # Escreve resumo usando o SUFIXO
        with open(arquivo_resumo, 'a') as f:
            f.write(f"[{caso} - {sufixo_atual}]\nTau_w: {tau_w_real}\nMax y+: {yplus_max}\nAvg y+: {yplus_avg}\nClockTime: {clock_time}s\n{'-'*30}\n")

        # Roda script grafico
        nome_script = f"GT1_{caso}.py"
        caminho_script = os.path.join(dir_base, nome_script)
        if os.path.exists(caminho_script):
            subprocess.run(['python3', caminho_script])

        # Move os Resultados (nomeando a pasta de acordo com o estudo parametrico)
        pasta_dest = os.path.join(dir_base, f'Resultados_{caso}_{sufixo_atual}')
        if os.path.exists('posprocesspython'):
            if os.path.exists(pasta_dest): shutil.rmtree(pasta_dest)
            os.rename('posprocesspython', pasta_dest)
            for arq in os.listdir('.'):
                if arq.endswith('.png'): shutil.move(arq, os.path.join(pasta_dest, arq))

os.chdir(dir_base)
print(f"\nSUCESSO TOTAL! Dados em {arquivo_resumo}")