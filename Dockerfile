FROM python:3.7-alpine
LABEL maintainer=Albert

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# for security purpose
# if the app is compromised, it wont have the root user access
RUN adduser -D user
USER user
