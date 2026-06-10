 #!/bin/bash

nprocs=4
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

#decomposePar
#mpirun -np $nprocs foamRun -parallel | tee log.solver

# foamRun | tee log.solver

# Modificado para rodar direito
simpleFoam | tee log.solver

# Apenas PostProcess
# postProcess here does not accept -solver in this OpenFOAM version.
postProcess -func wallShearStress -noZero -noFunctionObjects -latestTime

# postProcess here does not accept -solver in this OpenFOAM version.
postProcess -func yPlus

postProcess -func sampleDict0 -latestTime -noZero
#foamPostProcess -func probesDict0 -latestTime -noZero
