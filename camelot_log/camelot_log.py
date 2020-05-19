#!/usr/bin/env python3
"""
CAMELOT 2 logger

Creates log for CAMELOT 2 FITS images.

Examples:

    # Create a log for all directories in the default directory
    $ camelot-log

    # Read all the images in the directory, not only the new ones.
    $ camelot-log --all

    # Create a log for a specific subdirectory, with structure YYMmmdd
    $ camelot-log -d /path/to/subdirectory

    # Verbose output
    $ camelot-log -v

    # Set base directories, space separated
    camelot-log -b "/camelot2p/data_raw /camelot2q/data_processed"

"""
from pathlib import Path
from glob import glob
import argparse
from sys import exit
import configparser
from . import logger
import os

import warnings
warnings.filterwarnings("ignore")

__version__ = 0.3

def main():

    config = configparser.ConfigParser()
    config.read( os.path.dirname(os.path.abspath(__file__)) + '/config.ini')

    BASE_DIRECTORIES = config['directories']['default'].split()

    parser = argparse.ArgumentParser(description=__doc__, usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-d", "--directory", 
                            help="Specific directory to log",                 
                            type=str)

    parser.add_argument("-v", "--verbose", 
                            help="Verbose output",
                            action='store_true'              
                            )

    parser.add_argument("-a", "--all", 
                            help="Read all the images in the directory, not only the new ones.",
                            action='store_true'              
                            )

    parser.add_argument("-b", "--base-directories", 
                            help="Set the base directories to search subdirectories with images.",
                            type=str, default=False)

    args = parser.parse_args()

    # set the default directories and exit
    if args.base_directories:
        logger.set_directories(args.base_directories, config)
        exit(0)

    if args.directory:
        directories = [args.directory]
    else:
        directories = []
        for directory in BASE_DIRECTORIES:
            directories += glob(directory + '/' + '[0-9][0-9]???[0-9][0-9]')
            logger.create_index(directory)
        directories = list(map(Path, directories)) 

    for directory in directories:
        logger.read_directories(directory, args)
