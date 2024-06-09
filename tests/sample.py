import cbpyjsonrpc
import threading
import time

server = cbpyjsonrpc.JsonRPCServerUDP("localhost",10012)

def serverloop():
    server.set_method("echo",echo_method)
    server.run_forever()

def echo_method(req:dict):
    server._run_flag = False
    #time.sleep(2)
    print("server recved",req)
    return req

s_thread = threading.Thread(target=serverloop)
s_thread.start()


time.sleep(1)

client = cbpyjsonrpc.JsonRPCClientUDP("localhost",10012)
client.settimeout(1)
print("test",client.request_method("echo",{"test":"aaa"}))
