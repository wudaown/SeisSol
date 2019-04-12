#!/bin/bash
# $1 [lts1,lts2]
source env.sh
THREAD=9
for i in {1..4}
do
    NUM=$(( ${THREAD} + 1 ))
    mkdir output 
    OMP_NUM_THREADS=${THREAD} KMP_AFFINITY=compact,granularity=thread mpirun -np 1 -host athena0 -ppn 1  ./SeisSol_release_generatedKernels_dskx_hybrid_none_9_6 ${1}.par | tee $1_${NUM}_core_order6.run
    mv output output_${NUM}_${1}
    THREAD=$(( ${THREAD} + 10 ))
done
