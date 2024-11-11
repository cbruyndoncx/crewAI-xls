#test.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
import gradio as gr
import requests

app = FastAPI()

# Add session middleware with a secret key
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Route to set session data
@app.get("/set-session")
async def set_session(request: Request):
    request.session['user_info'] = {
        'username': 'test_user',
        'preferences': {
            'theme': 'dark',
            'language': 'en'
        }
    }
    return {"message": "Session data set"}

# Route to clear session data
@app.get("/clear-session")
async def clear_session(request: Request):
    request.session.clear()
    return {"message": "Session data cleared"}

# API endpoint to get session data
@app.get("/get-session")
async def get_session(request: Request):
    user_info = request.session.get('user_info', {})
    return JSONResponse(user_info)

# Gradio interface function to fetch session data
def fetch_session_data():
    response = requests.get("http://localhost:7860/get-session")
    if response.status_code == 200:
        user_info = response.json()
        username = user_info.get('username', 'Guest')
        theme = user_info.get('preferences', {}).get('theme', 'default')
        return f"Hello, {username}! Your preferred theme is: {theme}"
    return "Could not fetch session data."

# Create the Gradio interface
with gr.Blocks() as gradio_blocks:
    gr.Interface(
        fn=fetch_session_data,
        inputs=[],
        outputs="textje"
    )

# Mount the Gradio app globally at a specific path
app = gr.mount_gradio_app(app, gradio_blocks, path="/")


# To run the app, use the command: uvicorn <filename>:app --reload
