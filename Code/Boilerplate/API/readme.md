Server-
    main.py -> Our main server starting, includes all the middlewares & routes. Refer https://gitlab-in.globallogic.com/hitachigenai/accelerator/-/blob/dev/Code/Boilerplate/API/api.py?ref_type=heads
Controller-
    service.py -> All the api endpoints will be here
Data Adapter-
    meta.json -> The conf json file having 
Models-
    service.py -> 
Service-

    Core - 
        Logging -
            logging.py
        Config -
            config.py
        Exceptions -
            class_exceptions.py
        Middlewares (Classes)-
            auth.py
            logging.py
            exception.py
            config.py

    Domain - Service

scripts-
tests-
utils-
DockerFile
version.json
readme.md
requirements.txt
.env.example
.gitignore