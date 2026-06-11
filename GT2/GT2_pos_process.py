import os
import glob

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
                        # a linha padrao tem o formato: min/max(bottom) = (x y z), (x y z)
                        min_vec = linha.split('=')[1].split('),')[0].replace('(', '').strip()
                        max_vec = linha.split('),')[1].replace('(', '').strip()
                        
                        # extrai apenas o valor X e pega o modulo mais alto
                        val_min = abs(float(min_vec.split()[0]))
                        val_max = abs(float(max_vec.split()[0]))
                        tau_w = max(val_min, val_max)
                    except: pass

        # adiciona os valores no resumo
        with open(arquivo_resumo, 'a') as f:
            f.write(f"[{subpasta}]\n")
            f.write(f"Tau_w: {tau_w}\n")
            f.write(f"Max y+: {yplus_max}\n")
            f.write(f"Avg y+: {yplus_avg}\n")
            f.write(f"ClockTime: {clock_time}s\n")
            f.write("-" * 30 + "\n")

print(f'Sucesso! Resumo extraido em: {arquivo_resumo}')