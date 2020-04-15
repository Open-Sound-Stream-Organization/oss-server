# OpenSoundStream Server
## Deployment
The recommended and easiest way of deploying the OpenSoundStream Server is to use the available docker container.

`docker run -d -p 8099:8000 --mount source=oss-server-db,target=/oss_server/db --name oss-server opensoundstream/oss-server:alpine`

##### Parameter Explanation:
- `-d` Run the server in detached mode (-> in Background)
- `-p 8099:8000` Expose port 8000 (HTTP Interface) of container to local port 8099, the local port can be changed to any free port.
- `--mount source=oss-server-db,target=/oss_server/db` A docker volume is used to persist the sqlite-database: If the container is deleted and instanciated again the Volume and therefore teh Database is used again.
- `--name oss-server` Name the container 'oss-server' for future reference
- `opensoundstream/oss-server:alpine` Specifies to use the alpine image of the oss-server and pulls it from dockerhub if not available locally