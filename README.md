# recipe-app-api

# Setup new project (git, GitHub and Docker)

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

    - ```version: "3"```: sets up the version of Docker Compose that we are
      going to use.
    - ```services:```: defines the services that make up our application.
    - ```app:```: this is the name of our service.
    - ```build:```: this is the build section.
    - ```context: .```: determines that the project in your current directory
      will be a service.
    - ```ports: - "8000:8000"```: maps your project from port 8000 on your
      host to port 8000 on your image.
    - ```volumes: - ./app:/app```: allows you to get the updates, that you
      make to our project, into your Docker image in real time. This means
      that whenever you change a file or you change something in the project,
      it will be automatically updated in the container and you do not need
      to restart Docker to get the changes into effect. ```- ./app:/app```
      maps the **app** directiory whichyou have in your project to the **app**
      directory in your Docker image.
    - ```command: > sh -c "python manage.py runserver 0.0.0.0:8000"```: command
      that you are going to use to run your application in your Docker container.
      The ```>``` is used to break the command into the next line (remember that
      the next line has to be indented by one). ```sh -c``` stands for running
      a **shell command**.
  * Within terminal type ```docker-compose build``` to build your image using the
    *docker-compose* configuration.

  Note: Alpine is very light version so the process of building should be fast
        as it is additionally cached.

7. Create Django project by running ```docker-compose run app sh -c "django-admin.py startproject app ."```.
   (if exceptions are being raised, try course's troubleshoot).

Note: ```sh -c``` is not needed but it makes it clear that we are executing shell
      command.
