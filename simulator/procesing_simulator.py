#! /usr/bin/env python

#############################################
'''
This is the driver script for the processing simulator.
It initializes the PROCESSING class and starts the task management process.
'''

import os, argparse, datetime, sys
from   sys import exit

# ---
parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")

args        = parser.parse_args()
verbose     = args.verbose

if verbose:
    print(f'''*** {'Verbose mode            ':<20} {verbose:>20} ***''')

# ---
try:
    SWF_COMMON_LIB_PATH = os.environ['SWF_COMMON_LIB_PATH']
    if verbose:
        print(f'''*** The SWF_COMMON_LIB_PATH is defined in the environment: {SWF_COMMON_LIB_PATH}, will be added to sys.path ***''')

    if SWF_COMMON_LIB_PATH not in sys.path: sys.path.append(SWF_COMMON_LIB_PATH)
    src_path = SWF_COMMON_LIB_PATH + '/src/swf_common_lib'
    if src_path not in sys.path:
        sys.path.append(src_path)
        if verbose: print(f'''*** Added {src_path} to sys.path ***''')
    else:
        if verbose: print(f'''*** {src_path} is already in sys.path ***''')
except:
    if verbose: print('*** The variable SWF_COMMON_LIB_PATH is undefined, will rely on PYTHONPATH ***')


# import utils
from utils import *
from utils.environment import tst

tst()

