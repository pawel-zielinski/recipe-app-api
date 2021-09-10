# recipe-app-api

## Setup new project (git, GitHub and Docker)

1. Connect to GitHub using SSH: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh
  * Go to your GitHub repository page and copy the SSH URL to your clipboard.
  * Head over to terminal and change the location to **recipe_app_api**.
  * Type ```git clone <COPIED LINK>``` (if any problems, go to 1. step) - this
    command clones GitHub repo to your local machine.
  * ```cd``` to change into the recipe app API folder and then type ```atom .```.
2. Add *Dockerfile* within **recipe_app_api**.
3. Setup *Dockerfile*:
  * First line of the Dockerfile is the image that you are going to inherit
    your Docker file from (list of available images: https://hub.docker.com/).

Note: ```ENV PYTHONUNBUFFERED 1``` - it is recommended to run in unbuffered
      mode when running Python within Docker containers. The reason for this
      is that it does not allow Python to buffer the outputs. It just prints
      them directly.

  * add empty folder within **recipe_app_api** with the name defined in
    the *Dockerfile*.
4. Add *requirements.txt* within **recipe_app_api** and set up dependencies:
  * Head over to *Dockerfile* and add ```COPY ./requirements.txt /requirements.txt```
    to copy the *requirements* file that we are going to create here and copy
    it on the Docker image to */requirements.txt*.
  * Run ```RUN pip install -r /requirements.txt``` to take the *requirements.txt*
    file that we have just copied and it installs it using pip into the Docker
    image.
  * Run ```RUN mkdir /app```, then ```WORKDIR /app``` and then ```COPY ./app /app```
    to create an empty folder, make it as a default directory and copy it from
    your local machine to the **app** folder that we have created on an image.

Note: Following 2 steps are for security purposes.

  * Create a user that is going to run your application using Docker - ```RUN adduser -D user```
    (```-D``` - user is going to be used for running applications only).
  * Switch to the created newly created user - ```USER user```.

5. Build Docker by going to terminal and typing ```docker build .```
   (if *Got permission denied*, try ```sudo usermod -aG docker $USER```
   and then ```newgrp docker```).

6. Create Docker Compose configuration for your project:

Note: Docker Compose is a tool that allows you to run your Docker image easily
      from your project location. It allows you to easily manage the different
      services tat make up your project. For example one service might be the
      Python application that we run, another service migth be the database.

  * Create *docker-compose.yml* file within the root of your project
    (**recipe-app-api** folder):

Note: This file contains the configuration for all of the services that
      make up your project.

---

* `version: "3"`: sets up the version of Docker Compose that we are
  going to use.
* `services:`: defines the services that make up our application.
* `app:`: this is the name of our service.
* `build:`: this is the build section.
* `context: .`: determines that the project in your current directory
  will be a service.
* ports: - "8000:8000": maps your project from port 8000 on your
  host to port 8000 on your image.
* `volumes: - ./app:/app`: allows you to get the updates, that you
  make to our project, into your Docker image in real time. This means
  that whenever you change a file or you change something in the project,
  it will be automatically updated in the container and you do not need
  to restart Docker to get the changes into effect. `- ./app:/app`
  maps the **app** directiory whichyou have in your project to the **app**
  directory in your Docker image.
* `command: > sh -c "python manage.py runserver 0.0.0.0:8000"`: command
  that you are going to use to run your application in your Docker container.
  The `>` is used to break the command into the next line (remember that
  the next line has to be indented by one). `sh -c` stands for running
  a **shell command**.

---

  * Within terminal type `docker-compose build` to build your image using the
    *docker-compose* configuration.

  Note: Alpine is very light version so the process of building should be fast
        as it is additionally cached.

7. Create Django project by running `docker-compose run app sh -c "django-admin.py startproject app ."`.
   (if exceptions are being raised, try course's troubleshoot).

Note: ```sh -c``` is not needed but it makes it clear that we are executing shell
      command.

## Setup automation (Travis-CI)

Note: Travis-CI lets you automate some of the tests and check on your project
      every time you push it to GitHub. For example every time you push a change
      to GitHub you can make it run your Python unit tests and your Python linting.
      So if there is any issue with your code you can see straight away via
      an email notification that the build is broken.

---

### Create account and connect it to GitHub

1. Head over to https://travis-ci.com.
2. Sign up using GitHub account.
3. After redirecting to your *Dashboard* you should see your repos. If not,
   synchronize your GitHub repos to Travis account.

 ---

### Setup project in Travis-CI

1. Find your project on *Dashboard* and *Trigger a build*.
2. Head over to Atom and create *.travis.yml* file within **recipe_app_api**:

Note: *.travis.yml* is the configuration file that tells Travis what to do every
      time you push a change to your project.

---

* `language: python`: tells what language Travis should expect your project
  to be in.
* `python: - "3.6"`: sets the version of the language. This is only for Travis -
  at the end *docker-compose* file determines in which version project will
  be running as it is a configuration file.
* `services: - docker`: tells Travis what services you need to use. All sub
  services are going to be contained within your *docker-compose* file
  configuration.
* `before_install: - echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME --password-stdin`:
  before installation `echo $DOCKER_PASSWORD` prints the password to the screen,
  `docker login --username $DOCKER_USERNAME` calls the Docker login command with
  the username you set in the environment variables* and `--password-stdin`
  accepts the password in a way that prevents it being printed to the screen.

      *Docker have applied a rate limit on pulling images to 100 pulls within 6 hours
      for unauthenticated users and 200 for authenticated users. Because Travis_CI
      uses a shared IP, the 100 pulls is consumed quickly.
      The solution is to authenticate with Docker in the Travis-CI job, so you can take
      advantage of the 200 pulls every 6 hours. You can do it by following the below
      steps:
      1. Register on Docker Hub at https://hub.docker.com/.
      2. Add credentials to Travis-CI project:
        * Login to https://travis-ci.com/ and head over to your project.
        * Choose *More options* > *Settings*.
        * Find *Environment Variables*.
        * Add variables **DOCKER_USERNAME** - the username for your Docker Hub
          account, **DOCKER_PASSWORD** - the password for your Docker Hub account.

* `before_script: pip install docker-compose`: executes before running script.
  This is because you need to install docker-compose.
* `script: - docker-compose run app sh -c "python3 manage.py test && flake8"`:
  specifies the script. You need to run your docker-compose command for running
  your tests. Command also runs linting tool (flake8) which you need to install
  in your project.

3. Open up *requirements.txt* in your project.
4. Add line `flake8>=3.6.0,<3.7.0`.
5. Create new configuration file *.flake8* within your project's root directory.
6. Add line `[flake8]` and `exclude = migrations, __pycache__, manage.py, settings.py`
  to exclude some of the automated scripts and tools that are created by Django
  so it does not fail on the linting when you run that.
