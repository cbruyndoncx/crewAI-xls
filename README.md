# CrewAI excel xls template runner

## CrewAI
A new clean requirements.txt is generated; command is in .sh file

### CrewAI package
Default pip install of the package

### Tools
Default install of the crewai tools

### Langchain
Other langchain packages that are used are listed in requirements.txt

## XLS
Excel format is xlsx, list of sheets are read and loaded.
The actual preparation of the crews is done beforehand as the crew details do not change much once developed.

## Run locally
First get the project dependencies installed
 
`pip install -r requirements.txt`

just run locally as
`python3 main.py`

## Docker
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
