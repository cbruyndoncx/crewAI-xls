# init.py

import os
import sys

from fastapi import Request

from src.complex_logger import ComplexLogger

import logging
logging.basicConfig(
    level=logging.INFO,
    format='INFO:     %(message)s'
)

#######################################
# initialisations
#######################################
crews_dir = ""

#######################################
# Functions
#######################################

def initialize_config(team_id='default'):
    BASE_FOLDER = f"./data/team_{team_id}/"
    CREWS_FOLDER = BASE_FOLDER + "crews/"
    XLS_FOLDER = BASE_FOLDER + "xls/"
    OUT_FOLDER = BASE_FOLDER + "output/"
    LOG_FOLDER = BASE_FOLDER + "log/"
    logfile = LOG_FOLDER + "output.log"
    output_log_sheet = OUT_FOLDER + "output_log.xlsx"
    
    DIR = {
        "base_folder": BASE_FOLDER,
        "crews_folder": CREWS_FOLDER,
        "xls_folder": XLS_FOLDER,
        "out_folder": OUT_FOLDER,
        "log_folder": LOG_FOLDER,
        "logfile": logfile,
        "output_log_sheet": output_log_sheet
    }
    
    return DIR

def get_team_id(request: Request):
    return request.session.get('team_id', 'default')

def initialize_team_config(request: Request):
    team_id = get_team_id(request)
    return initialize_config(team_id)

# Example usage within a FastAPI route or function
def initialize_directories_and_logging(request: Request):
    DIR = initialize_team_config(request)
    init_default_dirs(DIR)
    logger = init_logging(DIR["logfile"])
    return logger

def create_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    logging.info(folder + " created or exists")
    
def init_default_dirs(DIR):
    create_dir(DIR["base_folder"])
    create_dir(DIR["crews_folder"])
    create_dir(DIR["xls_folder"])
    create_dir(DIR["out_folder"])
    create_dir(DIR["log_folder"])

def init_logging(logfile):
    logger = ComplexLogger(logfile)
    logger.reset_logs()
    sys.stdout = ComplexLogger(logfile)
    return logger

def read_logs(logfile):
    sys.stdout.flush()
    with open(logfile, "r") as f:
        tmplog = f.read()
        return tmplog

def reset_logs(logfile):
    logger = ComplexLogger(logfile)
    logger.reset_logs()

