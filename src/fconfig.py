class FileConfig:

    def __init__(self, path):

        self.data = {}

        last_key = None

        with open(path) as f:
            for line in f:
                line = line.strip()
                if len(line) == 0:
                    continue

                if '=' in line:
                    pos = line.index('=')
                    key = line[:pos].strip().upper()
                    val = line[pos+1:].strip()
                    self.data[key] = [val, None]
                    last_key = key
                else:
                    if self.data[last_key][1] == None:
                        self.data[last_key][1] = ''
                    else:
                        self.data[last_key][1] += '\n'
                    self.data[last_key][1] += line

    def get_val(self, key):
        return self.data[key.upper()][0]

    def get_desc(self, key):
        return self.data[key.upper()][1]
