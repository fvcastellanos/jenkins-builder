FROM jenkins/jenkins:lts

USER root

RUN apt-get update -y \
    && apt-get install -y \
        vim \
        net-tools \
        iputils-ping \
        iproute2

USER jenkins

ENV JAVA_OPTS "-Djenkins.install.runSetupWizard=false -Djava.awt.headless=true"
ENV JENKINS_HOME /var/jenkins_home
ENV CASC_JENKINS_CONFIG ${JENKINS_HOME}/casc_configs
ENV JENKINS_LOCATION_URL http://jenkins.local:8080

RUN mkdir -p ${JENKINS_HOME} ${CASC_JENKINS_CONFIG}/default

COPY ./files/jenkins_plugins.txt /usr/share/jenkins/ref/jenkins_plugins.txt
COPY ./files/jcasc/default.yml ${CASC_JENKINS_CONFIG}/default/default.yml

RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/jenkins_plugins.txt

EXPOSE 8080
EXPOSE 50000

VOLUME [ ${JENKINS_HOME} ]
