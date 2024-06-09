import json
from typing import Callable
from .jsonrpc_exception import *

class JsonRPCServerBase:
    _method_list:dict

    def __init__(self) -> None:
        self._method_list = {}
    
    def set_method(self,method:str,func:Callable):
        self._method_list[method] = func
    
    def _request_received(self,recv_data):
        err = None
        try:
            json_data = json.loads(recv_data)
        except Exception as ex:
            err  = JsonRPCParseError(str(ex))
        
        if err != None:
            raise err
        
        if isinstance(json_data,list):
            # batch exec
            res_json = []
            for data in json_data:
                res_child = self._exec_remote_func(data)
                if res_child != None:
                    res_json.append(res_child)
        else:
            # one exec
            res_json = self._exec_remote_func(json_data)

        return res_json

    def _exec_remote_func(self,json_data:dict):
        ret = None
        if 'id' in json_data:
            id = json_data['id']
        else:
            id = None
        if 'params' in json_data:
            params = json_data['params']
        else:
            params = None

        try:
            if not 'jsonrpc' in json_data:
                raise JsonRPCIvalidRequestError('jsonrpc not exists')

            if json_data['jsonrpc'] != '2.0':
                raise JsonRPCIvalidRequestError('jsonrpc version is not 2.0')
            
            method = self._get_method_func(json_data)
            result = method(params)

            # id == None is notify
            if id != None:
                ret = {
                    'jsonrpc':'2.0',
                    'id':id,
                    'result':result
                }
        except JsonRPCResponseException as ex:
            ret = {
                'jsonrpc':'2.0',
                'id':id,
                'error': ex.toJsonDict()
            }
        except Exception as ex:
            err  = JsonRPCInternalError(str(ex))
            ret = {
                'jsonrpc':'2.0',
                'id':id,
                'error': err.toJsonDict()
            }
        return ret

    def _get_method_func(self,data:dict)->Callable:
        if not 'method' in data:
            raise JsonRPCIvalidRequestError('method not exists')
        method_name = data['method']

        if not method_name in self._method_list:
            raise JsonRPCMethodNotFoundError(method_name)
        
        methdo = self._method_list[method_name]

        return methdo