from .jsonrpc_exception import *

class JsonRPCClientBase:
    id_increment:int

    def __init__(self) -> None:
        self.id_increment = 1
    
    def settimeout(self,time_sec):
        raise JsonRPCClientException('not implemented')

    def _request(self,req_dict:dict, wait_res:bool)->dict:
        raise JsonRPCClientException('not implemented')

    def request_notify(self,method:str,params:dict):
        req_dict = {
            'jsonrpc':'2.0',
            'method':method,
            'params':params
        }
        self._request(req_dict, wait_res=False)

    def request_method(self,method:str,params:dict)->dict:
        self.id_increment = self.id_increment + 1
        id = self.id_increment
        req_dict = {
            'jsonrpc':'2.0',
            'id':id,
            'method':method,
        }
        if params != None:
            req_dict['params'] = params
        res_json = self._request(req_dict,wait_res=True)

        if not 'jsonrpc' in res_json:
            raise JsonRPCClientException('jsonrpc not exists')

        if res_json['jsonrpc'] != '2.0':
            raise JsonRPCClientException('jsonrpc version is not 2.0')

        if 'error' in res_json:
            if not 'code' in res_json['error']:
                raise JsonRPCClientException('error code not exists' + str(res_json['error']))
            if not 'message' in res_json['error']:
                raise JsonRPCClientException('error message not exists' + str(res_json['error']))
            raise JsonRPCResponseException(res_json['error']['code'], res_json['error']['message'])
        
        if not 'id' in res_json:
            raise JsonRPCClientException('id not exists')
        
        if res_json['id'] != id:
            raise JsonRPCClientException('id not match')
        
        if not 'result' in res_json:
            raise JsonRPCClientException('result not exits')
        return res_json['result']
