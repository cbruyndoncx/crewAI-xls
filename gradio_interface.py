import os
import gradio as gr
from src.crew_operations import upload_env_file, get_crews_jobs_from_template, get_crew_jobs_list, setup, get_jobdetails, parse_details, run_crew, upload_file
from src.excel_operations import list_xls_files_in_dir
from src.init import init_default_dirs, read_logs, init_logging, XLS_FOLDER, CREWS_FOLDER

# Ensure default directories exist
init_default_dirs()

# start logging
logger = init_logging()

def run_gradio():
    custom_css = """
    #console-logs textarea {
        background-color: black; 
    }
    .gr-input textarea {
        background-color: white; /* Set textarea background to black */
        color: black; /* Optional: Change textarea text color to white for better contrast */
    }
    .gr-button, .gr-dropdown .wrap, .gr-radio label, .gr-input textarea {
        border: 2px solid #FFFFFF !important;
    }
    .gr-button{
        font-weight: bold;
    }
    """
    crews_list = []
    jobs_list = []
    templates_list = list_xls_files_in_dir(XLS_FOLDER)
    crewjobs_list = get_crew_jobs_list(CREWS_FOLDER)
    download_files=gr.Markdown("running")  
    with gr.Blocks(theme='freddyaboulton/dracula_revamped', css=custom_css) as crewUI_gradio:
    #with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="slate")) as demo:
        gr.Button("Logout", link="/logout")
        gr.Markdown("# Your CREWAI XLS Runner")
        gr.Markdown("__Easy as 1 - 2 - 3__")
        with gr.Tab("0 - Upload Environment"):
            with gr.Row():
                gr.Markdown("### Upload Environment File")
                env_file = gr.File(label="Select .env file")
                tenant_id = gr.Textbox(label="Tenant ID")
                upload_env_btn = gr.Button("Upload", elem_classes="gr-button")
                upload_env_result = gr.Markdown("")

            upload_env_btn.click(upload_env_file, inputs=[env_file, tenant_id], outputs=upload_env_result)

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
                    upload_button = gr.UploadButton("Upload xls crewAI template", file_types=["file"], file_count="multiple", elem_classes="gr-button")
        with gr.Tab("2 - Prepare"):
            with gr.Row():
                gr.Markdown("## Prepare new Crew-Job combination from loaded template")
            with gr.Row():
                gr.Markdown("### TEMPLATES ")  
                with gr.Column():       
                    template = gr.Dropdown(choices=templates_list, label='' , elem_classes="gr-dropdown")
                    upload_button.upload(upload_file, upload_button, outputs=[xls_template, template])
                with gr.Column():     
                    read_template_btn = gr.Button("Get Crews and Jobs defined", elem_classes="gr-button")
                with gr.Column():
                    gr.Markdown("After selection of template; crews and jobs become available")
            with gr.Row():
                with gr.Column(scale=1, variant="compact"): 
                    #crew = gr.Textbox(label="2) Enter Crew")
                    gr.Markdown("### CREWS")
                    crew = gr.Radio(choices=[], label='' , elem_classes="gr-radio")
                with gr.Column(scale=1, variant="compact"): 
                    gr.Markdown(f"### JOBS")
                    #job = gr.Textbox(label="3) Enter Job")
                    job = gr.Radio(choices=jobs_list, label='', elem_classes="gr-radio")
            with gr.Row():
                with gr.Column(scale=1, variant="compact"): 
                    setup_btn = gr.Button("Generate Crew-Job combination", elem_classes="gr-button")
                    setup_result = gr.Markdown(".")


        with gr.Tab("3 - Run"):
            with gr.Row():
                with gr.Column(scale=1, variant="default"):
                    #get_crew_jobs_btn = gr.Button("Get prepared teams and")
                    gr.Markdown("## Complete the prompt ")
                    crewjob = gr.Dropdown(choices=crewjobs_list, label="Select team", allow_custom_value=True , elem_classes="gr-dropdown")
                    jobdetails = gr.Textbox(lines=5, label="Specify what exactly needs to be done", elem_classes="gr-input")
                    input1 = gr.Textbox(lines=1, visible=False, label="input 1", elem_classes="gr-input")
                    input2 = gr.Textbox(lines=1, visible=False, label="input 2", elem_classes="gr-input")
                    input3 = gr.Textbox(lines=1, visible=False, label="input 3", elem_classes="gr-input")
                    input4 = gr.Textbox(lines=1, visible=False, label="input 4", elem_classes="gr-input")
                    input5 = gr.Textbox(lines=1, visible=False, label="input 5", elem_classes="gr-input")
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
                    download_files = gr.Markdown("init")
                    gr.Markdown("### Download Results")
                    output_files = os.listdir(f"{CREWS_FOLDER}output")
                    for output_file in output_files:
                        gr.File(value=f"{CREWS_FOLDER}output/{output_file}", label=os.path.basename(output_file))
            with gr.Row():
                with gr.Column():
                    with gr.Accordion("Console Logs"):
                        logs = gr.Textbox(label="", lines=30, elem_id="console-logs", elem_classes="gr-textbox")
                        t = gr.Timer(3, active=True)
                        t.tick(lambda x:x, logs)
                        crewUI_gradio.load(read_logs, None, logs, lambda: gr.Timer(active=True), None, t)

        read_template_btn.click(get_crews_jobs_from_template, inputs=[template, crew, job], outputs=[crew, job])
        setup_btn.click(setup, inputs=[template,crew,job], outputs=[setup_result, crewjob])
        run_crew_btn.click(run_crew,inputs=[crew,job, crewjob,jobdetails,input1,input2,input3,input4,input5], outputs=[output, metrics, download_files])

    return crewUI_gradio.queue()

    #crewUI.queue().launch(show_error=True, auth=get_authenticated())
    #demo.queue().launch(share=True, show_error=True, auth=("user", "pwd"))
