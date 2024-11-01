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
    client = get_gspread_client(credentials_file)
    sheet = client.open_by_url(sheet_url).sheet1
    teams = sheet.get_all_records()
    return teams
