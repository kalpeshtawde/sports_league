# syntax=docker/dockerfile:1

# pull base image
FROM python:3

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /code

# install dependenceies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY . /code/
