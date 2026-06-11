import os
import subprocess
import shutil

dir_base = os.getcwd()

# turbulent_planar roda 1 vez
# turbulent_wedge roda 3 vezes.
configuracoes = {
    'turbulent_planar': ['Padrao'], 
    'turbulent_wedge': ['kEpsilon', 'kOmegaSST', 'SpalartAllmaras']
}

arquivo_resumo = os.path.join(dir_base, 'Resumo_Para_IA.txt')

# Inicializa o arquivo de resumo
with open(arquivo_resumo, 'w') as f:
    f.write("=== DADOS EXTRAIDOS DO GT1 PARA ANALISE ===\n\n")

for caso, modelos in configuracoes.items():
    dir_caso = os.path.join(dir_base, caso)
    
    if not os.path.exists(dir_caso):
        print(f"Aviso: Pasta {caso} nao encontrada. Pulando...")
        continue

    # Entra na pasta do caso
    os.chdir(dir_caso)
    
    for modelo in modelos:
        print(f"\n{'='*50}")
        print(f"Processando: CASO [{caso}] | MODELO [{modelo}]")
        print(f"{'='*50}")

        # Se nao for o caso Padrao, edita o arquivo turbulenceProperties
        if modelo != 'Padrao':
            arq_config = 'constant/turbulenceProperties'
            if os.path.exists(arq_config):
                with open(arq_config, 'r') as f: linhas = f.readlines()
                with open(arq_config, 'w') as f:
                    for linha in linhas:
                        if 'RASModel' in linha and '{' not in linha:
                            f.write(f"    RASModel        {modelo};\n")
                        else:
                            f.write(linha)
            else:
                print(f"Aviso: {arq_config} nao encontrado no {caso}.")

        # Executa a simulacao e os scripts do Gnuplot nativos
        subprocess.run(['sh', 'run_all.sh'])

        # Extrai dados do log.solver para os graficos e para o TXT
        tau_w_real = 0.001 
        yplus_max = "N/A"
        
        if os.path.exists('log.solver'):
            with open('log.solver', 'r') as log:
                conteudo = log.readlines()
                for linha in conteudo:
                    if 'patch top y+ :' in linha:
                        try:
                            yplus_max = linha.split('max =')[1].split(',')[0].strip()
                        except: pass
                    if 'min/max(top)' in linha:
                        try:
                            vetor_saida = linha.split('), (')[1]
                            tau_w_real = abs(float(vetor_saida.split()[0]))
                        except: pass
        
        # Salva a tensao num txt temporario
        with open("valor_tau_w.txt", "w") as f:
            f.write(str(tau_w_real))

        # Escreve as metricas fisicas no arquivo para analise
        with open(arquivo_resumo, 'a') as f:
            f.write(f"[{caso} - {modelo}]\n")
            f.write(f"Tensão na Parede (Tau_w): {tau_w_real}\n")
            f.write(f"Maior y+ na malha: {yplus_max}\n")
            f.write("-" * 30 + "\n")

        # Roda o script de grafico do Python buscando-o na pasta raiz
        nome_script = f"GT1_{caso}.py"
        caminho_script = os.path.join(dir_base, nome_script)
        
        if os.path.exists(caminho_script):
            subprocess.run(['python3', caminho_script])
        else:
            print(f"Aviso: Script {nome_script} nao encontrado na raiz GT1.")

        
        pasta_graficos_python = 'posprocesspython'
        pasta_destino = os.path.join(dir_base, f'Resultados_{caso}_{modelo}')

        if os.path.exists(pasta_destino): 
            shutil.rmtree(pasta_destino)
            
        # Renomeia a pasta gerada pelo script Python
        if os.path.exists(pasta_graficos_python):
            os.rename(pasta_graficos_python, pasta_destino)
        else:
            os.makedirs(pasta_destino)

        # Captura os 3 graficos .png do Gnuplot que estao soltos na pasta e os move para os resultados
        for arquivo in os.listdir('.'):
            if arquivo.endswith('.png'):
                caminho_origem = os.path.join('.', arquivo)
                caminho_final = os.path.join(pasta_destino, arquivo)
                shutil.move(caminho_origem, caminho_final)

# Volta para a raiz ao finalizar tudo
os.chdir(dir_base)
print(f"\nSUCESSO TOTAL! Os dados estao em {arquivo_resumo} e as pastas de Resultados foram populadas com sucesso!")