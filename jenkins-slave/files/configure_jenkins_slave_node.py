from jenkinsapi.jenkins import Jenkins
import os
import signal
import sys
import urllib.request
import subprocess
import shutil
import requests
import time

# -----------------------------
# JenkinsSlaveConfigurer
# -----------------------------


class JenkinsSlaveConfigurer():

    jenkins_slave_node_process = None

    def __init__(self):
        # Jenkins master node
        self.__jenkins_master_node_url = os.environ['JENKINS_MASTER_NODE_URL']
        self.__jenkins_master_node_username = os.environ['JENKINS_MASTER_NODE_USERNAME']
        self.__jenkins_master_node_password = os.environ['JENKINS_MASTER_NODE_PASSWORD']
        self.__jenkins_master_node_slave_jar_url = self.__jenkins_master_node_url + '/jnlpJars/slave.jar'

        # Jenkins slave node
        self.__jenkins_slave_node_jar_path = '/var/lib/jenkins/slave.jar'
        self.__jenkins_slave_node_woring_directory = '/home/jenkins'
        self.__jenkins_slave_node_labels = os.environ['JENKINS_SLAVE_NODE_LABELS'] if os.environ['JENKINS_SLAVE_NODE_LABELS'] != '' else 'none'
        self.__jenkins_slave_node_executors = os.environ['JENKINS_SLAVE_NODE_EXECUTORS'] if os.environ['JENKINS_SLAVE_NODE_EXECUTORS'] != '' else 1
        self.__jenkins_slave_node_address = os.environ['JENKINS_SLAVE_NODE_ADDRESS']
        self.__jenkins_slave_node_secret = os.environ['JENKINS_SLAVE_NODE_SECRET']
        self.__jenkins_slave_node_name = os.environ['JENKINS_SLAVE_NODE_NAME'] if os.environ['JENKINS_SLAVE_NODE_NAME'] != '' else 'slave-' + os.environ['HOSTNAME']
        self.__jenkins_slave_node_agent_jnlp = self.__jenkins_master_node_url + '/computer/' + self.__jenkins_slave_node_name + '/slave-agent.jnlp'

    def get_jenkins_master_node_url(self):
        return self.__jenkins_master_node_url

    def get_jenkins_slave_node_name(self):
        return self.__jenkins_slave_node_name

    def get_jenkins_slave_node_woring_directory(self):
        return self.__jenkins_slave_node_woring_directory

    def get_jenkins_slave_node_labels(self):
        return self.__jenkins_slave_node_labels

    def is_jenkins_master_node_ready(self):
        try:
            request = requests.head(
                self.__jenkins_master_node_slave_jar_url, verify=False, timeout=None)
            return request.status_code == requests.codes.ok
        except:
            return False

    def download_jenkins_slave_jar(self):
        if os.path.isfile(self.__jenkins_slave_node_jar_path):
            os.remove(self.__jenkins_slave_node_jar_path)

        urllib.request.urlretrieve(
            self.__jenkins_master_node_slave_jar_url, self.__jenkins_slave_node_jar_path)

    def create_jenkins_slave_node(self):
        jenkins = Jenkins(self.__jenkins_master_node_url,
                          self.__jenkins_master_node_username, self.__jenkins_master_node_password)
        node_properties = {
            'num_executors': int(self.__jenkins_slave_node_executors),
            'node_description': '',
            'remote_fs': self.__jenkins_slave_node_woring_directory,
            'labels': self.__jenkins_slave_node_labels,
            'exclusive': True
        }
        jenkins.nodes.create_node(self.__jenkins_slave_node_name, node_properties)

    def delete_jenkins_slave_node(self):
        jenkins = Jenkins(self.__jenkins_master_node_url,
                          self.__jenkins_master_node_username, self.__jenkins_master_node_password)
        del jenkins.nodes[self.__jenkins_slave_node_name]

    def run_jenkins_slave_node(self):
        parameters = ['java', '-jar', self.__jenkins_slave_node_jar_path,
                      '-jnlpUrl', self.__jenkins_slave_node_agent_jnlp]

        if self.__jenkins_slave_node_address != '':
            parameters.extend(
                ['-connectTo', self.__jenkins_slave_node_address])

        if self.__jenkins_slave_node_secret == '':
            parameters.extend(['-jnlpCredentials', self.__jenkins_master_node_username +
                               ':' + self.__jenkins_master_node_password])
        else:
            parameters.extend(['-secret', self.__jenkins_slave_node_secret])

        return subprocess.Popen(parameters, stdout=subprocess.PIPE)

    def clean_working_directory(self):
        for root, directories, files in os.walk(self.__jenkins_slave_node_woring_directory):
            for file in files:
                os.unlink(os.path.join(root, file))

            for directory in directories:
                shutil.rmtree(os.path.join(root, directory))

    def handle_jenkins_slave_node_process_signal(self, signal_number, frame):
        if self.jenkins_slave_node_process != None:
            self.jenkins_slave_node_process.send_signal(signal.SIGINT)
    # def handle_jenkins_slave_node_process_signal(self, signal_number, frame):
    # 	if self.__jenkins_slave_node_process != None:
    # 		jenkins_slave_node_process.send_signal(signal.SIGINT)

# -----------------------------
# Main
# -----------------------------


def main():

    jenkins_slave_configurer = JenkinsSlaveConfigurer()

    # Wait until jenkins jenkins master node is ready
    while not jenkins_slave_configurer.is_jenkins_master_node_ready():
        print(
            f'jenkins master [{jenkins_slave_configurer.get_jenkins_master_node_url()}] is not ready yet, retrying in 10 seconds...')
        time.sleep(10)

    # Download jenkins slave node jar from jenkins master node
    jenkins_slave_configurer.download_jenkins_slave_jar()
    print('jenkins slave jar was downloaded successfully')

    # if os.environ['JENKINS_SLAVE_NODE_WORING_DIRECTORY']:
    # 	os.setcwd(os.environ['JENKINS_SLAVE_NODE_WORING_DIRECTORY'])

    # Clean jenkins slave node working directory
    jenkins_slave_configurer.clean_working_directory()
    print(
        f'working directory [{jenkins_slave_configurer.get_jenkins_slave_node_woring_directory()}] was cleaned up successfully')

    # Create jenkins slave node
    jenkins_slave_configurer.create_jenkins_slave_node()
    print(f'jenkins slave node [{jenkins_slave_configurer.get_jenkins_slave_node_name()}] with labels [{jenkins_slave_configurer.get_jenkins_slave_node_labels()}] was created successfully')

    # Run jenkins slave node process
    signal.signal(
        signal.SIGINT, jenkins_slave_configurer.handle_jenkins_slave_node_process_signal)
    signal.signal(
        signal.SIGTERM, jenkins_slave_configurer.handle_jenkins_slave_node_process_signal)

    jenkins_slave_node_process = jenkins_slave_configurer.run_jenkins_slave_node()
    jenkins_slave_configurer.jenkins_slave_node_process = jenkins_slave_node_process

    # Start jenkins slave node
    print(
        f'starting jenkins slave node [{jenkins_slave_configurer.get_jenkins_slave_node_name()}] with labels [{jenkins_slave_configurer.get_jenkins_slave_node_labels()}]')
    jenkins_slave_configurer.jenkins_slave_node_process.wait()

    # Remove jenkins slave node process
    print(
        f'stopping jenkins slave node [{jenkins_slave_configurer.get_jenkins_slave_node_name()}]')
    jenkins_slave_configurer.delete_jenkins_slave_node()
    print(
        f'jenkins slave node [{jenkins_slave_configurer.get_jenkins_slave_node_name()}] was removed successfully')


if __name__ == '__main__':
    main()
