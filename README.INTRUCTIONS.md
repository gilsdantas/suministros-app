# Maria Online Store App Summary
This is a web app using Python and Flask. For this project, the strategy was to
use a flask application factory approach with blueprints. This is a recommendation as
good practices to build Flask applications.

## Technical Requirements

These are the main tech requirement. The complete list is in requirements.txt.

- [Python 3](http://python.org/)
- [Pip](https://pip.pypa.io/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLite](http://sqlite.org/) (or any other supported database)


### Installing

The next step is install the project's Python dependencies. Make sure you have the
Python installed. if you still don't have it go to the [official site](http://python.org/)
and get it done. Python usually comes with [Pip](https://pip.pypa.io/). This tool
will install all necessary project dependencies.

Installing with **Pip**:

    cd path/to/project/suministros-app
    pip install -r requirements.txt


### Run

Following the best practices from the official Flask documentation, you have to
define a few variables and create the database.

**Note:** The virtual environment should be done.

Set the environment variables::

    ```bash
    $ export FLASK_APP=run
    $ export FLASK_ENV=development
    $ export FLASK_CONFIG=development
    ```

Or on Windows cmd:

    ```console
    c:\path\to\project\suministros-app> set FLASK_APP=run
    c:\path\to\project\suministros-app> set FLASK_ENV=development
    c:\path\to\project\suministros-app> set FLASK_CONFIG=development
    ```

Create the database::

**Note:** The below first line (db init) is only needed when running for the first time

    ```bash
    $ flask db init
    $ flask db migrate
    $ flask db upgrade
    ```

Run the application::

    ```bash
    $ flask run
    ```

Open <http://127.0.0.1:5000> in a browser.

Note: An _ADMIN_ user should be add first. After that, you can add questions. Check the next section for more details.

## Author

- [Maria Dantas](https://github.com/mariadantas)

## License

This project is licensed under the GNU License - see the [License](./LICENSE) file for details.
