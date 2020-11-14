FROM python:3.7-alpine
LABEL maintainer=Albert

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# dependencies for psycopg2, needed by psycopg2
RUN apk add --update --no-cache postgresql-client
# dependencies for Pillow
RUN apk add --update --no-cache jpeg-dev
# also dependencies for psycopg2, but only required during build
# so can delete after, hence we use --virtual
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
# build dependencies for Pillow, we can actually combine this
# with the above, however for clarity it is added separately
RUN apk add --update --no-cache --virtual .tmp-build-deps-pillow \
      musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps
RUN apk del .tmp-build-deps-pillow

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# store recipe image
RUN mkdir -p /vol/web/media
# store static files e.g. css
RUN mkdir -p /vol/web/static

# for security purpose
# if the app is compromised, it wont have the root user access
RUN adduser -D user
# set ownership of all the folders in vol to user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user
