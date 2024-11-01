# main.py

import sys
from fastapi import Depends, FastAPI, Request
#from fastapi.middleware.wsgi import WSGIMiddleware
#from fastapi.responses import RedirectResponse
import uvicorn
#from auth import app as auth_app  # Import the FastAPI app for authentication

import os
from authlib.integrations.starlette_client import OAuth, OAuthError
from starlette.config import Config
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

import gradio as gr
from src.init import init_env, create_dir

# Configuration for demo mode
DEMO_MODE = os.environ.get('DEMO_MODE', 'false').lower() == 'true'
DEMO_USERNAME = 'demo'
DEMO_PASSWORD = 'demo'

from src.gradio_interface import run_gradio
from hello import hello

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
        return RedirectResponse(url='/login-demo')

@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')

@app.route('/login')
async def login(request: Request):
    if DEMO_MODE:
        return RedirectResponse(url='/gradio')
    else:
        redirect_uri = request.url_for('auth')
        return await oauth.google.authorize_redirect(request, redirect_uri)

@app.route('/auth')
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError: # type: ignore
        return RedirectResponse(url='/')
    request.session['user'] = dict(access_token)["userinfo"]
    return RedirectResponse(url='/')


## Main processing
with gr.Blocks() as login_demo:
    gr.Button("Login", link="/login")

#app = gr.mount_gradio_app(app, login_demo, path="/login-demo",server_name="localhost", server_port=8000)
app = gr.mount_gradio_app(app, login_demo, path="/login-demo")

def greet_username(request: gr.Request):
    return request.username

crewUI = run_gradio()

app = gr.mount_gradio_app(app, blocks=crewUI, path="/gradio", auth_dependency=get_user)

if __name__ == '__main__':
#    uvicorn.run(app)
    print("Start application from commandline using:")
    print("python -m uvicorn main:app --reload")
