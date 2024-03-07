import json
import sys
import os

file_path = os.path.abspath( os.path.dirname(__file__) )
lib_path = os.path.dirname(file_path)
root_path = os.path.dirname(lib_path)

sys.path.append(file_path)
sys.path.append(lib_path)

from dataclasses import dataclass, asdict

from server import Server

@dataclass
class Settings:
    server:str = Server.MAIN.value
    
    def __post_init__(self):
        with open(r'./data/settings.json', 'r', encoding='utf-8') as f:
            data:dict = json.load(f)
        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])
        
    
    def save(self):
        with open(r'./data/settings.json', 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent = 4)
            
    def __repr__(self) -> str:
        return 'Dictionary containing settings.'

        

        
