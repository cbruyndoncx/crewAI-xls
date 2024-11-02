# main.py

import sys
import logging
from fastapi import Depends, FastAPI, Request, HTTPException
#from fastapi.middleware.wsgi import WSGIMiddleware
#from fastapi.responses import RedirectResponse
import uvicorn
#from auth import app as auth_app  # Import the FastAPI app for authentication

import os
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

import gradio as gr
from src.init import init_env, create_dir, XLS_FOLDER

# Configuration for demo mode
DEMO_MODE = os.environ.get('DEMO_MODE', 'false').lower() == 'true'
DEMO_USERNAME = os.environ.get('DEMO_USERNAME', 'demo')
DEMO_PASSWORD = os.environ.get('DEMO_PASSWORD', 'demo')

from src.gradio_interface import run_gradio
from src.google_sheets import get_gspread_client, get_sheet_from_url, get_teams_from_sheet, get_users_from_sheet, get_teams_users_from_sheet, add_user_to_team, add_team, add_user

# init environment variables
init_env()

# Create a FastAPI app and mount the Gradio interface
app = FastAPI()

# Get OAuth ENV Vars
GOOGLE_CLIENT_ID =  os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET =  os.environ.get('GOOGLE_CLIENT_SECRET')
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')

# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Dependency to get the current user
def get_user(request: Request):
    try:
        if DEMO_MODE:
            user_email = DEMO_USERNAME
            logging.info(f"Demo mode active. Using demo user: {user_email}")
        else:
            user = request.session.get('user')
            if user:
                user_email = user['name']
                logging.info(f"User retrieved from session: {user_email}")
            else:
                logging.warning("No user found in session.")
                return None

        client = get_gspread_client(credentials_file='gsheet_credentials.json')
        sheet = get_sheet_from_url(client=client, sheet_url='https://docs.google.com/spreadsheets/d/1C84WFsdTs5X0O5hbN7tCqxytLCe4srLQy3OcEtGKsqw/')
        users = get_users_from_sheet(sheet)
        teams_users = get_teams_users_from_sheet(sheet)

        # Find the team for the logged-in user
        user_team = next((entry['team'] for entry in teams_users if entry['user'] == user_email), None)
        if user_team:
            os.environ['TENANT_ID'] = user_team
            logging.info(f"Team found for user '{user_email}': {user_team}")
        else:
            logging.error(f"No team found for user '{user_email}'.")
            raise ValueError(f"No team found for user '{user_email}'.")

    except Exception as e:
        logging.error(f"Error accessing Google Sheets: {e}")
        return None

    return user_email
    if DEMO_MODE:
        logging.info("Demo mode active. Using demo credentials.")
        return DEMO_USERNAME
    else:
        user = request.session.get('user')
        if user:
            logging.info(f"User retrieved from session: {user['name']}")
            return user['name']
        logging.warning("No user found in session.")
        return None

## FastAPI Routes
@app.get('/')
def public(user: dict = Depends(get_user)):
    if user:
        return RedirectResponse(url='/gradio')
    else:
        return RedirectResponse(url='/auth')

@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')

@app.route('/auth')
async def auth(request: Request):
    try:
        if DEMO_MODE:
            logging.info("Demo mode active. Redirecting to Gradio interface.")
            return RedirectResponse(url='/gradio')
        else:
            # HACK Google error
            logging.info("Redirecting to Gradio interface due to Google error.")
            return RedirectResponse(url='/gradio')
            # REENABLE
            #redirect_uri = request.url_for('register')  
            #return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        return RedirectResponse(url='/')

@app.route('/register')
async def register(request: Request):
    try:
        redirect_uri = request.url_for('create_team')
        logging.info("Redirecting to Google for user registration.")
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except OAuthError as e:
        logging.error(f"OAuth error during registration: {e}")
        return RedirectResponse(url='/')
    except Exception as e:
        logging.error(f"Unexpected error during registration: {e}")
        return RedirectResponse(url='/')
    
@app.post('/register')
async def register_user(request: Request):
    form = await request.form()
    username = form.get('username')
    team = form.get('team')

    # Here you would add logic to save the user and team to the database
    # For now, we'll just print them
    print(f"Registering user: {username}, Team: {team}")

    return RedirectResponse(url='/login')

@app.route('/setup-team')
async def setup_team(request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url='/login')

    # Fetch teams from Google Sheets
    try:
        client = get_gspread_client(credentials_file='gsheet_credentials.json')
        sheet = get_sheet_from_url(client = client, sheet_url='https://docs.google.com/spreadsheets/d/1C84WFsdTs5X0O5hbN7tCqxytLCe4srLQy3OcEtGKsqw/')
        teams = get_teams_from_sheet(sheet)
        users = get_users_from_sheet(sheet)
        teams_users = get_teams_users_from_sheet(sheet)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing Google Sheets: {e}")

    # Render a form to select a team
    team_options = "".join([f'<option value="{team["team"]}">{team["team"]}</option>' for team in teams])
    return HTMLResponse(f"""
    <form action="/setup-team" method="post">
        <label for="team">Select Team:</label><br>
        <select id="team" name="team">
            {team_options}
        </select><br>
        <input type="submit" value="Select Team">
    </form>
    <form action="/create-team" method="post">
        <label for="new_team">Create New Team:</label><br>
        <input type="text" id="new_team" name="new_team" required><br>
        <input type="submit" value="Create Team">
    </form>
    <form action="/add-user-to-team" method="post">
        <label for="team">Add User to Team:</label><br>
        <select id="team" name="team">
            {team_options}
        </select><br>
        <label for="email">User Email:</label><br>
        <input type="email" id="email" name="email" required><br>
        <input type="submit" value="Add User">
    </form>
    """)

@app.post('/setup-team')
async def create_team(request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url='/login')

    form = await request.form()
    team_name = form.get('team')

    # Here you would add logic to save the team to the database
    # For now, we'll just print the team name
    print(f"Creating team: {team_name} for user: {user}")

    return RedirectResponse(url='/gradio')

@app.post('/create-team')
async def create_team(request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url='/login')

    form = await request.form()
    new_team_name = form.get('new_team')

    # Add the new team to Google Sheets
    try:
        client = get_gspread_client(credentials_file='gsheet_credentials.json')
        sheet = get_sheet_from_url(client=client, sheet_url='https://docs.google.com/spreadsheets/d/1C84WFsdTs5X0O5hbN7tCqxytLCe4srLQy3OcEtGKsqw/')
        add_team(sheet, new_team_name)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating Google Sheets: {e}")

    return RedirectResponse(url='/setup-team')
async def add_user_to_team(request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url='/login')

    form = await request.form()
    team_name = form.get('team')
    user_email = form.get('email')

    # Add the user to the team in Google Sheets
    try:
        client = get_gspread_client(credentials_file='gsheet_credentials.json')
        sheet = get_sheet_from_url(client=client, sheet_url='https://docs.google.com/spreadsheets/d/1C84WFsdTs5X0O5hbN7tCqxytLCe4srLQy3OcEtGKsqw/')
        add_user_to_team(sheet, team_name, user_email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating Google Sheets: {e}")

    return RedirectResponse(url='/setup-team')
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError: # type: ignore
        return RedirectResponse(url='/')
    request.session['user'] = dict(access_token)["userinfo"]
    return RedirectResponse(url='/')

## Main processing
with gr.Blocks() as login_demo:
    gr.Button("Login", link="/auth")

#app = gr.mount_gradio_app(app, login_demo, path="/login-demo",server_name="localhost", server_port=8000)
app = gr.mount_gradio_app(app, login_demo, path="/login")

crewUI = run_gradio()
app = gr.mount_gradio_app(app, blocks=crewUI, path="/gradio", auth_dependency=get_user)

def greet_username(request: gr.Request):
    return request.username

if __name__ == '__main__':
#    uvicorn.run(app)
    print("Start application from commandline using:")
    print("python -m uvicorn main:app --reload")
