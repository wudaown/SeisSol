#!/bin/bash

# $1 build or run
# $2 arch [skx,hsw]

export OMP_NUM_THREADS=40
export KMP_AFFINITY=compact,granularity=thread
for i in {4..7}
do
  if [[ "${1}" == 'run' ]]; then
  ./auto_tune.py --equations elastic --order ${i} --arch d${2} --workingDir ./${2}/order${i} --nelem 100000 --ntimesteps 1000run
  elif [[ "${1}" == 'ana' ]]; then
  ./auto_tune.py --equations elastic --order ${i} --arch d${2} --workingDir ./${2}/order${i} --nelem 100000 analyse
  else
  ./auto_tune.py --equations elastic --order ${i} --arch d${2} --workingDir ./${2}/order${i} --nelem 100000 --ncompileJobs 44 build &
  fi
done

