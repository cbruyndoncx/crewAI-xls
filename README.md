# CrewAI excel xls template runner

## Intro
This repository contains code to load crewAI configuration usin gq Grqdio UI from excel xls and generate the python code for a crew-job combination. A job is a sequence of tasks. 
The source of the crews is defined in the xls. It allows for quick prototyping and iterations without having to edit code,
There is a set of basic agents which have tools defined. This is only a subset of what currently is available through crewai tools. 

## Prerequisites

### CrewAI
A new clean requirements.txt is generated; command is in .sh file

#### CrewAI package
Default pip install of the package

#### Tools
Default install of the crewai tools

#### Langchain
Other langchain packages that are used are listed in requirements.txt

### XLS
Excel format is xlsx, list of sheets are read and loaded.
The actual preparation of the crews is done beforehand as the crew details do not change much once developed.

### API Keys
API keys need to be provided as part of the environment, both running straight from source and when using docker container eg when hosting on render.com

## Run locally
First get the project dependencies installed
 
`pip install -r requirements.txt`

just run locally as
`python3 main.py`

and follow the gradio instructions on screen to open your browser and use the UI.

## Run in Docker container
To allow easy deployment a docker image is provided;

### Building and running your application

When you're ready, start your application by running:
`docker compose up --build`.

Your application will be available at http://localhost:8000.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)

## Screenshots

### Browser GradioUI

#### Optional Step 1 Downloading and uploading xls template files
![ui step 1 xls](./docs/screenshots/ui_step_1_xls.png)

#### Optional Step 2
##### Select xls configuration
![ui step 2A select xls](./docs/screenshots/ui_step_2A_select_xls.png)

##### Select a crew and job combination to generate crew for
![ui step 2B select combi](./docs/screenshots/ui_step_2B_select_combi.png)

#### Straight to Step 3 if nothing changed in xls
##### Select job to run from generated crews
![ui step 3A Run Job](./docs/screenshots/ui_step_3A_Run_Job.png)

##### Job is selected and default prompt is provided
![ui step 3B Select Job](./docs/screenshots/ui_step_3B_Select_Job.png)

##### Provide specific additional inputs
![ui step 3C provide input](./docs/screenshots/ui_step_3C_provide_input.png)

##### Wait for final results and see detailed logging
![ui step 3D logging downloads](./docs/screenshots/ui_step_3D_logging_and_dwnloads.png)


### Excel xls
The excel file contains the complete setup to run a crew.
Please note , not all parameters are implemented yet, but most are and up-to-date with version 0.41 from crewAI.
> Supporting additonal parameters entails adding the column, matching the name to the template {variable} taking care of quoteds strings when needed. If something more fancy is needed, you have to either add to the generate_crew code, or within the class constructor. 

#### LLM providers and models
Defining the providers and available models.
The templates/llm_class_template.py has the import statement for the provider.
To support additional providers, you need to add these to the class template, additional models for already configured providders, you only need to add a row in the xls sheet with the details.

![LLM providers and models](./docs/screenshots/xls_llms.png)

#### Jobs to be done and task definitions
To stick to crewAI terminology, a job is a collection of tasks

![Jobs to be done](./docs/screenshots/xls_jobs.png)

![Jobs consisting of multiple tasks](./docs/screenshots/xls_tasks.png)

> The xls contains the trip planner example, other jobs and tasks are development test cases, not necessarily working well.

#### Crews and crewmembers
Crews are defined to tackle specific jobs.
Agens have the tools and are assebled into crews.

![Crews are defined to tackle specific jobs](./docs/screenshots/xls_crews.png)

![Agents have the tools and can be specified at the task level](./docs/screenshots/xls_agents.png)

![For a specifc job a crewmembers are assembled from the available agents.](./docs/screenshots/xls_crewmembers.png)
