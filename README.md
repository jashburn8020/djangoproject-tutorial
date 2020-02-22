# Create a project

-   `django-admin startproject mysite`
    -   creates a `mysite` directory in your current directory
-   Files:
    -   outer `mysite/`: Container for your project
    -   `manage.py`: command-line utility that lets you interact with this Django project
    -   inner `mysite/`: the actual Python package for your project; its name is the Python package name you’ll need to use to import anything inside it
    -   `mysite/__init__.py`: an empty file that tells Python that this directory should be considered a Python package
    -   `mysite/settings.py`: settings/configuration for this Django project
    -   `mysite/urls.py`: URL declarations for this Django project
    -   `mysite/asgi.py`: entry-point for ASGI-compatible web servers
    -   `mysite/wsgi.py`: entry-point for WSGI-compatible web servers

# Run the development server

-   `python manage.py runserver`
-   by default, the runserver command starts the development server on the internal IP at port 8000
-   to change the server's port: `python manage.py runserver 8080`

# Create an app

-   Project
    -   a collection of configuration and apps for a particular website
    -   can contain multiple apps
-   App
    -   a Web application that does something, e.g., a small poll app
    -   can be in multiple projects
    -   can live anywhere on your Python path
-   `python manage.py startapp polls`
-   Files:
    -   `polls/`
        -   `__init__.py`
        -   `admin.py`
        -   `apps.py`
        -   `migrations/`
            -   `__init__.py`
        -   `models.py`
        -   `tests.py`
        -   `views.py`

# Database setup

-   `mysite/settings.py` > `DATABASES`
-   For databases other than SQLite:
    -   install the appropriate database bindings
    -   change the following keys to match your database connection settings:
        -   `ENGINE` - either `django.db.backends.sqlite3`, `django.db.backends.postgresql`, `django.db.backends.mysql`, or `django.db.backends.oracle`
            -   other backends are also available
        -   `NAME` - the name of your database
    -   additional settings such as `USER`, `PASSWORD`, and `HOST` must be added
    -   create a database with `CREATE DATABASE database_name;`
    -   make sure that the database user provided has `create database` privileges
-   Some of the applications in `mysite/settings.py` > `INSTALLED_APPS` make use of at least one database table, so we need to create the tables in the database before we can use them
    -   `python manage.py migrate`
    -   `migrate` command looks at the `INSTALLED_APPS` setting and creates any necessary database tables according to the database settings in your `mysite/settings.py` file and the database migrations shipped with the apps

# Models and database

-   Define models in `polls/models.py`
    -   allows Django to
        -   create a database schema (`CREATE TABLE` statements) for this app
        -   create a Python database-access API for accessing `Question` and `Choice` objects
-   Tell our project that the `polls` app is installed
    -   `PollsConfig` class is in the `polls/apps.py` file, so its dotted path is `polls.apps.PollsConfig`
    -   add that dotted path to the `mysite/settings.py` > `INSTALLED_APPS` setting
-   Tell Django that you've made some changes to your models (in this case, you've made new ones) and that you'd like the changes to be stored as a _migration_
    -   `python manage.py makemigrations polls`
-   Migrations are how Django stores changes to your models (and thus your database schema)
    -   migration for your new model is in the file `polls/migrations/0001_initial.py`
-   See what SQL that migration would run
    -   `python manage.py sqlmigrate polls 0001`
-   Check for any problems in your project without making migrations or touching the database
    -   `python manage.py check`
-   Create model tables in your database
    -   `python manage.py migrate`
-   The `migrate` command takes all the migrations that haven't been applied and runs them against your database
    -   Django tracks which ones are applied using a special table in your database called `django_migrations`
    -   synchronizes the changes you made to your models with the schema in the database
    -   lets you change your models over time, as you develop your project, without the need to delete your database or tables and make new ones
    -   specializes in upgrading your database live, without losing data
-   Commit migrations to your version control system and ship them with your app
    -   make your development easier
    -   usable by other developers and in production

# Database API

-   Invoke the Python shell
    -   `python manage.py shell`
-   Use the database API
    -   see <https://docs.djangoproject.com/en/3.0/topics/db/queries/>

# Django Admin

-   Create an admin user
    -   `python manage.py createsuperuser`
-   Start the development server
    -   `python manage.py runserver`
-   Go to <http://127.0.0.1:8000/admin/> on your browser
    -   you should see a few types of editable content: groups and users - provided by `django.contrib.auth`, the authentication framework shipped by Django
-   Make the poll app modifiable in the admin site
    -   tell the admin site that `Question` objects have an admin interface
    -   add `admin.site.register(Question)` to `polls/admin.py`
-   The Questions admin form:
    -   automatically generated from the `Question` model
    -   different model field types (`DateTimeField`, `CharField`) correspond to the appropriate HTML input widget

# Views

-   A "type" of Web page that generally serves a specific function and has a specific template
-   Each view is represented by a Python function (or method, in the case of class-based views)
-   To get from a URL to a view, Django uses 'URLconfs'
    -   map URL patterns to views
    -   see <https://docs.djangoproject.com/en/3.0/topics/http/urls/>
-   When a request is made to, say, "/polls/34/"
    -   Django will load the `mysite.urls` Python module
        -   pointed to by `ROOT_URLCONF` in `mysite/settings.py`
    -   finds the variable named `urlpatterns` and traverses the patterns in order
    -   after finding the match at `polls/`, it strips off the matching text, `polls/`, and sends the remaining text, `34/`, to the `polls.urls` URLconf for further processing
        -   `path("polls/", include("polls.urls"))`
    -   there it matches `<int:question_id>/`, resulting in a call to the `detail()` view
        -   `path("<int:question_id>/", views.detail, name="detail")`
-   Each view is responsible for doing one of two things
    1.  returning an `HttpResponse` object containing the content for the requested page, or
    2.  raising an exception such as `Http404`

## Templates

-   Your project's `mysite/settings.py` > `TEMPLATES` setting describes how Django will load and render templates
    -   configures a `DjangoTemplates` backend whose `APP_DIRS` option is set to `True`
    -   by convention `DjangoTemplates` looks for a `templates` subdirectory in each of the `INSTALLED_APPS`
-   Create templates in `polls/templates/polls/<template>`, including all preceding subdirectories
    -   refer to this template within Django as `polls/<template>`, e.g., `polls/index.html`
-   Template namespacing
    -   you might be able to get away with putting our templates directly in `polls/templates` (rather than creating another polls subdirectory)
    -   Django will choose the first template it finds whose name matches
    -   if you had a template with the same name in a different application, Django would be unable to distinguish between them
    -   the best way to avoid this problem is by namespacing them
        -   by putting those templates inside another directory named for the application itself
-   See <https://docs.djangoproject.com/en/3.0/topics/templates/>

# Sources

-   "Writing your first Django app, part 1." <https://docs.djangoproject.com/en/3.0/intro/tutorial01/>.
-   "Writing your first Django app, part 2." <https://docs.djangoproject.com/en/3.0/intro/tutorial02/>.
-   "Writing your first Django app, part 3." <https://docs.djangoproject.com/en/3.0/intro/tutorial03/>.
-   "django-admin and manage.py." <https://docs.djangoproject.com/en/3.0/ref/django-admin/>.
