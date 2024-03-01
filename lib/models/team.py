import json
import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)
root_path = os.path.dirname(lib_path)
data_path = os.path.join(root_path, 'data')

sys.path.append(file_path)
sys.path.append(lib_path)

class Team:
    data: dict = None
    
    def __init__(self):
        try:
            with open(os.path.join(data_path, 'teams.json'), "r", encoding='utf-8') as f:
                self.data = json.load(f)
        except:
            raise Exception('Unable to get Names&IDs of release groups.')
    
    def __repr__(self) -> str:
        return 'Dictionary containing names and id of Release Teams.'
    
    def __getitem__(self, name):
        if name in self.data:
            return self.data[name]
        else:
            raise Exception('Team: Name not exist!')
        
    def __iter__(self):
        return iter(self.data.items())

teams = Team()

if __name__ == '__main__':
    breakpoint()