def run_gradio():
    with gr.Blocks(theme='freddyaboulton/dracula_revamped', css="#console-logs { background-color: black; }") as demo:
    #with gr.Blocks(theme=gr.themes.Soft(primary_hue="indigo", secondary_hue="slate")) as demo:
        gr.Markdown("# Your CREWAI XLS Runner")
        gr.Markdown("__Easy as 1 - 2 - 3__")
        with gr.Tab("1 - Download xls Template"):
            with gr.Row():
                with gr.Column(scale=1, variant="compact"):            
                    gr.Markdown("### Available Templates")
                    xls_files = list_xls_files_in_dir(XLS_FOLDER)
                    for xls_file in xls_files:
                        gr.File(value=xls_file, label=os.path.basename(xls_file))
        with gr.Tab("2 - Prepare"):
            #with gr.Accordion("Open to Load and generate crews", open=False):
            with gr.Row():
                with gr.Column(scale=1, variant="compact"):            
                    gr.Markdown("### load a new configuration template")
                    xls_template = gr.File()
                    upload_button = gr.UploadButton("Upload xls crewAI template", file_types=["file"], file_count="multiple")
                    gr.Markdown("### Prepare new Crew-Job combination from loaded template")
                    template = gr.Dropdown(choices=templates_list, label="1) Select from templates")
                    upload_button.upload(upload_file, upload_button, outputs=[xls_template, template])
                    read_template_btn = gr.Button("Get Crews and Jobs defined")
                with gr.Column(scale=2, variant="compact"): 
                    #crew = gr.Textbox(label="2) Enter Crew")
                    crews =  gr.Markdown(f"# CREWS {crews_list}")
                    crew = gr.Dropdown(choices=crews_list, label="Select crew")
                with gr.Column(scale=2, variant="compact"): 
                    jobs =  gr.Markdown(f"# JOBS {jobs_list}")
                    #job = gr.Textbox(label="3) Enter Job")
                    job = gr.Dropdown(choices=jobs_list, label="Select job")
                with gr.Column(scale=1, variant="compact"): 
                    setup_btn = gr.Button("Generate Crew-Job combination")
                    setup_result = gr.Markdown(".")


        with gr.Tab("3 - Run"):
            with gr.Row():
                with gr.Column(scale=1, variant="default"):
                    #get_crew_jobs_btn = gr.Button("Get prepared teams and")
                    gr.Markdown("## Complete the prompt ")
                    crewjob = gr.Dropdown(choices=crewjobs_list, label="Select team", allow_custom_value=True)
                    jobdetails = gr.Textbox(lines=5, label="Specify what exactly needs to be done")
                    input1 = gr.Textbox(lines=1, visible=False, label="input 1")
                    input2 = gr.Textbox(lines=1, visible=False, label="input 2")
                    input3 = gr.Textbox(lines=1, visible=False, label="input 3")
                    input4 = gr.Textbox(lines=1, visible=False, label="input 4")
                    input5 = gr.Textbox(lines=1, visible=False, label="input 5")
                    crewjob.change(get_jobdetails, inputs=[crewjob], outputs=[jobdetails])
                    jobdetails.blur(parse_details, inputs=[jobdetails], outputs=[input1,input2,input3,input4,input5])
                with gr.Column(scale=1, variant="default"):
                    gr.Markdown("##  Hit the button")
                    run_crew_btn = gr.Button("Run Crew-Job for job details")
                    metrics = gr.Textbox(lines=2, label="Usage Metrics")
                with gr.Column(scale=2):
                    gr.Markdown("## Wait for results below")
                    gr.Markdown("#### (or watch progress in the console at the bottom)")
                    output = gr.Textbox(lines=20, label="Final output")

            with gr.Row():
                with gr.Column():
                    with gr.Accordion("Console Logs"):
                        # Add logs
                        logs = gr.Code(label="", language="shell", interactive=False, container=True, lines=30, elem_id="console-logs")
                        demo.load(read_logs, None, logs, every=1)
                        demo.load(read_logs, None, logs, every=1)
                        #logs = gr.Textbox()

        read_template_btn.click(get_crews_jobs_from_template, inputs=[template, crew, job], outputs=[crew, crews, job, jobs])
        setup_btn.click(setup, inputs=[template,crew,job], outputs=[setup_result, crewjob])
        #get_crew_jobs_btn.click(get_crew_job, inputs=[], outputs=[crewjob])
        
        #output = run_crew_btn.click(module_callback,[crew,job, crewjob,jobdetails])
        run_crew_btn.click(run_crew,inputs=[crew,job, crewjob,jobdetails,input1,input2,input3,input4,input5], outputs=[output, metrics])

        log = read_logs()

    demo.queue().launch(show_error=True)
    #demo.queue().launch(share=True, show_error=True, auth=("user", "pwd"))
