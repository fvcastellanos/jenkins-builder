# **Jenkins Builder**

Provides Jenkins instance preconfigured with a bunch of [plugins](files/jenkins_plugins.txt) used to work with pipelines

## **Prerequisites**

* Docker 17.09+
* Docker Compose 1.16+

## **Steps**

* Build docker image

```sh
docker build -t jenkins:1.0 .
```

* Create a volume to mount container's {JENKINS_HOME} directory into the host. **Note. Replace ${HOST_PATH} with the host path where you can mount the volume**

```sh
docker volume create --driver local \
    --opt type=none \
    --opt device=${HOST_PATH}/jenkins_home \
    --opt o=bind \
    jenkins_home
```

**Note. If you don't want to mount a volume, comment all between the `volumes` tag in the `docker-compose.yml` file.**

* Run with `docker-compose`

```sh
docker-compose up -d
```

* Go to Jenkins UI at [http://127.0.0.1:8080](http://127.0.0.1:8080). Default username:password `admin:admin`
