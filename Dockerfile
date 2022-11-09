FROM python:3.10.8-slim as builder-py

ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONPATH /code
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore

RUN apt-get update && apt-get install -y build-essential gcc libffi-dev libpq-dev python-dev && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip

COPY ./requirements.txt ./code/requirements.txt

RUN python3 -m venv /venv

RUN . /venv/bin/activate; pip install --no-compile  -r /code/requirements.txt
FROM python:3.10.8-slim

ENV PATH /venv/bin:/bin:/usr/bin:/usr/local/bin
ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONPATH /code
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore

RUN apt-get update && apt-get install -y libpq-dev libffi-dev && rm -rf /var/lib/apt/lists/*

RUN mkdir /code

COPY . /code/
COPY --from=builder-py /venv/ /venv/
COPY --from=builder-py /code/ /code/

WORKDIR /code

CMD ["gunicorn", "-c", "/code/gunicorn.conf.py", "config.wsgi"]

ENV X_IMAGE_TAG v0.0.0

LABEL Description="AO3 Tracker" Vendor="Lacey Williams Henschel"
LABEL Version="${X_IMAGE_TAG}"
