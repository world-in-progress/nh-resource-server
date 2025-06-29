import c_two as cc
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from icrms.ihello import IHello

client = cc.rpc.Client('http://172.24.144.1:9000/api/proxy/relay?node_key=root.hello')
address = 'http://172.24.144.1:9000/api/proxy/relay?node_key=root.hello'

with cc.compo.runtime.connect_crm(address, IHello) as hello:
    res = hello.hello()
    print(res)
