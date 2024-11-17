# src/config,py
import os
import sys
import logging
from icecream import ic
from dotenv import load_dotenv

import gradio as gr
from fastapi import Depends, Request

from .complex_logger import ComplexLogger
from .google_sheets import get_gspread_client, get_sheet_from_url, get_teams_from_sheet, get_users_from_sheet, get_teams_users_from_sheet, add_user_to_team, add_team, add_user

# Load all environment variables
load_dotenv()
load_dotenv('.env.demo')
load_dotenv('.env.google')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Initializing global configurations...")

# Configuration for demo mode
DEMO_MODE = os.getenv('DEMO_MODE', 'false').lower() == 'true'
DEMO_USERNAME = os.getenv('DEMO_USERNAME', 'demox')
DEMO_PASSWORD = os.getenv('DEMO_PASSWORD', 'demo')

# Get OAuth ENV Vars
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')

class GlobalSettings:
    BASE_FOLDER_TEMPLATE = "./data/team_{team_id}/"
    CREWS_FOLDER_TEMPLATE = "./data/team_{team_id}/crews/"
    XLS_FOLDER_TEMPLATE = "./data/team_{team_id}/xls/"
    OUTPUT_FOLDER_TEMPLATE = "./data/team_{team_id}/crews/output/"
    LOG_FOLDER_TEMPLATE = "./data/team_{team_id}/log/"
    LOG_FILE_TEMPLATE = "./data/team_{team_id}/log/output.log"
    OUTPUT_LOG_SHEET_TEMPLATE = "./data/team_{team_id}/crews/output/output_log.xlsx"

class GlobalConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, user_specific_options=None):
        self.settings = { "user" : "demo"}
        if user_specific_options:
            self.settings.update(user_specific_options)

    def get_setting(self, key):
        value = self.settings.get(key)
        if value is None:
            logging.warning(f"Setting '{key}' not found in configuration.")
        return value

    def set_setting(self, key, value):
        self.settings[key] = value

    def update_user_settings(self, new_user_options):
        if new_user_options:
            self.settings.update(new_user_options)

    def update_team_settings(self, team_id):
        self.settings.update({
            "team_id": team_id,
            "base_folder": GlobalSettings.BASE_FOLDER_TEMPLATE.format(team_id=team_id),
            "crews_folder": GlobalSettings.CREWS_FOLDER_TEMPLATE.format(team_id=team_id),
            "xls_folder": GlobalSettings.XLS_FOLDER_TEMPLATE.format(team_id=team_id),
            "output_folder": GlobalSettings.OUTPUT_FOLDER_TEMPLATE.format(team_id=team_id),
            "log_folder": GlobalSettings.LOG_FOLDER_TEMPLATE.format(team_id=team_id),
            "log_file": GlobalSettings.LOG_FILE_TEMPLATE.format(team_id=team_id),
            "output_log_sheet": GlobalSettings.OUTPUT_LOG_SHEET_TEMPLATE.format(team_id=team_id)
        })
        create_default_dirs(self.settings)
        return self
    
def get_team_id(user: str) -> str:

    try:
        if DEMO_MODE:
            team_id = "demo"
        else:
            if not user:
                logging.warning("No user passed")
                return None

            client = get_gspread_client(credentials_file='gsheet_credentials.json')
            sheet = get_sheet_from_url(client=client, sheet_url='https://docs.google.com/spreadsheets/d/1C84WFsdTs5X0O5hbN7tCqxytLCe4srLQy3OcEtGKsqw/')
            users = get_users_from_sheet(sheet)
            teams_users = get_teams_users_from_sheet(sheet)

            # Find the team for the logged-in user
            user_team = next((entry['team'] for entry in teams_users if entry['user'] == user), None)
            if user_team:
                team_id = user_team
                logging.info(f"Team found for user '{user}': {user_team}")
            else:
                # Set the team_id to the user's identification if no team is found
                team_id = user.replace("@", "_at_").replace(".com", "_dot_com")
                logging.info(f"No team found for user '{user}'. Using user identification as team_id.")

    except Exception as e:
        logging.error(f"Error accessing Google Sheets: {e}")
        return None

    return team_id

#async def get_user(request: Request, session_settings: dict = Depends(get_session_settings)):
async def get_user(request: Request):
    try:
        if DEMO_MODE:
            user_email  = DEMO_USERNAME
            logging.info(f"Demo mode active. Using demo user: {user_email}")
        else:
            user = request.session['user'] 
            if user:
                    logging.info(f"Got real user {user}")
            else:
                # default to demo vfor initial CFG dependency
                return { "user" : "demo"}

    except Exception as e:
        logging.error(f"Error accessing user info: {e}")
        return None
    
    return user


def create_default_dirs(settings):
    # create base and other dependent folders
    if not os.path.exists(settings["base_folder"]):
        create_dir(settings["base_folder"])
        create_dir(settings["crews_folder"])
        create_dir(settings["xls_folder"])
        create_dir(settings["out_folder"])
        create_dir(settings["log_folder"])

def create_dir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    logging.info(folder + " created or exists")

def init_logging(logfile):
    logger = ComplexLogger(logfile)
    logger.reset_logs()
    sys.stdout = logger  # Ensure sys.stdout is set to the logger instance
    return logger

def read_logs(logfile):
    logging.info("Reading logs from file: " + logfile)
    sys.stdout.flush()
    # Check if the log file exists
    if logfile is not None and os.path.exists(logfile):
        # Read the contents of the log file
        with open(logfile, "r") as f:
            tmplog = f.read()
            logging.info("Log content read successfully")
            logging.debug(f"Log content: {tmplog}")
            return tmplog
    else:
        # Return a message or handle the case where the file does not exist
        return "Log file does not exist or is empty."

def reset_logs(logfile):
    if logfile is not None and os.path.exists(logfile):
        with open(logfile, "w") as f:
            f.truncate(0)
    logging.info(f"Logs reset for file: {logfile}")

def log_and_return(logfile):
    log_content = read_logs(logfile)
    logging.debug(f"Log content to be displayed: {log_content}")
    return log_content
    logger = ComplexLogger(logfile)
    logger.reset_logs()

