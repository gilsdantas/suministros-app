## Technical Requirements

These are the main tech requirement. The complete list is in requirements.txt.

- [Python 3](http://python.org/)
- [Pip](https://pip.pypa.io/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLite](http://sqlite.org/) (or any other supported database)

These are optional but recommended.

- [Black](http://black.readthedocs.io/)
- [Codecov](http://codecov.io/)
- [Flake8](http://flake8.pycqa.org/)
- [Pipenv](http://pipenv.readthedocs.io)
- [Pre-commit](http://pre-commit.com/)

### Installing

The default Git version is the master branch. ::

    # clone the repository
    $ cd desired/path/
    $ git clone git@github.com:ericrommel/quizz-app.git/

The next step is install the project's Python dependencies. Just like _Git_ if you still don't have it go to the [official site](http://python.org/) and get it done. You'll also need [Pip](https://pip.pypa.io/), same rules applies here. Another interesting tool that is not required but strongly recommended is [Pipenv](http://pipenv.readthedocs.io), it helps to manage dependencies and virtual environments.

Installing with **Pip**:

    cd path/to/quiz-project
    pip install -r requirements.txt

Installing with **Pipenv**:

    pip install --upgrade pipenv
    cd path/to/quiz-project
    pipenv sync -d

### Start Container

Docker and docker-compose should be installed first. [Tutorial here](https://docs.docker.com/install/).
At the repo root run:
    $ docker-compose up --build

Now you can use. Open <http://127.0.0.1:5000> in a browser and enjoy!

### Run

If you want to run without docker, configure the application manually. This will require you to define a few variables and create the database.

Note: The pipenv virtual environment should be done.

Set the environment variables::

    export FLASK_APP=backend/run
    export FLASK_ENV=development
    export FLASK_CONFIG=development

Or on Windows cmd::
    > set FLASK_APP=src
    > set FLASK_ENV=development
    > set FLASK_CONFIG=development

Create the database::

    flask db init
    flask db migrate
    flask db upgrade

Run the application::

    flask run

Open <http://127.0.0.1:5000> in a browser.

Note: An _ADMIN_ user should be add first. After that, you can add questions. Check the next section for more details.
