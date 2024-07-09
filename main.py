# main.py

import gradio as gr
import sys

from init_config import init_default_dirs, init_logging, XLS_FOLDER, CREWS_FOLDER
from excel_operations import list_xls_files_in_dir
from crew_operations import get_crew_jobs_list
from gradio_interface import run_gradio
from gradio_interface import run_gradio

#############################################################################
# START PROCESSING
#############################################################################

# Ensure default directories exist
init_default_dirs()

# start logging
logger=init_logging()

crews_list = []
jobs_list = []
templates_list = list_xls_files_in_dir(XLS_FOLDER)
crewjobs_list = get_crew_jobs_list(CREWS_FOLDER)

run_gradio()
