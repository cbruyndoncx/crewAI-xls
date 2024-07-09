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

from init_config import create_default_dir, init_default_dirs, init_logging, read_logs
from excel_operations import sanitize_for_excel, open_workbook, save_workbook, write_log_sheet, add_md_files_to_log_sheet, list_xls_files_in_dir, get_distinct_column_values_by_name
from crew_operations import module_callback, run_crew, get_crew_jobs_list, get_crew_job, setup, get_crews_details, get_jobs_details, get_crews_jobs_from_template, upload_file, extract_variables, map_variables_to_ui_fields, get_ui_field_labels, get_mapped_variables, get_input_mapping, parse_details, get_jobdetails
from gradio_interface import run_gradio

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
