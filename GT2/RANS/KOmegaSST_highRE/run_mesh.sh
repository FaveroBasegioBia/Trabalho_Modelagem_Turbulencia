#!/bin/bash

. /usr/lib/openfoam/openfoam2206/etc/bashrc

foamCleanTutorials

blockMesh

checkMesh | tee log.checkMesh
