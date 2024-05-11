from modal import Image
import modal

app = modal.App()  # Note: app were called "stub" up until April 2024


crewai_image = (
    Image.debian_slim(python_version="3.10.13")
    .apt_install("git")
    .run_commands("git clone https://github.com/cbruyndoncx/crewAI-xls && echo 'ready to go!'")
    .pip_install(" -r requirements.txt")
    .env({"HALT_AND_CATCH_FIRE": 0})

)

@app.function(image=crewai_image)
def run_gradio():
    import gradio as gr

    def greet(name):
        return f"Hello {name}!"

    iface = gr.Interface(fn=greet, inputs="text", outputs="text")
    iface.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    run_gradio()
