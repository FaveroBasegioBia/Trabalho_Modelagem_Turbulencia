 #!/bin/bash

nprocs=4
foamDictionary system/decomposeParDict -entry numberOfSubdomains -set $nprocs

decomposePar 

# Use simpleFoam and postProcess because foamRun and foamPostProcess are not available here.
mpirun -np $nprocs simpleFoam -parallel | tee log.solver
reconstructPar 

#postProcess -func 'grad(U)' -latestTime -noZero
#postProcess -func sampleDict -latestTime -noZero
#postProcess -func surfacesDict -latestTime -noZero

postProcess -solver incompressibleFluid -func wallShearStress -noZero -noFunctionObjects

#postProcess -func 'grad(U)' -noZero
#postProcess -func sampleDict -noZero
#postProcess -func surfacesDict -noZero

postProcess -func 'grad(U)' -noZero
postProcess -func sampleDict -latestTime
postProcess -func surfacesDict -latestTime
