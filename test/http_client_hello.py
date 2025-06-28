import c_two as cc

client = cc.rpc.Client('http://172.24.144.1:9000/api/proxy/relay?node_key=root.hello')

client.call("hello")
