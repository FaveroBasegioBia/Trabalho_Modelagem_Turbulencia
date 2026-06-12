import os
import subprocess
import time

dir_base = os.getcwd()

# Matriz Oficial de Casos do GT2
configuracoes = {
    'RANS': ['KEpsilon_highRE_V1', 'KEpsilon_lowRE_V1', 'KOmegaSST_highRE', 'KOmegaSST_lowRE_V1', 'SA_LRN'],
    'SRS': ['DES_KO_LRN', 'LES-WALE_LRN']
}

print(" INICIANDO BATERIA DE SIMULAÇÕES DO GT2 ")
tempo_inicio_global = time.time()

# Varre todas as pastas e roda as simulações
for pasta_mae, subpastas in configuracoes.items():
    for subpasta in subpastas:
        dir_caso = os.path.join(dir_base, pasta_mae, subpasta)
        
        if not os.path.exists(dir_caso):
            print(f"[AVISO] Pasta não encontrada: {pasta_mae}/{subpasta} - Pulando...")
            continue

        print(f"\n>>> Processando: Abordagem [{pasta_mae}] | Modelo [{subpasta}]")
        os.chdir(dir_caso)
        
        # Executa o script do OpenFOAM para rodar malha, solver e sampling
        if os.path.exists('run_all.sh'):
            print(f"    Rodando run_all.sh")
            tempo_inicio_caso = time.time()
            
            try:
                # Mudança aqui: capture_output=True permite ler o erro se ele acontecer
                subprocess.run(['sh', 'run_all.sh'], capture_output=True, text=True, check=True)
                
                tempo_fim_caso = time.time()
                duracao = (tempo_fim_caso - tempo_inicio_caso) / 60
                print(f"    [OK] Simulação concluída em {duracao:.2f} minutos.")
                
            except subprocess.CalledProcessError as e:
                print(f"    [ERRO] A simulação falhou ou foi interrompida no modelo {subpasta}.")
                print(f"    [DETALHE DO ERRO]:")
                
                # Junta o log padrão e o log de erro do OpenFOAM
                log_completo = e.stdout + e.stderr
                linhas_erro = log_completo.strip().split('\n')
                
                # Imprime apenas as últimas 15 linhas no terminal (onde o erro Fatal costuma ficar)
                print("    " + "-"*50)
                for linha in linhas_erro[-15:]:
                    print(f"    | {linha}")
                print("    " + "-"*50)
                
                # Salva o erro completo em um arquivo de texto para você poder analisar
                arq_erro = "FALHA_SIMULACAO.log"
                with open(arq_erro, 'w') as f_erro:
                    f_erro.write(log_completo)
                print(f"    [AJUDA] O log completo do erro foi salvo em: {pasta_mae}/{subpasta}/{arq_erro}")
                
        else:
            print(f"    [ERRO] Arquivo 'run_all.sh' não encontrado em {subpasta}!")

# Retorna para a raiz do projeto
os.chdir(dir_base)

tempo_fim_global = time.time()
duracao_total = (tempo_fim_global - tempo_inicio_global) / 60

print(f"\n SIMULAÇÕES FINALIZADAS! (Tempo total: {duracao_total:.2f} min) ")
print(" INICIANDO PÓS-PROCESSAMENTO AUTOMÁTICO ")

# Roda o script de pós-processamento e geração de gráficos (que criamos anteriormente)
if os.path.exists('GT2_pos_process.py'):
    print("\n-> Extraindo dados do log.solver...")
    print("-> Plotando gráficos dimensionais...")
    print("-> Plotando gráficos adimensionais (Lei da Parede e Cf)...")
    
    # Chama o script Python de forma limpa
    subprocess.run(['python3', 'GT2_pos_process.py'])
    
    print("\n[SUCESSO ABSOLUTO] Todo o fluxo de trabalho do GT2 foi concluído!")
    print("Verifique o arquivo 'Resumo_Para_Analisar.txt' e a pasta 'Resultados_GT2'.")
else:
    print("\n[ERRO FATAL] O script 'GT2_pos_process.py' não foi encontrado na raiz do projeto!")
    print("Certifique-se de que ele está salvo na mesma pasta que este arquivo master.")