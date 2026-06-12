#!/bin/bash

. /usr/lib/openfoam/openfoam2206/etc/bashrc

nprocs=8
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs > /dev/null 2>&1

echo "-> Iniciando o solver simpleFoam (Erros serao mostrados com localizacao)..."

# O -A 20 garante que, se houver erro, as próximas 20 linhas explicativas apareçam na tela
simpleFoam 2>&1 | tee log.solver | grep -A 20 --color=always -E "ERROR|FATAL|Warning|Exception|Aborted|core dumped"

# Pos-processamento direcionado para o log de forma silenciosa
simpleFoam -postProcess -func wallShearStress -latestTime >> log.solver 2>&1 | grep -E "ERROR|FATAL|Warning|Exception"
simpleFoam -postProcess -func yPlus -latestTime >> log.solver 2>&1 | grep -E "ERROR|FATAL|Warning|Exception"
simpleFoam -postProcess -func sampleDict -latestTime >> log.solver 2>&1 | grep -E "ERROR|FATAL|Warning|Exception"
simpleFoam -postProcess -func probesDict -latestTime >> log.solver 2>&1 | grep -E "ERROR|FATAL|Warning|Exception"

# Executa o script python silenciosamente
python3 GT2_pos_process.py > /dev/null 2>&1
