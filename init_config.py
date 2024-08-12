# main.py

import os
import sys
from logger import ComplexLogger

#######################################
# initialisations
#######################################
crews_dir = ""
CREWS_FOLDER_NAME = "crews"
CREWS_FOLDER = "./" + CREWS_FOLDER_NAME + "/"
XLS_FOLDER = "./xls/"    
OUT_FOLDER = CREWS_FOLDER  + "output/"
LOG_FOLDER = "./log/"
logfile = LOG_FOLDER + "output.log"
output_log_sheet = OUT_FOLDER + "output_log.xlsx"

#######################################
# Functions
#######################################
def create_default_dir(folder):
    if not os.path.exists(folder):    
        os.mkdir(folder)   
    print(folder +"  created or exists")
    
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

# Convert ANSI escape sequences to HTML
#from ansi2html import Ansi2HTMLConverter
#conv = Ansi2HTMLConverter()

def read_logs():
    sys.stdout.flush()
    with open(logfile, "r") as f:
        tmplog = f.read()
        #return '<code>' + conv.convert(tmplog, full=False) + '</code><br/>'
        #return conv.convert(tmplog, full=False)
        return tmplog

def reset_logs():
    logger = ComplexLogger(logfile)
    logger.reset_logs()
