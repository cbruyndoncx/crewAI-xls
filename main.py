# main.py

import gradio as gr
import os
import sys
import openpyxl
import pandas as pd

from generate_crew import read_variables_xls, snake_case
from importlib import import_module

crews_dir = ''
 
import argparse
from logger import ComplexLogger
logfile = "output.log"
logger = ComplexLogger(logfile)
logger.reset_logs()
sys.stdout = ComplexLogger(logfile)

# def read_logs():
#     sys.stdout.flush()
#     with open(logfile, "r") as f:
#         return f.read()
def module_callback(crew,job, crewjob, details):
    """

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
        run_crew(crew,job, crewjob, details)
        print("\nDone.")
        gr.Info("Completed process!")
    except Exception as e:
        gr.Error("Could not complete process!")
        #print(f"ERROR: {e}\n{traceback.format_exc()}")

    sys.stdout = console

def list_xls_files_in_dir(directory):
    """
    This is used to generate the list of template files to choose from
    """
    files_in_directory = os.listdir(directory)
    xlsfiles = [file for file in files_in_directory if file.endswith('.xls') or file.endswith('.xlsx')]
    return xlsfiles

def md_list(items):
        return "\n".join(f"* {item}" for item in items)
    
# Function to get distinct values from a named column in a named sheet
def get_distinct_column_values_by_name(workbook_path, sheet_name, column_name):
    """
    Extracts distinct values from a specified named column in an Excel sheet.

    :param workbook_path: The path to the Excel workbook.
    :param sheet_name: The name of the worksheet to use.
    :param column_name: The name of the column to extract values from.
    :return: A set of distinct values.
    """
    # Load the workbook and select the specified sheet
    workbook = openpyxl.load_workbook(workbook_path)
    sheet = workbook[sheet_name]

    # Find the index of the specified column by name
    column_index = 0
    for col in sheet.iter_cols(min_row=1, max_row=1, values_only=True):
        column_index = column_index +1
        if col[0] == column_name:
            break
    else:
        # If no matching header is found, raise an error
        raise ValueError(f"Column with header '{column_name}' not found.")

    # Use a set to store unique values as sets do not allow duplicates
    distinct_values = set()

    # Iterate over all rows in the specified named column (excluding the header)
    for row in sheet.iter_rows(min_row=2, min_col=column_index, max_col=column_index, values_only=True):
        cell_value = row[0]
        if cell_value is not None:  # Exclude empty cells
            distinct_values.add(cell_value)

    # Close the workbook after processing
    workbook.close()

    return sorted(list(distinct_values))

def run_crew(crew,job, crewjob, details):
    """
    This is the main function that you will use to run your custom crew.
    """
    (crew, job) = crewjob.split('-', maxsplit=1)   
    crews_dir=f"crews.{crew}-{job}"
    select_language='en'

    # Import the  module dynamically
    crew_module = import_module(f"{crews_dir}.crew")
    CustomCrew = getattr(crew_module, 'CustomCrew')
    custom_crew = CustomCrew(details, select_language)

    # from document_crew import describe_crew_instances2
    # print(describe_crew_instances2(custom_crew))

    (result, metrics) = custom_crew.run()

    return (result['final_output'], metrics)
    #return f"{result}"

def get_crew_jobs_list(crewdir):
    crewjobs_list = os.listdir(crewdir)
    crewjobs_list.sort()
    return crewjobs_list

def get_crew_job(crewdir='crews/'):
    crewjobs_list = get_crew_jobs_list(crewdir)
    crewjob = gr.Dropdown(choices=crewjobs_list, label="Prepared teams")
    return crewjob

def setup(template,crew, job):
    """
    This is used to generate a new crew-job combination
    """
    crews_dir = f"./crews/{crew}-{job}/"
    # Check if the directory already exists
    if not os.path.exists(crews_dir):
        # If it doesn't exist, create it (including any intermediate directories)
        os.makedirs(crews_dir)
    #read_variables_xls('vars_in.xlsx',crew, job, crews_dir)    
    read_variables_xls(template,crew, job, crews_dir)
    crewjob = get_crew_job('crews/')
    
    return("Crew for Job " + crews_dir + " created!" , crewjob)

def get_jobs_details(template):
    df = pd.read_excel(template, sheet_name='tasks', usecols=['task', 'job'])

    # Group the DataFrame by 'Job' and aggregate subtasks into lists
    grouped_jobs = df.groupby('job')['task'].apply(list)

    # Generate Markdown output
    markdown_output = ""
    for job, task in grouped_jobs.items():
        # Format each job with its subtasks as a bullet point in Markdown
        markdown_output += f"* {job} ({', '.join(task)})\n"

    return markdown_output

def get_crews_jobs_from_template(template, input_crew, input_job):
    """
    This is used to fetch list of available crews and jobs in selected template
    """
    
    crews_list=get_distinct_column_values_by_name(template, 'crews', 'crew')
    for value in crews_list:
        print(value)

    jobs_list=get_distinct_column_values_by_name(template, 'tasks', 'job')
    for value in jobs_list:
        print(value)

    crew = gr.Dropdown(choices=crews_list, label="Select crew")
    job = gr.Dropdown(choices=jobs_list, label="Select job")

    #crews_md =  gr.Markdown(md_list(crews_list))
    #jobs_md =  gr.Markdown(md_list(jobs_list))
    jobs_md = gr.Markdown(get_jobs_details(template))
    
    return (crew, job, jobs_md)

crews_list = list()
jobs_list = list()    
templates_list = list_xls_files_in_dir('.')
crewjobs_list = get_crew_jobs_list('crews/')


with gr.Blocks() as demo:
    gr.Markdown("# Your CREWAI XLS Runner")
    with gr.Row():
        with gr.Column(scale=1, variant="compact"):
            #get_crew_jobs_btn = gr.Button("Get prepared teams and")
            crewjob = gr.Dropdown(choices=crewjobs_list, label="Select team", allow_custom_value=True)
            gr.Markdown("### Specify what exactly needs to be done")
            jobdetails = gr.Textbox(lines=5, label="Job Details")
            run_crew_btn = gr.Button("Run Crew-Job for job details")
        with gr.Column(scale=2):
            gr.Markdown("## Results")
            output = gr.Textbox(lines=20, label="Final output")
            metrics = gr.Textbox(lines=2, label="Usage Metrics")
    with gr.Row():
        with gr.Column(scale=1, variant="compact"):
            gr.Markdown("### Prepare new Crew-Job combination from loaded template")
            template = gr.Dropdown(choices=templates_list, label="1) Select from templates")
            read_template_btn = gr.Button("Get Crews and Jobs defined")
            #crew = gr.Textbox(label="2) Enter Crew")
            crew = gr.Dropdown(choices=crews_list, label="Select crew")
            jobs =  gr.Markdown(f"{jobs_list}")
            #job = gr.Textbox(label="3) Enter Job")
            job = gr.Dropdown(choices=jobs_list, label="Select job")
            setup_btn = gr.Button("Generate Crew-Job combination")
            setup_result = gr.Markdown(".")

            gr.Markdown("### Or load a new configuration template first")
            xls = gr.UploadButton(label="Upload xls crewAI template")
    # with gr.Row():
    #     with gr.Column():
    #         with gr.Accordion("Console Logs"):
    #             # Add logs
    #             logs = gr.Code(label="", language="shell", interactive=False, container=True, lines=30)
    #             #logs = gr.Textbox()
    #             demo.load(logger.read_logs, None, logs, every=1)
    read_template_btn.click(get_crews_jobs_from_template, inputs=[template, crew, job], outputs=[crew, job, jobs])
    setup_btn.click(setup, inputs=[template,crew,job], outputs=[setup_result, crewjob])
    #get_crew_jobs_btn.click(get_crew_job, inputs=[], outputs=[crewjob])
    
    #output = run_crew_btn.click(module_callback,[crew,job, crewjob,jobdetails])
    run_crew_btn.click(run_crew,inputs=[crew,job, crewjob,jobdetails], outputs=[output, metrics])

demo.queue().launch(show_error=True)
#demo.queue().launch(share=True, auth=("brncx", "carine"))