import socket
import logging
from .jsonrpc_server import *

logger = logging.getLogger(__name__)


class JsonRPCServerTCP (JsonRPCServerBase):
    host:str
    port:int
    packet_size:int
    _run_flag:bool
    def __init__(self, host:str,port:int) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.packet_size = 1024
    
    def stop_request(self):
        self._run_flag = False

    def run_forever(self):
        self._run_flag = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            while self._run_flag:
                recv_sock ,cli_addr= sock.accept()
                logger.debug('addrress:%s',cli_addr)
                res_json = None
                try:
                    recv_data = recv_sock.recv(self.packet_size)
                    logger.debug('data:%s',recv_data)
                    res_json = self._request_received(recv_data)
                except JsonRPCResponseException  as ex:
                    res_json = {
                        'jsonrpc':'2.0',
                        'id':None,
                        'error': ex.toJsonDict()
                    }
                except KeyboardInterrupt:
                    self._run_flag = False
                except Exception as ex:
                    logger.exception("method run error")
                    res_json = {
                        'jsonrpc':'2.0',
                        'id':None,
                        'error': {
                            "code":ERROR_CODE_INTERNAL_ERROR,
                            "message": str(ex)
                        }
                    }

                if res_json != None:
                    recv_sock.send(json.dumps(res_json).encode(encoding='utf-8'))
                recv_sock.close()

        self._run_flag = False
