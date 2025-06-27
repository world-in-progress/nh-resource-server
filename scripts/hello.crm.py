import os
import sys
import logging
import argparse
import c_two as cc

# Import Hello (CRM)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crms.hello import Hello

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hello Launcher')
    parser.add_argument('--server_address', type=str, required=True, help='TCP address for the server')
    args = parser.parse_args()
    
    server_address = args.server_address

    # Init CRM
    crm = Hello()
    
    # Launch CRM server
    logger.info('Starting CRM server...')
    server = cc.rpc.Server(server_address, crm)
    server.start()
    logger.info('CRM server started at %s', server_address)
    try:
        if server.wait_for_termination():
            server.stop()

    except KeyboardInterrupt:
        server.stop()
        logger.info('CRM server stopped by keyboard interrupt')
    except Exception as e:
        logger.error('CRM server stopped with error: %s', str(e))
        server.stop()