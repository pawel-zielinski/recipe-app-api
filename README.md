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
* `script: - docker-compose run app sh -c "python manage.py test && flake8"`:
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

6. Run test - `docker-compose run app sh -c "python3 manage.py test`. Expect OK.

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

## Set Up Django Admin

### Add Tests For Listing Users In Django Admin

> Note: Now you are going to update you Django admin so that you can manage your
        custom user model. This will give you a nice easy interface that you can
        use to log in and see which users have been created, create users or make
        changes to existing users.

1. Create a new file within **tests** directory and name it *test_admin.py*.
2. Import *TestCase* and *Client* from *django.test*, *get_user_model* from
   *django.contrib.auth* and *reverse* from *django.urls*.

> Note: *reverse* is is a helper function which will allow you to generate URLs
        for your Django admin page. *Client* will allow you to make test requests
        to your application in your unit tests. Django documentation:
        https://docs.djangoproject.com/en/2.2/topics/testing/tools/#overview-and-a-quick-example

3. Create test class: `class AdminSiteTests(TestCase):`.

---

#### Add setUp Method

1. Create *setUp* method: `def setUp(self):`.

> Note: *setUp* method is a method that is ran before every test that you run.
        So sometimes there are setup tasks that need to be done before every
        test in your TestCase class. You can do this using *setUp* method.

This *setUp* method is going to consist of creating your test client. You are
going to add a new user that you can use. To test you are going to make sure the
user is logged into your client. Finally you are going to create a regular user
that is not authenticated or that you can use to list in your admin page.

2. Create a *client* variable accessible in the other tests: `self.client = Client()`.
3. Create an *admin_user* variable accessible in the other tests:
```python
self.admin_user = get_user_model().objects.create_superuser(
        email='admin@gmail.com',
        password='admin123'
    )
```
4. Log in an *admin_user* using the Client helper function that allows you to log
   a  user in with the Django authentication.

> Note: This really helps make your tests a lot easier to write because it means
        you do not have to manually log the user in. You can just use this helper
        function.

5. Next create a *user* variable accessible in the other tests:
```python
self.user = get_user_model().objects.create_user(
        email='test@gmail.com',
        password='admin123',
        name='Sample Name'
    )
```

Now you have a *client*, an *admin* (the *admin* is logged into the client) and
a spare user that you can use for testing listing and things like that.

---

#### Add Tests For Listing Users

> Note: Now you have to test that the users are listed in your Django admin. The
        reason you need to add a test for this is because you need to slightly
        customize the Django admin to work with your custom user model. The
        default user model expects a username and as such the default Django
        admin for the user model also expects a username witch you do not have.
        You have the email address instead. You need a few small changes to your
        *admin.py* file just to make sure it supports your custom user model.

1. Create a new test called *test_users_listed*: `def test_users_listed(self):`.
2. Within this method create the URL first, using the *reverse* helper function:
   `url = reverse('admin:core_user_changelist')`.

> Note: The way that you use *reverse* is you simply type the app that you are
        going for ()`admin`), then `:` and the URL that you want (`core_user_changelist`).
        These URLs are actually defined in the Django admin documentation
        (https://docs.djangoproject.com/en/2.1/ref/contrib/admin/). Basically
        what this will do is it will generate the URL for your list user page.
        The reason you use this reverse function instead of just typing the URL
        manually is because if you ever want to change the URL in a future it
        means you do not have to go through and change it everywhere in you test
        because it should update automatically based on reverse.

3. Create a *response* variable as a *client's* reaction on the URL:
   `res = self.client.get(url)`.

> Note: This will use you test client to perform a HTTP GET on the URL.

4. Use assertion to check if response matches with the logged user's name and
   email: `self.assertContains(res, self.user.name)` and
   `self.assertContains(res, self.user.email)`.

> Note: The *assertContains* assertion is a Django custom assertion that will
        check that your response here contains a certain item. It also has some
        additional checks that it does that are not quite clear from just this
        lines. What it does is it checks that the HTTP response was *HTTP 200*.
        It also looks into the actual content of this *res* because it is an
        object so it is intelligent enough to look into the actual output that
        is rendered and to check for the contents there.

5. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

### Modify Django Admin To List Your Custom User Model

1. Go over to *admin.py* file and import the default Django user admin to change
   some of the class variables to support your custom user admin:
   `from django.contrib.auth.admin import UserAdmin as BaseUserAdmin`.
2. Import *models* from your *core* API: `from core import models`.
3. Create Custom user admin class: `class UserAdmin(BaseUserAdmin):`.
4. Change the ordering to the ID: `ordering = ['id']`.
5. Set *list_display* to show email and name: `list_display = ['email', 'name']`.
6. Register your *custom user model* and newly modified *user admin model*:
   `admin.site.register(models.User, UserAdmin)`.
7. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
   Expect OK.

---

### Modify Django Admin To Support Changing User Model

> Note: Next you need to check if the "change user" page renders correctly.

1. Create a new test called *test_user_change_page*:
   `def test_user_change_page(self):`.
2. Generate a URL which will depend on ID of which user we want to access:
   `url = reverse('admin:core_user_change', args=[self.user.id])`.

> Note: The *reverse* function will create a URL like this: /admin/core/user/<ID>.
        This <ID> is how the *args* work in the *reverse* function. So basically
        anything you pass in here will get assigned to the argument of the URL,
        here at the end.

3. Do an HTTP GET on the URL and assign it to variable: `res = self.client.get(url)`.
4. Test that this page renders okay: `self.assertEqual(res.status_code, 200)`.

> Note: A status code for the response that your client gives is HTTP 200, which
        us a status code for "okay". So the page worked.

5. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

Now you need to customize your user admin *fieldsets* to support your custom model
as opposed to the default model that it is expecting.

6. Head over to the *admin.py/UserAdmin*.
7. Add *fieldsets* class variable:
```python
fieldsets = (
      (None, {'fields': ('email', 'password')}),
      (_('Personal Info'), {'fields': ('name',)}),
      (
          _('Permissions'),
          {'fields': ('is_active', 'is_staff', 'is_superuser')}
      ),
      (_('Important dates'), {'fields': ('last_login',)})
  )
```
*Fieldsets* are based on sections. So as you can see you have 4 sections:
* `(None, {'fields': ('email', 'password')}),`: `None` because this is the title
  for the section and you do not need this. This section will contain `email` and
  `password`.

> Note: Before you create next section you need to import the *gettext* as *_*
        from *django.utils.translation*. This is recommended convention for
        converting strings in your Python to human readable text. The reason you
        do this is just so it gets passed through the translation engine.

* `(_('Personal Info'), {'fields': ('name',)}),`: This section is for personal
  information. This will contain only `name`.
* `(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),`:
  This is a permission section which contains fields like `is_active`, `is_staff`
  and `is_superuser`.
* `(_('Important dates'), {'fields': ('last_login',)})`: This section is called
  `Important dates` and it contains a field of a date that the user was last
  logged in.

> Note: If you ever want to add extra fields to your user model, just add them here.

8. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
   Expect OK.

---

### Modify Django Admin To Support Creating Users

> Note: There is one last thing you need to change in your Django admin before
        it will work with your custom user model and that is the **add** page.

1. Head over to tests and create a new method called *test_create_user_page*:
   `def test_create_user_page(self):`.
2. Create the URLs variable: `url = reverse('admin:core_user_add')`.

> Note: `core_user_add` is the standard URL alias for the add page for your
        user model.

3. Create variable with client's try of making HTTP GET to this *url*:
   `res = self.client.get(url)`.
4. Check if this response is correct: `self.assertEqual(res.status_code, 200)`.
5. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

6. Head over to *admin.py/UserAdmin*.
7. Create *add_fieldsets* variable:
```python
add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('email', 'password1', 'password2')
      }),
  )
```

> Note: The user admin by default takes an *add_fieldsets* which defines the
        fields that you include on the add page which is the same as the create
        user page.

All you are doing here is customizing this fieldset to include your email address,
password1 and password2, so you can create a new user in the system with a very
minimal data that is required and then if you want to add extra fields like the
name and customize that stuff later, you can do that in the *Edit Page*.

This *add_fieldsets* variable that you have created, has one section with no name -
`None` - because it is going to be very small and you are not going to be creating
multiple tiles. Then in `{}` brackets there is a definition of the fields that you
include in the form. These are just a defaults from the user admin documentation -
`'classes': ('wide', ),`. Then you add fields that you want in that form -
`'fields': ('email', 'password1', 'password2')`.

8. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
   Expect OK.

> Recommended: Push to GitHub.

---

## Set Up Database - Postgres

> Note: In this section you are going to set up your Django project to use
        Postgres instead of the default sqlite database.

### Add Postgres To Docker Compose

> Note: You are going to start by making some changes to your *docker-compose.yml*
        file that allow you to create a database service and also pass in some
        database settings into both your app and the database that you are going
        to run.

1. Start by opening up the *docker-compose.yml* file.
2. Add the database service: `db:` (on the `app:` level as an another service).
3. Add an image `image: postgres:10-alpine`.

> Note: This locates the Postgres image on DockerHub and it pulls down the
        version with the tag 10 alpine. So this is a lightweight version of the
        Postgres SQL version 10 of the image. See all available configuration
        options which can be passed in as environment variables of that image -
        https://docs.docker.com/compose/environment-variables/.

4. Define environment variables (`environment:`):
* Database name: `- POSTGRES_DB=app`.
* Username: `- POSTGRES_USER=postgres`.
* Password: `- POSTGRES_PASSWORD=supersecretpassword`.

> Note: You would not use the same password here that you would use on a production
        system. What you would do in production is on your build server or whatever
        is building your application like Jenkins or Travis you would the add an
        encrypted environment variable that overrides this when you push your
        application.

5. To modify your app service to set some environment variables and also depend
   on your DB service, start by adding `environment:` within `app:`.
6. Then add:
* Host: `- DB_HOST=db` (it has to be equal to the name of the service
   that runs your database).
* Name: `- DB_NAME=app` (it has to be equal to your *POSTGRES_DB*).
* Username: `- DB_USER=postgres`.
* Password: `- DB_PASS=supersecretpassword` (same to the one that you have created
  in point 4.).
7. Add *depends_on* within *app* service: `depends_on:`. Set it to *db*: `- db`.

> Note: When you run *docker-compose* you can set different services to depend
        on other services. You want your app service to depend on the database
        service that you create here. What this means is two things:
        1. The *database* service will start before the *app* service.
        2. The *database* service will be available via the network when you use
           the hostname DB. So when you are inside you *app* service you can
           connect to the hostname DB and then it will connect to whatever
           container is running on your DB service.

---

### Add Postgres Support To Dockerfile

> Note: Next you are going to add Postgres support to your DockerFile. You
        basically need to install the Python package that is used for Django to
        communicate with Docker and in order to do this you are going to have to
        add some dependencies to your Dockerfile during the build process. So
        what you need to do is you need to update your *requirements.txt* file
        to add the necessary package and then you need to make some small
        changes to your Dockerfile to add the dependencies required to install
        these packages.

1. Open up *requirements.txt* file.
2. The package that Django recommends for communicating between Django and
   Postgres is called **psycopg2**. Add the version between 2.7.5 (including)
   and 2.8.0: `psycopg2>=2.7.5,<2.8.0`.
3. Head over to *Dockerfile* and between `COPY ./requirements.txt /requirements.txt`
   and `RUN pip install -r /requirements.txt` add:
* `RUN apk add --update --no-cache postgresql-client`: installs the PostgreSQL
  client. It uses the package manager that comes with Alpine. `--update` means
  to update the registry before you add PostgreSQL. `--no-cache` means to do not
  store the registry index on your Dockerfile. The reason you do this is because
  you really want to minimalize the number of extra files and packages that are
  included in your Docker container. This is best practice because it means that
  your Docker container for your application has the smallest footprint possible
  and it also means that you do not include any extra dependencies or anything
  on your system which may cause unexpected side effects or it may even create
  security vulnerabilities in your system.
* `RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev`: installs some temporary packages that need to be
  installed on the system while you run your *requirements.txt*. `--virtual`
  sets up an alias for your dependencies that you can use to easily remove all
  those dependencies later after *requirements* installation
  (alias: `.tmp-build-deps`).

> Note: This is all part of making sure your Dockerfile has the absolute minimal
        footprint possible. You do not want any extra dependencies in your
        Dockerfile unless they are absolutely necessary.

4. After the `RUN pip install -r /requirements.txt` add `RUN apk del .tmp-build-deps`
   to remove the temporary packages.
5. Head over to terminal and type `docker-compose build` to make sure that your
   image can build successfully.

---

### Configure Database In Django

> Note: Now, that you have Docker all set up, you can go ahead and configure
        your Django project to use your Postgres database.

1. Head over to the *settings.py* and find *DATABASES* variable.
2. Remove `'ENGINE': 'django.db.backends.sqlite3',` and
   `'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),`.
3. Instead of these 2 lines add:
* `'ENGINE': 'django.db.backends.postgresql',`: sets up the database engine that
  your are going to use.
* `'HOST': os.environ.get('DB_HOST'),`: sets up the host.
* `'NAME': os.environ.get('DB_NAME'),`: sets up the name.
* `'USER': os.environ.get('DB_USER'),`: sets up the username.
* `'PASSWORD': os.environ.get('DB_PASS'),`: sets up the password.

> Note: The benefit of this is that you can easily change your configuration
        when you run your app on different servers by simply changing them in
        the environment variables and you do not have to make any changes to
        your source code in order to modify the hostname, the name, the username
        or the password. This makes it really useful when running your
        application in production because you can simply upload your Dockerfile
        to a service like Amazon ECS or Kubernets and you can just set the
        appropriate environment variables and then application should work.

## Waiting For Postgres To Start & Mocking

### Mocking

In this section you are going to use an advanced area of testing called *mocking*.
**Mocking is when you override or change the behavior of the dependencies of the**
**code that you are testing**. We use mocking to **avoid any unintended side effects**
and also to **isolate the specific piece of code that we want to test**. For example
imagine you are testing a function that sends an email. There are two good
reasons that you would not want to actually send an email every time you run
your tests:
1. The first reason is that **you should never write tests that depend on external services**.
   This is because you can not guarantee that these services will be available
   at the point that you run the test. This makes the test **unpredictable**
   and **unreliable**.
2. The second reason is you do not want to be **sending spam emails** each time
   you run your test suite. Even if you are using a fake address, those emails
   would still be backing up on a server somewhere.

When you write your test you can use mocking to avoid sending an actual email.
You can override the function in dependency that sends the email and replace it
with a mock object. Using this mock object you can avoid sending an actual email
and instead just check that the function was called with the correct parameters.

---

### Add Tests For wait_for_db Command

> Note: In this part you are going to add a test for management command.
        Management command is going to be a helper command that allows you to
        wait for the database to be available before continuing and running other
        commands. This command will be used in your *docker-compose.yml* file
        when starting your Django app. The reason that you need this command is
        because it seems that sometimes when using Postgres with docker-compose
        in a Django app, the Django app fails to start because of a database
        error. It turns out that this is because once the Postgres service has
        started there are a few extra setup tasks that need to be done on the
        Postgres before it is ready to accept connections. What this means is
        your Django app will try and connect to your database before the
        database is ready and therefore it woll fail with an exception and you
        will need to restart the app. To improve the reliability of your project
        you are going to add this helper command that you can put in front of
        all of the commands you have run in docker-compose and that will ensure
        that the database is up and ready to accept connections before you try
        and access the database. This will make your application a lot more
        reliable when running it locally as a development server and also if you
        ever deploy it as a production system.

1. Head over to **test** folder and create a new *test_commands.py* file which
   will contain tests for commands.
2. Do some imports:
* `from unittest.mock import patch`: this is going to allow you to mock the
  behavior of the Django "get database" function.

> Note: You can basically simulate the database being available and not being
        available for when you test your command.

* `from django.core.management import call_command`: allows you to call the
  command in your source code.
* `from django.db.utils import OperationalError`: this is an error that Django
  throws when the database is unavailable. You are going to use this error to
  simulate the database being available or not when you run your command.
* `from django.test import TestCase`.
3. Create a *CommandTests* class - `class CommandTests(TestCase):`.
4. Add method to test the scenario when you want to connect to the database when
   it is already available:
* Definition: `def test_wait_for_db_ready(self):`.

> Note: To setup you test here you need to simulate the behavior of Django when
        the database is available. Your management command is going to basically
        try and retrieve the database connection from Django and it is going to
        check if when you try and retrieve it, it retrieves an *OperationalError*
        or not. So if it retrieves an *OperationalError* then the database is not
        available. If an *OperationalError* is not thrown, then the database is
        available and the command will continue. To setup the test you are going
        to override the behavior of the *ConnectionHandler* and you are just going
        to make it return True and not throw any exception and therefore your
        call command (or your management commands) should just continue and allow
        you to continue with the execution flow.

* Use the *patch* to mock the *ConnectionHandler* to just return *True* every
  time  it is called: `with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:`.

> Note: As you will find when you create your management command, the way that
        you tested the database is available in Django, is you just try and
        retrieve the default database via the *ConnectionHandler*. The location
        of the code that is being called is in this
        `django.db.utils.ConnectionHandler` module and the function that is
        actually called when you retrieve the database is `__getitem__`.
        You are going to mock this behavior using *path* which is assigned as
        a variable called *gi*.

* `gi.return_value = True`: mock the returned value. Whenever this is called
  during your test execution, instead of actually before performing whatever
  behavior this does in Django, it will override it and just replace it with
  a mock object which does two things. One of them is it will just return this
  value that you specify here (*True*) and the second thing is it allows you to
  monitor how many times it was called and the different calls that were made
  to it.

* `call_command('wait_for_db')`: call the tested `wait_for_db` command.
* `self.assertEqual(gi.call_count, 1)`: assertion if the command was executed
  as planned. If the database was available all the time, the `wait_for_db`
  command should be executed only once.

5. Add method to test the scenario when you want to connect to the database when
   it is not available for 5 seconds:
* Decorator: `@patch('time.sleep', return_value=True)`. What this mock does here
  is it replaces the behavior of *time.sleep* and just replaces it with a mock
  function that returns *True*. That means during your test it will not actually
  wait the second or however long you have it to wait in your code. The reason
  you do this is simply just to speed up the test when you run them because if
  you are checking the database five times then that is five extra seconds that
  it would take to run your test.

> Note: The way the management command is going to work is it is going to be a while
        loop that checks to see if the *ConnectionHandler* raises the
        *OperationalError*. Then it is going to wait a second and then try again.
        This is just so that it does not flood the output by trying every
        microsecond to test fro the database. It adds a little delay there and
        you can actually remove that delay in your unit test by adding this
        decorator to mock the `time.sleep`. When you use *patch* as a decorator
        you can actually pass in the *return_value* as part of the function
        call. *Patch* as a decorator does pretty much the same thing as you do
        with *with* expression. This decorator also passes in the argument to
        your function so you have to remember to add it to your function's
        parameters even if you will not use it.

* Declaration: `def test_wait_for_db(self, ts):` (`ts` is a parameter for
  decorator's variable).
* `with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:`.
* Add a *side_effect*. The Python unit tests mock module has a really useful
  option where you can set a side effect to the function that you are mocking.
  Use it to raise the *OperationalError* 5 times and then on the sixth time
  just return: `gi.side_effect = [OperationalError] * 5 + [True]`.
* Call your command: `call_command('wait_for_db')`. It should have been called
  the first five times to wait and then it should on the sixth time have been
  successful.
* Check that using assertion: `self.assertEqual(gi.call_count, 6)`. There should
  simply be 6 calls of the `__getitem__` - 5 times *OperationalError*, 1 time
  OK and return.

6. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
   Expect fail.

---

### Add wait_for_db Command

> Note: Now you can go ahead and create your wait_for_db management command.

1. Create the dictionary in your **core** app. You are going to store your
   management commands in here. Call it **management**.

> Note: This is the Django convention and it is recommended on the Django website
        to put all of your commands in a directory called **management/commands**
        within your **core** app.

2. Create file *\_\_init\_\_.py* in that folder.
3. Create a **management/commands** folder and add there an *\_\_init\_\_.py* file.
4. Within **commands** create a *wait_for_db.py* app.
5. Do some imports:
* `import time`: you will use that to make your applications for a few seconds
  in between each database check.
* `from django.db import connections`: you can use it to test if the database
  connection is available.
* `from django.db.utils import OperationalError`: this error will be thrown when
  the database will not be available.
* `from django.core.management.base import BaseCommand`: the class that you need
  to build on, in order to create your custom command.
  (More about custom managment commands - https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/#module-django.core.management)
6. Create a *Command* class according to the convention: `class Command(BaseCommand):`.
7. Create a class method called *handle*: `def handle(self, *args, **options):`.

> Note: `*args` and `**options` allow you to pass in custom arguments and options
        to your management commands.

8. Add line to print message while executing command: `self.stdout.write('Waiting for database...')`.
9. Assign a variable called *db_conn*: `db_conn = None` (it can also equal
   empty string or *False*).
10. Open *while* loop in which connection attempts will be made: `while not db_conn:`.
11. Open *try/except* expression to try to connect to the database:
* Try to set *db_conn* to the database connection:
```python
try:
  db_conn = connections['default']
```
* If there is no connection, raise *OperationalError* exception: `except OperationalError:`:
  - Write a message that will be displayed in terminal: `self.stdout.write('Database unavailable, waiting 1 secound...')`.
  - Sleep for 1 second: `time.sleep(1)`.
12. Exit *while* loop and add message: `self.stdout.write(self.style.SUCCESS('Database available!'))`

> Note: So when you run this if Django raises the *OperationalError* then method
        will catch that and is going to output the message. Then it will wait for
        a second and try again. It will continue this process until the database
        is available.

13. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
    Expect OK.

---

### Make Docker Compose Wait For Database

> Note: Now, as you have your wait_for_db command, you can go ahead and configure
        Docker Compose to use this command before it starts your Django app.

1. Head over to the *docker-compose.yml* file.
2. In *app/command* change this command to:
```yml
command: >
  sh -c "python manage.py wait_for_db &&
         python manage.py migrate &&
         python manage.py runserver 0.0.0.0:8000"
```

> Note: `python manage.py wait_for_db` means that your wait_for_db command will
        be executed before starting server. Then there is `python manage.py migrate`
        It is a good idea to run it before starting the server because if you start
        your app without running the migrations you may run into some issues.

3. Head over to terminal and type `docker-compose up` to start your app and run
   migrations. You should see by the messages that the *wait_for_db* is working.
4. Run test - `docker-compose run app sh -c "python3 manage.py test && flake8`.
   Expect OK.

> Recommended: Push to GitHub.

---

### Make Travis-CI Wait For Database

> Note: You might find that Travis is still failing with the *OperationalError*.
        In this section there is a solution for that problem.

1. Head over to *.travis-ci.yml*.
2. In *script* change your script to following one:
   `docker-compose run app sh -c "python manage.py wait_for_db && python3 manage.py test && flake8"`

> Note: This correction should ensure that the app waits for the database to be
        available before running the tests. It is also important to mention that
        there is a difference between *python* and *python3* while writing those
        scripts and you should stick to this instruction.

3. You can test if the server is working by going to your browser and heading
   over to *127.0.0.1:8000*.
4. Head over to *127.0.0.1:8000/admin/* to check if you can access admin panel.
5. You can create a superuser by typing
   `docker-compose run app sh -c "python manage.py createsuperuser"` in your
   terminal.
6. After creating superuser you can login to admin panel. Check if everything
   is working.

## Create User Management Endpoints

> Note: In this section you are going to create your *manage user* endpoints.
        These endpoints are going to allow you to create and update users, to
        change a user's password and to create user authentication tokens which
        can be used to authenticate requests to the other APIs in your project.

### Create Users App

1. Open up terminal and run
   `docker-compose run --rm app sh -c "python manage.py startapp user"`
   command within **recipe-app-api** directory.

> Note: `--rm` removes the container after it has ran the command. This is
        optional on any command that you just want to run once and you do not
        want the docker container to linger on the system after it's ran.
        It should basically remove the container and just keep the system
        a little cleaner so it does not fill up.

2. Clean up a little bit by removing **migrations** directory (you are going to
   keep all of them within the **core** app), *admin.py* file (you are going to
   keep all admin files in the **core** app), *models.py* file (they also all
   are going to be stored in **core** app).
3. Create a new subfolder for test within the **user** app. Add *\_\_init\_\_.py*
   in that folder.
4. Head over to *settings.py* file and add `rest_framework` (to enable REST),
   `rest_framework.authtoken` (to enable auth token app) and `user` in the
   *INSTALLED_APPS*.

---

### Add Tests For Create User API

> Note: First API that you are going to create in your users project is the
        create users API. You are going to start by adding some unit tests
        to test creating users and different scenerios when you give different
        post requests.

1. Head over to **user/tests** and create *test_user_api.py* file.
2. Do imports:
* `from django.test import TestCase`.
* `from django.contrib.auth import get_user_model`: you are going to be needing
  the User model for out tests.
* `from django.urls import reverse`: so you can generate your API URL.
* `from rest_framework.test import APIClient`: to have a test client that you
  can use to make requests to your API and then check what the response is.
* `from rest_framework import status`: contains some status code that you can
  see in basically human readable form.
3. Recommended at the beginning of any API test is to add either a helper
   function or a constant variable for your URL that you are going to be testing.
   Create a user URL: `CREATE_USER_URL = reverse('user:create')` (Uppercase
   variables means that the variable is predicted to be constant - naming
   convention).
4. Add a helper function that you can use to create some example users for your
   tests so you do not have to create user for each test individually:

```python
def create_user(**params):
    """Create user."""
    return get_user_model().objects.create_user(**params)
```

5. Create the test class: `class PublicUserApiTests(TestCase):`.

> Note: The reason you call it public is because it is good habit to separate
        your API tests into public and private tests. It keeps the tests nice
        and clean because then in your setup you can have one that authenticates
        and one that does not authenticate. A public API is one that is
        unauthenticated so that is just anyone from the Internet can make
        a request. For example create user because when you typically create
        a user on a system usually you are creating user because you haven't
        got authentication set up already. A private API might be something
        like modify the user or change the password. For those types of requests
        you would expect to be authenticated.

6. Add setUp method to make it a little easier to call your client in your test
   so you do not have to manually create this API client every single test.
   In this way you just have one client for your test suite that you can reuse
   for all of the tests:

```python
def setUp(self):
      """Set up the client."""
      self.client = APIClient()
```

7. Create a test that validates the user is created successfully:

```python
def test_create_valid_user_success(self):
    """Test creating user with valid payload is successful."""
    payload = {
        'email': 'test@gmail.com',
        'password': 'admin123',
        'name': 'Test Name'
    }
    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    user = get_user_model().objects.get(**res.data)
    self.assertTrue(user.check_password(payload['password']))
    self.assertNotIn('password', res.data)
```

> Note: `payload` is the object that you pass to the API when you make the
        request. You are just going to test that if you pass in all the correct
        fields then the user is created successfully. `res` does a HTTP POST
        request to your client to your URL for creating users. Next you check if
        the outcome is what you expect - HTTP 201 CREATED. The next two lines
        are creating a user out of the data passed as response in `res` and
        checking if the password matches with the payload's one. Last line checks
        that the password is not returned as part of this object. You do that
        because you do not want the password being returned in the request
        because it is a potential security vulnerability. You should ensure that
        the passwords are kept as secret as possible even the encrypted version
        of the password there is no need to really send that to the user. You
        can always just check the passwords that they send you using
        *check_password*. So just to be safe, you want to make sure that the
        password is not returned, you return your user.

8. Next you are going to test what happens if there is an attempt on trying to
   create a user that already exists. Create a new test for that:

```python
def test_user_exists(self):
    """Test creating a user that already exists fails."""
    payload = {'email': 'test@gmail.com', 'password': 'admin123'}
    create_user(**payload)

    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

> Note: Create a payload as data to create a basic user account. Next you want
        to create a user (you can use a handy *create_user()* function that you
        created earlier) to simulate that there already is an account with these
        data. Next lets create a request to the user creation site with the
        payload data. In this way views method should try to create a user.
        In the last line check if the request's status code is HTTP 400 BAD
        REQUEST. It should be 400 because the user already exists.

9. Now you need a test to check if the password is too short. You are going to
   add a password restriction. Phrase should be longer than 5 characters:

```python
 def test_password_too_short(self):
     """Test that the password must be more that 5 characters."""
     payload = {'email': 'test@gmail.com', 'password': 'pw', 'name': 'Test'}
     res = self.client.post(CREATE_USER_URL, payload)

     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
     user_exists = get_user_model().objects.filter(
         email=payload['email']
     ).exists()
     self.assertFalse(user_exists)
```

> Note: Firstly create a payload with data to create a user. Remember that
        password is intentionally shorter that 5 characters. Then create
        request of user creation using payload. Check if the request's status
        code is HTTP 400 BAD REQUEST. It should be because the password is too
        short. So now you want to check if the user was never created. You do
        that by creating a *user_exists* variable which tries to define if a user
        with the payload's email in the user's model exists. Then you make an
        assertion that the *user_exists* should be False.

Every single test is isolated because each test resets the database from scratch.

10. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
    Expect fail.

---

### Add Create User API

> Note: Next you are going to implement your create user API to make your tests
        pass. What you are going to do is you are going to create a serializer
        for your *create_user* request. Then you are going to create a view
        which will handle the request. Then you are going to wire this up to
        a URL which will allow you to access the API and also make your tests pass.

1. Create a *serializers.py* file within *user* app.
2. Head over to that file and do imports:
* `from django.contrib.auth import get_user_model`: because you are going to need
  the User model to create your model serializer.
* `from rest_framework import serializers`.
3. Create serializer class: `class UserSerializer(serializers.ModelSerializer):`.

> Note: Django REST Framework has a built-in serializer that you can do this with.
        You just need to specify the fields that you want from your model and it
        does the database conversion for you. It also helps with the creating
        and retrieving from the database.

4. Now specify a meta class: `class Meta:`:
* Specify the model that you want to base your model serializer from:
  `model = get_user_model()`.
* Specify the fields that you want to include in serializer. These are the fields
  that are going to be converted to and from JSON when you make your HTTP POST
  and then you retrieve that in your view and then you want to save it to a model.
  So it basically are the fields that you want to make accessible in the API
  either to read or write: `fields = ('email', 'password', 'name')`.

> Note: These are 3 fields that you are going to accept when you create users.

* Add *extra_kwargs* to allow you to configure a few extra settings in your model
  serializer. What you are going to use this for is to ensure that the
  password is *write_only* and that the minimum required length is 5 characters:
  `extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}`.
5. Configure the *create* method. This method is called when you create
   a new object:

```python
def create(self, validated_data):
    """Create a new user with encrypted password and return it."""
    return get_user_model().objects.create_user(**validated_data)
```

> Note: This is all from the DJango REST Framework documentation
        (https://www.django-rest-framework.org/api-guide/serializers/#modelserializer)
        It basically specifies all the available functions that you can override
        in the different serializers that are available. You are going to override
        the *create* function here. In this method you are calling the *create_user*
        function in you model because by default it only calls the *create* function
        and you want to use your *create_user* model manager function that you
        created in your models to create the user. What Django REST Framework
        does is when you are ready to create the user it will call this *create*
        function and it will pass in the *validated_data*. The *validated_data*
        will contain all of the data that was passed into your serializer which
        would be the JSON data that was made in the HTTP POST. Then it passes it
        as the argument and then you can use that to create your user.

6. Next head over to *views.py* in **user** and do some imports:
* `from user.serializers import UserSerializer`.
* `from rest_framework import generics`: this is a view that is pre-made for you
  that allows you to easily make a API that creates an object in a database
  using the serializer that you are going to provide.
7. Add a view for managing your create user API:

```python
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer
```

> Note: All you actually need to specify in this view is a class variable that
        points to the serializer class that you want to use to create the object.

8. Create a *urls.py* within **user** app.
9. Import *path* and *views*, add *app_name* and set it to `user`.
10. Add *urlpatterns* with one path for *CreateUserView* view:
    `urlpatterns = [path('create/', views.CreateUserView.as_view(), name='create')]`.
11. Head over to *urls.py* in **app** app and import *include*.
12. Create a new path to include **user**'s *urls.py*:
    `path('api/user/', include('user.urls')),`.
13. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
    Expect OK.

---

### Add Tests for Creating A New Token

> Note: The next thing you are going to add to your user's API is the *create*
        *token* endpoint. This is going to be an endpoint that you can make
        a HTTP POST request and you can generate a temporary auth token that you
        can then use to authenticate future requests with the API. With you API
        you are going to be using token authentication. The way that you log in
        is you use this API to generate a token and then you provide that token
        as the authentication header for future requests which you want to
        authenticate. The benefit of this is you do not need to send the user's
        username and password with every single request that you make. You just
        need to send it once to create the token and then you can use that token
        for future requests. If you ever want to revoke the token you can do
        that in the database. You are going to start by creating 4 unit tests:
        **test that the token is created okay**, **check what happens if you**
        **provide invalid credentials**, **check if you are trying to authenticate**
        **against a non-existent user** and **check if you provide a request that**
        **does not include a password**. You are going to add them to the
        *test_user_api.py* file in your **user**'s tests directory.

1. Head over to *test_user_api.py* in **user** app.
2. Add new *TOKEN_URL* under the already existing *CREATE_USER_URL*:
   `TOKEN_URL = reverse('user:token')`.

> Note: This is going to be the URL that you are going to use to make the HTTP
        POST request to generate you token.

3. **Because you do not need to add authentication to this API because the**
   **purpose of this API is to start the authentication head over to the bottom**
   **of the PublicUserApiTests class** and create new *test_create_token_for_user*
   test:

```python
def test_create_token_for_user(self):
    """Test that a token is created for user."""
    payload = {
        'email': 'test@gmail.com',
        'password': 'admin123',
        'name': 'Test'
    }
    create_user(**payload)
    res = self.client.post(TOKEN_URL, payload)

    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
```

> Note: First you create a payload with data to create a user to test API.
        Next you create user that matches this authentication so you can test
        against that user. Then you make you request to the TOKEN_URL and store
        it in a variable called *res*. At this point because you made a request
        for a login with the email and password from payload and because this
        user exists as you created it in *create_user(**payload)*, you should
        get a HTTP 200 response and it should contain a token in the data
        response. So next you do the assertions: check if the token is a part
        of *res*' data and check if the status code is HTTP 200 OK. In this case
        you only check if the token exist but not if it is correct. This is
        because you are using the built-in Django authentication system. So that
        will already have its own unit test as part of the Django REST Framework
        unit test suite.

4. Next add test for creating token in case of invalid credentials:

```python
def test_create_token_invalid_credentials(self):
    """Test that token is not created if invalid credentials are given."""
    create_user(email='test@gmail.com', password='admin123', name='Test')
    payload = {
        'email': 'test@gmail.com',
        'password': 'wrong',
        'name': 'Test'
    }
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

> Note: First you create a user with sample email, password and name. Then create
        payload with an email and email same as the user's that you created.
        The password should be different (case of invalid credentials). Next you
        make a request that you expect to be HTTP 400. Then you check if the
        token is not in *res*' data (it should not as the password was invalid).
        Finally you check if the response's status code is HTTP 400 BAD REQUEST.

5. The next test is to test if the token will be created if the user does not
   exist:

```python
def test_create_token_no_user(self):
    """Test that token is not created if user does not exist."""
    payload = {
        'email': 'test@gmail.com',
        'password': 'admin123',
        'name': 'Test'
    }
    res = self.client.post(TOKEN_URL, payload)
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

> Note: So the first thing you create is a user's payload. Then you create
        the TOKEN_URL's response on payload's data. In this case you just tried
        to log in as the user that does not exist. So next thing you do is
        assertion to check if the token does not exist within *res*' data and
        the status code of the site is HTTP 400 BAD REQUEST.

6. Finally create a test to check what happens when the user's fields are
   missing:

```python
def test_create_token_missing_field(self):
    """Test that email and password are required."""
    res = self.client.post(TOKEN_URL, {
        'email': 'one',
        'password': '',
        'name': ''
    })
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

> Note: So there is no need to create payload so just create response with the
        data for login but with the missing password and name. Next you assert
        that there is no token in response's data and the status code is HTTP
        400 BAD REQUEST.

7. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

### Add Create Token API

> Note: So next you can go ahead and implement your create token API to make
        your unit tests pass.

1. Head over to your *serializers.py* within **user** app.

> Note: Next you are going to create *AuthTokenSerializer*. So you are going to
        create a new serializer just based off the Django standard serializers
        module and you are going to use this for authenticating your requests.

2. Create the *AuthTokenSerializer*:
   `class AuthTokenSerializer(serializers.Serializer):`.
3. Add a couple more imports to the top:
* `from django.contrib.auth import authenticate`: Django helper command for
  working with the Django authentication system. So you simply pass in the
  username and password and you can authenticate a request.
* `from django.utils.translation import ugettext_lazy as _`: **whenever you are**
  **outputting any messages in the Python code that are going to be output to the**
  **screen it is a good idea to pass them through this translation system just so**
  **if you ever do add any extra languages to your projects you can easily add the**
  **language file and it will automatically convert all of the text to the correct**
  **language**.
4. Add a class variables in *AuthTokenSerializer* serializer class:
* `email = serializers.CharField()`: standard email input.
* Password field:

```python
password = serializers.CharField(
      style={'input_type': 'password'},
      trim_whitespace=False,
      )
```

> Note: `trim_whitespace=False` because passwords can have spaces.

5. Next add your *validate* command. This function is called when you validate
   your serializer. So the validation is basically checking that the inputs are
   all correct. So that is an *email* field and *password* field. And as part of
   the validation function you are also going to validate that the authentication
   credentials are correct. This class is based off the default token serializer
   that is built into the Django REST Framework. You are just modifying it slightly
   to accept your email address instead of username:

```python
def validate(self, attrs):
    """Validate and authenticate the user."""
    email = attrs.get('email')
    password = attrs.get('password')

    user = authenticate(
        request=self.context.get('request'),
        username=email,
        password=password
    )
    if not user:
        msg = _('Unable to authenticate with provided credentials.')
        raise serializers.ValidationError(msg, code='authentication')
    attrs['user'] = user
    return attrs
```

> Note: `attrs` stands for attributes that you are going to be validating. These
        attributes are basically just every field that makes up your serializer.
        So any field that makes up a serializer, it will get passed into the
        *validate* function here as this dictionary and then you can retrieve
        the fields via this attributes and you can then valudate whatever you
        want to pass this validation or you want to fail the validation. Firstly
        you retrieve the *email* address and the *password* from these attributes.
        Next you use the *authenticate* method to authenticate your request.
        With *authenticate* the first argument is the *request* that you want to
        authenticate. So `request=self.context.get('request')` is how you
        basically access the context of the request that was made. You are going
        to pass this into your view set and what the Django REST Framework view
        set does is when a request is made it passes the context into the
        serializer in this `context` class variable here and from that you can
        get ahold of the request that was made. So that is what you are going to
        do here. You are going to pass the request in and then you are going to
        pass the username as email (because we are authenticating via email) and
        also add your password as password. Then you create an *if* statement
        in case that this authentication did not work to raise an *ValidationError*.
        Notice the *_* before message. Finally you set your user in the attributes
        which you return. Remember that whenever you are overriding the *validate*
        function, you must return the value at the end once the validation is
        successful.

6. Go to *views.py* within your **user** app and do some imports:
* `from rest_framework.authtoken.views import ObtainAuthToken`: if you are
  authenticated using a username and password as standard, it is very easy to
  just switch this on. You can just pass in the *ObtainAuthToken* view directly
  into your URLs. Because you are customizing it slightly you need to just
  basically import it into your views and then extend it with a class and then
  make a few changes to the class variables.
* `from rest_framework.settings import api_settings`.
* `from user.serializers import AuthTokenSerializer`.
7. Create your view:

```python
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
```

> Note: `renderer_classes` sets the renderer so you can view this endpoint in the
        browser with the browsable API. It menas that you can login using e.g.
        Chrome or whatever and you can type in the username and password and can
        click post and then it should return the token. If you do not do this
        then you have to use a tool such as C URL or some other tool to make the
        HTTP POST request. `api_settings.DEFAULT_RENDERER_CLASSES` to use the
        default renderer class. Using this expresion, if you ever change the
        renderer class and you want to use a different class to render your
        browsable API then you can do that in the settings and it will update in
        your view automatically.

8. Head over to *urls.py* within this app and add new path:
   `path('token/', views.CreateTokenView.as_view(), name='token'),`.
9. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.
10. Run `docker-compose up` to start the server and head over to your browser
    to check if everything is working. You can head over to the
    *http://127.0.0.1:8000/api/user/create* to create a user and
    *http://127.0.0.1:8000/api/user/token* to log in and check if token is created.

So when you create your client app that consumes the API what you would do is
you would take this token that is created and you would store it in a cookie or
in the some kind of persistent storage that you could then use to authenticate
with future requests.

> Recommended: Push to GitHub.
