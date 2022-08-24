import os

class SubmissionManager():

    def __init__(self, path, config, array, partition, mem, ntasks_per_node, time, arguments='', nodes=1, cpus_per_task=1):
        self.set_names(path)
        self.config = config
        
        self.set_array(array)
        
        self.partition = partition
        self.mem = mem
        self.ntasks_per_node = ntasks_per_node
        self.time = time

        self.arguments = arguments
        
        self.nodes = nodes
        self.cpus_per_task = cpus_per_task


    def set_array(self, array):
        if len(array) == 1:
            try:
                i = int(array[0])
                self.array = f'0-{i}'
                self.array_list = list(range(i))
            except:
                self.array = array[0]
                array_split = array[0].split('%')[0].split('-')
                self.array_list = list(range(array_split[0], array_split[1]))

        else:
            self.array = ''.join([i+',' for i in array])[:-1]
            self.array_list = [int(i) for i in array]


            
                
        
    def set_names(self, path):
        self.full_path = os.path.abspath(path)
        self.directory_path = os.path.dirname(self.full_path)
        self.runscript_name = os.path.basename(self.full_path)
        self.runscript_name_no_ext, _ = os.path.splitext(self.runscript_name)
        self.main_dir, self.directory_name = os.path.split(self.directory_path)
        print(self.full_path)
        print(self.directory_path)
        print(self.runscript_name)
        print(self.runscript_name_no_ext)
        print(self.directory_name)
        print(self.main_dir)


        if self.directory_name == 'runscripts':
            self.data_dir = os.path.join(self.main_dir, 'data')
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
        else:
            self.data_dir = os.path.join(self.directory_path + 'data')
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)

        self.data_dir_array = os.path.join(self.data_dir, self.runscript_name_no_ext)

        



    def make_job_file(self, scratch=True):
        lb = '\n'
        C = self.config['DEFAULT']['COMMAND']
        s = self.config['DEFAULT']['SHEBANG'] + lb

        s += f"""{C} --jobname={self.runscript_name_no_ext}
{C} --partition={self.partition}
{C} --ntasks-per-node={self.ntasks_per_node}
{C} --cpus-per-task={self.cpus_per_task}
{C} --mem={self.mem}G
{C} --time={self.time}:00:00
{C} --array={self.array}"""
        s += self.config['DEFAULT']['SUBMIT'].format(C)

        s += lb
        s += self.config['SUB']['PRE']
        s += lb

        if scratch:
            s += self.config['SUB']['PRESCRATCH'].format(self.data_dir)
            s += lb
        
        s += self.config['SUB']['DO'].format(self.full_path, self.arguments)
        
        if scratch:
            s += self.config['SUB']['POSTSCRATCH']
            s += lb
        
        s += lb        
        s += self.config['SUB']['POST']

        return s
