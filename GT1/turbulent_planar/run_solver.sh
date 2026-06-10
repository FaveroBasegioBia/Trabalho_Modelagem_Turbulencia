 #!/bin/bash

nprocs=4
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

# Clean previous run data so the solver starts from a fresh case.
foamCleanTutorials

#decomposePar
#mpirun -np $nprocs foamRun -parallel | tee log.solver

# foamRun | tee log.solver

# Modificado para rodar direito
simpleFoam | tee log.solver

# Apenas PostProcess
# postProcess here does not accept -solver in this OpenFOAM version.
postProcess -func wallShearStress -noZero -noFunctionObjects -latestTime

# yPlus is handled by controlDict yplus_stats in this case.

postProcess -func sampleDict0 -latestTime -noZero
#foamPostProcess -func probesDict0 -latestTime -noZero
