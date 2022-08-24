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
    'time': '6',
}

# EVERYTHING THAT IS DONE FOR SUBMISSION
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

