# Python image

FROM python:2.7-slim

# System requirements

RUN apt-get -y update && apt-get -y install \
    gcc \
    python-setuptools \
    python-dev \
    libmysqlclient-dev \
    libldap2-dev \
    libsasl2-dev

# Copy code into image

RUN mkdir /art17-consultation
COPY . /art17-consultation
WORKDIR /art17-consultation

# Install requirements

RUN pip install -U setuptools
RUN pip install -r requirements-dev.txt --trusted-host eggshop.eaudeweb.ro
RUN mkdir instance
COPY /settings.py.docker instance/settings.py
RUN ls instance

# Expose needed port

EXPOSE 5000

# Default command

CMD python manage.py runserver -p 5000
