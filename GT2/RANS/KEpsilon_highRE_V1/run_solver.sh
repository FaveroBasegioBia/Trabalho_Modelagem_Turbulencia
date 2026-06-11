#!/bin/bash

. /usr/lib/openfoam/openfoam2206/etc/bashrc

nprocs=8
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

#decomposePar
#mpirun -np $nprocs simpleFoam -parallel | tee log.solver

# Executa o solver gerando o log inicial
simpleFoam | tee log.solver

# Injeta os dados de pos-processamento no fim do log de forma correta
simpleFoam -postProcess -func wallShearStress -latestTime >> log.solver 2>&1
simpleFoam -postProcess -func yPlus -latestTime >> log.solver 2>&1
simpleFoam -postProcess -func sampleDict -latestTime >> log.solver 2>&1

# Executa o script python individual da propria pasta para gerar o grafico e o txt local
python3 /home/danilom/Trabalho_Modelagem_Turbulencia/GT2/GT2_pos_process.py


#^ REFERENCIA DE CODIGO ORIGINAL
# source /Volumes/OpenFOAM/OpenFOAM-12/etc/bashrc

# nprocs=4
# foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

# #decomposePar
# #mpirun -np $nprocs foamRun -parallel | tee log.solver

# foamRun | tee log.solver

# foamPostProcess -solver incompressibleFluid -func wallShearStress -noZero -noFunctionObjects

# #foamPostProcess -solver incompressibleFluid -func yPlus

# foamPostProcess -func sampleDict -noZero

# foamPostProcess -func probesDict -noZero