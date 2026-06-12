 #!/bin/bash

#foamPostProcess -solver incompressibleFluid -func wallShearStress -noZero -noFunctionObjects

echo "Resultado do sampling"

postProcess -func  sampleDict -noZero | grep -A 20 --color=always -E "ERROR|FATAL|Warning|Exception|Aborted|core dumped"

postProcess -func  probesDict -noZero | grep -A 20 --color=always -E "ERROR|FATAL|Warning|Exception|Aborted|core dumped"


