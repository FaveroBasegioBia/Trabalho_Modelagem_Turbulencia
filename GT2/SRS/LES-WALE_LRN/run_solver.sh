#!/bin/bash
set -e

nprocs=8
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs > /dev/null 2>&1

echo "--Comeco simulacao--"

# Roda o solver transiente de forma 100% silenciosa e joga tudo (saída e erros) para o log.solver
pimpleFoam > log.solver 2>&1

# Extrai os dados das sondas (sampleDict) apenas no último tempo salvo de forma silenciosa
postProcess -func sampleDict -latestTime > /dev/null 2>&1