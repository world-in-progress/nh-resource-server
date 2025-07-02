import os
import sys
import logging
import argparse
import c_two as cc
from pathlib import Path

# Import Hello (CRM)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crms.simulation import Simulation
from src.nh_resource_server.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulation Launcher')
    parser.add_argument('--server_address', type=str, required=True, help='TCP address for the server')
    parser.add_argument('--name', type=str, required=True, help='Simulation name')
    parser.add_argument('--solution_name', type=str, required=True, help='Solution name')

    args = parser.parse_args()
    
    server_address = args.server_address

    crm = Simulation(args.name, args.solution_name)
    server = cc.rpc.Server(server_address, crm)
    server.start()
    logger.info(f'Starting CRM server at {server_address}')
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info('Stopping CRM...')
    finally:
        server.stop()
        logger.info('Server stopped')
    
