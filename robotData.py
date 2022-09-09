import json

class robotData:
    def __init__(self):
        pass
    
    def read(self, filename):
        try:
            with open(filename, 'r') as fromFile:
                data = json.load(fromFile)
                return data
        except OSError:
            print("read {} error".format(filename))
            return None
        
    def write(self, filename, data):
        try:
            with open(filename, 'w') as out_file:
                out_file.write(json.dumps(data, indent=4))
        except OSError:
            print("write {} error".format(filename))
            return None
        
    
    