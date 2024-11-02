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
    sheet = client.open_by_url(sheet_url).sheet1
    return sheet
    
# Function to get team data from Google Sheets
def get_teams_from_sheet(sheet):
    teams = sheet.worksheet('teams').get_all_records()
    return teams

def get_users_from_sheet(sheet):
    users = sheet.worksheet('users').get_all_records()
    return users

def get_teams_users_from_sheet(sheet):
    teams_users = sheet.worksheet('teams_users').get_all_records()
    return teams_users



def add_user_to_team(sheet, team_name, user_email):
    teams_users_sheet = sheet.worksheet('teams_users')
    teams_users_sheet.append_row([team_name, user_email])
