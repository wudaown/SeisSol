#!/bin/bash
# $1 folder
# $2 [hard,non]
get_result(){
    # count number of cores
  coreNum=$(echo ${1} | cut -d_ -f2 | sed -e 's/.\///g')
  if [[ ! $coreNum =~ ^-?[0-9]+$ ]]; then
    coreNum=$(echo ${1} | cut -d_ -f3 | sed -e 's/.\///g')
  fi
    # get get DR, WP and Wall time
  if [[ "${2}" == 'hard' ]]; then
    WP_GFLOP=$(egrep 'WP calculated HW' $1 | awk '{print $9}')
    DR_GFLOP=$(egrep 'Total calculated HW' $1 | awk '{print $9}')
  else
    WP_GFLOP=$(egrep 'WP calculated NZ' $1 | awk '{print $9}')
    DR_GFLOP=$(egrep 'Total calculated NZ' $1 | awk '{print $9}')
  fi
  WT=$(egrep 'Wall time:' $1 | awk '{print $8}')
    # endtime based on endtime in parameter file
  ENDTIME=60.5680253545
    # regex to match sic expression
  for i in ${WP_GFLOP}
  do
    SIS=$(echo ${i} | cut -d+ -f1)
    if [ -z ${SIS} ]; then
        GFLOP=$(echo "$i /  $WT" | bc -l)
    else
        CONVERT=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<< "${i}")
        GFLOP=$(echo "$CONVERT /  $WT" | bc -l)
    fi
    core=$(echo "$GFLOP / ${coreNum}" | bc -l)
    echo WP Per Core $core
  done
  
 for i in ${DR_GFLOP}
  do
    SIS=$(echo ${i} | cut -d+ -f1)
    if [ -z ${SIS} ]; then
        GFLOP=$(echo "$i /  $WT" | bc -l)
    else
        CONVERT=$(sed -E 's/([+-]?[0-9.]+)[eE]\+?(-?)([0-9]+)/(\1*10^\2\3)/g' <<< "${i}")
        GFLOP=$(echo "$CONVERT /  $WT" | bc -l)
    fi
    core=$(echo "$GFLOP / ${coreNum}" | bc -l)
    echo TOTAL Per Core $core
  done
  
  ET=$(echo "$WT * $ENDTIME / 3600" | bc -l)
  echo Expect hour $ET
  
  #echo $WT
}

for i in $(ls ./${1}/*.run)
do
  get_result $i $2
done
