from dotenv import load_dotenv
load_dotenv()

#os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")
#os.environ["OPENAI_ORGANIZATION"] = config("OPENAI_ORGANIZATION_ID") 

# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    print("## Welcome to Crew AI XLS Crew ##")
    print("---------------------------------")
    #input_details = input(dedent("""Specify your job details: """))
    input_details = "My name is Carine"

    #select_language = input(dedent("""Specify the language to use: """))
    # Got Error
    #select_language='en'
    select_language='en'

    custom_crew = CustomCrew(input_details, select_language)

    #function calls asoff v0.22.5 in docstrings
    #help(custom_crew)
    #help(custom_crew.agents)
    #help(custom_crew.tasks)


    result = custom_crew.run()
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)
