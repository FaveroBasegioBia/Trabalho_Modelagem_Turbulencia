#!/bin/bash

nprocs=8
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

# Executa o solver principal com espaço correto
simpleFoam | tee log.solver

# Calcula a tensao cisalhante na parede (Corrigido: sem o -solver)
postProcess -func wallShearStress -noZero -noFunctionObjects -latestTime

# Calcula o yPlus (Corrigido: sem o -solver)
postProcess -func yPlus -latestTime

# Executa a amostragem de dados do perfil de velocidade
postProcess -func sampleDict0 -latestTime -noZero



# nprocs=4
# foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

# # Executa o solver principal com espaço correto
# simpleFoam | tee log.solver

# # Calcula a tensao cisalhante na parede (Corrigido: sem o -solver)
# postProcess -func wallShearStress -noZero -noFunctionObjects -latestTime

# # Calcula o yPlus (Corrigido: sem o -solver)
# postProcess -func yPlus -latestTime

# # Executa a amostragem de dados do perfil de velocidade
# postProcess -func sampleDict0 -latestTime -noZero