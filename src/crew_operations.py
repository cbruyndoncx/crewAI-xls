# main.py

import gradio as gr
import shutil
import os
import sys
import re
import json
import traceback
from datetime import datetime
import openpyxl
import glob
import pandas as pd

import argparse
from src.complex_logger import ComplexLogger
from src.init import create_dir,reset_logs

from src.generate_crew import read_variables_xls, snake_case
from importlib import import_module

from config import CREWS_FOLDER, logfile, CREWS_FOLDER_NAME, output_log_sheet, XLS_FOLDER, TEAM_FOLDER_TEMPLATE
from excel_operations import write_log_sheet, add_md_files_to_log_sheet, list_xls_files_in_dir, get_distinct_column_values_by_name

def module_callback(crew, job, crewjob, details):
    """
    Callback function to run the crew job.
    """
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
        print("\nDone.")
        gr.Info("Completed process!")
    except Exception as e:
        gr.Error("Could not complete process!")
        print(f"ERROR: {e}\n{traceback.format_exc()}")

    sys.stdout = console

def upload_env_file(file, tenant_id):
    # Save the uploaded file with a tenant-specific name
    file_path = f".env.{tenant_id}"
    with open(file_path, "wb") as f:
        f.write(file.read())
    return f"Environment file for tenant {tenant_id} uploaded successfully."
    
def run_crew(crew, job, crewjob, details, input1, input2, input3, input4, input5, team_id):
    """
    This is the main function that you will use to run your custom crew.
    """
    reset_logs()
    (crew, job) = crewjob.split('-', maxsplit=1)
    crews_dir = f"{TEAM_FOLDER_TEMPLATE.format(team_id=team_id)}{CREWS_FOLDER_NAME}/{crew}-{job}"
    select_language='en'

    input_mapping = get_input_mapping(details,input1,input2,input3,input4,input5)
    expanded_details = details.format(**input_mapping)

    # Import the  module dynamically
    # Note this is incompatible with langtrace
    module_crew_name = f"{crews_dir}.crew"
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

    print('before xls out')
    print(result)

    #write_log_sheet(output_log_sheet,details, read_logs(), result['final_output'], json.dumps(metrics, indent=4))
    #write_log_sheet(output_log_sheet,details, read_logs(), result, json.dumps(metrics, indent=4))
    add_md_files_to_log_sheet(output_log_sheet,f"{CREWS_FOLDER}{crew}-{job}")

    # copy contents of output subdirectory to directory up one level
    shutil.copytree(src=f"{crews_dir}/output", dst=f"{TEAM_FOLDER_TEMPLATE.format(team_id=team_id)}output", dirs_exist_ok=True)
 
    download_files = gr.Markdown("Fetching")
    outfiles = os.listdir(f"{CREWS_FOLDER}output")
    if (outfiles):
        download_files = gr.Column()
    #return (result['final_output'], metrics)
    return (result, metrics, download_files)

def get_crew_jobs_list(crewdir):
    crewjobs_list = [f for f in os.listdir(crewdir) if not f.startswith('output')]    
    crewjobs_list.sort()
    return crewjobs_list

def get_crew_job(crewdir=CREWS_FOLDER):   
    crewjobs_list = get_crew_jobs_list(crewdir)
    crewjob = gr.Dropdown(choices=crewjobs_list , label="Prepared teams")
    return crewjob
    
def setup(template,crew, job):
    """
    This is used to generate a new crew-job combination
    """
    (crew, agents) = crew.split(' (', maxsplit=1) 
    (job, tasks) = job.split(' (', maxsplit=1) 

    crews_dir = f"{CREWS_FOLDER}{crew}-{job}/"
    create_dir(crews_dir)
    create_dir(f"{CREWS_FOLDER}{crew}-{job}/output/")

    read_variables_xls(template,crew, job, crews_dir)
    crewjob = get_crew_job(CREWS_FOLDER)
    
    return("Crew for Job " + crews_dir + " created!" , crewjob)

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

def get_crews_jobs_from_template(template, input_crew, input_job):
    """
    This is used to fetch list of available crews and jobs in selected template
    """
    #crews_list = get_distinct_column_values_by_name(template, 'crews', 'crew')
    #jobs_list = get_distinct_column_values_by_name(template, 'tasks', 'job')
    
    crew = gr.Radio(choices=get_crews_details(template), label="Select crew", elem_classes="gr.dropdown")
    job = gr.Radio(choices=get_jobs_details(template), label="Select job", elem_classes="gr.dropdown")
    
    return (crew, job)

def upload_file(in_files):  
    # theoretically allow for multiple, might add output file
    file_paths = [file.name for file in in_files]
    for file in in_files:
        shutil.copy(file, XLS_FOLDER)    
    gr.Info("Files Uploaded!!!")    

    templates_list = list_xls_files_in_dir(XLS_FOLDER)
    template = gr.Dropdown(choices=templates_list, label="1) Select from templates")

    return (file_paths, template)

def extract_variables(details):
    from textwrap import dedent
    
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
            print(f"Warning: Not enough UI fields to map all variables. Variable '{var}' is ignored.")
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

def parse_details(details):

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
    
    return (local_input1, local_input2, local_input3, local_input4, local_input5)
    
def get_jobdetails(crewjob):
    def read_prompt_from_disk(file_name):
        with open(file_name, 'r') as file:
            prompt = file.read()
        return prompt

    return gr.Textbox(lines=5, value=read_prompt_from_disk( f"{CREWS_FOLDER}{crewjob}/job_default_prompt.txt"), label="Got default prompt")


