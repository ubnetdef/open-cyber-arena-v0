FROM python:3.7-slim

ENV PATH /opt/arena/.venv/bin:$PATH
ENV PIP_NO_CACHE_DIR 0
ENV PIPENV_VENV_IN_PROJECT 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/arena

RUN pip install --trusted-host pypi.python.org pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --ignore-pipfile

COPY manage.py .
COPY static/src static/src
COPY arena arena

RUN python manage.py collectstatic --no-input

USER www-data

CMD ["gunicorn", "arena.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1"]
