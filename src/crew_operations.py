# crew_operations.py
import os
import re
import pandas as pd
import logging
import gradio as gr
from icecream import ic

from src.config import create_dir
from src.generate_crew import read_variables_xls


"""
def module_callback(crew, job, crewjob, details):
    
    #Callback function to run the crew job.
    
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
"""


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
    
def setup(template,crew, job):
    """
    This is used to generate a new crew-job combination
    """
    (crew, agents) = crew.split(' (', maxsplit=1) 
    (job, tasks) = job.split(' (', maxsplit=1) 
    from main import CFG
    crews_folder = CFG.get_setting('crews_folder')
    logging.info(CFG.settings)

    crew_dir = f"{crews_folder}{crew}-{job}/"
    create_dir( crew_dir)
    create_dir(f"{crew_dir}output/")

    read_variables_xls(template,crew, job, crew_dir)
    crewjob = get_crew_job(crews_folder)
    
    return ("Crew for Job " + crew_dir + " created!" , crewjob)

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
    

