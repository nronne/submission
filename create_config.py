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
    {0} --nodes=1
    {0} --cpus-per-task=1
    """,
    'array': '10',
    'partition': 'q48,q40,q36,q28',
    'mem': '12',
    'ntasks-per-node': '1',
    'time': '6',
    'LOAD':
    """
    source ~/.basrc
    workon AGOX
    WD=$(pwd)
    agox
    git status
    cd $WD
    
    """
}


config['ARRAY'] = {
    'PRE':
    """
    RUNDIR={0}/$SLURM_ARRAY_TASK_ID
    mkdir $RUNDIR
    cd $RUNDIR
    cp {1} .
    """,
    'DO':
    """
    python {0} {1}
    """,
    'POST':
    """
    """,
    'PRESCRATCH':
    """
    cd /scratch/$SLURM_JOB_ID
    mkdir $SLURM_ARRAY_TASK_ID
    cd $SLURM_ARRAY_TASK_ID
    cp {0}/* .

    while true; do
        sleep 60m
        rsync -u * {0}/$SLURM_ARRAY_TASK_ID
    done &
    """,
    'POSTSCRATCH':
    """
    rsync -u * {0}/$SLURM_ARRAY_TASK_ID
    """        
}

config['SUB'] = {
    'PRE':
    """
    source ~/.basrc
    workon AGOX
    WD=$(pwd)
    agox
    git status
    cd $WD
    
    """,
    'DO':
    """
    python {0} {1}
    """,
    'POST':
    """
    """,
    'PRESCRATCH':
    """
    cd /scratch/$SLURM_JOB_ID
    mkdir $SLURM_ARRAY_TASK_ID
    cd $SLURM_ARRAY_TASK_ID
    
    """,
    'POSTSCRATCH':
    """
    
    """        
}



with open(NAME, 'w') as configfile:
    config.write(configfile)

