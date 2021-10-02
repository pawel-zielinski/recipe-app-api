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

---

### Add Tests For Manage User Endpoint

> Note: Next you are going to add your manage user endpoint. The manage user
        endpoint will allow the authenticated user to update their own profile.
        This includes changing their name, password and viewing their user
        object.

1. Head over to the **/user/tests/test_user_api.py/PublicUserApiTests** because
   you are going to test as if you are an unauthenticated user and since you do
   not add any authentication in this client, you can go ahead and use this
   class to run the following test.
2. Before you add a test to the *PublicUserApiTests*, go to the top of the file
   and add new *ME_URL* which will represent the manage user endpoint:
   `ME_URL = reverse('user:me')`.
3. Now add test to check if authentication is required for the endpoint. This is
   important to check because it affects the security of it and you do not want
   APIs being made publicly by accident. Great way to prevent against that is
   to add unit tests to make sure that after any changes that you make, those
   APIs will always be private:

```python
def test_retrieve_user_unauthorized(self):
    """Test that authentication is required for users."""
    res = self.client.get(ME_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
```

> Note: All this does is it makes sure that if you call the URL without any  
        authentication it returns HTTP 401 UNAUTHORIZED.

Next you are going to ass some authenticated requests to your endpoint. So
the tests that you are going to add is `test_retrieve_profile_success`,
`test_post_me_not_allowed` (so you are not going to support POST on the *ME*
endpoint, you are just going to support *PATCH* and *PUT* to update it) and
`test_update_user_profile`.

4. Create a new test class and call it *PrivateUserApiTests*. **The _private_**
   **means that authentication is required before you can use these endpoints**:
   `class PrivateUserApiTests(TestCase):`.
5. Create a *setUp* class method that is going to do the authentication for each
   test that you do. So you do not need to set the authentication every single
   test. You are just doing the *setUp* and then that happens automatically
   before each test:

```python
def setUp(self):
    """Set up the client authenticated as user."""
    self.user = create_user(
        email='test@gmail.com',
        password='admin123',
        name='Test'
    )
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)
```

> Note: Firstly you create a user with demo credentials. Then using *APIClient*
        you create a reusable client. Then you do the force authentication
        to authenticate any requests that the client makes with your sample user.
        *force_authenticate* is a helper function that just makes it really easy
        to simulate or make authenticated requests. So whichever request you make
        with this *client*, now will be authenticated with your sample user.

6. Add test to check that you can retrieve the profile of the logged in user:

```python
def test_retrieve_profile_success(self):
    """Test retrieving profile for logged id user."""
    res = self.client.get(ME_URL)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, {
        'name': self.user.name,
        'email': self.user.email
    })
```

> Note: You only do request because you have already authenticated in your *setUp*
        so you do not need to do that authentication. Then you test if the  
        status code of the response is OK and if the name and email from the
        response matches the users data. You want to exclude the password because
        sending a it, even if it is the hash of the password, is never recommended.

7. Test that you cannot do a HTTP POST request on the profile.

```python
def test_post_me_not_allowed(self):
    """Test that POST is not allowed on the me url."""
    res = self.client.post(ME_URL, {})

    self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
```

> Note: Firstly you post the empty object to test it. Then you add your
        assertion to check if you get HTTP 405 METHOD NOT ALLOWED response.
        This is the standard response when you try and do a HTTP method that is
        not allowed on the API.

8. Next add your user profile update test.

```python
def test_update_user_profile(self):
    """Test updating the user profile for authenticated user."""
    payload = {'name': 'Test', 'password': 'not_admin123'}

    res = self.client.patch(ME_URL, payload)

    self.user.refresh_from_db()
    self.assertEqual(self.user.name, payload['name'])
    self.assertTrue(self.user.check_password(payload['password']))
    self.assertEqual(res.status_code, status.HTTP_200_OK)
```

> Note: Firstly you create a payload with a data that differs from the *setUp*'s
        user by password. Create a PATCH response from */me/* URL. Then you
        use the *refresh_from_db* helper function on your user to update the user
        with the latest values from the database. Then you check if the name and
        password of the user matches with the payload's. Finally you check if
        the status code is HTTP 200 OK.

9. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

### Add Manage User Endpoint

> Note: Now you can actually create your manage user endpoint. You are going to
        use your existing *UserSerializer* but you are going to add an additional
        function to the serializer for updating your user object. You are also
        going to add a custom view using the retrieve update API view using the
        Django REST Framework generic API view options.

1. Head over to the *app/user/views.py* file and do some imports:
* `from rest_framework import authentication, permissions`: these are Django
  REST Framework classes that you are going to use for your authentication and
  permissions of your user endpoint.
2. Create you *ManageUserView* class and base it from *RetrieveUpdateAPIView*:
   `class ManageUserView(generics.RetrieveUpdateAPIView):`.
3. First thing, just like other views that you create, create a **serializer class**
   **attribute**: `serializer_class = UserSerializer`.
4. Add two additional class variables for authentication and permission:
   `authentication_classes = (authentication.TokenAuthentication,)` and
   `permission_classes = (permissions.IsAuthenticated,)`.

> Note: Authentication is the mechanism by which the authentication happens so
        this could be cookie authentication or (what you are going to use) token
        authentication. The permissions are the level of access that the user
        has. The only permission you are going to add is that the user must be
        authenticated to use the API. They do not have to have any special
        permissions, they just have to be logged in.

5. Add a *get_object* method to your API view:

```python
def get_object(self):
    """Retrieve and return authentication user."""
    return self.request.user
```

> Note: So typically what would happen with an APIView is you would link it to
        a model and it could retrieve the item and you would retrieve data based
        models. In this case you are going to just get the model for the logged
        in user. You are going to override the *get_object* and you are going to
        return the user that is authenticated. When the *get_object* is called,
        the request will have the user attached to it because of the
        authentication classes, so because you have the authentication class that
        takes care of getting the authenticated user and assigning it to request.
        This is a great feature of Django REST Framework. Django has a similar
        thing out of the box as well.

6. Move on to your *app/user/serializers.py/UserSerializer* and add *update*
   method:

```python
def update(self, instance, validated_data):
    """Update a user, setting the password correctly and return it."""
    password = validated_data.pop('password', None)
    user = super().update(instance, validated_data)

    if password:
        user.set_password(password)
        user.save()

    return user
```

> Note: The purpose of this is you want to make sure the password is set using
        the *set_password* function instead of just setting it to whichever
        value is provided. The *instance* is going to be the model instance that
        is linked to your model serializer. That is going to be your user object.
        The *validated_data* is going to be fields passed in *Meta* (these
        fields that have been through the validation and ready to update). So
        firstly you remove the password from the *validated_data* and set it to
        the *password* variable by using *pop* function. The default value is
        *None* because you are going to allow the users to optionally provide
        a password. Next you run update request on the rest of your
        *validated_data*. So whatever is left, that is everything except the
        password, you can update. And what you do here with *super* is you call
        the *ModelSerializer* update function (so the default one), it will call
        the default function in your function so you can make use of all the
        functionality that is included in the default one whilst extending it
        slightly to customize it for your needs. Next you set the password if
        user has provided a password. Finally you return user.

7. Head over to the *app/user/urls.py* file and add new path:
   `path('me/', views.ManageUserView.as_view(), name='me'),`.
8. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.
9. Test API in the browser by heading over to the *127.0.0.1:8000/api/user/token*,
   log in and copy the token. Paste it in *Mod Header* with the name
   *Authentication* and value *Token <COPIED TOKEN>*. Then visit
   *127.0.0.1:8000/api/user/me*. You should see that the user is authenticated.
   Try to change the details of the user using *PATCH*. Try to change the password
   and to log in again.

> Recommended: Push to GitHub.

## Create Tags Endpoint

> Note: In this section you are going to add your *tags* API. The *tags* API is
        going to allow you to manage tags which you can assign to recipes in
        order to help with sorting and filtering of your recipes in the system.
        You are going to create your tags endpoint in a new app called *recipe*.
        The *recipe* app is where you are going to store all the recipe related
        endpoints such as the one for creating and uploading recipes and the ones
        for creating and updating tags and ingredients. You are going to start
        with tags.

### Create Recipe App

1. Head over to terminal and create a *recipe* app within the *recipe-app-api*
   project: `docker-compose run --rm app sh -c "python manage.py startapp recipe"`.
2. In *recipe* app remove: *admin.py* (because you are going to keep all the
   admin code in the *core* app), *models.py* (because that is also in the
   *core* app), *migrations* and *test.py* (but create a new folder for hosting
   your test - that folder is going to be *tests* with the *\_\_init\_\_.py*
   file in it).
3. Go to the *app/settings.py* and add *recipe* to the *INSTALLED_APPS*.

---

### Create Tags Model

> Note: Next you are going to create a new database model for handling your tag
        objects. Your tag model is going to be very basic. It is just going to
        accept the name of the tag and the user who owns the tag. You are going
        to start by adding a unit test for getting the tag object as a string
        and then you are going to implement your model. Then you are going to
        run your migrations to create the migration which would create the model
        in the database.

1. Head over to the *core* app and the *tests* folder and open up the
   *test_models.py* file.
2. Add a new helper function at the top to create users. That makes it easy for
   you to create user in your test:

```python
def sample_user(email='test@gmail.com', password='admin123'):
    """Create a sample user."""
    return get_user_model().objects.create_user(email, password)
```

> Note: Firstly you set up a default options in the parameters because in most
        cases this data is decent for the sample user and usually it is the same
        user with the same data.Then you return the user created using the
        *create_user* custom method.

3. Import *models* from *core* app and scroll down to the *test_create_new_superuser*
   method and under it create a test that creates a tag and verifies that it
   converts to the correct string representation:

```python
def test_tag_str(self):
    """Test the tag string representation."""
    tag = models.Tag.objects.create(
        user=sample_user(),
        name='Vegan'
    )

    self.assertEqual(str(tag), tag.name)
```

> Note: Firstly you create a *tag* variable that contains the object of Tag model
        with the data of user (created using the helper function that you have
        just created) and the tag's name. Then you assert to check if after
        string conversion of *tag* the value is the tag's name. With Django models
        you can specify what field you want to use when you convert the model to
        a string representation and you are going to set it to the name.

4. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.
5. Go over to you *models.py* and below, under the *User* model, create a new
   *Tag* model class which is going to inherit from models' Model:

```python
class Tag(models.Model):
    """Tag to be used for a recipe."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
```

> Note: Firstly you create a *name* character field with the max length of 255
        characters. Then you assign the *user* ForeignKey to your user object.
        But instead of referencing to the user object directly which you could
        do, you are going to use the **best practice method of retrieving the**
        **AUTH_USER_MODEL setting from your Django settings.** To do that you
        have to import *settings* from *django.conf*. This is recommended way to
        retrieve different settings from the Django settings file. Then you set
        up that when the user is deleted, tags are deleted as well.

6. Add a string representation method of tags:

```python
def __str__(self):
    """Represent tag as string value."""
    return self.name
```

7. Head over to the *app/core/admin.py* to register this model:

```python
admin.site.register(models.Tag)
```

8. Run migrations using terminal: `docker-compose run --rm app sh -c "python manage.py makemigrations"`.
9. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK with one error in views about import not used.

---

### Add Tests For Listing Tags

> Note: Next you are going to create your list tags API. Firstly you will start
        by creating unit tests to test that the API requires authentication to
        access it then you are going to test that you can list tags in your API
        and finally you are going to test that the tags that are listed are
        specifically for the user that is authenticated.

1. Go ahead and create a test module within your *recipe/tests* folder called
   *test_tags_api.py*.
2. Do some imports:
* `from django.contrib.auth import get_user_model` to get user model.
* `from django.urls import reverse` to generate URL.
* `from django.test import TestCase`.
* `from rest_framework import status`.
* `from rest_framework.test import APIClient`.
* `from core.models import Tag`.
* `from recipe.serializers import TagSerializer`.
3. Create tags URL: `TAGS_URL = reverse('recipe:tag-list')`. The URL is going to
   be using a ViewSet so that will automatically append the action name to the
   end of the URL for you using the router. `recipe` identifies the *app_name*.
   `tag` finds the route based on the model name assigned to the `queryset` class
   variable of the view (converted to lowercase). `-list` refers to the actions
   which are provided by default in the *ModelViewset* class.
4. Create the public API tests: `class PublicTagsApiTests(TestCase):`.
5. Add *setUp* method within that class to configure client:

```python
def setUp(self):
    """Set up the client."""
    self.client = APIClient()
```

6. Add *test_login_required* method to *PublicTagsApiTests* class to check if
   the login is required for retrieving tags:

```python
def test_login_required(self):
    """Test that login is required for retrieving tags."""
    res = self.client.get(TAGS_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
```

> Note: This is going to make an unauthenticated request to your tags API URL.
        Then it is going to check if the request's status code is HTTP 401
        UNAUTHORIZED.

7. Next add the authenticated tests by creating a class called *PrivateUserApiTests*:
   `class PrivateTagsApiTests(TestCase):`.
8. Create a *setUp* method to set up the client authenticated as the user:

```python
def setUp(self):
    """Set up the client."""
    self.user = get_user_model().objects.create_user(
        'test@gmail.com',
        'admin123'
    )
    self.client = APIClient()
    self.client.force_authenticate(self.user)
```

9. Create test to test retrieving the tags. You are going to set it up by
   creating a couple of sample tags and then you are going to make the request
   to the API. Then you are going to check that the tags returned equal what you
   expect them to equal:

```python
def test_retrieve_tags(self):
    """Test retrieving tags."""
    Tag.objects.create(user=self.user, name='Vegan')
    Tag.objects.create(user=self.user, name='Dessert')

    res = self.client.get(TAGS_URL)
    tags = Tag.objects.all().order_by('-name')
    serializer = TagSerializer(tags, many=True)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
```

> Note: Firstly you create two Tag objects - Vegan and Dessert. Then you create
        a response from the TAGS_URL. Next you create *tags* variable with all
        Tag's objects ordered by the reversed alphabetical order. Then you create
        a *serializer* variable with serialized *tags* variable data (`many=True`
        because *tags* contains more than one object and **serializers only**
        **serialize one object at the time**). Then you check if the request's
        status code is equal to the HTTP 200 OK and the request's data is equal
        to the *serializer*'s data.

10. Test that the tags that are retrieved are limited just to the user that is
    logged in. You only want to see tags that are assigned to the authenticated
    user:

```python
def test_tags_limited_to_user(self):
    """Test that returned tags are for the authenticated user."""
    user2 = get_user_model().objects.create_user(
        'other@gmail.com',
        'testpass'
    )
    Tag.objects.create(user=user2, name='Fruity')
    tag = Tag.objects.create(user=self.user, name='Comfort Food')

    res = self.client.get(TAGS_URL)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 1)
    self.assertEqual(res.data[0]['name'], tag.name)
```

> Note: Firstly you create *user2* in addition to the user that is created at the
        *setUp* just so you can assign a tag to that user. Then you can compare
        that that tag was not included in the response because it was not the
        authenticated user. Then you create a new tag object assigned to the
        *user2*. Then you create a new tag assigned to the user that you are
        authenticated with and save it in a *tag* variable for the assertion
        purposes. Then you create a response from the tags' URL. Next you check
        if the response's status code is HTTP 200 OK. It should because you
        authenticate as the authenticated user. Then you check if the length
        of the response's data is 1. It should because you want only
        authenticated users' tags. Finally you check if the response's data
        contains the tag that is the same as the tag that authenticated user has.

11. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

### Add Feature To List Tags

> Note: Next you are going to implement the feature to list you tags from your
        list tags API.

1. Create a new *serializers.py* file within *recipe* app.
2. Do some imports:
* `from rest_framework import serializers`.
* `from core.models import Tag`.
3. Create a simple *TagSerializer*. You are going to link this to your *Tag*
   model and pull in the ID and the name values:

```python
class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects."""

    class Meta:
        """Meta class of TagSerializer."""

        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
```

4. Move to *app/recipe/views.py* file.

> Note: The view that you are going to create is a ViewSet and you are going to
        base it off the generic ViewSet and you are specifically going to use
        the *ListModelMixin*. This is a Django REST Framework feature where you
        can pull in different parts of a ViewSet that you want to use for your
        application. You only wanto to take the *list model* function. You do not
        want to add the *create*, *update*, *delete* function. You are just going
        to add the *list model* function and you can do that very easily by using
        a combination of the generic ViewSet and the *ListModelMixin*.

5. Delete all the content in this file and do imports:
* `from rest_framework import viewsets, mixins`.
* `from rest_framework.authentication import TokenAuthentication`: because you
  want to authenticate the request.
* `from rest_framework.permissions import IsAuthenticated`.
* `from core.models import Tag`.
* `from recipe import serializers`.
6. Create a *TagViewSet* class:

```python
class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
```

> Note: For more about the different mixins that are available:
        *https://www.django-rest-framework.org/api-guide/viewsets/#genericviewset*,
        *https://www.django-rest-framework.org/api-guide/viewsets/#example_3*.
        Firstly you add variables to require that token authentication is used
        and the user must be authenticated to use the API. Next you create
        *queryset*. When you are defining a *ListModelMixin* in the generic
        ViewSet, you need to provide the *queryset* that you want to return.
        Then you add a *serializer_class* to wire this up to the *TagSerializer*.

7. Move to the *app/recipe/urls.py* file and do some imports:
* `from django.urls import path, include`.
* `from rest_framework.routers import DefaultRouter`.
* `from recipe import views`.

> Note: The *DefaultRouter* is a feature of the Django REST Framework that will
        automatically generate the URLs for your ViewSet. When you have a ViewSet
        you may have multiple URLs associated with that one ViewSet. So one URL
        might be the */api/recipe/tags* and another URL might be */tag/<TAG ID*
        *TO RETRIEVE THE SPECIFIC ITEM>* and in another you might add some
        additional ones like you might add some custom actions to it like you
        did with the users where you did the change password and what the
        *DefaultRouter* does is it automatically registers the approprate URLs
        for all of the actions in your ViewSet.

8. Then create a router variable with the *DefaultRouter* object:

```python
router = DefaultRouter()
```

9. Next, because you are working on ViewSet, you can register this ViewSet to
   this router:

```python
router.register('tags', views.TagViewSet)
```

10. Then you add an *app_name*:

```python
app_name = 'recipe'
```

11. And new path to *urlpatterns*:

```python
urlpatterns = [
    path('', include(router.urls))
]
```

12. Head over to the *app/app/urls.py* file and add new path to *urlpatterns*:

```python
path('api/recipe/', include('recipe.urls')),
```

13. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
    Expect to fail.
14. Head over to the *app/recipe/views.py/TagViewSet* and add a function which
    will override the *get_queryset* function:

```python
def get_queryset(self):
    """Return objects for the cirrent authenticated user only."""
    return self.queryset.filter(user=self.request.user).order_by('-name')
```

> Note: When the list function is invoken so when your ViewSet is invoken from
        a URL it will call *get_queryset* to retrieve these objects and this is
        where you can apply any custom filtering like limiting it to the
        authenticated user. **Whatever you return here, will be displayed in the**
        **API. This is just how the Django REST Framework functions** and this is
        all explained and outlined in their documentation. If you do return
        *self.queryset*  you could reference *Tag.objects.all()* directly but this
        would not recommended because the if you changed the object that you are
        retrieving then it would not work so you want to be able to change it in
        one place and this should be the objects that are being rendered by the
        ViewSet. The request objects should be passed in to the self as a class
        variable and then the user should be assigned to that because authentication
        is required. If they manage to get this far in calling the API then they
        would have already been authenticated and they would already have these
        authenticated permission prove otherwise they would have just received an
        unauthenticated request error.

15. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
    Expect OK.

---

### Add Create Tags Feature

> Note: Next you are going to add the create tags feature. You are going to start
        by adding some basic tests to your test suite to check that you can
        create tags and also to check that when you create tags validation
        is performed correctly on the create request.

1. Head over to the *app/recipe/tests/test_tags_api.py/PrivateTagsApiTests*
   and create a test to check if the tag is created in a proper way:

```python
def test_create_tag_successful(self):
    """Test creating a new tag."""
    payload = {'name': 'Test tag'}
    self.client.post(TAGS_URL, payload)

    exists = Tag.objects.filter(
        user=self.user,
        name=payload['name']
    ).exists()

    self.assertTrue(exists)
```

> Note: Firstly you create the *payload* with the tag's data. Then you post
        this data to the tags' URL as client authenticated as user. Next you
        create the *exists* variable to keep boolean value about the existence
        of the tag created by this user and with the name from the payload.
        Finally you assert that *exists* is *True*.

2. Add the test to check what happens when the tag has invalid name:

```python
def test_create_tag_invalid(self):
    """Test creating a new tag with invalid payload."""
    payload = {'name': ''}
    res = self.client.post(TAGS_URL, payload)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

> Note: Firstly you create a payload with the tag's empty name field. Then
        you do the POST method on the tags' URL with the payload's data
        and the client authorized as user. Then you check if the status code
        of the response is HTTP 400 BAD REQUEST.

3. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.
4. Head over to the *views.py* and add *CreateModelMixin* to the parameters of
   *TagViewSet* as an another class that this is going to be based on:

```python
class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
```

> Note: You can add these mixins to customize the functionality that is available
        for your ViewSet. You do not have to do the standard model ViewSet and
        accept everything because there might be some cases where you do not
        want to allow users to do everything and you do not need that feature
        so there is no point implementing it. So you can customize it by adding
        the specific mixins for what you want to do and in this case you are
        going to add the *mixin.CreateModelMixin*. So this will add the **create**
        option.

5. Now you have to override the *perform_create* so that you can assign the tag
   to the correct user:

```python
def perform_create(self, serializer):
    """Create a new tag."""
    serializer.save(user=self.request.user)
```

> Note: Very similar to the *get_queryset*, the *perform_create* function
        is a function that allows you to hook into the create process when
        creating and object and what happens is when you do a create object in
        your ViewSet this function will be invoked and the validated serializer
        will be passed in as a serializer argument and then you can perform any
        modifications here that you would like to create process. All you are
        going to do is you are just going to do *serializer.save* and set the
        user to the authenticated user.

6. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.

> Recommended: Push to GitHub.

## Create Ingredients Endpoint

> Note: In this section you are going to create your ingredients endpoint. The
        ingredients endpoint is going to be very similar to the tags endpoint in
        that it allows you to create and list ingredients which you can later
        assign to recipes for the purposes of filtering.

### Add Ingredient Model

> Note: You are going to start by adding your ingredient model.

1. Had over to *app/core/tests/test_models.py/ModelTests* and add new test to
   to check the ingredient's string representation:

```python
def test_ingredient_str(self):
    """Test the ingredient string representation."""
    ingredient = models.Ingredient.objects.create(
        user=sample_user(),
        name='cucumber'
    )

    self.assertEqual(str(ingredient), ingredient.name)
```

> Note: Firstly you create an ingredient registered by a user and saved as
        *ingredient* variable. Then you check if the string representation of
        this object matches with it's name.

2. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.
3. Open up the *app/core/models.py* and add new *Ingredient* model at the bottom:

```python
class Ingredient(models.Model):
    """Ingredient to be user in a recipe."""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Represent ingredient as string value."""
        return self.name
```

4. Open up terminal and run migrations to create your migration file:
   `docker-compose run --rm app sh -c "python manage.py makemigrations core"`
5. Head over to the *app/core/admin.py* to register new model:

```python
admin.site.register(models.Ingredient)
```

6. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.

---

### Add Tests For Listing Ingredients

> Note: Next you are going to add some tests for listing ingredients. You are
        going to create the same type of API that you created for your tags
        except you are going to list ingredients. You are going to start
        by adding the unit tests.

1. Head over to the *app/recipe/tests* folder and create a new test module called
   *test_ingredients_api.py*.
2. Go to that test module and add some imports:
* `from django.contrib.auth import get_user_model`.
* `from django.urls import reverse`.
* `from django.test import TestCase`.
* `from rest_framework import status`.
* `from rest_framework.test import APIClient`.
* `from core.models import Ingredient`.
* `from recipe.serializers import IngredientSerializer`.
3. Add ingredients URL and create your public ingredients API tests:

```python
INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API."""
```

> Note: You are also going to use a default router for your ingredients API and
        it is going to have the */list*. The URL name is going to reference your
        listing URL.

4. Add *setUp* method for creating an unauthorized client (as this is within
   the public class):

```python
def setUp(self):
    """Set up the client."""
    self.client = APIClient()
```

5. Add your login required test to ensure that login is always required for this
   endpoint:

```python
def test_login_required(self):
    """Test that login is required to access the endpoint."""
    res = self.client.get(INGREDIENTS_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
```

> Note: Firstly you create a request from the ingredients' URL as an unauthorized
        client. This should respond with HTTP 401 UNAUTHORIZED.

6. So you have now tested that login is required. You can then move on to testing
   listing your ingredients. You will create a new private test class below the
   *PublicIngredientsApiTests*:

```python
class PrivateIngredientsApiTests(TestCase):
    """Test the private ingredients API."""
```

7. Then you create a *setUp* method for creating a client authorized as user
   (as this is within the private class):

```python
def setUp(self):
    """Set up the client."""
    self.client = APIClient()
    self.user = get_user_model().objects.create_user(
        'test@gmail.com',
        'admin123'
    )

    self.client.force_authenticate(self.user)
```

> Note: Firstly you create a class variable with the client's object.
        Then you create a user and finally you authenticate the client with the
        user.

8. Add your retrieve ingredients test:

```python
def test_retrieve_ingredient_list(self):
    """Test retrievint list of ingredients."""
    Ingredient.objects.create(user=self.user, name='Kale')
    Ingredient.objects.create(user=self.user, name='Salt')

    res = self.client.get(INGREDIENTS_URL)

    ingredients = Ingredient.objects.all().order_by('-name')
    serializer = IngredientSerializer(ingredients, many=True)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
```

> Note: Firstly you create two sample ingredients. Then you get the response
        from the ingredients' URL using the authorized client and you save it
        in the *res* variable. Then you create *ingredients* variable to store
        all (two) created *Ingredient*'s objects. Next you run serialization
        process using *IngredientSerializer* on *ingredients* variable.
        Finally you check if the response from the endpoint is correct and the
        response's data matches with the serializer's data.

9. Next you will test that the ingredients are limited to the authenticated user:

```python
def test_ingredients_limited_to_user(self):
    """Test that ingredients for the authenticated user are returned."""
    user2 = get_user_model().objects.create_user(
        'other@gmail.com',
        'testpass'
    )
    Ingredient.objects.create(user=user2, name='Vinegar')
    ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

    res = self.client.get(INGREDIENTS_URL)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 1)
    self.assertEqual(res.data[0]['name'], ingredient.name)
```

> Note: Firstly you create the additional user (unauthorized). Then you create
        the *Vinegar* ingredient using this user. Then you create another
        ingredient called *Tumeric* and save it in *ingredient* variable. This
        ingredient is going to be signed by the user.
        First ingredient was not assigned to the variable because you did not
        really needed to reference it at any point in this test whereas the
        second ingredient you do reference because you check that the name of
        this *ingredient* matches the name of the ingredient you created.
        So you check if the response is correct, the length of the response's
        data is only one (as there should be only one ingredient (*Tumeric*)
        which was added by the authorized user) and you check if that *Tumeric*
        is really this only ingredient stored in response's data.

10. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

### Implement Feature For Listing Ingredients

> Note: Next you are going to add the feature to list ingredients from your
        ingredients endpoint.

1. Head over to *app/recipe/serializers.py* file and import *Ingredient* model:

```python
from core.models import Ingredient
```

2. Create the *IngredientSerializer* serializer similar to the tag serializer.
   It is going to contain *ID* and *name* fields and the *ID* is going to be
   read only:

```python
class IngredientSerializer(serializers.ModelSerializer):
    """Serialzier for ingredient objects."""

    class Meta:
        """Meta class of IngredientSerializer."""

        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
```

> Note: The reason why you do not include *user* field is that you narrow all
        the ingredients to these which are added by the authenticated user.
        So there is no need to add that field as the user is going to be the same
        constantly.

3. Now head over to the *app/recipe/views.py* file. Now you are going to create
   a ingredient ViewSet. I is going to be similar to the *TagViewSet*:

```python
class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    """Manage ingredients in the database."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
```

> Note: `mixins.ListModelMixin` is to give this ViewSet support for listing
        your ingredients. Then you add *TokenAuthentication*
        to *authentication_classes* because this ViewSet is going to use the
        *token authentication*. Next you add *IsAuthenticated* to your
        *permission_classes* because you want to make sure all the users that
        use this API are authenticated. Then you add *queryset* with all
        ingredients.Finally you add *serializer_class* to connect to the
        *IngredientSerializer*.

4. Add the *get_queryset* method so that you can filter by the objects assigned
   to the user that is currently authenticated and also order them by name:

```python
def get_queryset(self):
    """Return objects from the current authenticated user only."""
    return self.queryset.filter(user=self.request.user).order_by('-name')
```

> Note: This is why you did not add the *user* in the serializer's *fields*.
        You filter by logged in user only.

5. Now open *app/recipe/urls.py* file and register this ViewSet with a URL Router
   so you can access the endpoint from the web:

```python
router.register('ingredients', views.IngredientViewSet)
```

6. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.

> Recommended: Push to GitHub.

---

### Implement Feature For Creating Ingredients

> Note: Next you are going to implement the feature for creating ingredients
        with your API. You are going to start by adding some basic tests and
        then you are going to modify your ViewSet to support the *create*
        function.

1. Open up *test_ingredients_api.py* module and after
   *test_ingredients_limited_to_user* add test to check if the correctly
   created ingredient exists in the database with proper data:

```python
def test_create_ingredient_successful(self):
    """Test create a new ingredient."""
    payload = {'name': 'Cabbage'}
    self.client.post(INGREDIENTS_URL, payload)

    exist = Ingredient.objects.filter(
        user=self.user,
        name=payload['name']
    ).exists()

    self.assertTrue(exist)
```

> Note: Firstly you create the *payload* with the ingredient's data. Then you
        post it on the INGREDIENTS_URL. After that you create a variable to store
        the boolean value which will depend on whether that *payload*'s ingredient,
        signed by the authorized user, exists, or not. Then you assert that
        this variable should be True.

2. Add another test in case the ingredient has invalid name:

```python
def test_create_ingredient_invalid(self):
    """Test creating invalid ingredient fails."""
    payload = {'name': ''}
    res = self.client.post(INGREDIENTS_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

> Note: You create a payload with the empty name field of the ingredient.
        Then you post it as a registered client and save it in *res* variable.
        Finally you check if the status code of response is the HTTP 400 BAD
        REQUEST.

3. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.
4. Head over to *app/recipe/views.py* and add *mixins.CreateModelMixin*
   within *IngredientViewSet* as the inherited module. This enables you to
   override the *perform_create* method:

```python
class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
```

5. Add the *perform_create* method within *IngredientViewSet*:

```python
def perform_create(self, serializer):
    """Create a new ingredient."""
    serializer.save(user=self.request.user)
```

6. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.
7. Open up browser and go to *127.0.0.1:8000/api/user/create* and create new
   user. Go to *127.0.0.1:8000/api/user/token* to log in. Copy token and add it
   to *ModHeader* extension: Name: *Authorization*, Token: *Token <YOUR TOKEN>*.
   Go to *127.0.0.1:8000/api/recipe*. Go to *127.0.0.1:8000/api/recipe/ingredients/*.
   Add new ingredient and hit *POST*. Click on the searching bar and hit enter
   to "refresh" the page.

> Recommended: Push to GitHub.

---

### Re-factor Tags And Ingredients ViewSets

> Note: Next you are going to re-factor your tags and ingredients API. You may
        have noticed when you were building your tags and ingredients API that
        there are a lot of commonalities between the two. You can re-factor this
        code to reduce the code duplication. You are going to create a new base
        class that contains the common components from the tags and the
        ingredients ViewSets. Then you are going to base the tag and ingredient
        ViewSets off this common class. This will help make your code easier
        to read and reduce the code duplication.

1. Head over to the *app/recipe/views.py* file and create a new class above both
   the tag and ingredients classes:

```python
class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
```

> Note: As you can see the things that both classes had in common were: inherited
        modules, *authentication_classes* and *permission_classes*.

2. Next add methods that are common in tag and ingredient ViewSets to this new
   class:

```python
def get_queryset(self):
    """Return objects from the current authenticated user only."""
    return self.queryset.filter(user=self.request.user).order_by('-name')

def perform_create(self, serializer):
    """Create a new object."""
    serializer.save(user=self.request.user)
```

> Note: Both methods are the same in tag and ingredient ViewSets so you can
        rewrite them in *BaseRecipeAttrViewSet* as its methods. Only in
        *perform_create* you have to generalize the doc string.

3. Now that you have your base class ready, you can delete the inherited modules
   from tag and ingredient ViewSets. You can also delete their methods,
   *authentication_classes* and *permission_classes* as they already are
   in *BaseRecipeAttrViewSet* class. Now base your *TagViewSet* and
   *IngredientViewSet* on *BaseRecipeAttrViewSet*:

```python
class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects from the current authenticated user only."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object."""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
```

4. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.

> Recommended: Push to GitHub.

## Create Recipe Endpoint

> Note: In this section you are going to be creating your recipe endpoint.
        You are going to star by creating a new model in your database for
        handling recipe objects. Once you create the model you are then going
        to run the migrations and create the migration file that will create
        the recipe table in the database.

### Add Recipe Model

1. Head over to the *app/core/tests/test_models.py* file and scroll down to
   the bottom (under *test_ingredient_str*) to add a new test converting your
   recipe to string:

```python
def test_recipe_str(self):
    """Test the recipe string representation."""
    recipe = models.Recipe.objects.create(
        user=sample_user(),
        title='Steak and mushtoom sauce',
        time_minutes=5,
        price=5.00
    )
    self.assertEqual(str(recipe), recipe.title)
```

> Note: You create the recipe which will have 4 fields that are mandatory to
        create an instance of recipe model. Then you check if the string
        representation of that recipe object is its title. Some of the fields
        are going to be required and others are going to be optional.

2. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.
3. Go over to the *app/core/models.py* and under the *Ingredient* model create
   *Recipe* model:

```python
class Recipe(models.Model):
    """Recipe object."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredient')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        """Represent recipe as string value."""
        return self.title
```

> Note: *user* as the *ForeignKey* because only one user can create a recipe
        and there will be many recipes. *title* as *CharField*.
        *time_minutes* as *IntegerField*. *price* as *DecimalField*.
        *max_digits* for maximum digits that the field can take.
        *decimal_places* for digits after dot. *link* (optional - that is why
        `blank=True`) as *CharField*. *ingredients* as *ManyToManyField* because
        many ingredients can be added to many recipes. *tags* as *ManyToManyField*
        because many tags can be added to many recipes. Then string conversion
        to represent object as its title.

> Note: Instead of `ingredients = models.ManyToManyField('Ingredient')` and
        `tags = models.ManyToManyField('Tag')` you could use
        `ingredients = models.ManyToManyField(Ingredient)`
        and `tags = models.ManyToManyField(Tag)`. The difference is that in
        the first example you can put *Recipe* class wherever you want within
        this file. In the second example you have to make sure that the called
        class already exists. Django has this useful feature where you can just
        provide the name of the class in a string and then it does not matter
        which order you place your models in.

4. Run migrations by heading to your terminal and typing:
   `docker-compose run --rm app sh -c "python manage.py makemigrations core"`.
5. Go to *app/core/admin.py* to register new model:

```python
admin.site.register(models.Recipe)
```

6. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.

> Recommended: Push to GitHub.

---

### Add Tests For Listing Recipes

> Note: Next you are going to add your list recipe API. Before that lets create
        some tests.

1. Head over to *app/recipe/tests* and add new test module called *test_recipe_api.py*
   and add some imports:
* `from django.contrib.auth import get_user_model`.
* `from django.test import TestCase`.
* `from django.urls import reverse`.
* `from rest_framework import status`.
* `from rest_framework.test import APIClient`.
* `from core.models import Recipe`.
* `from recipe.serializers import RecipeSerializer`.
2. Assign a variable for your recipe URL. Since you are going to need to access
   the URL in more or less all the tests, assign that as a variable at top of the
   class:

```python
RECIPES_URL = reverse('recipe:recipe-list')
```

> Note: First `recipe` is the name of the app which you set up in *urls.py* in
        *app_name* variable. Second `recipe` is from queryset's model name, all
        lowercase, provided in ViewSet that you wire up to that URL. This is
        how routers work.

3. Create a helper function called *sample_recipe* to allow you to easily create
   test sample recipes for you to play with in your tests:

```python
def sample_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)
```

> Note: This concept of creating a helper function is used when you need repeated
        objects in your tests. So you know that you are going to need to create
        a lot of recipes for these tests and the *Recipe* has three required
        parameters that you need to pass each one. This function allows you to
        create a recipe with a set of default values that you can optionally
        change.  

4. Create class for public recipe tests:

```python
class PublicRecipeApiTests(TestCase):
    """Test unauthenticated recipe API access."""
```

5. Add *setUp* function to create an unauthorized client:

```python
def setUp(self):
    """Set up an unauthorized client."""
    self.client = APIClient()
```

6. Then test that authentication is required by making an unauthenticated request:

```python
def test_auth_required(self):
    """Test that authentication is required."""
    res = self.client.get(RECIPES_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
```

7. Create class for private recipe tests:

```python
class PrivateRecipeApiTests(TestCase):
    """Test authenticated recipe API access."""
```

8. Add *setUp* command for creating an authorized client:

```python
def setUp(self):
    """Set up an authorized client."""
    self.client = APIClient()
    self.user = get_user_model().objects.create_user(
        'test@gmail.com',
        'admin123'
    )
    self.client.force_authenticate(self.user)
```

9. Now verify that the output is what you expected:

```python
def test_retrieve_recipes(self):
    """Test retrieving a list of recipes."""
    sample_recipe(user=self.user)
    sample_recipe(user=self.user)

    res = self.client.get(RECIPES_URL)

    recipes = Recipe.objects.all().order_by('-id')
    serializer = RecipeSerializer(recipes, many=True)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
```

> Note: Firstly you create two sample recipes. They can be the same - it does
        not matter. Then you create GET response as authenticated client.
        So you *get* these sample recipes as fixed data from URL.
        Next you get all created recipes from *Recipe* model and store it in
        variable. After that you serialize all the data stored in this variable
        and save it in *serializer* variable. Finally you assert that response's
        status code is OK and that responses data is the same as the serializer's.

10. Add test to check that recipes are limited to authenticated users only:

```python
def test_recipes_limited_to_user(self):
    """Test retrieving recipes for user."""
    user2 = get_user_model().objects.create_user(
        'other@gmail.com',
        'passphrase'
    )
    sample_recipe(user=user2)
    sample_recipe(user=self.user)

    res = self.client.get(RECIPES_URL)

    recipes = Recipe.objects.filter(user=self.user)
    serializer = RecipeSerializer(recipes, many=True)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(len(res.data), 1)
    self.assertEqual(res.data, serializer.data)
```

> Note: So firstly you create the user that is not authorized. Then you
        create two recipes: one as unauthorized user and one as authorized
        user. Then you create a GET request from the website as the
        authorized user. Next you get all recipes that are
        created by authorized user. Then you serialize these recipes. You should
        expect to be only one recipe but still you should add `many=True`
        because this makes serializer create a list of data and in this format
        you want data to retrieve. Otherwise this it would make the API
        inconsistent and you would not know what to expect when you call the API.
        After that you check that response's status code is OK, there is only
        one recipe in response's data and that response's data is similar to
        the serializer's.

11. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
    Expect to fail.

---

### Implement Feature For Listing Recipes

> Note: Now that you have your test added, you can go ahead and implement
        your feature for listing recipes.

1. Head over to *app/recipe/serializers.py* file and import *Recipe* model:

```python
from core.models import Recipe
```

2. Create a new class below *IngredientSerializer*:

```python
class RecipeSerializer(serializers.ModelSerializer):
    """Serializer a recipe."""
```

3. Add *Meta* class to specify fields to serialize:

```python
class Meta:
    """Meta class of RecipeSerializer."""

    model = Recipe
    fields = (
        'id', 'title', 'ingredients', 'tags', 'time_minutes',
        'price', 'link'
    )
    read_only_fields = ('id',)
```

> Note: The reason why you add `id` in `read_only_fields` is just to prevent the
        user from updating the ID when they may create or edit requests. This is
        best practice as you do not want to have the primary key changing unless
        you have a really good reason to change it which is quite unlikely.

4. Next you need to define the *PrimaryKeyRelatedField* within your fields:

```python
ingredients = serializers.PrimaryKeyRelatedField(
    many=True,
    queryset=Ingredient.objects.all()
)
tags = serializers.PrimaryKeyRelatedField(
    many=True,
    queryset=Tag.objects.all()
)
```

> Note: Because the *ingredients* and *tags* are not actually part of the
        serializer, they are referencesto the *Ingredient* and *Tag* models. You
        need to define these as special fields. You have to add two class
        variables to the top of your *RecipeSerializer*. What this does is it
        creates a *PrimaryKeyRelatedField* and it says to allow many and the
        queryset that you are going to use or that you are going to allow
        to be part of this is going to be from the *Ingredient.objects.all()*
        or *Tag.objects.all()* (depending on whether it is *ingredients* or *tags*
        class variable). What this does is it simply lists the objects
        (ingredients or tags) with their primary key ID. This is how you want
        it to appear when you are listing your recipes because you do not want
        it to include the full name and all the values of the object. You just
        want to list the IDs and then if you want to i.e. retrieve the full name
        of the name, you can use the *detail API* which you will create in a moment.
        (https://www.django-rest-framework.org/api-guide/relations/#primarykeyrelatedfield)

5. Head over to *app/recipe/views.py* and create a new ViewSet called
   *RecipeViewSet*:

```python
class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database."""
```

> Note: You inherit from `viewsets.ModelViewSet` because you want to provide
        functionality of creating, listing, updating and viewing details.

6. Then add serializer class, queryset, authentication class and permission class
   for that ViewSet:

```python
serializer_class = serializers.RecipeSerializer
queryset = Recipe.objects.all()
authentication_classes = (TokenAuthentication,)
permission_classes = (IsAuthenticated,)
```

7. Head over to the top of the file and import *Recipe* model:

```python
from core.models import Recipe
```

8. Add the *get_queryset* method to limit the objects to the authenticated user:

```python
def get_queryset(self):
    """Return objects from the current authenticated user only."""
    return self.queryset.filter(user=self.request.user).order_by('-name')
```

9. Open up *app/recipe/urls.py* and register this ViewSet with your default router:

```python
router.register('recipes', views.RecipeViewSet)
```

10. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
    Expect OK.

> Recommended: Push to GitHub.

---

### Add Tests For Retrieving Recipe Detail

> Note: Now you are going to add your recipe detail endpoint. The recipe detail
        is going to allow you to retrieve a specific recipe returning more
        details that what the list recipes endpoint returns. The list recipe
        endpoint is more like a summary of all the recipes that you have and
        the detailed recipe endpoint is going to be for a specific recipe.
        The main difference in your app is that the list recipe endpoint is only
        going to return the IDs of the tags and ingredients that are assigned
        to that recipe whereas the detail view will return the actual name and
        the ID of each tag and ingredient that is assigned. This allows the
        consumer of the API which would be a front-end client or something like
        that to have more flexibility about how much data is transferred when
        retrieving lists and retrieving the specific details. For example when
        you are listing you may only want to see a preview so you may only need
        the basic fields like title and the photo or whatever basic fields you
        have on the recipe. Whereas you might also want to add a detail view so
        they can select a recipe and then you see all of the details such as all
        of the tags and ingredients that are assigned.

1. Head over *app/recipe/tests/test_recipe_api.py* and at the top of the file
   add some more helper functions for creating sample tags and ingredients.
   To do that firstly you need to import *Tag* and *Ingredient* models:

```python
from core.models import Tag, Ingredient
```

then create these helper functions:

```python
def sample_tag(user, name='Main course'):
    """Create and return a sample tag."""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """Create and return a sample ingredient."""
    return Ingredient.objects.create(user=user, name=name)
```

2. Create a new helper function for creating the URL. Unlike the *RECIPES_URL*
   which is just a standard URL, you are going to require an argument in you URL
   which is the ID of recipe you want to retrieve the detail for:

```python
def detail_url(recipe_id):
    """Return recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])
```

> Note: So if you thing about the API you are going to have, it is going to look
        i. e. *127.0.0.1:8000/api/recipe/recipes/<ID OF A SPECIFIC RECIPE>/*,
        when the *RECIPES_URL* is going to be more like
        *127.0.0.1:8000/api/recipe/recipes/*.
        You need to pass in this argument whenever you create the detail URL.
        **`recipe-detail` is the name of the endpoint that the DefaultRouter**
        **will create for your ViewSet because you are going to have a detail**
        **action**. `args=[recipe_id]` - this is how you pass in arguments in
        *reverse* function. The reason it is a list is because you may have multiple
        arguments for a single URL. You are only going to be using one so you
        just pass in a single item into you list.

3. Scroll down to the bottom under the `test_recipes_limited_to_user` and add
   new test to the `PrivateRecipeApiTests` test suite to check if the detail
   ViewSet works:

```python
def test_view_recipe_detail(self):
    """Test viewing a recipe detail."""
    recipe = sample_recipe(user=self.user)
    recipe.tags.add(sample_tag(user=self.user))
    recipe.ingredients.add(sample_ingredient(user=self.user))

    url = detail_url(recipe.id)
    res = self.client.get(url)

    serializer = RecipeDetailSerializer(recipe)

    self.assertEqual(res.data, serializer.data)
```

> Note: Firstly you create a sample recipe as a user. Then you add one tag
        and one ingredient (this is how you add ForeignKeys to the *ManyToManyField*
        fields). Next you create a URL with the recipe's ID. Then you create
        GET response as the Client authorized as user on this recipe's detail URL.
        Next you serialize this recipe using recipe detail serializer.
        Finally you check if the data from response matches with data from
        serializer.

> Note: `serializer = RecipeDetailSerializer(recipe)` - as you remember from the
        previous tests, you were passing in `many=True` and this is because you
        were returning the ListView or you wanted to simulate the ListView in
        your serializer. In this case you just want to serialize a single object
        (because this is a detail view and there will always be only one object).

4. Go to the top of the file and import *RecipeDetailSerializer*:

```python
from recipe.serializers import RecipeDetailSerializer
```

5. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

### Implement Feature For Retrieving Recipe Detail

> Note: Next you are going to implement your feature for retrieving the recipe
        detail. You are going to start by adding a recipe detail serializer and
        then you are going to modify your ViewSet to return this serializer when
        accessing the detail action in the ViewSet.

1. Open up *app/recipe/serializers.py* file and create recipe detail serializer
   class using *RecipeSerializer* as the only difference between these two
   serializers is that you want full information about ingredients and tags in
   DetailView:

```python
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer a recipe detail."""

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
```

> Note: The difference between your List and DetailView would be that the detail
        one would specify the actual ingredients and the tag objects that are
        assigned to that recipe. Whereas this ListView as you can see is using the
        *PrimaryKeyRelatedField* so it is only going to return the primary key or
        the ID of the ingredient and the tags associated to that recipe. So what you
        are doing here is that you reuse *TagSerializer* and *IngredientSerializer*
        to create full objects of ingredients and tags added to specific recipe and
        you base the rest of the serializer on the list serializer as the rest of
        that serializer is the same. So you can nest serializers inside each other
        so you can have one recipe detail serializer and then the related key object
        renders or returns the ingredients or tags objects which you can then pass
        into ingredient or tag serializer and use that to convert it to this type of
        object. You also want ingredients and tags to be read only because that is
        the only way that it is going to work for your DetailView.  

2. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail. Error should say that the expected output in your assertion
   was not the same as the actual output. This is because you are not using
   the serializer yet.
3. Head over to *app/recipe/views.py* and modify your *RecipeViewSet*.
   You are going to override a function called *get_serializerclass*. **This is**
   **a function that if called to retrieve the serializer class for a particular**
   **request and it is this function that you would use if you wanted to change the**
   **serializer class for the different actions that are available on the**
   **_RecipeViewSet_. You have a number of actions available by default in the model**
   **ViewSet. One of them is _list_ in which case you just want to return the default**
   **and the other action is _retrieve_ (default action of ViewSet) in which case you**
   **want to return the detail serializer so then when you call the _retrieve_ action**
   **it serializes it using that serializer instead of the default one.**
   (https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions)

```python
def get_serializer_class(self):
    """Return appripriate serializer class."""
    if self.action == 'retrieve':
        return serializers.RecipeDetailSerializer
```

4. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.

> Recommended: Push to GitHub.

---

### Add Tests For Creating Recipes

> Note: Next you are going to implement you feature to create recipes with your
        recipe API. You are going to start by adding some unit tests for creating
        recipes. You are going to create three tests: one to test creating a basic
        recipe, two to test creating a recipe with tags assigned and three to test
        creating a recipe with ingredients assigned.

1. Head over to the *app/recipe/tests/test_recipe_api.py/PrivateRecipeApiTests*
   and add *test_create_basic_recipe*:

```python
def test_create_basic_recipe(self):
    """Test creating recipe."""
    payload = {
        'title': 'Chocolate cheesecake',
        'time_minutes': 30,
        'price': 5.00
    }

    res = self.client.post(RECIPES_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    recipe = Recipe.objects.get(id=res.data['id'])
    for key in payload.keys():
        self.assertEqual(payload[key], getattr(recipe, key))
```

> Note: Firstly you create payload with data to create basic recipe.
        Then you post it on RECIPES_URL as client authenticated as user.
        Next you check if the response is HTTP 201 CREATED. After that you create
        *recipe* variable with all recipes that has id similar to the response's
        data id. Next you loop through all payload's keys and check if the
        payload's keys match with *recipe*'s keys.
        `recipe = Recipe.objects.get(id=res.data['id'])` - When you create an object
        using the Django REST Framework the default behavior is that it will return
        a dictionary containing the created object. This is how You know that if you
        do `res.data` and retrieve the ID key this will get the ID of the created
        object. `getattr(recipe, key)` - You cant just to `recipe.key` because then
        it will try and retrieve the key named *key* from your recipe. Instead you
        would need to use a special Python helper function called *getattr* which is
        a function that allows  you to retrieve an attribute from an object by
        passing in a variable.

2. Next add a test for creating a recipe with tags assigned to it. The way that
   you can assign tags using your recipe API will be to pass in a list of tag IDs
   when you create the recipe and then it will assign those tags to the recipe:

```python
def test_create_recipe_with_tags(self):
    """Test creating recipe with tags."""
    tag1 = sample_tag(user=self.user, name='Vegan')
    tag2 = sample_tag(user=self.user, name='Dessert')

    payload = {
        'title': 'Avocado lime cheesecake',
        'tags': [tag1.id, tag2.id],
        'time_minutes': 60,
        'price': 20.00
    }

    res = self.client.post(RECIPES_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    recipe = Recipe.objects.get(id=res.data['id'])
    tags = recipe.tags.all()
    self.assertEqual(tags.count(), 2)
    self.assertIn(tag1, tags)
    self.assertIn(tag2, tags)
```

> Note: Firstly you create two sample tags. Then you create payload with the
        data to create recipe with these two tags using their IDs. Next you
        do post on the RECIPES_URL using this payload and the Client authorized
        as user. Then you check if the status code from the website is HTTP 201
        CREATED. After that you create *recipe* variable to list all recipe
        objects with the ID of the responses data. Then you also list all tags
        from this recipe that you have just created. Next you check if
        both tags are assigned to that recipe.

3. Add a test for recipe with ingredients:

```python
def test_create_recipe_with_ingredients(self):
    """Test creating recipe with ingredients."""
    ingredient1 = sample_ingredient(user=self.user, name='Prawns')
    ingredient2 = sample_ingredient(user=self.user, name='Ginger')

    payload = {
        'title': 'Thai prawn red curry',
        'ingredients': [ingredient1.id, ingredient2.id],
        'time_minutes': 20,
        'price': 7.00
    }

    res = self.client.post(RECIPES_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    recipe = Recipe.objects.get(id=res.data['id'])
    ingredients = recipe.ingredients.all()
    self.assertEqual(ingredients.count(), 2)
    self.assertIn(ingredient1, ingredients)
    self.assertIn(ingredient2, ingredients)
```

4. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

### Implement Feature For Creating Recipes

> Note: Next you can implement the feature for creating recipes. The only thing
        that you need to change in your ViewSet to enable creating recipes is you
        need to add a *perform_create* function that assigns the user of the recipe
        to the current authenticated user.

1. Open up *app/recipe/views.py/RecipeViewSet* and at the bottom of the ViewSet
   add *perform_create* method:

```python
def perform_create(self, serializer):
    """Create a new recipe."""
    serializer.save(user=self.request.user)
```

> Note: This is all you need to do to make your test pass because the *ModelViewSet*
        allows you to create objects out of the box. So with the default
        functionality of it is if you pass a serializer class and it is assigned
        to a model then it knows how to create new objects with that model when
        you do HTTP POST. The only thing you need to do is to assign the
        authenticated user to that model once it has been created.

2. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.
3. Run `docker-compose up` to start server and check the functionality of this
   API:
* Create a user on *127.0.0.1:8000/api/user/create/*.
* Log in using token on *127.0.0.1:8000/api/user/token/*.
* Add ingredient on *127.0.0.1:8000/api/recipe/ingredients/*.
* Add tags on *127.0.0.1:8000/api/recipe/tags/*.
* Create recipe on *127.0.0.1:8000/api/recipe/recipes/*.
* Check details of that recipe on *127.0.0.1:8000/api/recipe/recipes/<ID>*.

> Recommended: Push to GitHub.

---

### Add Tests For Updating Recipes

> Note: Next you are going to add some tests for updating your recipes. Since
        the *update* feature comes with the Django REST Framework out of the box
        for the *ModelViewSet* you technically do not need to create these tests
        because you are testing functionality that is already there however just
        to make sure that your tests fully cover all features that you are going
        to be using in your app and also to show how you would test updating API,
        you are going to create the test for updating the recipe anyway.
        There are two ways in which you can update an object using the API.
        There is two different HTTP methods: one is *PATCH* and the other
        is *PUT*. *PATCH* is used to update the fields that are provided in the
        *payload* so the only fields that are going to change are the fields
        that are provided and any fields that are omitted from the request will
        be not modified in the object that is being updated.  

1. Head over to *app/recipe/tests/test_recipe_api.py/PrivateRecipeApiTests* and
   add test for partial update:

```python
def test_partial_update_recipe(self):
    """Test updating a recipe with patch."""
    recipe = sample_recipe(user=self.user)
    recipe.tags.add(sample_tag(user=self.user))
    new_tag = sample_tag(user=self.user, name='Curry')

    payload = {'title': 'Chicken tikka', 'tags': [new_tag.id]}
    url = detail_url(recipe.id)
    self.client.patch(url, payload)

    recipe.refresh_from_db()

    self.assertEqual(recipe.title, payload['title'])
    tags = recipe.tags.all()
    self.assertEqual(len(tags), 1)
    self.assertIn(new_tag, tags)
```

> Note: You start by creating a sample recipe. Then you add a tag to the recipe.
        Then you create a new tag. Then you create a payload with the new
        title and that new tag. What you expect is the title and tag will update
        to payload's. So there will be new title and only one, newly replaced
        tag. Then you create recipe detail URL from your new recipe.
        after that you *patch* the recipe's data with the payload's. You are
        going to retrieve an update to the recipe from the database and then
        you are going to check the fields that are assigned and just to make
        sure they match what you expect. `recipe.refresh_from_db()` refreshes
        the details in your recipe from the database. **Typically when you**
        **create a new model and you have a reference to a model, the details**
        **of that will not change unless you do refresh from DB if the values**
        **have changed in the database. So once you have retrieved them from**
        **the database, thy are the same in Python and even if you change them**
        **in the Postgres database, they do not update in your object unless**
        **you call _refresh_from_db()**. Next you assert that the title is equal
        to the new title. Then you store all recipe's tags in a variable and
        you check if the length of this variable is one and if newly created tag
        is in these tags that you retrieved. To check length of these lists you
        can use `count()` or `len()`.

2. Test full update recipe using HTTP PUT:

```python
def test_full_update_recipe(self):
    """Test updating a recipe with put."""
    recipe = sample_recipe(user=self.user)
    recipe.tags.add(sample_tag(user=self.user))
    payload = {
        'title': 'Spaghetti carbonara',
        'time_minutes': 25,
        'price': 5.00
    }
    url = detail_url(recipe.id)
    self.client.put(url, payload)

    recipe.refresh_from_db()

    self.assertEqual(recipe.title, payload['title'])
    self.assertEqual(recipe.time_minutes, payload['time_minutes'])
    self.assertEqual(recipe.price, payload['price'])
    tags = recipe.tags.all()
    self.assertEqual(len(tags), 0)
```

> Note: What you expect to happen with a *PUT* is it will replace the object
        that you are updating with the full object that is provided in the
        request. That means if you exclude any fields in the *payload*, those
        fields will actually be removed from the object that you are updating.
        So you create sample recipe and then add sample tag to that recipe.
        Next you create a *payload* with data to update. Then you create the URL
        and request. Next you refresh recipe and check if the *title*,
        *time_minutes* and *price* in payload is the same as the retrieved
        recipe object. Finally you check that the tags assigned are zero because
        when you do a HTTP PUT and you omit a field, that should clear the value
        of that field. Now your recipe that did have a sample tag assigned,
        should not have any tags assigned.  

3. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.

## Add Upload Image Endpoint

> Note: In this section you are going to add your image upload feature to the
        recipe endpoint. This will allow you to upload images to go along with
        your recipes. Before you can upload images you are going to need to add
        a image field to your recipe model in order to use the image field in
        Django. You need to install the *Pillow* Python package which is used
        for manipulating images which are uploaded in Python. If you have not
        done so already, make sure you commit all of the changes that you have
        done so far.

### Add Pillow Requirement

1. Open up your *requirements.txt* file and add *Pillow* dependency underneath
   *psycopg2*: ```Pillow>=5.3.0,<5.4.0```.

2. *Pillow* requires some Linux packages to be installed before you can
   successfully compile and install it using the PIP package manager. You are
   going to make some small changes to the *Dockerfile* to support installing
   *Pillow*. Head over to the *Dockerfile* and add `jpeg-dev` to the
   `RUN apk add --update --no-cache postgresql-client` command:
   `RUN apk add --update --no-cache postgresql-client jpeg-dev`.

> Note: This adds the JPEG dev binaries to your *Dockerfile*.

3. Next add some temporary build dependencies that are required for installing
   the *Pillow* package. Update command with installation of the temporary
   dependencies to:

```
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
```

> Note: These `musl-dev`, `zlib` and `zlib-dev` packages are retrieved from the
        PyPI page for the *Pillow* dependencies. It outlines all the dependencies
        that you need to have installed before you can install the requirement.

4. Next make some changes to the file structure in your Docker container. This
   is so you have a place where you can store the static and media files within
   your container without getting any permission errors:
* Above `RUN adduser -D user` command add `RUN mkdir -p /vol/web/media` and
  `RUN mkdir -p /vol/web/static` to create *media* and *static* folders.
  `-p` means to create whole path. Other way it would say that there is no path
  like `/vol/web/` to create *media*/*static*. So if the */vol/web/* directory does
  not exist, it will create them. Good habbit is to store any files that may need to
  be shared with other containers in a subdirectory called *vol*. This way you know
  where all of the volume mappings need to be in your container if you need to share
  this data with other containers in your service. For example if you had an EngineX
  or a web server that needed to serve these media files you know that you would
  need to map this volume and share it with the web server container.
  You create *static* because in Django you typically have two files that hold
  static data. Ine is the *static* and that is typically used for things like
  JavaScript CSS files or any static files that you may want to serve which are not
  typically changing during the execution of the application. The *media* directory
  is typically used for any media files that are uploaded by the user. So that is
  where you are going to store your recipe images.
* Then you add user with the `RUN adduser -D user` command and after that change
  the ownership of these files to the user that you have added. It is very important
  that you do this before you switch to the user because once you switch to the user
  it cannot give itself permissions to view or access these files. You need to give
  it while you are still running as the root user which is before you switch to the
  user. So set the ownership of all the directiories within the *vol* directory to
  your custom user: `RUN chown -R user:user /vol/`. `-R` means recursive so instead
  of just setting the *vol* permissions it will set any subdirectories in the *vol*
  folder. Next add permissions to that folder. `-R 755` means that the user (now
  owner) can do everything with the directory and the rest can read and execute from
  the directory.
5. Head over to the *app/app/settings.py* file and configure static URL, media
   URL, static root and media root. Scroll to the bottom of the file and after
   `STATIC_URL = '/static/'` add:

```python
MEDIA_URL = '/media/'

MEDIA_ROOT = 'vol/web/media'
STATIC_ROOT = '/vol/web/static'
```

> Note: Static files will be served from the */static/* part of your web server
        and the media from */media/* part. For example when you upload an image
        there will be created the URL with this image on
        `127.0.0.1:8000/media/uploads/recipe/<YOUR_UUID_NAME>.png`. That way when
        you upload media files you have an accessible URL so that you can access
        them through your web server. Next you add media and static root. What
        it does is it tells Django where to store all the media/static files. You
        want all of the media/static files to be stored in the */vol/web/media/*
        (or */vol/web/static/*) directory that you create as part of your build
        process in your Docker container. Django actually comes with a command
        called *collect staticfiles* and it collects all the staticfiles from any
        dependency that you have and it combines them all and stores  them in the
        *static root*. You can run this one starting your project and it will pull
        all of the CSS and JavaScript that are required for the Django REST
        Framework browsable API and for the Django admin and it will sore them in
        this static directory. That means when you are serving your project in
        production you can access these staticfiles and you can view the Django
        admin just as you can view it in your local machine.

6. Open up *app/app/urls.py* file and do some imports:
* `from django.conf.urls.static import static`.
* `from django.conf import settings`.
7. Add a URL for your media files to the *urlpatterns*:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

> Note: By default the Django development server will serve static files for any
        dependencies in your project. However it does not serve media files by
        default. You need to manually add this in the URLs. What this does is it
        makes the media URL available in your development server so you can test
        uploading images for your recipes without having to set up a separate web
        server for serving these media files.

8. Build your Docker image and make sure that it builds successfully with your
   new dependencies. Head over to the terminal and run `docker-compose build`.

---

### Modify Recipe Model

> Note: Next you are going to modify your recipe model to accept an *ImageField*.
        You are going to start by adding the function that generated the name which
        you are going to call the *ImageField* on the system after the image has
        been uploaded. Whenever you upload a file to a Django model you need to
        make sure you change the name and you do not just use the same name that
        was uploaded. This is to make sure all the names are consistent and also
        to make sure that there are no conflicts with the name that you upload.
        You are going to generate a function which will create the path to the
        image on your system and you are going to use a *UUID* to uniquely
        identify the image that you assign to the *ImageField*. You start with
        some unit tests to test this new function.

1. Head over to the *app/core/tests/test_models.py* and import:
   `from unittest.mock import patch`.
2. Scroll to the bottom of *ModelTests* and add *test_recipe_file_name_uuid*
   under the *test_recipe_str*:

```python
@patch('uuid.uuid4')
def test_recipe_file_name_uuid(self, mock_uuid):
    """Test that image is saved in the correct location."""
    uuid = 'test-uuid'
    mock_uuid.return_value = uuid
    file_path = models.recipe_image_file_patch(None, 'myimage.jpg')

    exp_path = f'uploads/recipe/{uuid}.jpg'
    self.assertEqual(file_path, exp_path)
```

> Note: You are going to mock the UUID function from the default UUID library
        that comes with Python and you are going to change the value that it
        returns. Then you are going call your function and and make sure that
        the string that is created for the path matches what you expect it to
        match with the sample UUID.. You add *patch* decorator to the top of
        this function and then the path of the function that you are going to
        mock is going to be `uuid.uuid4`. UUID module will generate a unique
        UUID version 4. Next you create `uuid` variable to choose the value
        that you will use when mocking. After that you mock the UUID - pass
        the functionality of the UUID to mock. Mock will use this
        functionality and then it will set the returned value to the *uuid*
        variable. Next you create a file path using *recipe_image_file_patch*
        which basically stripes the format of the media (i. e. *.jpg* or *.png)*
        from the name, remembers the format, sets new name using UUID (mocked
        to the *uuid* variable) and adds format. After that you create path
        that you expect it to be so `uploads/recipe/test-uuid.jpg`. Finally
        you check if the expected file path is the same as the path that was
        created using UUID and recipe_image_file_patch model's method.

3. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.
4. Head over to the *app/core/models.py* file and import:
* `import uuid`: to generate UUID.
* `import os`: to create a valid path for your file destination.
5. Create the *recipe_image_file_patch* function just above *UserManager*:

```python
def recipe_image_file_patch(instance, filename):
    """Generate file path for new recipe image."""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/recipe/', filename)
```

> Note: Two parameters: *instance* is creating the path, *filename* the
        original filename of the file. Then you split the filename to the name
        and file type and the you save the last part to the *ext* variable.
        Next your generate UUID version 4 name and add the extension of the
        original file. Finally you return the new filename with full path that
        you want to use as the storage for that file.

6. Scroll down to the *Recipe* model and add new *image* field:

```python
image = models.ImageField(null=True, upload_to=recipe_image_file_patch)
```

> Note: This field is optional so the `null=True`. You do not want to add the
        `()` at the end of `upload_to=recipe_image_file_patch` because you do
        not want to call the function, you just want to pass a reference to
        the function so it can be called every time you upload. It gets called
        in the background by Django by the *ImageField* feature.

7. Head over to the terminal and run migrations:

```
docker-compose run --rm app sh -c "python manage.py makemigrations core"
```

8.  Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.

> Recommended: Push to GitHub.

---

### Add Tests For Uploading Image To Recipe

> Note: Now that you have your image field available on your *Recipe* model,
        you can add the API for uploading images. You are going to start by
        adding a few tests to test uploading images through your API.

1. Head over to the *app/recipe/tests/test_recipe_api.py* and do some imports:
* `import tempfile`: a Python function that comes out of the box of Python
  that allows you to generate temporary files. It allows you to call a
  function which will then create a temp file somewhere in the system and then
  you can remove that file after you have used it.
* `import os`: allows to perform creating path names and also checking if
  files exist on the system.
* `from PIL import Image`: `PIL` is *Pillow* requirement and this is basically
  the original name and the *Pillow* is just a fork of it which was then built
  on and is the recommended latest version by Django. This import will let you
  create test images which you can then upload to your API.
2. Next add a helper function at the top. This function will return URL for
   recipe image upload:

```python
def image_upload_url(recipe_id):
    """Return URL for recipe image upload."""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])
```

> Note: You are going to need an existing recipe to call this function.
        First `recipe` is the name of the app defined in
        *app/recipe/urls.py/app_name*. Second `recipe` is the name of the
        model linked to the ViewSet's *queryset* (converted to lowercase).
        `upload-image` is `upload_image` method in
        *app/recipe/views.py/RecipeViewSet* identified by the `url_path` in
        the `upload_image`'s `action` decorator.

3. Scroll to the bottom and add new test class because there is going to be
   some common functionality for the image upload test that you are going to
   want to repeat and it is a good idea to keep it separate from the rest:

```python
class RecipeImageUploadTests(TestCase):
    """Test Image Upload API."""
```

4. Add *setUp* function to create the authenticated client and recipe:

```python
def setUp(self):
    """Set up authorized client and recipe."""
    self.client = APIClient()
    self.user = get_user_model().objects.create_user(
        'test@gmail.com',
        'admin123'
    )
    self.client.force_authenticate(self.user)
    self.recipe = sample_recipe(user=self.user)
```

> Note: You add recipe because it is going to be a consistent theme for all of
        the tests.

5. Add *tearDown* function. As the *setUp* is always called before tests, the
   *tearDown* is being called after the tests. You create this so that after
   the tests all the sample images stored in the file system would be deleted.
   Thanks to that method you will make sure that your file system is kept
   clean after your tests:

```python
def tearDown(self):
    """Clean after tests."""
    self.recipe.image.delete()
```

6. Add `test_upload_image_to_recipe` to test uploading an image to recipe:

```python
def test_upload_image_to_recipe(self):
    """Test uploading an image to recipe."""
    url = image_upload_url(self.recipe.id)
    with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
        img = Image.new('RGB', (10, 10))
        img.save(ntf, format='JPEG')
        ntf.seek(0)
        res = self.client.post(url, {'image': ntf}, format='multipart')

    self.recipe.refresh_from_db()
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertIn('image', res.data)
    self.assertTrue(os.path.exists(self.recipe.image.path))
```

> Note: You create a recipe's (from *setUp*) URL for uploading image to that
        recipe using *image_upload_url* helper function that you have just
        created. This is going to use the sample recipe that gets created and
        then you are going to use a context manager `with`. This creates a
        named temporary file on the system at a random location (usually in
        */temp* folder). You do it using *NamedTemporaryFile*. You also can
        give it a suffix which is going to be the extension that you want to
        use (you want picture so *.jpg*). Next you put `nft` and the reason
        you named temporary file is because you want to pass it into the
        *ImageField*. So that context manager creates a temporary file in the
        system that you can then write to and then after you exit the context
        manager it will automatically remove that file. So within that `with`
        statement, so within that temporary file (set up to *.jpg*), you write
        an image (a 10x10 resolution black square) and then save it as the
        JPEG file. `ntf.seek(0)` it is the way that Python reads files. So
        because you have saved the file, the seeking will be done to the end
        of the file. If you try to access it then it would just be blank
        because you have already read up the end of the file so use this
        `seek` function to set the pointer back to the beginning of the file
        so then it is as if you have just opened it. Then you create a POST
        request on the image upload URL with the payload containing temp
        image. You also define format as *multipart* to tell Django that you
        want to make a multi-part form request which means a form that
        consists of data. By default it would just be a form that consists of
        a JSON object and you actually want to post data so you need to pass
        in this `format='multipart'`. Then you run assertions that the
        response's status code should be OK, the image should be the part of
        responses data and you check if the path to that image exists.

7. Create test uploading a bad image:

```python
def test_upload_image_bad_request(self):
    """Test uploading an invalid image."""
    url = image_upload_url(self.recipe.id)
    res = self.client.post(url, {'image': 'notimage'}, format='multipart')

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
```

> Note: You create URL for uploading image for the pre-created reciepe.
        Then you create a POST request on that URL as the authorized as user
        client passing string as image (which is wrong). You also set up the
        format to the multipart because you only want the image type to be
        bad. Finally you assert that the response should be HTTP 400.

8. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect to fail.

---

### Add Feature To Upload Image

> Note: Next you can implement the feature to upload your image and make your
        test pass. You are going to start by creating a serializer that will
        handle the uploaded image and then you are going to **modify your**
        **ViewSet to accept a new action that allows you to upload an image**
        **for a recipe**.

1. Head over to the *app/recipe/serializers.py* and create a new serializer to
   the bottom:

```python
class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes."""

    class Meta:
        """Meta class of RecipeImageSerializer."""

        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)
```

2. Head over to the *app/recipe/views.py* file and import:
* `from rest_framework.decorators import action`: decorator to add custom actions
  to your ViewSet.
* `from rest_framework.response import Response`: for returning a custom response.
* `from rest_framework import status`: the same module that you import in your
  test to check the status. You are going to use it to generate a status for your
  custom action.
3. Scroll down to the *RecipeViewSet* and add a new action:

__You define actions as functions in the ViewSet. By default it has these__
__*get_queryset*, *get_serializer_class* and *perform_create*. These are all__
__default actions that you override. So if you did not override them then they__
__will just perform the default action that the Django REST Framework does. You__
__can actually add custom functions here and define them as custom actions. The__
__way you do that is you use the *action* decorator and defining the method__
__that your action is going to accept. So the method could be POST, PUT, PATCH__
__or GET. You are going to make the action just POST. You are going to allow__
__users to post an image to your recipe.__

```python
@action(methods=['POST'], detail=True, url_path='upload-image')
def upload_image(self, request, pk=None):
    """Upload an image to a recipe."""
    recipe = self.get_object()
    serializer = self.get_serializer(
        recipe,
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
```

> Note: In *action* decorator you set up the method that you want to allow
        users to perform. Next `detail=True` to say this action will be for
        the detail and the *detail* is a specific recipe so you are going to
        only be able to upload images for recipe that already exist and you
        will use the detail URL that has the ID of the recipe in the URL. It
        knows which one to upload the image to. Then you add
        `url_path='upload-image'`. That is the path name for your URL; the
        path that is visible within the URL (so it will be the detail URL) so
        *127.0.0.1:8000/api/recipe/recipes/<RECIPE'S ID>/upload-image/*. Next
        you create the *upload_image* with the `pk=None` parameter as primary
        key that is passed in with the URL gets passed into the view as *pk*.
        Then you retrieve the recipe object that is being accessed based on
        the ID in the URL. Then you call serializer to pass in your recipe
        and the request's data. Then you check if the serilizer is valid.
        This validates the data to make sure it is all correct. It makes sure
        that the image field is correct and that no other extra fields have
        been provided. If it is valid you can use the *save* function to save
        object. That basically performs a *save* on the recipe model with the
        updated data. Next your return a response with the content of
        serializer's data which is going to contain serilizer's objects that
        were uploaded which will be the ID of the recipe and the URL of the
        image. You also pass status code HTTP 200 OK to that response.
        If the serializer is invalid there is the standard way where you
        return the errors for the serializer (these are automatically
        generated by the Django REST Framework; it will perform some auto
        validation on your field and if it does not pass the validation then
        it creates these errors for you which lists all of the fields that
        have errors in the data) and then you assign the status of HTTP 400
        BAD REQUEST.

4. The last thing to do is to update the *get_serializer_class* function.

__You could have just got the serializer in *upload_image*'s *serializer* and__
__set the correct serializer to your *RecipeImageSerializer*. The reason you__
__do not do that is because the best practice is to return the serializer__
__using this *get_serializer_class*. This way the Django REST Framework knows__
__which serializer to display in the browsable API.__

So within *get_serializer_class* you will check if the *action* is *upload-image*:

```python
def get_serializer_class(self):
    """Return appripriate serializer class."""
    # retrieve is a default action of ViewSet
    if self.action == 'retrieve':
        return serializers.RecipeDetailSerializer
    elif self.action == 'upload_image':
        return serializers.RecipeImageSerializer

    return self.serializer_class
```

5. Run test - `docker-compose run --rm app sh -c "python3 manage.py test && flake8`.
   Expect OK.
6. Test the endpoint in the browser -
   *127.0.0.1:8000/api/recipe/recipes/1/upload-image/*.

> Recommended: Push to GitHub.
