import socket
import json
from .jsonrpc_client import JsonRPCClientBase,JsonRPCClientException

class JsonRPCClientUDP(JsonRPCClientBase):
    sock:socket.socket
    host:str
    port:int
    recv_size:int = 1024
    def __init__(self,host:str,port:int) -> None:
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
    
    def __del__(self):
        self.sock.close()
    
    def settimeout(self,time_sec:float):
        self.sock.settimeout(time_sec)

    def _request(self,req_dict:dict):
        json_str = json.dumps(req_dict) 
        json_byte = json_str.encode(encoding='utf-8')
        self.sock.sendto(json_byte,(self.host, self.port))

    def _wait_response(self):
        timeout=False
        try:
            res,(host,port)=self.sock.recvfrom(self.recv_size)
        except socket.timeout:
            timeout = True
        if timeout:
            raise JsonRPCClientException('Timeout')

        if port != self.port:
            raise JsonRPCClientException('port not match')
        return json.loads(res)
