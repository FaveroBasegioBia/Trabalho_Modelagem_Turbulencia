 #!/bin/bash

nprocs=4
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

#decomposePar
#mpirun -np $nprocs foamRun -parallel | tee log.solver

# Use simpleFoam and postProcess because foamRun and foamPostProcess are not available here.
simpleFoam | tee log.solver

postProcess -solver incompressibleFluid -func wallShearStress -noZero -noFunctionObjects

#postProcess -solver incompressibleFluid -func yPlus

postProcess -func sampleDict -noZero

postProcess -func probesDict -noZero