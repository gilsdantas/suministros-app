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
or, just in one line:

    ```bash
    $ export FLASK_APP=run && export FLASK_ENV=development && export FLASK_CONFIG=development
    ```

**Note:** If you want to run the app in debug mode, add the below environment variable as well:

    ```bash
    $ export FLASK_DEBUG=1
    ```

Or on Windows cmd:

    ```console
    c:\path\to\project\suministros-app> set FLASK_APP=run
    c:\path\to\project\suministros-app> set FLASK_ENV=development
    c:\path\to\project\suministros-app> set FLASK_CONFIG=development
    c:\path\to\project\suministros-app> set FLASK_DEBUG=1
    ```

Create the database::

**Note:** These commands are needed just when running for the first time

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

Note: An _ADMIN_ was created to allow access the admin page: admin@admin.com/admin

## Next Steps

As the next steps of this project, some topics should be addressed:
- Password are stored in plain text. Use a `passlib` or any other framework like `werkzeug.security`
- Redirecting is not working properly when a new user does a registration
- Click on Home or company name (Maria Online Store) is not redirecting to the home page
- Flash messages (notifications need to be revisited)
- Number formats are incorrect. E.g.: 23.5 or 54.989999999999995

## Author

- [Maria Dantas](https://github.com/mariadantas)

## License

This project is licensed under the GNU License - see the [License](./LICENSE) file for details.
