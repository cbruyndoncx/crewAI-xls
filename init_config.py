# main.py

import gradio as gr
import shutil
import os
import sys
import re
import json
from datetime import datetime
import openpyxl
import glob
import pandas as pd

import argparse
from logger import ComplexLogger

from generate_crew import read_variables_xls, snake_case
from importlib import import_module

#######################################
# initialisations
#######################################
crews_dir = ""
CREWS_FOLDER_NAME = "crews"
CREWS_FOLDER = "./" + CREWS_FOLDER_NAME + "/"
XLS_FOLDER = "./xls/"    
OUT_FOLDER = "./out/"
LOG_FOLDER = "./log/"
logfile = LOG_FOLDER + "output.log"
output_log_sheet = OUT_FOLDER + "output_log.xlsx"

#######################################
# Functions
#######################################
def create_default_dir(folder):
    if not os.path.exists(folder):    
        os.mkdir(folder)   

def init_default_dirs():
    create_default_dir(CREWS_FOLDER)  
    create_default_dir(XLS_FOLDER)
    create_default_dir(OUT_FOLDER)
    create_default_dir(LOG_FOLDER)

def init_logging():
    logger = ComplexLogger(logfile)
    logger.reset_logs()
    sys.stdout = ComplexLogger(logfile)
    return logger

def read_logs():
    sys.stdout.flush()
    with open(logfile, "r") as f:
        return f.read()

