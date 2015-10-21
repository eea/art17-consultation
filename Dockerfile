# Python image

FROM eeacms/python:2.7-slim

# Copy code into image

RUN mkdir /art17-consultation
COPY alembic /art17-consultation/alembic
COPY art17 /art17-consultation/art17
COPY zope_api /art17-consultation/zope_api
COPY contrib /art17-consultation/contrib
COPY docs  /art17-consultation/docs
COPY manage.py requirements.txt requirements-dev.txt /art17-consultation/
WORKDIR /art17-consultation

# Install requirements

RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt --trusted-host eggshop.eaudeweb.ro
RUN mkdir -p instance
COPY /settings.py.docker instance/settings.py

# Expose needed port

EXPOSE 5000

# Default command

CMD python manage.py runserver -t 0.0.0.0 -p 5000
