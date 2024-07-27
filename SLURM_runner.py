import os
import sys
import random
import time
import glob


#update
root_dir = "/project/jonccal/common/sdrbench/"
applications = ["nyx"]

if not os.path.exists("./slurm_scripts"):
    os.mkdir("slurm_scripts")


for app in applications:

    print("\n\n\nStarting application: " + app + "\n")
    for field in sorted(glob.glob( os.path.join(root_dir,app,"*") )):

        print("\t" + os.path.basename(field))
        fname = "job_"+app+"_"+ os.path.basename(field)+".slurm"
        with open(fname,"w") as outfile:

            #write slurm header
            outfile.write("#!/bin/bash\n"
                            "#SBATCH --nodes 1\n"
                            "#SBATCH --tasks-per-node 8\n"
                            "#SBATCH --mem 8gb\n"
                            "#SBATCH --time 09:00:00\n"
                            "#SBATCH --job-name my-job-name\n"
                            #"#SBATCH -j oe\n"
                            "\n")

            #load modules
            outfile.write("module purge\n"
                "module load gcc\n"
                #"module load mpich\n"
                "module list\n\n")

            #set up spack and load libpressio if needed
            outfile.write("source ~/spack/share/spack/setup-env.sh\n"
                            "spack env activate cprss\n\n")


            #go to the location where the slurm was submitted
            outfile.write("cd $SLURM_SUBMIT_DIR \n\n")


            #issue the cmds that you need to run your workflow
            outfile.write("./a.out \n")

        #launch the job and cleanup
        os.system("sbatch " + fname)
        os.rename(fname, os.path.join("./slurm_scripts", fname))
