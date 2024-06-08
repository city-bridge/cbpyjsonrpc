
class JsonRPCClientException(Exception):
    pass

class JsonRPCClientBase:
    id_increment:int

    def __init__(self) -> None:
        self.id_increment = 1
    
    def _request(self,req_dict:dict):
        raise JsonRPCClientException('not implemets')
    def _wait_response(self)->dict:
        raise JsonRPCClientException('not implemets')

    def request_notify(self,method:str,params:dict):
        req_dict = {
            'jsonrpc':'2.0',
            'method':method,
            'params':params
        }
        self._request(req_dict)

    def request_method(self,method:str,params:dict):
        self.id_increment = self.id_increment + 1
        id = self.id_increment
        req_dict = {
            'jsonrpc':'2.0',
            'id':id,
            'method':method,
        }
        if params != None:
            req_dict['params'] = params
        self._request(req_dict)
        res_json = self._wait_response()

        if 'error' in res_json:
            raise JsonRPCClientException(str(res_json['error']))
        
        if not 'id' in res_json:
            raise JsonRPCClientException('id not exists')
        
        if res_json['id'] != id:
            raise JsonRPCClientException('id not match')
        
        if not 'result' in res_json:
            raise JsonRPCClientException('result not exits')
        return res_json['result']
