# Solve-for-tomorrow-flights

## Setup Flask Server

* `pipenv shell`
* `pipenv install` - will create a virtual env and install the dependencies in it.
* `pipenv graph` - to see the dependenies installed.
* `pipenv install <package-name>` - to install any new dependency in the project.
* `export FLASK_APP=api` && `flask run` - run the web server [If on Windows - use `set` instead of `export`]
* `pip install Flask-PyMongo dnspython` - Somehow Flask-Pymongo even with pipenv installed not working.