FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt ./
RUN apt-get update && \
    apt-get install -y libgeos-dev &&\
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /code