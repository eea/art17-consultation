FROM python:2.7-slim
LABEL maintainer="EEA: IDM2 C-TEAM <eea-edw-c-team-alerts@googlegroups.com>"

ENV WORK_DIR=/var/local/art17
ENV DATA_DIR=/var/local/art17-data

RUN runDeps="curl gcc vim build-essential netcat default-libmysqlclient-dev default-mysql-client python-dev libldap2-dev libsasl2-dev libssl-dev libxrender1 libfontconfig1 libxext6 wkhtmltopdf" \
	&& apt-get update \
	&& apt-get install -y --no-install-recommends $runDeps \
	&& rm -vrf /var/lib/apt/lists/*


COPY . $WORK_DIR/
WORKDIR $WORK_DIR

RUN mkdir $WORK_DIR/logs \
	&& mkdir -p $DATA_DIR/maps \
	&& mkdir -p $DATA_DIR/factsheets \
	&& ln -s $DATA_DIR/maps $WORK_DIR/art17/static/maps \
	&& ln -s $DATA_DIR/factsheets $WORK_DIR/art17/static/factsheets

RUN mkdir $WORK_DIR/temp_static \
    && cp -a $WORK_DIR/art17/static/. $WORK_DIR/temp_static/

RUN sed '/st_mysql_options options;/a unsigned int reconnect;' /usr/include/mysql/mysql.h -i.bkp

RUN pip install -U setuptools \
	&& pip install -r requirements-dep.txt --trusted-host eggshop.eaudeweb.ro \
	&& mv docker-entrypoint.sh /bin/

ENTRYPOINT ["docker-entrypoint.sh"]
