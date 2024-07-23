import gradio as gr
import os
from excel_operations import list_xls_files_in_dir
from crew_operations import get_crews_jobs_from_template, setup, get_jobdetails, parse_details, run_crew, upload_file
from init_config import read_logs, XLS_FOLDER
from init_config import init_default_dirs, init_logging, XLS_FOLDER, CREWS_FOLDER
from excel_operations import list_xls_files_in_dir
from crew_operations import get_crew_jobs_list

# Ensure default directories exist
init_default_dirs()

# start logging
logger = init_logging()

#crews_list = []
#jobs_list = []
#templates_list = list_xls_files_in_dir(XLS_FOLDER)
#crewjobs_list = get_crew_jobs_list(CREWS_FOLDER)

def run_gradio():
    custom_css = """
    #console-logs {
        background-color: black; 
    }
    .gr-textbox {
        background-color: #333333; /* Darker background for input fields */
        color: white; /* Optional: Change text color to white for better contrast */
    }
        background-color: black; 
    }
    .gr-button, .gr-dropdown {
        font-weight: bold;
        border: 5px solid #FFFFFF;
    }
    """
    crews_list = []
    jobs_list = []
    templates_list = list_xls_files_in_dir(XLS_FOLDER)
    crewjobs_list = get_crew_jobs_list(CREWS_FOLDER)
    with gr.Blocks(theme='freddyaboulton/dracula_revamped', css=custom_css) as demo:
    #with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="slate")) as demo:
        gr.Markdown("# Your CREWAI XLS Runner")
        gr.Markdown("__Easy as 1 - 2 - 3__")
        with gr.Tab("1 - Setup Template"):
            with gr.Row():
                with gr.Column(scale=1, variant="compact"):            
                    gr.Markdown("### Download Templates")
                    xls_files = list_xls_files_in_dir(XLS_FOLDER)
                    for xls_file in xls_files:
                        gr.File(value=xls_file, label=os.path.basename(xls_file))
                with gr.Column(scale=1, variant="compact"):                       
                    gr.Markdown("### Upload a new configuration template")
                    xls_template = gr.File()
                    upload_button = gr.UploadButton("Upload xls crewAI template", file_types=["file"], file_count="multiple")
        with gr.Tab("2 - Prepare"):
            #with gr.Accordion("Open to Load and generate crews", open=False):
            with gr.Row():
                gr.Markdown("## Prepare new Crew-Job combination from loaded template")
            with gr.Row():
                gr.Markdown("### TEMPLATES ")  
                with gr.Column():       
                    template = gr.Dropdown(choices=templates_list, label='')
                    upload_button.upload(upload_file, upload_button, outputs=[xls_template, template])
                with gr.Column():     
                    read_template_btn = gr.Button("Get Crews and Jobs defined", elem_classes="gr-button")
                with gr.Column():
                    gr.Markdown("After selection of template; crews and jobs become available")
            with gr.Row():
                with gr.Column(scale=1, variant="compact"): 
                    #crew = gr.Textbox(label="2) Enter Crew")
                    gr.Markdown("### CREWS")
                    crew = gr.Radio(choices=[], label='')
                with gr.Column(scale=1, variant="compact"): 
                    jobs =  gr.Markdown(f"### JOBS")
                    #job = gr.Textbox(label="3) Enter Job")
                    job = gr.Radio(choices=jobs_list, label='')
            with gr.Row():
                with gr.Column(scale=1, variant="compact"): 
                    setup_btn = gr.Button("Generate Crew-Job combination", elem_classes="gr-button")
                    setup_result = gr.Markdown(".")


        with gr.Tab("3 - Run"):
            with gr.Row():
                with gr.Column(scale=1, variant="default"):
                    #get_crew_jobs_btn = gr.Button("Get prepared teams and")
                    gr.Markdown("## Complete the prompt ")
                    crewjob = gr.Dropdown(choices=crewjobs_list, label="Select team", allow_custom_value=True , elem_classes="gr.dropdown")
                    jobdetails = gr.Textbox(lines=5, label="Specify what exactly needs to be done", elem_classes="gr-textbox")
                    input1 = gr.Textbox(lines=1, visible=False, label="input 1", elem_classes="gr-textbox")
                    input2 = gr.Textbox(lines=1, visible=False, label="input 2", elem_classes="gr-textbox")
                    input3 = gr.Textbox(lines=1, visible=False, label="input 3", elem_classes="gr-textbox")
                    input4 = gr.Textbox(lines=1, visible=False, label="input 4", elem_classes="gr-textbox")
                    input5 = gr.Textbox(lines=1, visible=False, label="input 5", elem_classes="gr-textbox")
                    crewjob.change(get_jobdetails, inputs=[crewjob], outputs=[jobdetails])
                    jobdetails.blur(parse_details, inputs=[jobdetails], outputs=[input1,input2,input3,input4,input5])
                with gr.Column(scale=1, variant="default"):
                    gr.Markdown("##  Hit the button")
                    run_crew_btn = gr.Button("Run Crew-Job for job details", elem_classes="gr-button")
                    metrics = gr.Textbox(lines=2, label="Usage Metrics", elem_classes="gr-textbox")
                with gr.Column(scale=2):
                    gr.Markdown("## Wait for results below")
                    gr.Markdown("#### (or watch progress in the console at the bottom)")
                    output = gr.Textbox(lines=20, label="Final output", elem_classes="gr-textbox")

            with gr.Row():
                with gr.Column():
                    with gr.Accordion("Console Logs"):
                        # Add logs
                        logs = gr.Textbox(label="", lines=30, elem_id="console-logs", elem_classes="gr-textbox")
                        demo.load(read_logs, None, logs, every=3)

        read_template_btn.click(get_crews_jobs_from_template, inputs=[template, crew, job], outputs=[crew, job])
        setup_btn.click(setup, inputs=[template,crew,job], outputs=[setup_result, crewjob])
        #get_crew_jobs_btn.click(get_crew_job, inputs=[], outputs=[crewjob])
        
        #output = run_crew_btn.click(module_callback,[crew,job, crewjob,jobdetails])
        run_crew_btn.click(run_crew,inputs=[crew,job, crewjob,jobdetails,input1,input2,input3,input4,input5], outputs=[output, metrics])

        log = read_logs()

    demo.queue().launch(show_error=True)
    #demo.queue().launch(share=True, show_error=True, auth=("user", "pwd"))
