import os
import sys
import logging
import c_two as cc
import multiprocessing as mp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from icrms.ihello import IHello


def hello_request():
    address = 'http://172.24.144.1:9000/api/proxy/relay?node_key=root.hello'

    with cc.compo.runtime.connect_crm(address, IHello) as hello:
        res = hello.hello()
        logger.info(f'res: {res}')

if __name__ == '__main__':
    processes = []
    for i in range(10):
        p = mp.Process(target=hello_request)
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()

