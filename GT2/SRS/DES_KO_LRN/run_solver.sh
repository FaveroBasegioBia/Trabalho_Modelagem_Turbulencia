#!/bin/bash
set -e

nprocs=9
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs > /dev/null 2>&1

echo "--Comeco simulacao--"

# Roda o solver de forma 100% silenciosa e joga tudo (saída e erros) para o log.solver
pimpleFoam > log.solver 2>&1

# Extrai os dados das sondas (Opcional, caso você precise regerar os arquivos .xy localmente)
postProcess -func sampleDict -latestTime > /dev/null 2>&1
