import os
import subprocess


class MissingRunscript(Exception):
    pass


class SubmissionManager:
    def __init__(
        self,
        path,
        config,
        array,
        partition,
        mem,
        ntasks_per_node,
        time,
        gpus,
        exec_command,
        venv,
        venv_command,
        arguments="",
        nodes=1,
        cpus_per_task=1,
        run_in_data_dir=True,
    ):
        self.run_in_data_dir = run_in_data_dir

        self.set_paths(path)
        self.config = config

        self.set_array(array)

        self.partition = partition
        self.mem = mem
        self.ntasks_per_node = ntasks_per_node
        self.time = time

        self.arguments = arguments

        self.nodes = nodes
        self.cpus_per_task = cpus_per_task
        self.gpus = gpus

        self.exec_command = exec_command
        self.venv = venv
        self.venv_command = venv_command

    def set_array(self, array):
        if len(array) == 1:
            try:
                i = int(array[0])
                self.array = f"0-{i-1}"
            except:
                self.array = array[0]

        else:
            self.array = "".join([i + "," for i in array])[:-1]

    def set_paths(self, path):
        self.full_path = os.path.abspath(path)

        if not os.path.isfile(self.full_path):
            raise MissingRunscript("No runscript file is found!")

        self.directory_path = os.path.dirname(self.full_path)
        self.runscript_name = os.path.basename(self.full_path)
        self.runscript_name_no_ext, _ = os.path.splitext(self.runscript_name)
        self.main_dir, self.directory_name = os.path.split(self.directory_path)

        if self.directory_name == "runscripts":
            self.data_dir = os.path.join(self.main_dir, "data")
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
        else:
            self.data_dir = os.path.join(self.directory_path + "/data")
            if not os.path.exists(self.data_dir) and self.run_in_data_dir:
                os.makedirs(self.data_dir)

        if self.run_in_data_dir:
            self.run_dir = os.path.join(self.data_dir, self.runscript_name_no_ext)
        else:
            self.run_dir = os.path.join(self.directory_path, self.runscript_name_no_ext)

        if not os.path.exists(self.run_dir):
            os.makedirs(self.run_dir)

        self.paths = {
            "full_path": self.full_path,
            "directory_path": self.directory_path,
            "runscript_name": self.runscript_name,
            "runscript_name_no_ext": self.runscript_name_no_ext,
            "main_dir": self.main_dir,
            "directory_name": self.directory_path,
            "data_dir": self.data_dir,
            "run_dir": self.run_dir,
        }

    def make_job_file(self, sub_type, scratch=True, dry=False):
        lb = "\n"
        C = self.config["DEFAULT"]["COMMAND"]

        s = self.config["DEFAULT"]["SHEBANG"]
        s += lb
        s += f"""{C} --job-name={self.runscript_name_no_ext}
{C} --partition={self.partition}
{C} --nodes={self.nodes}
{C} --ntasks-per-node={self.ntasks_per_node}
{C} --cpus-per-task={self.cpus_per_task}
{C} --mem={self.mem}G
{C} --time={self.time}:00:00"""

        s += lb

        if sub_type == "ARRAY":
            s += f"{C} --array={self.array}"

        s += lb
        if self.gpus != 0:
            s += f"{C} --gres=gpu:{self.gpus}"

        s += lb
        s += self.config["DEFAULT"]["SUBMIT"].format(C)

        s += lb
        s += self.config["DEFAULT"]["LOAD"].format(
            venv_command=self.venv_command, venv=self.venv
        )
        s += lb

        s += lb
        s += self.config[sub_type]["PRE"].format(**self.paths)
        s += lb

        if scratch:
            s += self.config[sub_type]["PRESCRATCH"].format(**self.paths)
            s += lb

        s += self.config[sub_type]["DO"].format(
            **self.paths, arguments=self.arguments, exec_command=self.exec_command
        )

        if scratch:
            s += self.config[sub_type]["POSTSCRATCH"].format(**self.paths)
            s += lb

        s += lb
        s += self.config[sub_type]["POST"].format(**self.paths)

        if dry:
            print(s)
        else:
            with open(os.path.join(self.run_dir, "run.job"), "w") as f:
                f.write(s)

    def submit_job(self):
        os.chdir(self.run_dir)
        sbatch_out = str(subprocess.check_output("sbatch run.job", shell=True))
        print(sbatch_out)
