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

import init_config
import excel_operations
import crew_operations
import gradio_interface

#############################################################################
# START PROCESSING
#############################################################################

# Ensure default directories exist
init_default_dirs()

# start logging
logger=init_logging()

crews_list = list()
jobs_list = list()    
templates_list = list_xls_files_in_dir(XLS_FOLDER)
crewjobs_list = get_crew_jobs_list(CREWS_FOLDER)

run_gradio()
