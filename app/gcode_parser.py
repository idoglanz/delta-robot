import re
import numpy as np

def Convert(string):
    li = list(string.split("\n"))
    return li

# extract letter-digit pairs
g_pattern = re.compile('([A-Z])([-+]?[0-9.]+)')
# white spaces and comments start with ';' and in '()'
clean_pattern = re.compile('\s+|\(.*?\)|;.*')


class GcodeParser:
    def __init__(self, filename):
        with open(filename, 'r') as f_gcode:
            data = f_gcode.read()
            self.data_list = Convert(data)
        self.relevant_commands = ['G', 'X', 'Y', 'Z']
        self.command_history = []
        self.last_command = {}
        self._command = {}
        self.get = self.get_command()

    def get_command(self):
        for line in self.data_list:
            line = line.upper()
            line = re.sub(clean_pattern, '', line)
            if len(line) == 0: 
                continue
            if line[0] == ';':
                continue            
            m = g_pattern.findall(line)
            self.command_history.append(m)
            
            if m[0][0] in ['G', 'X', 'Y', 'Z']:
                for commands in m:
                    self.last_command[commands[0]] = commands[1]

                self._command['command'] = 'G'+self.last_command['G']
                if self.last_command.get('X'):
                    self._command['value'] = (float(self.last_command['X']), float(self.last_command['Y']), float(self.last_command['Z']))

                    yield self._command


if __name__ == "__main__":
    loader = GcodeParser('./gcode/D_leaf_test.gcode')
    data = []
    for command in loader.get_command():
        data.append(command['value'])
        print(command)
    data_array = np.array(data)
    print(np.max(data_array,axis=0))
    print(np.min(data_array,axis=0))
    print(np.mean(data_array,axis=0))
    
