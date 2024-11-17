import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up the Google Sheets API client
def get_gspread_client(credentials_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

# Function to get team data from Google Sheets
def get_sheet_from_url(client, sheet_url):
    # Access Google Sheets
    spreadsheet = client.open_by_url(sheet_url)
    return spreadsheet
    
# Function to get team data from Google Sheets
def get_teams_from_sheet(sheet):
    teams = sheet.get_worksheet(0).get_all_records()
    return teams

def get_users_from_sheet(sheet):
    users = sheet.get_worksheet(1).get_all_records()
    return users

def get_teams_users_from_sheet(sheet):
    teams_users = sheet.get_worksheet(2).get_all_records()
    return teams_users

def add_user(sheet, user_email):
    users_sheet = sheet.get_worksheet(1)
    existing_users = [user['user'] for user in users_sheet.get_all_records()]

    if user_email not in existing_users:
        users_sheet.append_row([user_email])
    else:
        raise ValueError(f"User '{user_email}' already exists.")
def add_team(sheet, team_name):
    team_name = team_name.upper()
    teams_sheet = sheet.get_worksheet(0)
    existing_teams = [team['team'].upper() for team in teams_sheet.get_all_records()]
    
    if team_name not in existing_teams:
        teams_sheet.append_row([team_name])
    else:
        raise ValueError(f"Team '{team_name}' already exists.")
def add_user_to_team(sheet, team_name, user_email):
    teams_users_sheet = sheet.get_worksheet(2)
    existing_entries = teams_users_sheet.get_all_records()

    # Check if the user is already in the team
    for entry in existing_entries:
        if entry['team'].upper() == team_name.upper() and entry['user'] == user_email:
            raise ValueError(f"User '{user_email}' is already in team '{team_name}'.")

    # Add the user to the team
    teams_users_sheet.append_row([team_name.upper(), user_email])
