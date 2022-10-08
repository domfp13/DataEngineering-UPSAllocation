FROM python:3.7.12-slim-buster
LABEL maintainer="Luis Enrique Fuentes Plata"

ENV APP_HOME /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libaio1 wget
RUN apt-get install -y unzip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/oracle
RUN wget \
    https://download.oracle.com/otn_software/linux/instantclient/214000/instantclient-basiclite-linux.x64-21.4.0.0.0dbru.zip && \
    unzip instantclient-basiclite-linux.x64-21.4.0.0.0dbru.zip && \
    rm -f instantclient-basiclite-linux.x64-21.4.0.0.0dbru.zip

RUN cd instantclient_21_4 && rm -f *jdbc* *occi* *mysql* *README *jar \
    uidrvci genezi adrci
RUN echo /opt/oracle/instantclient_21_4 > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig

ENV PATH=/opt/mssql-tools/bin:$PATH

RUN apt-get update \
    && apt-get install -y curl apt-transport-https locales gnupg2 \
    && locale-gen "en_US.UTF-8" \
    && export `grep "VERSION_ID" /etc/os-release | sed -e 's/^VERSION_ID=\"/VERSION_ID=/' -e 's/\"$//'` \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev \
    && apt-get remove -y curl apt-transport-https \
    && rm -f /etc/apt/sources.list.d/msprod.list \
    && rm -rf /var/lib/apt/lists/*

## should be set after locale was generated, overwise triggers warnings
ENV LANG="en_US.UTF-8" LANGUAGE="en_US.UTF-8" LC_ALL="en_US.UTF-8"

RUN python -m pip install cx_Oracle

ENV ORACLE_HOME=/opt/oracle/instantclient_21_4
ENV TNS_ADMIN=$ORACLE_HOME/network/admin

# Chaging the SECLEVEL to 1 since this is a debian based container
RUN sed -i -E 's/(CipherString\s*=\s*DEFAULT@SECLEVEL=)2/\11/' /etc/ssl/openssl.cnf

WORKDIR $TNS_ADMIN
COPY tnsnames.ora .

WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt -t .

COPY transformation .

CMD ["sleep", "1d"]
#CMD [ "python", "./main.py" ]
