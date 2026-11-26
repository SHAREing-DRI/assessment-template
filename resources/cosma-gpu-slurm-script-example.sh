!/bin/bash

# Adapted from the COSMA documentation which should be consulted for more settings and configurations
# Ref: https://cosma.readthedocs.io/en/latest/slurm.html

# All testbeds accessbile via queues are single node
# Request resources (modify or remove arguments as required):
#SBATCH --time=03:00:00               # time limit for job (format:  days-hours:minutes:seconds)
#SBATCH --exclusive                   # reserve the entire node for this job
#SBATCH --job-name="example-job"      # or '-J "example-job"'', the job's name
#SBATCH --output=%x-%A-%a.out         # the main output file, use '%' to substitute job details
                                      # e.g. '%x-%A-%a' = '<job-name>-<job-id>-<job-array-id>' 
#SBATCH --error=%x-%A-%a.err          # the error output file, re-use the output file's name to write 
                                      # both to the same file
#SBATCH --array=[0-2]                 # launch a job array with 3 jobs for repetitions and minor
                                      # parameter changes
#SBATCH -A do016                      # project name you have access to e.g. do016 for using
                                      # resources like the GPU testbeds
#SBATCH -p hardwarelab-gpu            # partition name e.g. gracehopper for gn003 and hardwarelab-gpu
                                      # for gn004 and gn005 (from 19:00 to 08:00)
#SBATCH -w gn004                      # specific node when submitting to hardwarelab-gpu


# Load required modules
module load nvhpc

# Set OpenMP configuration as required
export OMP_NUM_THREADS=1

# Commands to be run

mpirun ./cuda-executable