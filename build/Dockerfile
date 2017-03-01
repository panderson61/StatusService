FROM centos:7.2.1511

MAINTAINER Paul Anderson "panderson@avetta.com"

# Install needed packages
RUN yum -y install epel-release
RUN yum -y install git
RUN yum -y install python
RUN yum -y install python-pip
RUN pip install -r requirements.txt
RUN yum clean all

# Add the files
COPY files/app.py /opt/app/app.py
