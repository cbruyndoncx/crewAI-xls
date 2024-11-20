# main.py

from icecream import ic
import logging

from fastapi import Depends, FastAPI, Request, HTTPException
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError

import gradio as gr

from src.gradio_interface import *
from src.google_sheets import get_gspread_client, get_sheet_from_url, get_teams_from_sheet, get_users_from_sheet, get_teams_users_from_sheet, add_user_to_team, add_team, add_user

from src.config import GlobalConfig, init_logging, get_user, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SECRET_KEY, DEMO_MODE, GSHEET_CREDENTIALS_FILE, GSHEET_URL

# Create a FastAPI app and mount the Gradio interface
global app
app = FastAPI()

# Set up OAuth
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
print(GOOGLE_CLIENT_ID)
if not GOOGLE_CLIENT_ID:
    raise ValueError("No GOOGLE_CLIENT_ID set for application")

GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
if not GOOGLE_CLIENT_SECRET:
    raise ValueError("No GOOGLE_CLIENT_SECRET set for application")

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")

config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

## FastAPI Routes
@app.get('/')
def public(user: str = Depends(get_user)):
    if user:
        logging.info(f"in /public, got {user}, redirecting to /gradio ")
        return RedirectResponse(url='/gradio')
    else:
        return RedirectResponse(url='/login-ui')

@app.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')

@app.route('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError: # type: ignore
        return RedirectResponse(url='/')
    user = dict(access_token)["userinfo"]
    request.session['user'] = user['email']
    logging.info(f"in /auth {user['email']}" )
    CFG.set_setting('user', user['email'])
    #sessCFG.value.set_setting('user', user['email'])

    return RedirectResponse(url='/')

@app.get('/login')
async def login(request: Request):
    try:
        if DEMO_MODE == 'true':
            logging.info("Demo mode active. Redirecting to Gradio interface.")
            user = 'demo'
            request.session['user'] = user
            logging.info(f"in /login DEMO {user}" )
            CFG.set_setting('user', user )
            #sessCFG.value.set_setting('user', user )
            return RedirectResponse(url='/gradio')
        else:
            redirect_uri = request.url_for('auth')  
            return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        return RedirectResponse(url='/')

@app.get('/register')
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
    logging.info(f"Registering user: {username}, Team: {team}")

    return RedirectResponse(url='/login-ui')

@app.get('/setup-team')
async def setup_team(request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url='/login-ui')

    # Fetch teams from Google Sheets
    try:
        client = get_gspread_client(GSHEET_CREDENTIALS_FILE)
        sheet = get_sheet_from_url(client=client, sheet_url=GSHEET_URL)
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
        return RedirectResponse(url='/login-ui')

    form = await request.form()
    team_name = form.get('team')

    # Here you would add logic to save the team to the database
    # For now, we'll just print the team name
    logging.info(f"Creating team: {team_name} for user: {user}")

    return RedirectResponse(url='/gradio')

@app.post('/create-team')
async def create_team(request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url='/login-ui')

    form = await request.form()
    new_team_name = form.get('new_team')

    # Add the new team to Google Sheets
    try:
        client = get_gspread_client(GSHEET_CREDENTIALS_FILE)
        sheet = get_sheet_from_url(client=client, sheet_url=GSHEET_URL)
        add_team(sheet, new_team_name)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating Google Sheets: {e}")

    return RedirectResponse(url='/setup-team')

async def add_user_to_team(request: Request):
    user = get_user(request)
    if not user:
        return RedirectResponse(url='/login-ui')

    form = await request.form()
    team_name = form.get('team')
    user_email = form.get('email')

    # Add the user to the team in Google Sheets
    try:
        client = get_gspread_client(GSHEET_CREDENTIALS_FILE)
        sheet = get_sheet_from_url(client=client, sheet_url=GSHEET_URL)
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
with gr.Blocks() as login_ui:
    gr.Button("Login", link="/login")

app = gr.mount_gradio_app(app, login_ui, path="/login-ui")

CFG = GlobalConfig()
logfile = CFG.get_setting('log_file')
logger = init_logging(logfile)

#@app.route('/gradio')
#async def gradio_route(request: Request):

crewUI = run_gradio(CFG)

# initialise with demo user, as workaround
#crewUI = run_gradio(request=Request({"type": "http", "session": {"user": {"email": "demo@demo.com"}}}))
app = gr.mount_gradio_app(app, blocks=crewUI, path="/gradio", auth_dependency=get_user)


if __name__ == '__main__':
    logging.warning("Start application from commandline using:")
    logging.warning("python -m uvicorn main:app --reload")
