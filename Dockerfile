FROM ubuntu:20.04

WORKDIR /app

ADD req /app/req

RUN mkdir -p logs
RUN mkdir -p rockets


RUN sed 's/main$/main universe/' -i /etc/apt/sources.list
RUN apt-get update && apt-get install -y software-properties-common # python-software-properties
# RUN add-apt-repository ppa:webupd8team/java -y


RUN apt-get update
RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections


RUN apt-get install -y bzip2

RUN apt-get install -y oracle-java7-installer; exit 0;

RUN cat req/jdk_part* > req/jdk-7u80-linux-x64.tar.gz
RUN ls req
RUN mkdir /var/cache/oracle-java7-installer/
# RUN mv req/jdk-7u80-linux-x64.tar.gz /var/cache/oracle-java7-installer/
RUN tar zxvf req/jdk-7u80-linux-x64.tar.gz
# RUN apt-get install -y oracle-java7-installer
# RUN tar -jxvf req/jdk-7u80-linux-x64.tar.gz
# RUN ls req/
# RUN apt-get install -y req/jdk-7u80-linux-x64.tar.db

RUN apt-get install -y python3-dev python3-pip

# RUN export JAVA_HOME="/usr/lib/jvm/java-7-oracle/"
RUN export JAVA_HOME="/app/jdk1.7.0_80/"

RUN pip install numpy matplotlib jpype1==0.6.3 flask apscheduler
RUN sudo Xvfb :1 -screen 0 1024x768x24 </dev/null &
RUN export DISPLAY=":1"

RUN mkdir -p /root/.openrocket/ThrustCurves

# ADD . /app

# EXPOSE 80
# CMD ["python","app.py"]
