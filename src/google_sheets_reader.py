import gspread

def fetch_data_from_sheets():
    # Access Google Sheets
    gc = gspread.service_account(filename='path/to/credentials.json')
    sh = gc.open('Your Google Sheet Name')

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

if __name__ == "__main__":
    fetch_data_from_sheets()
