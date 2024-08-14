import socket
import json
from .jsonrpc_client import JsonRPCClientBase,JsonRPCClientException

class JsonRPCClientTCP(JsonRPCClientBase):
    sock:socket.socket
    host:str
    port:int
    recv_size:int = 1024
    timeout_sec:float = 5.0
    def __init__(self,host:str,port:int) -> None:
        super().__init__()
        self.host = host
        self.port = port
        
    def settimeout(self,time_sec:float):
        self.timeout_sec = time_sec

    def _request(self,req_dict:dict, wait_res = True)->dict:
        json_str = json.dumps(req_dict) 
        json_byte = json_str.encode(encoding='utf-8')
        res_json = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self.timeout_sec)
            sock.connect((self.host, self.port))
            sock.send(json_byte)
            if wait_res:
                res_data = sock.recv(self.recv_size)
                res_json = json.loads(res_data)
        return res_json

