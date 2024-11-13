import gradio as gr

# Define a configuration class
class Config:
    def __init__(self):
        self.settings = {
            "setting1": "default1",
            "setting2": "default2"
        }

    def update_setting(self, key, value):
        self.settings[key] = value

# Initialize the configuration and state
config = Config()


# Define a function to update the configuration and state
def update_config(new_value, state):
    # Update the configuration
    state.update_setting("setting1", new_value)
    # Return a message to indicate the update and the updated state
    return f"Updated setting1 to: {new_value}", state

# Define a function to use the updated configuration
def use_config(input_text, state):
    # Access the updated configuration
    setting1_value = state.value.settings["setting1"]
    return f"Input: {input_text}, Setting1: {setting1_value}"

# Create a Gradio interface
with gr.Blocks() as demo:
    state = gr.State(config)
    with gr.Row():
        input_text = gr.Textbox(label="Enter some text")
        setting_input = gr.Textbox(label="Update Setting1")
        output_text = gr.Textbox(label="Output")

    # Set up event handling
    setting_input.change(update_config, inputs=[setting_input, state], outputs=[output_text, state])
    input_text.submit(use_config, inputs=[input_text, state], outputs=output_text)

# Launch the interface
demo.launch()