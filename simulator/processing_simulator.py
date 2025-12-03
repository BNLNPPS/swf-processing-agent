#! /usr/bin/env python

#############################################
'''
This is the driver script for the processing simulator.
It initializes the PROCESSING class and starts the task management process.
'''

import  os, argparse, datetime, sys
from    pathlib import Path
from    sys     import exit


# test case for inputDS: group.daq:swf.101871.run
# ---
parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")
parser.add_argument("-t", "--test",     action='store_true',    help="Test mode")
parser.add_argument("-i", "--inDS",     type=str,               help='Input dataset (if testing standalone)', default='')
parser.add_argument("-o", "--outDS",    type=str,               help='Output dataset (if testing standalone)', default='user.potekhin.test1')

args        = parser.parse_args()
verbose     = args.verbose
test        = args.test
inDS        = args.inDS
outDS       = args.outDS

if verbose:
    print(f'''*** {'Verbose mode            ':<20} {verbose:>25} ***''')
    print(f'''*** {'Test mode               ':<20} {test:>25} ***''')
    if inDS != '':
        print(f'''*** {'inDS (for testing)     ':<20} {inDS:>25} ***''')

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



# Get the absolute path of the current file
current_path = Path(__file__).resolve()

# Get the directory above one containing the current file
top_directory = current_path.parent.parent
if verbose: print(f"*** Top directory: {top_directory} ***")

if top_directory not in sys.path:
    sys.path.append(str(top_directory))
    if verbose: print(f'''*** Added {top_directory} to sys.path ***''')
else:
    if verbose: print(f'''*** {top_directory} is already in sys.path ***''')

# print(sys.path)

# exit(0)

from processing import *

processing = PROCESSING(verbose=verbose)

if inDS != '':
    processing.test_panda(inDS, outDS)
    exit(0)

exit(0)

processing.run()



#############################################
# --- possible future development
# from utils import *
# from utils.environment import tst
# tst()