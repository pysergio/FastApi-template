FROM python:3.10.5

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY poetry.lock pyproject.toml ./
RUN pip install poetry==1.2.2 && \
    poetry config virtualenvs.in-project false && \
    poetry install --no-dev

COPY . ./

CMD poetry run uvicorn --host=0.0.0.0 app.main:app
