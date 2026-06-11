# GT1 - Escoamento Laminar e Turbulento em Duto Circular (OpenFOAM v2206)

Este diretório contém os casos de validação e estudo paramétrico para escoamento em duto circular (Re = 100 e Re = 10000).

## Estrutura de Pastas
* laminar/: Caso laminar padrão (Re = 100).
* turbulent_planar/: Caso turbulento em abordagem 2D planar (Re = 10000).
* turbulent_wedge/: Caso turbulento com simetria axial (Re = 10000).

## Como Rodar

### Execução Automatizada (Orquestrador Mestre)
Para rodar toda a matriz de testes, aplicar as variações de intensidade turbulenta, extrair os dados e gerar os gráficos automaticamente, execute na raiz do diretório:
python3 roda_tudo.py

### Execução Manual (Individual)
Para rodar ou inspecionar um caso isoladamente, navegue até a respectiva pasta e execute o script de submissão:
cd nome_da_pasta
sh run_all.sh

## Onde Encontrar os Resultados

Após o término das simulações pelo orquestrador, os dados consolidados e pós-processados serão organizados na raiz do diretório GT1:

### 1. Resumo Numérico
* Resumo_Para_Analisar.txt: Arquivo de texto unificado contendo os valores extraídos de Tensão de Cisalhamento na Parede (Tau_w), y+ máximo, y+ médio e tempo de execução (ClockTime) para cada caso e modelo.

### 2. Pastas de Resultados Individuais
Os gráficos gerados e os dados brutos de perfil de velocidade são movidos para pastas exclusivas identificadas pelo sufixo do teste:
* Resultados_laminar_Padrao/
* Resultados_turbulent_planar_Padrao/
* Resultados_turbulent_wedge_kEps_5pct/
* Resultados_turbulent_wedge_kEps_10pct/
* Resultados_turbulent_wedge_SST_5pct/
* Resultados_turbulent_wedge_SST_10pct/
* Resultados_turbulent_wedge_SA_5pct/

Cada uma dessas pastas conterá:
* O gráfico correspondente de validação do perfil de velocidade (.png).
* O arquivo de dados numéricos extraídos da linha de amostragem (dados_perfil.xy).