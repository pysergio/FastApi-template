
Quickstart
----------

Then run the following commands to bootstrap your environment with ``poetry``: ::

    git clone https://github.com/amm0day/FastApi-template
    cd terminal-api
    poetry install
    poetry shell

Then create ``.env`` file based on ``.env.example`` in project root and set environment variables for application: ::

    cp .env.example .env
    echo DB_CONNECTION=mongodb://$MONGO_USER:$MONGO_PASSWORD@$MONGO_HOST:$MONGO_PORT/$MONGO_DB >> .env
    echo SECRET_KEY=$(openssl rand -hex 32) >> .env

To run the web application in debug use::

    poetry run uvicorn app.main:app --reload

Run tests
---------

Tests for this project are defined in the ``tests/`` folder. 

This project uses `pytest
<https://docs.pytest.org/>`_ to define tests because it allows you to use the ``assert`` keyword with good formatting for failed assertations.


To run all the tests of a project, simply run the ``pytest`` command: ::

    $ pytest
    ================================================= test session starts ==================================================
    platform linux -- Python 3.8.3, pytest-5.4.2, py-1.8.1, pluggy-0.13.1
    rootdir: /home/some-user/user-projects/terminal-api, inifile: setup.cfg, testpaths: tests
    plugins: env-0.6.2, cov-2.9.0, asyncio-0.12.0
    collected 90 items

    tests/test_api/test_errors/test_422_error.py .                                                                   [  1%]
    tests/test_api/test_errors/test_error.py .                                                                       [  2%]
    tests/test_api/test_routes/test_articles.py .................................                                    [ 38%]
    tests/test_api/test_routes/test_authentication.py ..                                                             [ 41%]
    tests/test_api/test_routes/test_comments.py ....                                                                 [ 45%]
    tests/test_api/test_routes/test_login.py ...                                                                     [ 48%]
    tests/test_api/test_routes/test_profiles.py ............                                                         [ 62%]
    tests/test_api/test_routes/test_registration.py ...                                                              [ 65%]
    tests/test_api/test_routes/test_tags.py ..                                                                       [ 67%]
    tests/test_api/test_routes/test_users.py ....................                                                    [ 90%]
    tests/test_db/test_queries/test_tables.py ...                                                                    [ 93%]
    tests/test_schemas/test_rw_model.py .                                                                            [ 94%]
    tests/test_services/test_jwt.py .....                                                                            [100%]

    ============================================ 90 passed in 70.50s (0:01:10) =============================================
    $

If you want to run a specific test, you can do this with `this
<https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests>`_ pytest feature: ::

    $ pytest tests/test_api/test_routes/test_users.py::test_user_can_not_take_already_used_credentials

Deployment with Docker
----------------------

You must have ``docker`` and ``docker-compose`` tools installed to work with material in this section.
First, create ``.env`` file like in `Quickstart` section or modify ``.env.example``.
``POSTGRES_HOST`` must be specified as `db` or modified in ``docker-compose.yml`` also.
Then just run::

    docker-compose up -d app

Application will be available on ``localhost`` in your browser.

Web routes
----------

All routes are available on ``/docs`` or ``/redoc`` paths with Swagger or ReDoc.


Project structure
-----------------

Files related to application are in the ``app`` or ``tests`` directories.
Application parts are:

::

    app
    ├── api                     - web related stuff.
    │   ├── dependencies        - dependencies for routes definition.
    │   ├── errors              - definition of error handlers.
    │   └── routes              - web routes.
    ├── core                    - application configuration, startup events, logging.
    ├── db                      - db related stuff.
    │   ├── postgress   
    │   │   ├── migrations      - manually written alembic migrations.
    │   │   └── repositories    - all crud stuff.
    │   └── mongo   
    │       └── aggregations    - manually written optimized raw queries.
    ├── models                  - pydantic models for this application.
    │   ├── domain              - main models that are used almost everywhere.
    │   └── schemas             - schemas for using in web routes.
    ├── resources               - strings that are used in web responses.
    ├── services                - logic that is not just crud related.
    └── main.py                 - FastAPI application creation and configuration.


Code formatting
---------------

Before commiting new changes ensure code quality by running code formatter script

    poetry run scripts/format

Also in order to ensure the project will pass the tests run linting checker

    poetry run scripts/lint
