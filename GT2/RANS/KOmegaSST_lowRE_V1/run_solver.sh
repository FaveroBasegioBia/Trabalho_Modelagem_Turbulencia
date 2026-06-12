#!/bin/bash

. /usr/lib/openfoam/openfoam2206/etc/bashrc

nprocs=8
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs > /dev/null 2>&1

#decomposePar
#mpirun -np $nprocs foamRun -parallel | tee log.solver

echo "Comeco simulacao"
# Executa o solver
simpleFoam 2>&1 | tee log.solver | grep -A 20 --color=always -E "ERROR|FATAL|Warning|Exception|Aborted|core dumped"

# Pos-processamento corrigido e padronizado para a versao v2206
simpleFoam -postProcess -func wallShearStress -latestTime >> log.solver 2>&1
simpleFoam -postProcess -func yPlus -latestTime >> log.solver 2>&1
simpleFoam -postProcess -func sampleDict -latestTime >> log.solver 2>&1

# Executa o processamento python
python3 GT2_pos_process.py > /dev/null 2>&1