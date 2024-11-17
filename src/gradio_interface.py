import os
import shutil
import json
import gradio as gr
from importlib import import_module
from src.crew_operations import  get_crews_jobs_from_template, get_crew_jobs_list, setup, parse_details, get_input_mapping
from src.excel_operations import write_log_sheet, add_md_files_to_log_sheet, list_xls_files_in_dir
from src.config import get_team_id, read_logs, reset_logs

from icecream import ic
import logging


from fastapi import Request

import pprint

def dump_request(request: Request):
     # Use dir() to list all attributes and methods
     print("Attributes and methods:")
     for attr in dir(request):
         print(attr)

     # Use vars() to print the __dict__ attribute if available
     try:
         print("\n__dict__ attribute:")
         pprint.pprint(vars(request))
     except TypeError:
         print("\nNo __dict__ attribute available.")

     # Use pprint to print the request object itself
     print("\nPretty print of the request object:")
     pprint.pprint(request)

def run_crew(sessCFG, crew, job, crewjob, details, input1, input2, input3, input4, input5):
    """
    This is the main function that you will use to run your custom crew.
    """
    
    reset_logs(sessCFG.get_setting('log_file'))
    logging.info(f"CREW: {crew} - JOB: {job} = CREWJOB: {crewjob}") 
    (crew, job) = crewjob.split('-', maxsplit=1)


    # Import the  module dynamically
    # Note this is incompatible with langtrace
    
    team_id = sessCFG.get_setting('team_id')
    module_crew_name = f"data.team_{team_id}.crews.{crew}-{job}.crew"
    crew_module = import_module(module_crew_name)
    CustomCrew = getattr(crew_module, 'CustomCrew')
    
    input_mapping = get_input_mapping(details,input1,input2,input3,input4,input5)
    expanded_details = details.format(**input_mapping)
    select_language='en'
    custom_crew = CustomCrew(expanded_details, select_language)

    # NOK does not work properly
    #from document_crew import describe_crew_instances2
    #print(describe_crew_instances2(custom_crew))

    # OK, outputs the docstrings with basic config info
    #help(custom_crew)
    #help(custom_crew.agents)
    #help(custom_crew.tasks)

    (result, metrics) = custom_crew.run()

    ic(result)
    
    crews_folder = sessCFG.get_setting('crews_folder')
    output_folder = sessCFG.get_setting('output_folder')
    output_log_sheet = sessCFG.get_setting('output_log_sheet')
    crew_dir = f"{crews_folder}{crew}-{job}/"
    logfile = sessCFG.get_setting('log_file')

    write_log_sheet(output_log_sheet,details, read_logs(logfile), result.raw.replace('\n\n', '\n'), json.dumps(metrics, indent=4))
    add_md_files_to_log_sheet(output_log_sheet, output_folder)

    # copy contents of output subdirectory to directory up one level
    shutil.copytree(src=f"{crew_dir}/output", dst=output_folder, dirs_exist_ok=True)
 
    download_files = gr.Markdown("Fetching")
    outfiles = os.listdir(output_folder)
    if (outfiles):
        download_files = gr.Column()
    #return (result['final_output'], metrics)
    return (result, metrics, download_files)

def run_gradio(CFG):
    
    # Must use the complete CFG class var, just settings does not work
    user = CFG.get_setting('user')
    team_id = get_team_id(user)
    crews_folder = CFG.get_setting('crews_folder')
    xls_folder = CFG.get_setting('xls_folder')

    def get_jobdetails(crewjob, sessCFG):
        def read_prompt_from_disk(file_name):
            with open(file_name, 'r') as file:
                prompt = file.read()
            return prompt
        crews_folder = sessCFG.get_setting('crews_folder')
        job_txt = f"{crews_folder}{crewjob}/job_default_prompt.txt"
        ic(job_txt)

        return (gr.Textbox(lines=5, value=read_prompt_from_disk(job_txt ), label="Got default prompt"))
    
    def update_user(grUser, sessCFG):
        grUser = gr.Textbox(label="user", value=sessCFG.get_setting('user'))
        #grUser = gr.Textbox(label="user", value=user)
        team_id = get_team_id(sessCFG.get_setting('user'))
        sessCFG.update_team_settings(team_id)
        grTeamId = gr.Textbox(label="team", value=sessCFG.get_setting('team_id'))
        crews_folder = sessCFG.get_setting('crews_folder')
        xls_folder = sessCFG.get_setting('xls_folder')
        grCrewsFolder = gr.Textbox(label="crews folder", value=crews_folder)
        logging.info(f"crews_folder: {crews_folder} grCrewsFolder: {grCrewsFolder}")
        grXlsFolder = gr.Textbox(label="xls folder", value=xls_folder)
        grTemplate = gr.Dropdown(choices=list_xls_files_in_dir(xls_folder), label='Select XLS Template' , elem_classes="gr-dropdown")
        crewjob = gr.Dropdown(choices=get_crew_jobs_list(crews_folder), label="Select team", allow_custom_value=True , elem_classes="gr-dropdown")
                 
        return (grUser, grTeamId, grCrewsFolder, grXlsFolder , grTemplate, crewjob, sessCFG )  

    def upload_env_file(file, tenant_id):
        # Save the uploaded file with a tenant-specific name
        file_path = f"{xls_folder}.env.{tenant_id}"
        with open(file_path, "wb") as f:
            f.write(file.read())
        return (f"Environment file for tenant {tenant_id} uploaded successfully.")

    def upload_file(in_files, sessCFG ): 
        # theoretically allow for multiple, might add output file
        
        xls_folder = sessCFG.get_setting('xls_folder')
        logging.info(xls_folder)

        file_paths = [file.name for file in in_files]
        for file in in_files:
            shutil.copy(file, xls_folder)    
        gr.Info(f"Files Uploaded!!! to {xls_folder}")    

        templates_list = list_xls_files_in_dir(xls_folder)
        grTemplate = gr.Dropdown(choices=templates_list, label="Select XLS template")
        
        return (file_paths, grTemplate)

    custom_css = """
    #console-logs textarea { background-color: black; }
    .gr-input textarea {
        background-color: white; /* Set textarea background to black */
        color: black; /* Optional: Change textarea text color to white for better contrast */ }
    .gr-button, .gr-dropdown .wrap, .gr-radio label, .gr-input textarea { border: 2px solid #FFFFFF !important; }
    .gr-button-small { font-weight: bold; padding: 5px 10px; margin: 0 5px; }
    .gr-button { font-weight: bold; }
    """

    jobs_list = []
    download_files = gr.Markdown("running")
    with gr.Blocks(theme='freddyaboulton/dracula_revamped', css=custom_css, ) as crewUI_gradio:
    #with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="slate")) as demo:

        # >>>>>>>>  WARNING 
        sessCFG= gr.State(CFG)
        # !!! Use sessCG.value.method when in gradio, without value, just method within functions
        # gr.State must be declared within Blocks, otherwise error when passin as input or outpupt
        # <<<<<<<<< END WARNING
        logging.info(f"getting team stuff for {sessCFG.value.settings['user']}")
        logging.info(f"Got Session Settings: {sessCFG.value.settings}")
        logging.info(f"Got Crews folder: {sessCFG.value.get_setting('crews_folder')}")
        logging.info(f"Got Xls folder: {sessCFG.value.get_setting('xls_folder')}")

        with gr.Row():
            
            grUser = gr.Textbox(label="user")
            grTeamId = gr.Textbox(label="team")
            grUser.change(get_team_id, inputs=[grUser], outputs=[grTeamId])

            grCrewsFolder = gr.Textbox(label="crews folder")
            grXlsFolder = gr.Textbox(label="xls_folder")

            #grCfgButton = gr.Button("Load Cfg", elem_classes="gr-button-small")
            #grCfgButton.click(update_user, inputs=[grUser], outputs=[grUser, grTeamId])
            
            gr.Button("Setup Team", link="/setup-team", elem_classes="gr-button-small")
            gr.Button("Logout", link="/logout", elem_classes="gr-button-small")
        gr.Markdown("# Your CREWAI XLS Runner")
        gr.Markdown("__Easy as 1 - 2 - 3__")

        
        with gr.Tab("0 - Upload Environment"):
            with gr.Row():
                gr.Markdown("### Upload Environment File")
                env_file = gr.File(label="Select .env file")
                tenant_id = gr.Textbox(label="Tenant ID")
                upload_env_btn = gr.Button("Upload", elem_classes="gr-button")
                upload_env_result = gr.Markdown("")

            upload_env_btn.click(upload_env_file, inputs=[env_file, tenant_id], outputs=[upload_env_result])
        

        with gr.Tab("1 - Setup Template"):
            with gr.Row():
                with gr.Column(scale=1, variant="compact"):            
                    gr.Markdown("### Download Templates")
                    xls_files = list_xls_files_in_dir(xls_folder)
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
                    grTemplate = gr.Dropdown(choices=list_xls_files_in_dir(xls_folder), label='Select XLS Template' , elem_classes="gr-dropdown")
                    upload_button.upload(upload_file, inputs=[upload_button, sessCFG], outputs=[xls_template, grTemplate])
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
                    crewjob = gr.Dropdown(choices=get_crew_jobs_list(crews_folder), label="Select team", allow_custom_value=True , elem_classes="gr-dropdown")
                    jobdetails = gr.Textbox(lines=5, label="Specify what exactly needs to be done", elem_classes="gr-input")
                    input1 = gr.Textbox(lines=1, visible=False, label="input 1", elem_classes="gr-input")
                    input2 = gr.Textbox(lines=1, visible=False, label="input 2", elem_classes="gr-input")
                    input3 = gr.Textbox(lines=1, visible=False, label="input 3", elem_classes="gr-input")
                    input4 = gr.Textbox(lines=1, visible=False, label="input 4", elem_classes="gr-input")
                    input5 = gr.Textbox(lines=1, visible=False, label="input 5", elem_classes="gr-input")
                    crewjob.change(get_jobdetails, inputs=[crewjob,sessCFG], outputs=[jobdetails])
                    jobdetails.change(parse_details, inputs=[jobdetails], outputs=[input1,input2,input3,input4,input5])
                with gr.Column(scale=1, variant="default"):
                    gr.Markdown("##  Hit the button")
                    run_crew_btn = gr.Button("Run Crew-Job for job details", elem_classes="gr-button")
                    metrics = gr.Textbox(lines=2, label="Usage Metrics", elem_classes="gr-textbox")
                with gr.Column(scale=2):
                    gr.Markdown("## Wait for results below")
                    gr.Markdown("#### (or watch progress in the console at the bottom)")
                    with gr.Accordion('Answer:', open=True):
                        #output = gr.Textbox(lines=20, label="Final output", elem_classes="gr-textbox") 
                        output = gr.Markdown(elem_classes="gr-textbox") 
                    
            with gr.Row():
                with gr.Column():
                    download_files = gr.Markdown("init")
                    gr.Markdown("### Download Results")
                    if sessCFG.value.get_setting('crews_folder') is not None:
                        #print(f"{CFG.get_setting('crews_folder')}output")
                        output_files = os.listdir(f"{crews_folder}output")
                        for output_file in output_files:
                            gr.File(value=f"{crews_folder}output/{output_file}", label=os.path.basename(output_file))
            with gr.Row():
                with gr.Column():
                    with gr.Accordion("Console Logs"):
                        logs = gr.Textbox(label="", lines=30, elem_id="console-logs", elem_classes="gr-textbox")
                        #t = gr.Timer(10, active=True)
                        #t.tick(lambda x:x, logs)
                        #crewUI_gradio.load(read_logs, sessCFG.get_setting('logfile'), logs, lambda: gr.Timer(active=True), None, t)

        crewUI_gradio.load(update_user, inputs=[grUser, sessCFG], outputs=[grUser, grTeamId,grCrewsFolder, grXlsFolder, grTemplate, crewjob, sessCFG])
        read_template_btn.click(get_crews_jobs_from_template, inputs=[grTemplate, crew, job], outputs=[crew, job])
        setup_btn.click(setup, inputs=[grTemplate, crew, job], outputs=[setup_result, crewjob])
        run_crew_btn.click(run_crew,inputs=[sessCFG,crew,job, crewjob,jobdetails,input1,input2,input3,input4,input5], outputs=[output, metrics, download_files])
        #ic(crewUI_gradio)
    return  crewUI_gradio.queue()


    #crewUI.queue().launch(show_error=True, auth=get_authenticated())
    #demo.queue().launch(share=True, show_error=True, auth=("user", "pwd"))
