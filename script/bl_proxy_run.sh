#!/bin/bash
# $1 NELEM -- number of elements
# $2 TS -- timestep
# $3 folder -- folder to place result
# $4 del -- to remove result
# set -xe
export OMP_NUM_THREADS=40
export KMP_AFFINITY=compact,granularity=thread
run(){
  for i in $(ls -d */)
  do
    mkdir -p ${i}${3}
    for j in $(ls ${i}*.exe)
    do
      NAME=$(echo ${j} | cut -d/ -f2 | cut -d. -f1)
      ./${j} $1 $2 all >> ${i}${3}/${NAME}_$(date +%y_%m_%d_%H%M%S).run
    done
  done
}

remove_result(){
  find . -name '*.run' -exec rm {} \;
}


if [[ "${1}" == "del" ]]; then
 remove_result
else
 run $1 $2 $3
fi

