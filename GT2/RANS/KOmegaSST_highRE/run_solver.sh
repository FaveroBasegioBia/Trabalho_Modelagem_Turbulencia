#!/bin/bash

. /usr/lib/openfoam/openfoam2206/etc/bashrc

nprocs=8
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs > /dev/null 2>&1

echo "-> Aqui comeca o solver para o modelo k-omega SST !"

# Executa o solver principal filtrando erros com contexto
simpleFoam 2>&1 | tee log.solver | grep -A 20 --color=always -E "ERROR|FATAL|Warning|Exception|Aborted|core dumped"

echo "-> Executando pos-processamento..."

simpleFoam -postProcess -func wallShearStress -latestTime 2>&1 | tee -a log.solver | grep -A 20 --color=always -E "ERROR|FATAL|Warning|Exception"

simpleFoam -postProcess -func yPlus -latestTime 2>&1 | tee -a log.solver | grep -A 20 --color=always -E "ERROR|FATAL|Warning|Exception"

simpleFoam -postProcess -func sampleDict -latestTime 2>&1 | tee -a log.solver | grep -A 20 --color=always -E "ERROR|FATAL|Warning|Exception"
# =========================================================================

# Executa o processamento python
python3 GT2_pos_process.py > /dev/null 2>&1
