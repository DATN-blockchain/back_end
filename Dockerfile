FROM python:3.9-buster
ENV APPLICATION_SERVICE=/app


RUN apt-get update && apt-get install -y libgl1-mesa-glx

# set work directory
RUN mkdir -p $APPLICATION_SERVICE

# where the code lives
WORKDIR $APPLICATION_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY poetry.lock pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

# copy project
COPY . $APPLICATION_SERVICE

CMD alembic history --verbose && \
    alembic upgrade head && \
    gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --reload
