!/bin/bash

# Adapted from the Hamilton documentation which should be consulted for more settings and configurations
# Ref: https://www.durham.ac.uk/research/institutes-and-centres/advanced-research-computing/hamilton-supercomputer/usage/jobs/examplegpujobs/


# There is only one GPU node. 
# Resources such as the number of cores, memory and disk space cannot be configured
# Request resources (modify or remove arguments as required):
#SBATCH -p cuda                       # The GPU node/partition
#SBATCH --time=03:00:00               # time limit for job (format:  days-hours:minutes:seconds)
#SBATCH --job-name="example-job"      # or '-J "example-job"'', the job's name
#SBATCH --output=%x-%A-%a.out         # the main output file, use '%' to substitute job details
                                      # e.g. '%x-%A-%a' = '<job-name>-<job-id>-<job-array-id>' 
#SBATCH --error=%x-%A-%a.err          # the error output file, re-use the output file's name to write 
                                      # both to the same file
#SBATCH  --gres=gpu:h200_nvl:1        # number of whole GPUs 

# Load required modules
module load nvhpc

# Set OpenMP configuration as required
export OMP_NUM_THREADS=1

# Commands to be run
./cuda-executable