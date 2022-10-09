# Airflow Service

## Postgres Docker
 
Start PostgresDB in docker container:

0. Copy `.env.example` file to `.env` and correct variables

1. Start containers:

    ```
    $ docker-compose -f docker-compose.yml up -d
    ```


## Virtual Environment

0. Create Virtual Environment

    ```
    $ sudo apt install python3-pip python3-venv
    $ python3 -m venv .venv
    ```

1. Activate Virtual Environment

    ```
    source .venv/bin/activate
    ```

2. Install requirements

    ```
    (.venv)$ pip3 install --upgrade pip
    (.venv)$ pip install -r requirements.txt
    ```

## Run

Before running the app upgrade a DB with [Alembic][alembic_run]:

```
(.venv) $ alembic upgrade head
```

Run the app with:

```
(.venv) $ ./main.py
```

[alembic_run]: https://alembic.sqlalchemy.org/en/latest/tutorial.html

## Migrations Development

To make migration script with [Alembic][alembic_autogen] after db-models
changed run the command:

```
(.venv) $ alembic revision --autogenerate -m "<valuable message>"
```

Commit.

[alembic_autogen]: https://alembic.sqlalchemy.org/en/latest/autogenerate.html

## Running tests

```
(.venv) $ pytest tests/test_{file}.py --{method}
```