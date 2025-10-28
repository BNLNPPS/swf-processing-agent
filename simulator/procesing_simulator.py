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