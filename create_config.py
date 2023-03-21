import configparser

config = configparser.ConfigParser()


# CHANGE ALL TO MATCH YOUR SETUP
NAME = 'default.ini'

# DEFAULTS
config['DEFAULT'] = {
    'SHEBANG': '#!/bin/bash',
    'COMMAND': '#SBATCH ',
    'SUBMIT':
    """{0} --no-requeue
    """,
    'array': '10',
    'partition': 'q48,q40,q36,q28',
    'mem': '12',
    'nodes': 1,
    'ntasks-per-node': '1',
    'cpus-per-task': '1',
    'time': '6',
    'LOAD':
    """
    source ~/.bashrc
    workon AGOX
    # WD=$(pwd)mj
    # agox
    # git status
    # cd $WD
    
    """
}


config['ARRAY'] = {
    'PRE':
    """
    export OMPI_MCA_orte_tmpdir_base=/scratch/$SLURM_JOB_ID

    RUNDIR={run_dir}/$SLURM_ARRAY_TASK_ID
    mkdir $RUNDIR
    cd $RUNDIR
    cp {full_path} .
    """,
    'DO':
    """
    python {runscript_name} {arguments}
    """,
    'POST':
    """
    """,
    'PRESCRATCH':
    """
    cd /scratch/$SLURM_JOB_ID
    mkdir $SLURM_ARRAY_TASK_ID
    cd $SLURM_ARRAY_TASK_ID
    cp {run_dir}/$SLURM_ARRAY_TASK_ID/* .

    while true; do
        sleep 15m
        rsync -u db*.db {run_dir}
    done &
    """,
    'POSTSCRATCH':
    """
    rsync -u db*.db {run_dir}
    rsync -u * {run_dir}/$SLURM_ARRAY_TASK_ID
    """        
}

config['SUB'] = {
    'PRE':
    """
    """,
    'DO':
    """
    mpiexec python {full_path} {arguments}
    """,
    'POST':
    """
    """,
    'PRESCRATCH':
    """
    cd /scratch/$SLURM_JOB_ID
    mkdir $SLURM_ARRAY_TASK_ID
    cd $SLURM_ARRAY_TASK_ID
    cp {full_path} .
    
    """,
    'POSTSCRATCH':
    """
    rsync * {directory_path}
    """        
}



with open(NAME, 'w') as configfile:
    config.write(configfile)

