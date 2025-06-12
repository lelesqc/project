#!/bin/bash

TOTAL_JOBS=10
RADIUS=0.5
PARTICLES_PER_JOB=500

# -------------------------

echo "Starting batch generation of ${TOTAL_JOBS} initial condition files..."

for (( i=1; i<=${TOTAL_JOBS}; i++ ))
do
  echo "--- Running job with SEED=${i} ---"
  
  python generate_init_cond.py \
    --radius ${RADIUS} \
    --n_particles ${PARTICLES_PER_JOB} \
    --seed ${i}
    
  echo "Job with SEED=${i} finished."
  echo ""
done

echo "Batch generation complete."