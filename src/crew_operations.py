# main.py

import gradio as gr
import shutil
import os
import sys
import re
import traceback
from datetime import datetime
import pandas as pd

import argparse
from importlib import import_module

from src.complex_logger import ComplexLogger
from src.config import CFG, get_user, create_dir,reset_logs
from src.generate_crew import read_variables_xls
from icecream import ic
from src.excel_operations import write_log_sheet, add_md_files_to_log_sheet, list_xls_files_in_dir

def module_callback(crew, job, crewjob, details):
    """
    Callback function to run the crew job.
    """
    logfile = CFG.get_setting('logfile')
    console = sys.stdout
    sys.stdout = ComplexLogger(logfile)

    args = argparse.Namespace(
        crew=crew,
        job=job,
        crewjob=crewjob,
        details=details,
    )

    try:
        # Call the function
        gr.Info("Starting process...")
        run_crew(crew, job, crewjob, details)
        gr.Info("Completed process!")
    except Exception as e:
        gr.Error("Could not complete process!")
        ic(f"ERROR: {e}\n{traceback.format_exc()}")

    sys.stdout = console

def upload_env_file(file, tenant_id, state):
    # Save the uploaded file with a tenant-specific name
    file_path = f".env.{tenant_id}"
    with open(file_path, "wb") as f:
        f.write(file.read())
    return (f"Environment file for tenant {tenant_id} uploaded successfully.", state)
    
def run_crew(crew, job, crewjob, details, input1, input2, input3, input4, input5, state):
    """
    This is the main function that you will use to run your custom crew.
    """
    reset_logs(CFG.get_setting('logfile'))
    (crew, job) = crewjob.split('-', maxsplit=1)

    select_language='en'

    input_mapping = get_input_mapping(details,input1,input2,input3,input4,input5)
    expanded_details = details.format(**input_mapping)

    # Import the  module dynamically
    # Note this is incompatible with langtrace
    module_crew_name = f"data.team_{CFG.get_setting('team_id')}.crews.{crew}-{job}.crew"
    crew_module = import_module(module_crew_name)
    CustomCrew = getattr(crew_module, 'CustomCrew')
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

    #write_log_sheet(output_log_sheet,details, read_logs(), result['final_output'], json.dumps(metrics, indent=4))
    #write_log_sheet(output_log_sheet,details, read_logs(), result, json.dumps(metrics, indent=4))
    add_md_files_to_log_sheet(CFG.get_setting('output_log_sheet'), CFG.get_setting('out_folder'))

    # copy contents of output subdirectory to directory up one level
    shutil.copytree(src=f"{CFG.get_setting('crew_dir')}/output", dst=CFG.get_setting('out_folder'), dirs_exist_ok=True)
 
    download_files = gr.Markdown("Fetching")
    outfiles = os.listdir(f"{CFG.get_setting('crews_folder')}output")
    if (outfiles):
        download_files = gr.Column()
    #return (result['final_output'], metrics)
    return (result, metrics, download_files, state)

def get_crew_jobs_list(crewdir):
    if crewdir:
        crewjobs_list = [f for f in os.listdir(crewdir) if not f.startswith('output')]    
        crewjobs_list.sort()
        return crewjobs_list
    else:
        return []

def get_crew_job(crewdir):
    crewjobs_list = get_crew_jobs_list(crewdir)
    crewjob = gr.Dropdown(choices=crewjobs_list , label="Prepared teams")
    return crewjob
    
def setup(template,crew, job, state):
    """
    This is used to generate a new crew-job combination
    """
    (crew, agents) = crew.split(' (', maxsplit=1) 
    (job, tasks) = job.split(' (', maxsplit=1) 

    # Ensure directories are created
    create_default_dirs(CFG.settings)
    CFG.set_setting('crew_dir',f"{CFG.get_setting('crews_folder')}{crew}-{job}/")
    print(CFG.get_setting('crew_dir'))
    create_dir( CFG.get_setting('crew_dir'))
    create_dir(f"{CFG.get_setting('crew_dir')}output/")

    read_variables_xls(template,crew, job, CFG.get_setting('crew_dir'))
    crewjob = get_crew_job(CFG.get_setting('crews_folder'))
    
    return ("Crew for Job " + CFG.get_setting('crew_dir') + " created!" , crewjob, state)

def get_crews_details(template):
    df = pd.read_excel(template, sheet_name='crewmembers', usecols=['crewmember', 'crew'])

    # Group the DataFrame by 'Crew' and agents into lists
    grouped_crews = df.groupby('crew')['crewmember'].apply(list)
    return [(f"{crew} ({', '.join(agent)})") for crew, agent in grouped_crews.items()]

def get_jobs_details(template):
    df = pd.read_excel(template, sheet_name='tasks', usecols=['task', 'job'])

    # Group the DataFrame by 'Job' and aggregate subtasks into lists
    grouped_jobs = df.groupby('job')['task'].apply(list)
    return [(f"{job} ({', '.join(task)})") for job, task in grouped_jobs.items()]

def get_crews_jobs_from_template(template, input_crew, input_job, state):
    """
    This is used to fetch list of available crews and jobs in selected template
    """
    #crews_list = get_distinct_column_values_by_name(template, 'crews', 'crew')
    #jobs_list = get_distinct_column_values_by_name(template, 'tasks', 'job')
    
    crew = gr.Radio(choices=get_crews_details(template), label="Select crew", elem_classes="gr.dropdown")
    job = gr.Radio(choices=get_jobs_details(template), label="Select job", elem_classes="gr.dropdown")
    
    return (crew, job, state)

def upload_file(in_files, state): 
    # theoretically allow for multiple, might add output file
    file_paths = [file.name for file in in_files]
    for file in in_files:
        shutil.copy(file, CFG.get_setting("xls_folder"))    
    gr.Info(f"Files Uploaded!!! to {CFG.get_setting('xls_folder')}")    

    templates_list = list_xls_files_in_dir(CFG.get_setting("xls_folder"))
    template = gr.Dropdown(choices=templates_list, label="1) Select from templates")

    return (file_paths, template, state)

def extract_variables(details):
    #from textwrap import dedent
    
    # Regular expression pattern to find {variable} occurrences
    pattern = re.compile(r'\{(.*?)\}')
    
    # Find all matches of the pattern in the details
    matches = pattern.findall(details)
    
    # Return a list of unique variable names without duplicates
    return sorted(list(set(matches)))

def map_variables_to_ui_fields(description, ui_fields):
    # Extract variables from the description
    variables = extract_variables(description)

    # Map extracted variables to UI fields based on their order
    ui_field_values = {}
    for i, var in enumerate(variables):
        if i < len(ui_fields):
            ui_field_values[i] = var 
        else:
            ic(f"Warning: Not enough UI fields to map all variables. Variable '{var}' is ignored.")
            break
    
    return ui_field_values

def get_ui_field_labels():
    # Let's assume these are the fieldnames from your UI fields
    return ['input1', 'input2', 'input3', 'input4', 'input5']

def get_mapped_variables(details):
    # Map variables to UI fields
    return map_variables_to_ui_fields(details,  get_ui_field_labels())

def get_input_mapping(details, input1, input2, input3, input4, input5):
    # actual field names, so we can replace corresponsing labels
    ui_fields =  [ input1, input2, input3, input4, input5]
    variables = extract_variables(details)

    # Map extracted variables to UI fields based on their order
    input_mapping = {}
    for i, var in enumerate(variables):
        if i < len(ui_fields):
            input_mapping[var] = ui_fields[i]
        else:
            print(f"Warning: Not enough UI fields to map all variables. Variable '{var}' is ignored.")
            break
    
    return input_mapping

def parse_details(details, state):

    # Map variables to UI fields
    mapped_variables = get_mapped_variables(details)
  
    # Zero indexed !!!
    input_vars = len(mapped_variables)

    local_input1 = gr.Textbox(lines=1, label="input x")
    local_input2 = gr.Textbox(lines=1, label="input x")
    local_input3 = gr.Textbox(lines=1, label="input x")
    local_input4 = gr.Textbox(lines=1, label="input x")
    local_input5 = gr.Textbox(lines=1, label="input x")
    if input_vars > 0:
        local_input1 = gr.Textbox(lines=1, visible=True, label=mapped_variables[0])
    if input_vars > 1:
        local_input2 = gr.Textbox(lines=1, visible=True, label=mapped_variables[1])
    if input_vars > 2:
        local_input3 = gr.Textbox(lines=1, visible=True, label=mapped_variables[2])
    if input_vars > 3:
        local_input4 = gr.Textbox(lines=1, visible=True, label=mapped_variables[3])
    if input_vars > 4:
        local_input5 = gr.Textbox(lines=1, visible=True, label=mapped_variables[4])
    
    return (local_input1, local_input2, local_input3, local_input4, local_input5, state)
    
def get_jobdetails(crewjob, state):
    def read_prompt_from_disk(file_name):
        with open(file_name, 'r') as file:
            prompt = file.read()
        return prompt
    
    job_txt = f"{CFG.get_setting('crews_folder')}{crewjob}/job_default_prompt.txt"
    print(CFG.get_setting('crews_folder'))
    ic(job_txt)

    return (gr.Textbox(lines=5, value=read_prompt_from_disk(job_txt ), label="Got default prompt"), state)


