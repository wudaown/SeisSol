#!/bin/bash
# $1 [hard,non,'']
# $2 arch

take_result()(
  TTS=()
  # look at run file and sort to take out the best result
  for i in ${FILELIST[@]}
  do
    if [[ "${2}" == 'hardware' ]]; then
      TTS+=($(cat ${i} | grep -i 'GFLOPS (hard' | awk '{print $7}'))
    elif [[ "${2}" == 'non' ]]; then
      TTS+=($(cat ${i} | grep -i 'GFLOPS (non' | awk '{print $7}'))
    else
      TTS+=($(cat ${i} | grep -i 'time' | awk '{print $6}'))
    fi
  done

  if [[ "${2}" == 'hardware'  ]] || [[ "${2}" == 'non' ]]; then
    min=( $( printf "%s\n" "${TTS[@]}" | sort -rn ) )
  else
    min=( $( printf "%s\n" "${TTS[@]}" | sort -n ) )
  fi


  for i in ${FILELIST[@]}
  do
    if [[ "${2}" == 'hardware' ]]; then
      result=($(cat ${i} | grep -i 'GFLOPS (hard' | awk '{print $7}' | grep ${min}))
    elif [[ "${2}" == 'non' ]];then
      result=($(cat ${i} | grep -i 'GFLOPS (non' | awk '{print $7}' | grep ${min}))
    else
      result=$(cat ${i} | grep -i 'time' | awk '{print $6}' | grep ${min})
    fi
    if [[ -n ${result} ]]; then
      echo ${i}
      echo ${result}
    fi
  done
  )

for i in ./${2}/order{2..7}/results
do
  FILELIST=()
  for j in $(ls ${i}/*.run)
  do
    FILELIST+=(${j})
  done
  take_result ${FILELIST} $1
done

