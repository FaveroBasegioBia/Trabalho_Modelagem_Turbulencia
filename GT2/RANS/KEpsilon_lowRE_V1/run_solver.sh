 #!/bin/bash

nprocs=8
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

#decomposePar
#mpirun -np $nprocs foamRun -parallel | tee log.solver

simpleFoam | tee log.solver

postProcess -solver incompressibleFluid -func wallShearStress -noZero -noFunctionObjects

#postProcess -solver incompressibleFluid -func yPlus

postProcess -func sampleDict -noZero

postProcess -func probesDict -noZero


# nprocs=8
# foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

# #decomposePar
# #mpirun -np $nprocs foamRun -parallel | tee log.solver

# foamRun | tee log.solver

# foamPostProcess -solver incompressibleFluid -func wallShearStress -noZero -noFunctionObjects

# #foamPostProcess -solver incompressibleFluid -func yPlus

# foamPostProcess -func sampleDict -noZero

# foamPostProcess -func probesDict -noZero