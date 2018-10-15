#!/usr/bin/env python

from __future__ import print_function

from argparse import ArgumentParser as AP
from argparse import ArgumentDefaultsHelpFormatter as AHF

import os
import sys


slurm_txt = '''
#!/bin/bash
#
#------------------Scheduler Options--------------------
#SBATCH -J {jobname:s}         # Job name
#SBATCH -n {ntasks:d}          # Total number of tasks
#SBATCH -p vis                 # Queue name
#SBATCH -o {jobname:s}.o%j     # Name of stdout output file
#SBATCH -t {runtime:s}         # Run time (hh:mm:ss)
#SBATCH -A Hobby-Eberly-Telesco
#------------------------------------------------------

#------------------General Options---------------------
module load pylauncher
module unload xalt

cd {workdir:s}
echo " WORKING DIR: {workdir:s}/"

{launcherpath:s}/vdrprunner.py -c {ncores:d} {runfile}

echo " "
echo " Parameteric VDRP Job Complete"
echo " "
'''


def main(args):

    commands = []

    with open(args.cmdfile, 'r') as f:
        line = f.readline()
        while line != '':
            cmd = line.strip()
            # Skip empty lines and comments
            if cmd != '' and not cmd.startswith('#'):
                commands.append(cmd)
            line = f.readline()

    fname, fext = os.path.splitext(args.cmdfile)

    nc = len(commands)

    ncores = int(args.nodes * 20 / args.cores)
    nfiles = nc / args.jobs / ncores / args.tasks + 1

    print(ncores)
    print('Found %d commands' % nc)
    print('Splitting them onto %d nodes' % args.nodes)
    print('Running %d tasks per python instance' % args.tasks)
    print('Using %d cores per instance' % args.cores)
    print('Scheduling %d jobs per available core' % args.jobs)
    print('Scheduling %d jobs per node' % (nc/ncores*args.nodes+1))
    print('Resulting in %d jobfiles with up to %d instances'
          % (nfiles, args.jobs*ncores))

    file_c = 1
    cmd_c = 1

    while file_c <= nfiles:

        if not len(commands):
            raise Exception('Found fewer commands than expected!')

        cmd_file = '%s_%d%s' % (fname, file_c, fext)
        create_job_file(cmd_file, commands, ncores, args)

        file_c += 1


def create_job_file(fname, commands, ncores, args):

    ntasks = args.tasks
    njobs = args.jobs*ncores*ntasks
    runtime = args.runtime

    print(njobs)

    job_c = 0

    fn, _ = os.path.splitext(fname)

    with open(fname, 'w') as fout:

        subname = '%s.params' % (fn)
        min_t = 0

        with open(subname, 'w') as jf:

            while job_c < njobs:
                if not len(commands):
                    break
                if ntasks == 1:
                    # Only one task per instance, no need to run in multi mode
                    fout.write('%s\n' % commands.pop(0))
                else:
                    cmd = commands.pop(0)
                    jf.write('%s\n' % cmd.split(' ', 1)[1])

                    print(job_c+1, njobs)
                    if (job_c+1) % ntasks == 0 or job_c+2 == njobs:
                        taskname = cmd.split()[0]
                        fout.write('%s -M %s[%d:%d]\n' % (taskname, subname,
                                                          min_t, job_c))
                        min_t = job_c+1
                job_c += 1

    # Now write the corresponding slurm file

    launcherdir = os.path.dirname(os.path.abspath(__file__))
    with open(fn + '.slurm', 'w') as sf:
        sf.write(slurm_txt.format(jobname=fn, ntasks=njobs, runtime=runtime,
                                  workdir='./', ncores=args.cores,
                                  launcherpath=launcherdir,
                                  runfile=fname))


def parse_args(argv):
    """
    Command line parser

    Parameters
    ----------
    argv : list of strings
        list to parsed

    Returns
    -------
    namespace:
         Parsed arguments
    """

    p = AP(formatter_class=AHF)

    p.add_argument('--jobs', '-j', type=int, default=100,
                   help='Maximum number of job to run per core')
    p.add_argument('--nodes', '-n', type=int, default=1,
                   help='Number of nodes to use per job')
    p.add_argument('--tasks', '-t', type=int, default=1,
                   help='Number of tasks per python process')
    p.add_argument('--cores', '-c', type=int, default=1,
                   help='Number of cores for multiprocessing')
    p.add_argument('--runtime', '-r', type=str, default='00:30:00',
                   help='Expected runtime of slurm job')
    p.add_argument('cmdfile', type=str, help="""Input commands file""")

    return p.parse_args(args=argv)


if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    main(args)
