 #!/bin/bash

nprocs=8
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

# Executa o solver principal
simpleFoam | tee log.solver

# Pos-processamentos corrigidos para a versao v2206
postProcess -func wallShearStress -noZero -noFunctionObjects -latestTime
postProcess -func yPlus -latestTime
postProcess -func sampleDict0 -latestTime -noZero


# nprocs=8
# foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

# #decomposePar
# #mpirun -np $nprocs foamRun -parallel | tee log.solver

# foamRun | tee log.solver

# foamPostProcess -solver incompressibleFluid -func wallShearStress -noZero -noFunctionObjects -latestTime

# foamPostProcess -solver incompressibleFluid -func yPlus

# foamPostProcess -func sampleDict0 -latestTime -noZero