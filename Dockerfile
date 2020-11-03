FROM python:3.7-alpine
LABEL maintainer=Albert

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# dependencies for psycopg2
RUN apk add --update --no-cache postgresql-client
# also dependencies for psycopg2, but only required during build
# so can delete after, hence we use --virtual
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# for security purpose
# if the app is compromised, it wont have the root user access
RUN adduser -D user
USER user
