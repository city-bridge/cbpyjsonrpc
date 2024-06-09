# cbpyjsonrpc

## About

json-rpc 2.0 udp server and clinet.

[https://www.jsonrpc.org/](https://www.jsonrpc.org/)


## install
```
pip install git+https://github.com/city-bridge/cbpyjsonrpc.git
```

## server sample
```python
import cbpyjsonrpc
server = cbpyjsonrpc.JsonRPCServerUDP("localhost",10012)

def echo_method(req:dict):
    server._run_flag = False
    print("server recved",req)
    return req

server.set_method("echo",echo_method)
server.run_forever()
```

## client sample
```python
import cbpyjsonrpc
client = cbpyjsonrpc.JsonRPCClientUDP("localhost",10012)
print(client.request_method("echo",{"test":"aaa"}))
```

