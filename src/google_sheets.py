import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up the Google Sheets API client
def get_gspread_client(credentials_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

# Function to get team data from Google Sheets
def get_teams_from_sheet(sheet_url, credentials_file):

def fetch_data_from_sheets(credentials_file, sheet_name):
    # Access Google Sheets
    client = get_gspread_client(credentials_file)
    sh = client.open(sheet_name)

    # Fetch teams
    teams_sheet = sh.worksheet('teams')
    teams_records = teams_sheet.get_all_records()
    print("Teams:")
    for record in teams_records:
        print(record['team'])

    # Fetch users
    users_sheet = sh.worksheet('users')
    users_records = users_sheet.get_all_records()
    print("\nUsers:")
    for record in users_records:
        print(record['user'])

    # Fetch team-user relationships
    teams_users_sheet = sh.worksheet('teams_users')
    teams_users_records = teams_users_sheet.get_all_records()
    print("\nTeam-User Relationships:")
    for record in teams_users_records:
        print(f"Team: {record['team']}, User: {record['user']}")
    client = get_gspread_client(credentials_file)
    sheet = client.open_by_url(sheet_url).sheet1
    teams = sheet.get_all_records()
    return teams

def fetch_data_from_sheets(credentials_file, sheet_name):
    # Access Google Sheets
    client = get_gspread_client(credentials_file)
    sh = client.open(sheet_name)

    # Fetch teams
    teams_sheet = sh.worksheet('teams')
    teams_records = teams_sheet.get_all_records()
    print("Teams:")
    for record in teams_records:
        print(record['team'])

    # Fetch users
    users_sheet = sh.worksheet('users')
    users_records = users_sheet.get_all_records()
    print("\nUsers:")
    for record in users_records:
        print(record['user'])

    # Fetch team-user relationships
    teams_users_sheet = sh.worksheet('teams_users')
    teams_users_records = teams_users_sheet.get_all_records()
    print("\nTeam-User Relationships:")
    for record in teams_users_records:
        print(f"Team: {record['team']}, User: {record['user']}")
