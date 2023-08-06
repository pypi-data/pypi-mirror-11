#!/bin/bash
#PBS -l walltime=4:00:00
#PBS -l nodes=1:ppn=48
#PBS -N Cu_k20
#PBS -q standby

set echo

cd $PBS_O_WORKDIR

source /group/prism/data/memosa/env-hansen_seq.sh

puq start bm_seqUQ > bm_aout
puq start v_seqUQ > v_aout
puq start t_seqUQ > t_aout
puq start u_seqUQ > u_aout
puq start s_seqUQ > s_aout
python results.py

