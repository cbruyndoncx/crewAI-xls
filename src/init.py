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

def initialize_config(team_id='default'):
    CFG = {
        "team_id": team_id,
        "base_folder": f"./data/team_{team_id}/",
        "crews_folder": f"./data/team_{team_id}/crews/",
        "xls_folder": f"./data/team_{team_id}/xls/",
        "out_folder": f"./data/team_{team_id}/crews/output/",
        "log_folder": f"./data/team_{team_id}/log/",
        "logfile": f"./data/team_{team_id}/log/output.log",
        "output_log_sheet": f"./data/team_{team_id}/output/output_log.xlsx"
    }
    create_dir(CFG["base_folder"])
    create_dir(CFG["crews_folder"])
    create_dir(CFG["xls_folder"])
    create_dir(CFG["out_folder"])
    create_dir(CFG["log_folder"])
    
    return CFG

def create_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    logging.info(folder + " created or exists")
    


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

