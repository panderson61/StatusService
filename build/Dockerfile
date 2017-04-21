FROM centos:7.2.1511

MAINTAINER Paul Anderson "panderson@avetta.com"

# Install needed packages
RUN yum -y install epel-release
RUN yum -y install git
RUN yum -y install python
RUN yum -y install python-pip python-dev build-essential
RUN yum -y update
RUN yum clean all

RUN mkdir -p /opt/app/templates

WORKDIR /opt/app
COPY files/requirements.txt /opt/app/requirements.txt
RUN pip install -r requirements.txt

COPY files/app.py /opt/app/app.py
COPY files/logtest.py /opt/app/logtest.py

COPY files/static/style.css /opt/app/static/style.css
COPY files/static/avetta_favicon.png /opt/app/static/favicon.ico
COPY files/templates/hello.html /opt/app/templates/hello.html
COPY files/templates/index.html /opt/app/templates/index.html
COPY files/templates/login.html /opt/app/templates/login.html

EXPOSE 5000
CMD ["python", "/opt/app/app.py"]
