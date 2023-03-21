import argparse
from read_config import read
from submission_manager import SubmissionManager

def array():
    parser = argparse.ArgumentParser()
    parser.add_argument('runscript', type=str)
    parser.add_argument('args', nargs='?', default='-i $SLURM_ARRAY_TASK_ID', type=str)
    parser.add_argument('-i', '--array', nargs='+',
                        help="The array job array to start. Either as int, slurm input str or several ints")
    
    parser.add_argument('-p', '--partition', type=str)
    parser.add_argument('-m', '--mem', type=int)
    parser.add_argument('-n', '--ntasks-per-node', dest='ntasks_per_node', type=int)
    parser.add_argument('-t', '--time', type=int, help='Time in hours')
    parser.add_argument('-g', '--gpus', type=int, help='Number of GPUS')
    # parser.add_argument('-a', '--args', type=str, default='-i $SLURM_ARRAY_TASK_ID', help='arguments for runscript')
    
    parser.add_argument('--submit-on-main', dest='scratch', action='store_false')
    parser.add_argument('--dry-run', dest='dry', action='store_true')
    parser.add_argument('--config-file', dest='config_file', type=str)
    args = parser.parse_args()

    
    config = read(args.config_file)
    
    
    if args.array is None:
        args.array = [config['DEFAULT']['array']]

    if args.partition is None:
        args.partition = config['DEFAULT']['partition']

    if args.mem is None:
        args.mem = config['DEFAULT']['mem']                

    if args.ntasks_per_node is None:
        args.ntasks_per_node = config['DEFAULT']['ntasks-per-node']

    if args.time is None:
        args.time = config['DEFAULT']['time']        

    if args.gpus is None:
        args.gpus = config['DEFAULT'].get('gpus', 0)

    sm = SubmissionManager(args.runscript, config, args.array, args.partition, args.mem, args.ntasks_per_node,
                           args.time, args.gpus, arguments=args.args)
    
    
    sm.make_job_file('ARRAY', scratch=args.scratch, dry=args.dry)
    if not args.dry:
        sm.submit_job()
    

    
def sub():
    parser = argparse.ArgumentParser()
    parser.add_argument('runscript', type=str)
    parser.add_argument('args', nargs='?', default='-i $SLURM_ARRAY_TASK_ID', type=str)
    
    parser.add_argument('-p', '--partition', type=str)
    parser.add_argument('-m', '--mem', type=int)
    parser.add_argument('-n', '--ntasks-per-node', dest='ntasks_per_node', type=int)
    parser.add_argument('-t', '--time', type=int, help='Time in hours')
    parser.add_argument('-g', '--gpus', type=int, help='Number of GPUS')    
    # parser.add_argument('-a', '--args', type=str, default='', help='arguments for runscript')
    
    parser.add_argument('--submit-on-scratch', dest='scratch', action='store_true')
    parser.add_argument('--dry-run', dest='dry', action='store_true')
    parser.add_argument('--no-data-dir', dest='run_in_data_dir', action='store_false')
    parser.add_argument('--config-file', dest='config_file', type=str)
    args = parser.parse_args()

    
    config = read(args.config_file)
    
    
    if args.partition is None:
        args.partition = config['DEFAULT']['partition']

    if args.mem is None:
        args.mem = config['DEFAULT']['mem']                

    if args.ntasks_per_node is None:
        args.ntasks_per_node = config['DEFAULT']['ntasks-per-node']

    if args.time is None:
        args.time = config['DEFAULT']['time']

    if args.gpus is None:
        args.gpus = config['DEFAULT'].get('gpus', 0)

    

    sm = SubmissionManager(args.runscript, config, ['0'], args.partition, args.mem, args.ntasks_per_node, args.time, args.gpus,
                           arguments=args.args, nodes=config['DEFAULT']['nodes'],
                           cpus_per_task=config['DEFAULT']['cpus-per-task'], run_in_data_dir=args.run_in_data_dir)
    
    
    sm.make_job_file('SUB', scratch=args.scratch, dry=args.dry)
    if not args.dry:
        sm.submit_job()

