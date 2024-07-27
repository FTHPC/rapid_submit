import os
import sys
import random
import time
import glob


#update
root_dir = "/zfs/fthpc/common/sdrbench/"
applications = ["nyx"]

if not os.path.exists("./pbs_scripts"):
    os.mkdir("pbs_scripts")


for app in applications:

    print("\n\n\nStarting application: " + app + "\n")
    for field in sorted(glob.glob( os.path.join(root_dir,app,"*") )):

        print("\t" + os.path.basename(field))
        fname = "job_"+app+"_"+ os.path.basename(field)+".pbs"
        with open(fname,"w") as outfile:

            #write pbs header
            outfile.write("#!/bin/bash\n"
                            "#PBS -l select=1:ncpus=8:mem=2gb\n"
                            "#PBS -l walltime=09:00:00\n"
                            "#PBS -N ECE_6740_HW3\n"
                            "#PBS -j oe\n\n")

            #load modules
            outfile.write("module load gcc\n"
                #"module load mpich\n"
                "module list\n\n")

            #set up spack and load libpressio if needed
            outfile.write("source ~/spack/share/spack/setup-env.sh\n"
                            "spack load libpressio\n\n")


            #go to the location where the pbs was submitted
            outfile.write("cd $PBS_O_WORKDIR \n\n")


            #issue the cmds that you need to run your workflow
            outfile.write("./a.out \n")

        #launch the job and cleanup
        os.system("qsub " + fname)
        os.rename(fname, os.path.join("./pbs_scripts", fname))
