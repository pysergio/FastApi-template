Quickstart
----------

Then run the following commands to bootstrap your environment with ``poetry``:

    git clone https://github.com/pysergio/weather-app.git
    cd weather-app
    poetry install
    poetry shell

Then create ``.env`` file based on ``.env.example`` in project root and set environment variables for application: ::

    cp .env.example .env

To run the web application in debug use::

    poetry run uvicorn app.main:app --reload

Run with Docker
----------------------

You must have ``docker`` and ``docker-compose`` tools installed to work with material in this section.
First, create ``.env`` file like in `Quickstart` section or modify ``.env.example``.
**NOTE** ensure numbers of workers cover required performance 
Then just run::

    docker-compose up

Application will be available on [localhost](http://localhost:8000/docs#/) in your browser.

Web routes
----------

All routes are available on ``/docs`` or ``/redoc`` paths with Swagger or ReDoc.
