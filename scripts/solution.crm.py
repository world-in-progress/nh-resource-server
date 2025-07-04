import os
import sys
import logging
import argparse
import c_two as cc
from pathlib import Path

# Import Hello (CRM)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crms.solution import Solution
from src.nh_resource_server.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Solution Launcher')
    parser.add_argument('--server_address', type=str, required=True, help='TCP address for the server')
    parser.add_argument('--name', type=str, required=True, help='Solution name')
    parser.add_argument('--ne_path', type=str, required=True, help='NE path')
    parser.add_argument('--ns_path', type=str, required=True, help='NS path')
    parser.add_argument('--inp_path', type=str, required=True, help='IMP path')
    parser.add_argument('--rainfall_path', type=str, required=True, help='Rainfall path')
    parser.add_argument('--gate_path', type=str, required=True, help='Gate path')
    parser.add_argument('--tide_path', type=str, required=True, help='Tide path')

    args = parser.parse_args()
    
    server_address = args.server_address

    crm = Solution(args.name, args.ne_path, args.ns_path, args.inp_path, args.rainfall_path, args.gate_path, args.tide_path)
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
    
