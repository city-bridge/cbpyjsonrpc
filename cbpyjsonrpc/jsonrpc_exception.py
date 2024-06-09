from .jsonrpc_define import *

class JsonRPCException (Exception):
    pass

class JsonRPCClientException (JsonRPCException):
    pass

class JsonRPCResponseException (JsonRPCException):
    def __init__(self,code,message) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
    
    def toJsonDict(self):
        error_dict = {
            'code':self.code,
            'message':self.message
        }
        return error_dict

class JsonRPCParseError (JsonRPCResponseException):
    def __init__(self,msg) -> None:
        super().__init__(ERROR_CODE_PARSE_ERROR,'Parse error: ' + msg)

class JsonRPCInvalidRequestError (JsonRPCResponseException):
    def __init__(self, msg) -> None:
        super().__init__(ERROR_CODE_INVALID_REQUEST, 'Invalid Request: ' + msg)

class JsonRPCMethodNotFoundError (JsonRPCResponseException):
    def __init__(self,msg) -> None:
        super().__init__(ERROR_CODE_METHOD_NOT_FOUND, 'Method not found: ' + msg)

class JsonRPCInvalidParameterError (JsonRPCResponseException):
    def __init__(self,msg) -> None:
        super().__init__(ERROR_CODE_INVALID_PARAMS, 'Invalid params: ' + msg)

class JsonRPCInternalError (JsonRPCResponseException):
    def __init__(self,msg) -> None:
        super().__init__(ERROR_CODE_INTERNAL_ERROR,'Internal error: ' + msg)

