FROM ubuntu:18.04

ENV JENKINS_MASTER_NODE_URL http://jenkins.local
ENV JENKINS_MASTER_NODE_USERNAME admin
ENV JENKINS_MASTER_NODE_PASSWORD admin
ENV JENKINS_SLAVE_NODE_ADDRESS ''
ENV JENKINS_SLAVE_NODE_NAME ''
ENV JENKINS_SLAVE_NODE_EXECUTORS 1
ENV JENKINS_SLAVE_NODE_ADDRESS ''
ENV JENKINS_SLAVE_NODE_SECRET ''
ENV JENKINS_SLAVE_NODE_LABELS ''

RUN apt-get update && apt-get install -y \
      apt-transport-https \
      ca-certificates \
      software-properties-common \
      unzip \
      wget \
      curl \
      git \
      iputils-ping \
      net-tools \
      iproute2 \
      vim \
      curl \
      openjdk-8-jdk \
      python3 \
      python3-setuptools \
      python3-pip \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install \
      jenkinsapi \
      ansible \
  && mkdir -p /var/lib/jenkins \
  && useradd -d "/home/jenkins" -m -s /bin/bash jenkins \
  && chown -R jenkins /var/lib/jenkins

COPY ./jenkins-slave/files/configure_jenkins_slave_node.py /var/lib/jenkins/configure_jenkins_slave_node.py
COPY ./jenkins-slave/files/docker-entrypoint.sh /var/lib/jenkins/docker-entrypoint.sh

ENTRYPOINT ["/var/lib/jenkins/docker-entrypoint.sh"]

USER jenkins
