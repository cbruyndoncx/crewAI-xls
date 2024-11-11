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
# OAuth settings
load_dotenv('.env.google')

logging.info("Initializing global configurations...")

# Configuration for demo mode
DEMO_MODE = os.getenv('DEMO_MODE', 'false').lower() == 'true'
DEMO_USERNAME = os.getenv('DEMO_USERNAME', 'demox')
DEMO_PASSWORD = os.getenv('DEMO_PASSWORD', 'demo')

# Get OAuth ENV Vars
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')


class GlobalConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, user_specific_options=None):
        # Initialize default configuration settings
        self.settings = {
            'default_option_1': 'value1',
            'default_option_2': 'value2',
            # Add more default options as needed
        }

        # Update with user-specific options if provided
        if user_specific_options:
            self.settings.update(user_specific_options)

    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
        self.settings[key] = value

    def update_user_settings(self, new_user_options):
        # Update the configuration with new user-specific options.
        if new_user_options:
            self.settings.update(new_user_options)


def get_team_id(user_email: str) -> str:

    try:
        if DEMO_MODE:
            team_id = "demo"
        else:
            if not user_email:
                logging.warning("No user passed")
                return None

            client = get_gspread_client(credentials_file='gsheet_credentials.json')
            sheet = get_sheet_from_url(client=client, sheet_url='https://docs.google.com/spreadsheets/d/1C84WFsdTs5X0O5hbN7tCqxytLCe4srLQy3OcEtGKsqw/')
            users = get_users_from_sheet(sheet)
            teams_users = get_teams_users_from_sheet(sheet)

            # Find the team for the logged-in user
            user_team = next((entry['team'] for entry in teams_users if entry['user'] == user_email), None)
            if user_team:
                team_id = user_team
                logging.info(f"Team found for user '{user_email}': {user_team}")
            else:
                # Set the team_id to the user's identification if no team is found
                team_id = user_email
                logging.info(f"No team found for user '{user_email}'. Using user identification as team_id.")

        set_team_config(team_id)
        logging.info(CFG.get_setting('user_email'))
        logging.info(CFG.get_setting('mode'))
        logging.info(CFG.get_setting('team_id'))

    except Exception as e:
        logging.error(f"Error accessing Google Sheets: {e}")
        return None

    print(CFG.get_setting('team_id'))
    return CFG.get_setting('team_id')

#async def get_user(request: Request, session_settings: dict = Depends(get_session_settings)):
async def get_user(request: Request):

    try:
        if DEMO_MODE:
            user_email  = DEMO_USERNAME
            logging.info(f"Demo mode active. Using demo user: {user_email}")
            mode = 'demo'
            team_id = 'demo'
            await set_team_config(team_id, mode)
        else:
            mode = 'team'
            user = request.session.get('user')
            if not user:
                return None
            else:
                # google identification email is without spaces
                user_email = user['email']
                if user_email:
                    logging.info(f"User retrieved from session: {user_email}")
                    NEWCFG = {
                        "user_email": user_email,
                    }
                    # Updating user-specific settings dynamically
                    CFG.update_user_settings(NEWCFG)

                    logging.info("getting team stuff")
                    team_id = get_team_id(user_email)
                    logging.info(f"got {team_id}")
                else:
                    logging.warning("No user found in session.")
                    return None

    except Exception as e:
        logging.error(f"Error accessing user info: {e} {mode} {user}")
        return None
    
    logging.info(CFG.get_setting('user_email'))

    return {
        "user": user_email
    }  

def set_team_config(team_id, mode = 'team'):

    if team_id:
        NEWCFG = {
            "mode" : mode,
            "team_id": team_id,
            "base_folder": f"./data/team_{team_id}/",
            "crews_folder": f"./data/team_{team_id}/crews/",
            "xls_folder": f"./data/team_{team_id}/xls/",
            "out_folder": f"./data/team_{team_id}/crews/output/",
            "log_folder": f"./data/team_{team_id}/log/",
            "logfile": f"./data/team_{team_id}/log/output.log",
            "output_log_sheet": f"./data/team_{team_id}/output/output_log.xlsx"
        } 


        # create base and other dependent folders
        if not os.path.exists(NEWCFG["base_folder"]):
            create_default_dirs(NEWCFG)

        # Updating user-specific settings dynamically
        CFG.update_user_settings(NEWCFG)

def create_default_dirs(CFG):
    # create base and other dependent folders
    if not os.path.exists(CFG["base_folder"]):
        create_dir(CFG["base_folder"])
        create_dir(CFG["crews_folder"])
        create_dir(CFG["xls_folder"])
        create_dir(CFG["out_folder"])
        create_dir(CFG["log_folder"])

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


# Usage example
CFG = GlobalConfig()

logfile = CFG.get_setting('logfile')
logger = init_logging(logfile)