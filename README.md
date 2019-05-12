# **Jenkins Builder**

Provides Jenkins Master/Slave nodes instances preconfigured with a bunch of [plugins](files/jenkins_plugins.txt) used to work with pipelines.

## **Prerequisites**

* Docker 17.09+
* Docker Compose 1.16+
* Loopback Network Alias [192.168.99.1]

## **Jenkins Master**

* Build docker image

```sh
docker build -t jenkins-master:1.0 -f jenkins-master/Dockerfile .
```

* Create a volume to mount container's {JENKINS_HOME} directory into the host. **Note. Replace ${HOST_PATH} with the host path where you can mount the volume**

```sh
docker volume create --driver local \
    --opt type=none \
    --opt device=${HOST_PATH}/jenkins_home \
    --opt o=bind \
    jenkins_home_master
```

* Run with `docker-compose`

```sh
docker-compose -f jenkins-master/docker-compose.yml up -d
```

* Create a loopback network alias

  * OSX

    ```sh
    ifconfig lo0 alias 192.168.99.1
    ```

  * Linux

    ```sh
    echo `auto lo lo:10

    iface lo inet loopback
    iface lo:10 inet static
        address 192.168.99.1
        netmask 255.255.255.0
        network 192.168.99.1` >> /etc/network/interfaces
    ```

* Map in `/etc/hosts`

```file
192.168.99.1    jenkins.local
```

* Go to Jenkins Master UI at [http://192.168.99.1:8080](http://192.168.99.1:8080). Default username:password `admin:admin`

## **Jenkins Slave**

* Build docker image

```sh
docker build -t jenkins-slave:1.0 -f jenkins-slave/Dockerfile .
```

* Run with `docker-compose`

```sh
docker-compose -f jenkins-slave/docker-compose.yml up -d
```
