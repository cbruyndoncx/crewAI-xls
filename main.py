# main.py

import sys
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
from src.init import init_env, create_dir

# Configuration for demo mode
DEMO_MODE = os.environ.get('DEMO_MODE', 'false').lower() == 'true'
DEMO_USERNAME = os.environ.get('DEMO_USERNAME', 'demo')
DEMO_PASSWORD = os.environ.get('DEMO_PASSWORD', 'demo')

from src.gradio_interface import run_gradio
from src.google_sheets import get_teams_from_sheet

# init environment variables
init_env()

# Create a FastAPI app and mount the Gradio interface
app = FastAPI()

# Get OAuth ENV Vars
GOOGLE_CLIENT_ID =  os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET =  os.environ.get('GOOGLE_CLIENT_SECRET')
SECRET_KEY =  os.environ.get('SECRET_KEY')

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
    # HACK
    return DEMO_USERNAME
    # END HACK
    if DEMO_MODE:
        # Bypass OAuth and use demo credentials
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_type, credentials = auth_header.split()
            if auth_type.lower() == 'basic':
                username, password = credentials.split(':')
                if username == DEMO_USERNAME and password == DEMO_PASSWORD:
                    return DEMO_USERNAME
        return None
    else:
        user = request.session.get('user')
        if user:
            return user['name']
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
    if DEMO_MODE:
        return RedirectResponse(url='/gradio')
    else:
        # HACK Google error
        return RedirectResponse(url='/gradio')
        # REENABLE
        #redirect_uri = request.url_for('register')  
        #return await oauth.google.authorize_redirect(request, redirect_uri)

@app.route('/register')
async def register(request: Request):
    redirect_uri = request.url_for('create_team')
    return await oauth.google.authorize_redirect(request, redirect_uri)
    
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
        teams = get_teams_from_sheet(sheet_url='https://docs.google.com/spreadsheets/d/1C84WFsdTs5X0O5hbN7tCqxytLCe4srLQy3OcEtGKsqw/', credentials_file='gsheet_credentials.json')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error accessing Google Sheets: {e}")

    # Render a form to select a team
    team_options = "".join([f'<option value="{team["name"]}">{team["name"]}</option>' for team in teams])
    return HTMLResponse(f"""
    <form action="/setup-team" method="post">
        <label for="team">Select Team:</label><br>
        <select id="team" name="team">
            {team_options}
        </select><br>
        <input type="submit" value="Select Team">
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

"""
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError: # type: ignore
        return RedirectResponse(url='/')
    request.session['user'] = dict(access_token)["userinfo"]
    return RedirectResponse(url='/')
"""

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
