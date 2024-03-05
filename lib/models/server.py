from enum import Enum
from utils.ping import pingUrls

class Server(Enum):
    
    MAIN = 'https://www.dmhy.org/'
    WAAA = 'https://dmhy.waaa.moe/'
    ONEKUMA = 'https://garden.onekuma.cn/'
    
    @classmethod
    def ping(cls):
        servers = [server.value for server in cls]
        ping_result = pingUrls(servers)
        return ping_result
    
