# recipe-app-api - Python Django recipe Project

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

> Note: ```ENV PYTHONUNBUFFERED 1``` - it is recommended to run in unbuffered
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

> Note: Following 2 steps are for security purposes.

* Create a user that is going to run your application using Docker - ```RUN adduser -D user```
  (```-D``` - user is going to be used for running applications only).
* Switch to the created newly created user - ```USER user```.

5. Build Docker by going to terminal and typing ```docker build .```
   (if *Got permission denied*, try ```sudo usermod -aG docker $USER```
   and then ```newgrp docker```).

6. Create Docker Compose configuration for your project:

> Note: Docker Compose is a tool that allows you to run your Docker image easily
        from your project location. It allows you to easily manage the different
        services tat make up your project. For example one service might be the
        Python application that we run, another service migth be the database.

* Create *docker-compose.yml* file within the root of your project
  (**recipe-app-api** folder):

> Note: This file contains the configuration for all of the services that
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

> Note: Alpine is very light version so the process of building should be fast
        as it is additionally cached.

7. Create Django project by running `docker-compose run app sh -c "django-admin.py startproject app ."`.
   (if exceptions are being raised, try course's troubleshoot).

> Note: ```sh -c``` is not needed but it makes it clear that we are executing shell
        command.

## Setup Automation (Travis-CI)

> Note: Travis-CI lets you automate some of the tests and check on your project
        every time you push it to GitHub. For example every time you push a change
        to GitHub you can make it run your Python unit tests and your Python linting.
        So if there is any issue with your code you can see straight away via
        an email notification that the build is broken.

### Create account and connect it to GitHub

1. Head over to https://travis-ci.com.
2. Sign up using GitHub account.
3. After redirecting to your *Dashboard* you should see your repos. If not,
   synchronize your GitHub repos to Travis account.

### Setup project in Travis-CI

1. Find your project on *Dashboard* and *Trigger a build*.
2. Head over to Atom and create *.travis.yml* file within **recipe_app_api**:

> Note: *.travis.yml* is the configuration file that tells Travis what to do every
        time you push a change to your project.

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
6. Add lines `[flake8]` and `exclude = migrations, __pycache__, manage.py, settings.py`
  to exclude some of the automated scripts and tools that are created by Django
  so it does not fail on the linting when you run that.

## Test-driven Development - Simple Example

### Unit Test

1. Open up Atom and create *calc.py* file within **app/app**.
2. In that file create a simple *add* function to add two items.
3. In the same directory create *tests.py* file.

> Note: The Django Unit Test Framework looks for any files that begin with *tests*
        and it basically uses them as the tests when you run the *Django run unit tests*
        command. Make sure that any tests are in a folder or a file name that
        begins with *tests*.

4. Within newly created *tests.py* import TestCase - `from django.test import TestCase`.
5. Also import wanted function - `from app.calc import add`.
6. Declare CalcTest class - `class CalcTests(TestCase):`.
7. Define unit test for add function - `def test_add_numbers(self):`.

> Note: Remember that a name of testing method has to start with a word *test*.

8. Test is set up of two components. There usually is the setup stage which is
   where you would set your function up to be tested and then there is the
   assertion which is when you actually test the output and you confirm that
   the output equals what you expected it to equal. So what we are going to do
   is very simple to set up and the assertion can all be done on one line.
   Type `self.assertEqual(add(3, 8), 11)` to basically tell that you want to use
   *add* function to add 3 to 8 and you expect the result to be 11.

9. To run your docker container and test, head over to your terminal and type
   `docker-compose run app sh -c "python3 manage.py test"`.

## Test With Test-driven Development

> Note: Test-driven Development is simply when you write the test before you write
        the code.

1. Our plan is to create a function called *substract* within a *calc.py* file.
   To do that you firstly have to create a new method in */tests.py/CalcTests*
   called *test_substract_numbers*.

> Note: Again - remember that test method has to have word *test* at the beginning.

2. Make an **assertion** that **some kind of input equals some kind of output**.
3. Run `docker-compose run app sh -c "python3 manage.py test"` command in
   terminal to execute tests. Expect it to fail.
4. Head over to *calc.py* file and declare *substract* function (add *pass* in
   definition).
5. Run `docker-compose run app sh -c "python3 manage.py test"` again. Now it
   should fail with different error.
6. Finish definition of *substract* function.
7. Run `docker-compose run app sh -c "python3 manage.py test"` again. Terminal
   should show no errors. This is your goal.
8. Run `docker-compose run app sh -c "python3 manage.py test && flake8"` to check
   for errors and do linting as well just to see that there is no issues with
   the code.

> Note: In case of error like `sh: flake8: not found`, make sure that flake8 is on
        the *requirements.txt* list. Then run `docker-compose build` in terminal.

---

So what's the benefit of writing tests like this? Well the main benefit is that
you know your tests work so there's often cases where you'll write a unit test
and you think it's testing something but really it's not testing something so for
example maybe as I explained earlier you forgot to add the test string
to the beginning of the function name and therefore the test is just never
getting picked up by the test runner and therefore it seems like everything is
working fine but really your test is just not running. So it helps eliminate
those issues from your code also it helps improve the way you think about
your code because before you write the code you're thinking "well I need to
write code that I can test" and in order to do that you have to write basically
high quality code. Usually code that's easy to test is easy to maintain
and it's better quality than code that's just kind of being written without
thinking about the tests in advance.

---

## Configure Django Custom User Model

> Note: To make it clear, last steps connected with TDD were used as examples, so
        you can delete *calc.py* and *tests.py*.

1. Create a core app which will hold all of the central code that is important
   to the rest of the sub apps that you create in your system - open up terminal
   and within **recipe-app-api** folder type `docker-compose run app sh -c "python3 manage.py startapp core"`.

> Note: This app is going to contain anything that is shared between one or more
        apps, so things like the migrations, the database. Putting it in one
        module will make it very clear where the kind of central point of all
        these things is.

2. Delete files that will not be needed - *tests.py*, *views.py*

> Note: Tests are going to be listed in the **tests** folder as it makes it
        clearer where the tests are. You would like to keep all the tests grouped
        in this test folder. You can keep it in a file called *tests.py* but
        because with an app you may have multiple tests you may want to split them
        up into separate test files and you can only have it in a *test.py* file
        or the tests folder. You can not have both. If you have both in there,
        there will be an error. It is recommended putting it in a folder just so
        that it allows you to easily scale up your tests if necessary.

3. Create **tests** folder within the **core** app and add there the
   *\_\_innit.py\_\_* file.

---

### Create Custom User Manager Model

1. Go to *settings.py* and add newly created app.
2. Head over to **tests** and create *test_models.py*.
3. Import *TestCase* from *django.test* and *get_user_model* from *django.contrib.auth*.

> Note: You can import the user model directly from the models but this is not
        recommended with Django because at some point in the project you may want
        to change what your user model is and if everything is using the
        *get_user_model* function then that is really easy to do because you just
        change it in the settings instead of having to change all the references
        to the user model.

4. Declare test class - `class ModelTests(TestCase):`.
5. Create a **test case** - `def test_create_user_with_email_successful(self):`.
6. Create sample email and password variables.
7. Using *get_user_model()* and *create_user()* (which will be a *models.UserManager*
   method) create new user with sample email and password -
   `user = get_user_model().objects.create_user(email=email, password=password)`.
8. Check if the newly created user's email is equal to sample email -
   `self.assertEqual(user.email, email)`.
9. Check if the newly created user's password is equal to sample password -
   `self.assertTrue(user.check_password(password))`.

> Note: You can not check the password the same way as you checked the email
        because the password is encrypted. You can only check it using the
        *check_password* function on your user model. The reason you are using an
        *assertTrue* here is because this *check_password* function is a helper
        function that comes with the Django user model and it basically returns
        True if the password is correct or False if it is not correct.

10. Save the test and head over to terminal to run tests -
    `docker-compose run app sh -c "python3 manage.py test"`.

---

11. Head over to the *models.py* and import *AbstractBaseUser*, *BaseUserManager*
    and *PermissionsMixin* from *django.contrib.auth.models*.
12. Create *UserManager* class which inherits from *BaseUserManager* -
    `class UserManager(BaseUserManager):`.
13. Declare class method *create_user* - `def create_user(self, email, password=None, **extra_fields):`.

> Note: `password=None` in case you want to create a user that is not active.
        `**extra_fields` for additional fields - not required.

14. Create user `user = self.model(email=self.email, **extra_fields)`.

> Note: The way that the management commands work is you can access the model that
        the manager is for by just typing *self.model*. This is effectively the
        same as creating a new user model and assigning it to the user variable.

15. Below this set password - `user.set_password(password)`.

> Note: Remember that password has to be encrypted. So it is important to not
        store it in a clear text.

16. Save the user - `user.save(using=self._db)`.

> Note: `using=self._db` is required for supporting multiple databases.

17. Return user.

---

### Create User Model

1. Create *User* class within *models.py* file. It should inherit from
   *AbstractBaseUser* and *PermissionsMixin*.
2. Add user fields: *email*, *name*, *is_active* and *is_staff*.
3. Assign the UserManager to the object's attribute - `objects = UserManager()`.
4. Add the `USERNAME_FIELD = 'email'` below.

> Note: By defeault the user name field is username and you are customizing that
      to email so you can use an email address.

5. Head over to *settings.py* file, scroll to the bottom and add
   `AUTH_USER_MODEL = 'core.User'` to assign User as the custom user model.

> Recommended: Make migrations - `docker-compose run app sh -c "python3 manage.py makemigrations core"`.

6. Run tests - `docker-compose run app sh -c "python3 manage.py test`. Expect OK.

---

### Normalize Email Address

> Note: This step is not required but is recommended because the domain name for
        email addresses is case-insensitive. Because of that you need to make that
        part all lowercase every time a new user registers.

1. Head over to *test_models.py* and create the *test_new_user_email_normalized*
   method within the *ModelTests* class -`def test_new_user_email_normalized(self):`.
2. Add sample email with domain name all uppercase - `email = 'test@GMAIL.COM'`.
3. Create new user using sample email and password -
   `user = get_user_model().objects.create_user(email, 'admin123')`.
4. Check if normalizing method is working - `self.assertEqual(user.email, email.lower())`.
5. Run test - `docker-compose run app sh -c "python3 manage.py test`. Expect fail.

---

6. Head over to *models.py* and change the logic of *user* variable using
   *normalize_email* to `user = self.model(email=self.normalize_email(email), **extra_fields)`.

> Note: *normalize_email* is a helper function that comes with the BaseUserManager.

7. Run test - `docker-compose run app sh -c "python3 manage.py test`. Expect OK.

---

### Add Validation For Email Field

1. Head over to *test_models.py/ModelTests*.
2. Create new class method called *test_new_user_invalid_email*.

> Note: You want to make sure that if you call the *create_user* function and you
        do not pass an email address (if you just pass a blank string or non value),
        there will be raised ValueError saying that email address was not provided.

3. Use `self.assertRaises` and add `ValueError` as an argument. Anything that
   you run in here should raise the value error - `with self.assertRaises(ValueError):`.
4. Create sample user with no email - `get_user_model().objects.create_user(None, 'admin123')`.

---

5. Head over to *models.py* and within *create_user* method, at the beginning
   of the method's logic, add
```
if not email:
    raise ValueError('Users must have an email address')
```   
6. Run test - `docker-compose run app sh -c "python3 manage.py test`. Expect OK.

---

### Add Support For Creating Superusers

> Note: Now that you have your *create_user* method finished, there is just one
        more method that you need to add to your user model manager and that is
        the *create_superuser* method. *create_superuser* is a function used
        by to Django CLI when you are creating new users using command line.
        You want to make sure it is included in your custom user model so that you
        can take advantage of the Django management command for creating a super user.

1. Head over to *test_models.py/ModelTests* and create *test_create_new_superuser*
   method.
2. Within that method create superuser using *create_superuser()* sample email,
   password - `user = get_user_model().objects.create_superuser('test.gmail.com', 'admin123')`.
3. Use `assertTrue` to check if newly created sample superuser *is_superuser* and
   *is_staff* - `self.assertTrue(user.is_superuser)` and `self.assertTrue(user.is_staff)`.

> Note: `is_superuser` is a part of the PermissionsMixin so it actually is a part
        of the user.

---

4. Go to *models.py/UserManager* and create new method called *create_superuser* -
   `def create_superuser(self, email, password):`.

> Note: Because you are only really going to be using the *create_superuser* with
        command-line, you do not need to worry about the extra fields.

5. Create user using *create_user* - `user = self.create_user(email, password)`.
6. Set user to be a staff and a superuser - `user.is_staff = True`
   and `user.is_superuser = True`.
7. Because you modified the user, you need to save it - `user.save(using=self._db)`.
8. Return user.
9. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
   Expect OK.

> Recommended: Push to GitHub.
