# main.py


import os
import sys
from src.config import CREWS_FOLDER, XLS_FOLDER, OUT_FOLDER, LOG_FOLDER, logfile, output_log_sheet

from dotenv import load_dotenv

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
#CREWS_FOLDER_NAME = "crews"
#CREWS_FOLDER = "./" + CREWS_FOLDER_NAME + "/"
#XLS_FOLDER = "./xls/"    
#OUT_FOLDER = CREWS_FOLDER  + "output/"
#LOG_FOLDER = "./log/"
#logfile = LOG_FOLDER + "output.log"
#output_log_sheet = OUT_FOLDER + "output_log.xlsx"

#######################################
# Functions
#######################################
def init_env():
    # Load environment variables from a .env file
    load_dotenv()

    # OAuth settings
    load_dotenv(".env.google")

def init_tenant():
    # Example usage: load environment variables for a specific tenant
    tenant_id = os.getenv('TENANT_ID', 'default')  # Default to 'default' if TENANT_ID is not set
    load_dotenv(f".env.{tenant_id}")

    #def load_tenant_env(tenant_id):
    #    dotenv_path = f".env.{tenant_id}"
    #    load_dotenv(dotenv_path=dotenv_path)

def create_dir(folder):
    if not os.path.exists(folder):    
        os.mkdir(folder)   
    logging.info(folder +"  created or exists")
    
def init_default_dirs():
    create_dir(CREWS_FOLDER)  
    create_dir(XLS_FOLDER)
    create_dir(OUT_FOLDER)
    create_dir(LOG_FOLDER)

def init_logging():
    logger = ComplexLogger(logfile)
    logger.reset_logs()
    sys.stdout = ComplexLogger(logfile)
    return logger

def read_logs():
    sys.stdout.flush()
    with open(logfile, "r") as f:
        tmplog = f.read()
        return tmplog

def reset_logs():
    logger = ComplexLogger(logfile)
    logger.reset_logs()
