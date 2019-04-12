#!/bin/bash

MAKE=${MAKE:-make}

#SEISSOL_KERNELS_CONFIG=sparse_dense   #define this if you want to generate a sparse-dense tuned backend
SEISSOL_KERNELS_CONFIG=all_dense   #define this if you want to generate an all-dense backend
#SEISSOL_KERNELS_CONFIG=all_sparse   #define this if you want to generate an all-sparse backend
MEMKIND_ROOT_DIR=/swtools/memkind/latest

# some defaults
SIMARCH=skx_dp
KERNEL_FILE=dgemm_skx.cpp
KERNEL=all
CORES=40
TIMESTEPS=100
ORDER=5
ARCH_FLAGS="-mavx -xCORE_AVX512 -DALIGNMENT=64 -DDSKX -fopenmp"
SEISSOL_PROXY_ROOT=`pwd`
CONF="default"
GENCONF="default"
GENCODE="1"
PREFETCH="0"
DERS="0"
MEMKIND="0"

# some relative pathes
LIBXSMM_ROOT=${SEISSOL_PROXY_ROOT}/../../
SEISSOL_KERNELS_ROOT=${SEISSOL_PROXY_ROOT}/seissol_kernels
#SEISSOL_KERNELS_ROOT=/nfs_home/aheineck/Projects/SeisSol_workspace/seissol_kernels

# test for seissol kernels and clone from git hub if needed.
if [ ! -d "${SEISSOL_KERNELS_ROOT}" ]; then
  git clone --recursive https://github.com/TUM-I5/seissol_kernels.git
fi

while getopts a:k:c:n:t:o:p:g:s:d:m: opts; do
   case ${opts} in
      a) SIMARCH=${OPTARG} ;;
      k) KERNEL=${OPTARG} ;;
      c) CORES=${OPTARG} ;;
      n) NELEM=${OPTARG} ;;
      t) TIMESTEPS=${OPTARG} ;;
      o) ORDER=${OPTARG} ;;
      s) CONF=${OPTARG} ;;
      p) PREFETCH=${OPTARG} ;;
      g) GENCODE=${OPTARG} ;;
      d) DERS=${OPTARG} ;;
      m) MEMKIND=${OPTARG} ;;
   esac
done

case ${SIMARCH} in
  wsm_dp) ARCH_FLAGS="-msse3 -DALIGNMENT=16 -DDWSM -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=dgemm_wsm.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_dwsm.cpp ;;
  snb_dp) ARCH_FLAGS="-mavx -DALIGNMENT=32 -DDSNB -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=dgemm_snb.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_dsnb.cpp ;;
  hsw_dp) ARCH_FLAGS="-xCORE_AVX2 -fma -DALIGNMENT=32 -DDHSW -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=dgemm_hsw.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_dhsw.cpp ;;
  skx_dp) ARCH_FLAGS="-xCORE_AVX512 -fma -DALIGNMENT=64 -DDSKX -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=dgemm_skx.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_dskx.cpp ;;
  knc_dp) ARCH_FLAGS="-mmic -DALIGNMENT=64 -DDKNC -qopt-threads-per-core=4 -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=dgemm_knc.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_dknc.cpp ;;
  wsm_sp) ARCH_FLAGS="-msse3 -DALIGNMENT=16 -DSWSM -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=sgemm_wsm.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_swsm.cpp ;;
  snb_sp) ARCH_FLAGS="-mavx -DALIGNMENT=32 -DSSNB -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=sgemm_snb.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_ssnb.cpp ;;
  hsw_sp) ARCH_FLAGS="-xCORE_AVX2 -fma -DALIGNMENT=32 -DSHSW -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=sgemm_hsw.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_shsw.cpp ;;
  skx_sp) ARCH_FLAGS="-xCORE_AVX512 -fma -DALIGNMENT=64 -DSSKX -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=sgemm_skx.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_sskx.cpp ;;
  knc_sp) ARCH_FLAGS="-mmic -DALIGNMENT=64 -DSKNC -qopt-threads-per-core=4 -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=sgemm_knc.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_sknc.cpp ;;
  knl_dp) ARCH_FLAGS="-xMIC-AVX512 -fma -DALIGNMENT=64 -DDKNL -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=dgemm_knl.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_dknl.cpp ;;
  knl_sp) ARCH_FLAGS="-xMIC-AVX512 -fma -DALIGNMENT=64 -SDKNL -qopenmp -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=sgemm_knl.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_sknl.cpp ;;
  noarch_dp) ARCH_FLAGS="-DALIGNMENT=16 -DDNOARCH -qopenmp -mkl=sequential -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=dgemm_noarch.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_dnoarch.cpp ;;
  noarch_sp) ARCH_FLAGS="-DALIGNMENT=16 -DDNOARCH -qopenmp -mkl=sequential -static-libgcc -static-libstdc++ -static-intel"; MATMUL_KERNEL_DENSE_FILE=sgemm_noarch.cpp; MATMUL_KERNEL_SPARSE_FILE=sparse_snoarch.cpp ;;
  *) echo "Unsupported architecture -> Exit Launcher! Supported architectures are: wsm_dp, snb_dp, hsw_dp,skx_dp, skx_sp, knc_dp, wsm_sp, snb_sp, hsw_sp, knc_sp, knl_dp, knl_sp, noarch_dp, noarch_sp!"; exit ;;
esac

case ${KERNEL} in
  all) ;;
  local) ;;
  neigh) ;;
  ader) ;;
  vol) ;;
  bndlocal) ;;
  *) echo "Unsupported Kernel -> Exit Launcher! Supported kernels are: all, local, neigh, ader, vol, bndlocal!"; exit ;;
esac

case ${ORDER} in
  7) ;;
  6) ;;
  5) ;;
  4) ;;
  3) ;;
  2) ;;
  *) echo "Unsupported Order -> Exit Launcher! Supported orders are: 2,3,4,5,6,7!"; exit ;;
esac

case ${GENCODE} in
  0) ;;
  1) ;;
  *) echo "Unsupported Generation switch -> Exit Launcher! Supported switches are: 0(off) 1(on)!"; exit ;;
esac

if [ "${KERNEL}" == 'local' ]; then
  GENCONF="local_"${CONF}
fi
if [ "${KERNEL}" == 'ader' ]; then
  GENCONF="local_"${CONF}
fi
if [ "${KERNEL}" == 'vol' ]; then
  GENCONF="local_"${CONF}
fi
if [ "${KERNEL}" == 'bndlocal' ]; then
  GENCONF="local_"${CONF}
fi
if [ "${KERNEL}" == 'neigh' ]; then
  GENCONF="neighboring_"${CONF}
fi

set -x

if [ "${GENCODE}" == '1' ]; then
  # build libxsmm generator backend
  cd ${LIBXSMM_ROOT}
#  ${MAKE} realclean
  ${MAKE} generator

  cd ${SEISSOL_KERNELS_ROOT}/preprocessing
  rm -rf generated_code/*
  if [ "${CONF}" == 'default' ]; then
    python scripts/offlineAssembly.py --generateMatrixKernels ./matrices ./${SEISSOL_KERNELS_CONFIG} ${LIBXSMM_ROOT}bin/libxsmm_gemm_generator ./generated_code > /dev/null
  else
    python scripts/offlineAssembly.py --generateMatrixKernels ./matrices ./../auto_tuning/sparse_dense/${GENCONF} ${LIBXSMM}bin/libxsmm_gemm_generator ./generated_code > /dev/null
  fi

  cd ${SEISSOL_PROXY_ROOT}
fi

# added prefetch flag
if [ "${PREFETCH}" == '1' ]; then
  ARCH_FLAGS="${ARCH_FLAGS} -DENABLE_MATRIX_PREFETCH"
fi
if [ "${PREFETCH}" == '2' ]; then
  ARCH_FLAGS="${ARCH_FLAGS} -DENABLE_MATRIX_PREFETCH -DENABLE_STREAM_MATRIX_PREFETCH"
fi

# added use derivations flag
if [ "${DERS}" == '1' ]; then
  ARCH_FLAGS="${ARCH_FLAGS} -D__USE_DERS"
fi

# check for memkind
if [ "${MEMKIND}" == '1' ]; then
  ARCH_FLAGS="${ARCH_FLAGS} -DUSE_MEMKIND -I${MEMKIND_ROOT_DIR}/include -L${MEMKIND_ROOT_DIR}/lib -lmemkind"
fi


# edit to run a loop
build(){
for i in {4..7}
do
	mkdir order${i}
	FILENAME=driver_${SIMARCH}_${i}_${PREFETCH}_${SEISSOL_KERNELS_CONFIG}.exe
	rm -rf driver_${SIMARCH}_${i}.exe
	icpc -O3 -ip -ipo -DNDEBUG ${ARCH_FLAGS} -DCONVERGENCE_ORDER=${i} -DNUMBER_OF_QUANTITIES=9 -I${SEISSOL_KERNELS_ROOT}/src -I${SEISSOL_KERNELS_ROOT}/preprocessing/generated_code ${SEISSOL_KERNELS_ROOT}/src/Volume.cpp ${SEISSOL_KERNELS_ROOT}/src/Time.cpp ${SEISSOL_KERNELS_ROOT}/src/Boundary.cpp ${SEISSOL_KERNELS_ROOT}/preprocessing/generated_code/matrix_kernels/${MATMUL_KERNEL_DENSE_FILE} ${SEISSOL_KERNELS_ROOT}/preprocessing/generated_code/matrix_kernels/${MATMUL_KERNEL_SPARSE_FILE} proxy_seissol.cpp -o ${FILENAME}
	mv ${FILENAME} order${i}
done
}
build
