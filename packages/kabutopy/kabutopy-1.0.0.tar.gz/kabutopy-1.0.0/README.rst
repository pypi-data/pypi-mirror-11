Example usage
==============
::

    import time
    from kabutopy.client import Client

    # make a client instance with the base url of the kabuto service
    client = Client("http://localhost:5000")

    # registering a user
    client.register("user", "password", "email@email.com")

    # loging in with a user, the client keeps track of the cookies
    client.login("user", "password")

    # creating an image
    # name: string
    # dockerfile: raw string / open file / path to a file
    # repo_url: string
    # nocache: boolean
    image = client.create_image("my_image", dockerfile="some file", repo_url=None, nocache=False)

    # requesting the image status and image id will poll the server
    # if the id is still empty, or is the status is PENDING
    # it will update id, state and output if the state is SUCCESS
    # it will update state, error and output if the state is FAIL

    while image.status == 'PENDING':
        sleep(1)

    # creating a pipeline
    # name: string
    pipeline = client.create_pipeline("my_pipeline")

    # creating a job
    # command: string
    # image: Image / int / string that is castable to int
    # attachment: open file / path to a file (a list of these things also works when multiple files need to be uploaded)
    # pipeline: Pipeline / int / string that is castable to int
    job = client.create_job(command, image, attachments, pipeline)

    # getting logs
    # job: Job / int / string that is castable to int
    # job_id: int / string that is castable to int
    # you are able to get the logs trough the client
    logs = client.get_job_logs(job)

    # trough the job itself
    # job_id: int / string that is castable to int
    logs = job.get_logs()

    # getting results
    # job: Job / int / string that is castable to int
    # trough the client
    # will return None if the job has not yet started, is still running or has failed
    result = client.get_job_results(job)

    # trough the job itself
    result = job.get_results()


Classes and Methods
===================

Client:
-------

    - register(user, password, email)
    - login(user, password)
    - create_image(name, dockerfile=None, repo_url=None, nocache=False) returns Image
    - create_pipeline(name) returns Pipeline
    - create_job(command, image, attachments, pipeline) returns Job
    - submit_pipeline(pipeline)
    - get_job_logs(job, log_id=None) returns Log
    - get_job_results(job, pipeline=None) returns None or ByteIO
    - load_image(self, eid) returns loaded Image
    - load_pipeline(self, eid) returns loaded Pipeline
    - load_job(self, eid, pipeline) returns loaded Job

Image:
------

    - classmethod:load(eid) returns loaded image

Pipeline:
---------

    - submit()
    - classmethod:load(eid) returns loaded pipeline

Job:
----

    - get_logs(log_id=None) returns Log
    - get_results() returns None or ByteIO
    - classmethod:load(eid, pipeline) returns loaded job

Log:
----

    - readlines(raw=True) returns lines or (line_id, line) if raw is False
    - refresh()
