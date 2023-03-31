import argparse

from read_config import read
from submission_manager import SubmissionManager


def array():
    parser = argparse.ArgumentParser()
    parser.add_argument("runscript", type=str)
    # parser.add_argument("args", nargs="?", default="-i $SLURM_ARRAY_TASK_ID", type=str)
    parser.add_argument(
        "-i",
        "--array",
        nargs="+",
        help="The array job array to start. Either as int, slurm input str or several ints",
    )

    parser.add_argument("-p", "--partition", type=str)
    parser.add_argument("-m", "--mem", type=int)
    parser.add_argument("-n", "--ntasks-per-node", dest="ntasks_per_node", type=int)
    parser.add_argument("-t", "--time", type=int, help="Time in hours")
    parser.add_argument("-g", "--gpus", type=int, help="Number of GPUS")

    parser.add_argument(
        "-A",
        "--args",
        type=str,
        default="-i $SLURM_ARRAY_TASK_ID",
        help="Arguments for runscript. Default: -i $SLURM_ARRAY_TASK_ID. Add space before -",
    )

    parser.add_argument(
        "-V", "--venv", type=str, help="Name or path to virtual environment"
    )
    parser.add_argument(
        "--venv-command",
        type=str,
        dest="venv_command",
        help="Command to activate virtual environment",
    )

    parser.add_argument(
        "-E",
        "--exec-command",
        dest="exec_command",
        type=str,
        help="Program execution command",
    )

    parser.add_argument("-M", "--submit-on-main", dest="scratch", action="store_false")
    parser.add_argument("-D", "--dry-run", dest="dry", action="store_true")
    parser.add_argument("-C", "--config-file", dest="config_file", type=str)
    parser.add_argument(
        "--data-dir",
        dest="data_dir",
        action="store_false",
        help="Whether to run in seperate data directory",
    )

    args = parser.parse_args()

    config = read(args.config_file)

    if args.array is None:
        args.array = [config["DEFAULT"]["array"]]

    if args.partition is None:
        args.partition = config["DEFAULT"]["partition"]

    if args.mem is None:
        args.mem = config["DEFAULT"]["mem"]

    if args.ntasks_per_node is None:
        args.ntasks_per_node = config["DEFAULT"]["ntasks-per-node"]

    if args.time is None:
        args.time = config["DEFAULT"]["time"]

    if args.gpus is None:
        args.gpus = config["DEFAULT"].get("gpus", 0)

    if args.venv is None:
        args.venv = config["DEFAULT"].get("venv", "")

    if args.venv_command is None:
        args.venv_command = config["DEFAULT"].get("venv_command", "")

    if args.exec_command is None:
        args.exec_command = config["DEFAULT"].get("exec_command", "")

    sm = SubmissionManager(
        path=args.runscript,
        config=config,
        array=args.array,
        partition=args.partition,
        mem=args.mem,
        ntasks_per_node=args.ntasks_per_node,
        time=args.time,
        gpus=args.gpus,
        exec_command=args.exec_command,
        venv=args.venv,
        venv_command=args.venv_command,
        arguments=args.args,
        run_in_data_dir=args.data_dir,
    )

    sm.make_job_file("ARRAY", scratch=args.scratch, dry=args.dry)
    if not args.dry:
        sm.submit_job()
