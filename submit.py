import argparse
from read_config import read
from submission_manager import SubmissionManager

def array():
    parser = argparse.ArgumentParser()
    parser.add_argument('runscript', type=str)
    parser.add_argument('-i', '--array', nargs='+',
                        help="The array job array to start. Either as int, slurm input str or several ints")
    
    parser.add_argument('-p', '--partition', type=str)
    parser.add_argument('-m', '--mem', type=int)
    parser.add_argument('-n', '--ntasks-per-node', dest='ntasks_per_node', type=int)
    parser.add_argument('-t', '--time', type=int, help='Time in hours')
    parser.add_argument('-a', '--args', type=str, default='-i $SLURM_ARRAY_TASK_ID', help='arguments for runscript')
    
    parser.add_argument('--submit-on-main', dest='scratch', action='store_false')
    parser.add_argument('--config-file', dest='config_file', type=str)
    args = parser.parse_args()

    
    config = read(args.config_file)

    if args.array is None:
        args.array = config['DEFAULT']['array']

    if args.partition is None:
        args.partition = config['DEFAULT']['partition']

    if args.mem is None:
        args.mem = config['DEFAULT']['mem']                

    if args.ntasks_per_node is None:
        args.ntasks_per_node = config['DEFAULT']['ntasks-per-node']

    if args.time is None:
        args.time = config['DEFAULT']['time']        

    

    sm = SubmissionManager(args.runscript, config, args.array, args.partition, args.mem, args.ntasks_per_node, args.time,
                           arguments=args.args)
    
    
    s = sm.make_job_file(scratch=args.scratch)
    print(s)

    
def sub():
    print('not implementet yer')
