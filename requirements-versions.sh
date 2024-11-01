# this is a very long list of any installed even unused packages
#conda list --export > requirements-export.txt

# this documents the versions of all used packages
pip freeze > requirements-pip-freeze.txt

# this only keeps the essentials, update this list as required for troubleshooting
grep -E "crew|gradio|Jinja2|langchain|langchain-community|langchain-groq|langchain-openai|mdpdf|openai|openpyxl|pandas|python-dotenv|Requests|unstructured" requirements-pip-freeze.txt >> req.txt

# this only documents the versions of actually used packages into requirements.txt
mv requirements.txt requirements.bak
mv requirements-versions.txt requirements-versions.bak
pipreqs --ignore src/templates .
mv requirements.txt requirements-versions.txt

pipreqs --ignore src/templates --mode no-pin .

exit

#####################################################################################
pipreqs - Generate pip requirements.txt file based on imports

Usage:
    pipreqs [options] [<path>]

Arguments:
    <path>                The path to the directory containing the application
                          files for which a requirements file should be
                          generated (defaults to the current working
                          directory).

Options:
    --use-local           Use ONLY local package info instead of querying PyPI.
    --pypi-server <url>   Use custom PyPi server.
    --proxy <url>         Use Proxy, parameter will be passed to requests
                          library. You can also just set the environments
                          parameter in your terminal:
                          $ export HTTP_PROXY="http://10.10.1.10:3128"
                          $ export HTTPS_PROXY="https://10.10.1.10:1080"
    --debug               Print debug information
    --ignore <dirs>...    Ignore extra directories, each separated by a comma
    --no-follow-links     Do not follow symbolic links in the project
    --encoding <charset>  Use encoding parameter for file open
    --savepath <file>     Save the list of requirements in the given file
    --print               Output the list of requirements in the standard
                          output
    --force               Overwrite existing requirements.txt
    --diff <file>         Compare modules in requirements.txt to project
                          imports
    --clean <file>        Clean up requirements.txt by removing modules
                          that are not imported in project
    --mode <scheme>       Enables dynamic versioning with <compat>,
                          <gt> or <non-pin> schemes.
                          <compat> | e.g. Flask~=1.1.2
                          <gt>     | e.g. Flask>=1.1.2
                          <no-pin> | e.g. Flask
    --scan-notebooks      Look for imports in jupyter notebook files.
#####################################################################################
