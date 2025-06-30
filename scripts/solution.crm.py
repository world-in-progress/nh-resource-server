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
    parser = argparse.ArgumentParser(description='Nhwater Launcher')
    parser.add_argument('--server_address', type=str, required=True, help='TCP address for the server')
    args = parser.parse_args()
    
    server_address = args.server_address
    path = Path(__file__).parent.parent / 'resource' / 'solutions' / 'solution'
    ne_path = path / 'ne.txt'
    ns_path = path / 'ns.txt'
    rainfall_path = path / 'R22.txt_df7.csv'
    tide_path = path / 'D122_df7_hot_36.csv'

    # or_ne = [1, 1, 1, 1, 1, 3, 4, 2, 1, 817749.5, 831717.5, 27.923933045198655, 1]
    # or_ns = [1, 1, 0, 0, 1, 0, 32.0, 817749.5, 831733.5, 27.879844989939286, 1]
    # or_rainfall = ['2023-10-01', 'Station1', 5.0]
    or_sluice_gate = [1, 4.0, 0.0, True]
    # or_tide = ['2023-10-01', '12:00', 1.5]

    crm = Solution(path,ne_path,ns_path,rainfall_path, or_sluice_gate, tide_path)
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
    
