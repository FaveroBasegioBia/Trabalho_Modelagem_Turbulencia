 #!/bin/bash

# Use simpleFoam and postProcess because foamRun and foamPostProcess are not available here.
simpleFoam | tee log.simpleFoam
 
postProcess -func 'grad(U)' -latestTime

postProcess -func sampleDict -latestTime -noZero

postProcess -func surfacesDict -latestTime -noZero

