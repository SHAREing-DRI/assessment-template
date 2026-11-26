!/bin/bash

# Adapted from the Hamilton documentation which should be consulted for more settings and configurations
# Ref: https://www.durham.ac.uk/research/institutes-and-centres/advanced-research-computing/hamilton-supercomputer/usage/jobs/examplecpujobs/

# Request resources (modify or remove arguments as required):
#SBATCH --ntasks-per-node=8           # or '-n 8', number of MPI ranks (8 per node)
#SBATCH --cpus-per-task=16            # or '-c 16', number of cores/threads per rank 
                                      # (16 cores/threads per rank)
#SBATCH --mem=64G                     # memory required per node, in units M, G or T
#SBATCH --time=03:00:00               # time limit for job (format:  days-hours:minutes:seconds)
#SBATCH --nodes=1                     # or '-N 1', number of compute nodes allocated to this job  
#SBATCH --exclusive                   # reserve the entire node for this job
#SBATCH --job-name="example-job"      # or '-J "example-job"'', the job's name
#SBATCH --output=%x-%A-%a.out         # the main output file, use '%' to substitute job details
                                      # e.g. '%x-%A-%a' = '<job-name>-<job-id>-<job-array-id>' 
#SBATCH --error=%x-%A-%a.err          # the error output file, re-use the output file's name to write 
                                      # both to the same file
#SBATCH --array=[0-2]                 # launch a job array with 3 jobs for repetitions and minor
                                      # parameter changes 
#SBATCH --distribution=block:block    # distribute ranks in logical order 
                                      # eg. Rank 0 on CPU 0 on Node 0, Rank 1 on CPU 1 on Node 0,
                                      # ..., Rank 128 on CPU 1 on Node 1 etc. Other options are
                                      # block:cyclic, cyclic:block and cylic:cylic

# Use the 'test' queue for quick (max 10 min) jobs especially when testing settings
# Smaller jobs can run in the 'shared' queue.  
# Larger jobs that will occupy one or more whole nodes should use the 'multi' queue.
#SBATCH -p multi


# Load required modules
module load gcc openmpi

# Set OpenMP configuration as required (if not using likwid)
# e.g. set number of OpenMP threads to the number of cores/threads per rank
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_PLACES=cores
export OMP_PROC_BIND=close

# Commands to be run.  
# Note that mpirun will automatically launch the number of ranks specified above 

mpirun ./executable