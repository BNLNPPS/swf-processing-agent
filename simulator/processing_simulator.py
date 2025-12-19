#! /usr/bin/env python
#############################################

'''
This is the driver script for the processing simulator.
It initializes the PROCESSING class and starts the task management process.
'''

import  os, argparse, datetime, sys, shutil
from    pathlib import Path
from    sys     import exit

# Example of inputDS for the static test: group.daq:swf.101871.run

# Get the absolute path of the current file
current_path = Path(__file__).resolve()


# Get the directory above one containing the current file
top_directory   = current_path.parent.parent

# The default script path; note that any script will be copied to "payload.sh" and only then executed.
default_script  = str(top_directory / 'processing' / 'my_script.sh')

# Fix the peculiarity of the path in the testbed environment
if '/direct/eic+u' in default_script: default_script = default_script.replace('/direct/eic+u', '/eic/u')

# Copy the payload script from source path to current directory
shutil.copy(default_script, './payload.sh')

# ---
parser = argparse.ArgumentParser()

parser.add_argument("-v", "--verbose",  action='store_true',    help="Verbose mode")
parser.add_argument("-t", "--test",     action='store_true',    help="Test mode")
parser.add_argument("-i", "--inDS",     type=str,               help='Input dataset (if testing standalone)',  default='')
parser.add_argument("-o", "--outDS",    type=str,               help='Output dataset (if testing standalone)', default='user.potekhin.test1')
parser.add_argument("-s", "--script",   type=str,               help='Payload script', default=default_script)


args        = parser.parse_args()
verbose     = args.verbose
test        = args.test
inDS        = args.inDS
outDS       = args.outDS
script      = args.script

if verbose:
    print(f'''*** {'Verbose mode            ':<20} {verbose:>25} ***''')
    print(f'''*** {'Test mode               ':<20} {test:>25} ***''')
    if inDS == '':
        print("*** No input dataset provided, test mode is dynamic, using upstream data ***")
    else:
        print(f'''*** {'inDS (for static testing)     ':<20} {inDS:>25} ***''')

# ---
try:
    SWF_COMMON_LIB_PATH = os.environ['SWF_COMMON_LIB_PATH']
    if verbose: print(f'''*** The SWF_COMMON_LIB_PATH is defined in the environment: {SWF_COMMON_LIB_PATH}, will be added to sys.path ***''')

    if SWF_COMMON_LIB_PATH not in sys.path: sys.path.append(SWF_COMMON_LIB_PATH)
    src_path = SWF_COMMON_LIB_PATH + '/src/swf_common_lib'
    if src_path not in sys.path:
        sys.path.append(src_path)
        if verbose: print(f'''*** Added {src_path} to sys.path ***''')
    else:
        if verbose: print(f'''*** {src_path} is already in sys.path ***''')
except:
    if verbose: print('*** The variable SWF_COMMON_LIB_PATH is undefined, will rely on PYTHONPATH ***')


if verbose:
    print(f"*** Top directory:    {top_directory} ***")
    print(f"*** Test script path: {script} ***")

# exit(0)

if top_directory not in sys.path:
    sys.path.append(str(top_directory))
    if verbose: print(f'''*** Added {top_directory} to sys.path ***''')
else:
    if verbose: print(f'''*** {top_directory} is already in sys.path ***''')

# Initialize processing class
from processing import *

processing = PROCESSING(verbose=verbose, test=test)

if inDS != '': # Static test mode, with a provided input dataset
    if verbose: print(f'''*** Running in the static test mode with inDS: {inDS}, outDS: {outDS} ***''')
    processing.test_panda(inDS, outDS, "myout.txt")
    exit(0)



processing.run()
exit(0)


#############################################
# --- possible future development
# from utils import *
# from utils.environment import tst
# tst()