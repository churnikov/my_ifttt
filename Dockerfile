FROM python:3.10

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN /root/.local/bin/poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN /root/.local/bin/poetry install -n -q --no-cache --only main

WORKDIR /app

COPY . /app
RUN /root/.local/bin/poetry install -n -q --no-cache --only main

CMD ["python", "/app/my_ifttt/main.py"]

