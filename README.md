# OpenSoundStream Server

OpenSoundStream is a system for managing and listening to songs from your private music collection. Beside it's website there are (native) client applications for Android and Windows available. It is meant to be used as a self-hosted application. It has a multi user system built in, so you can use your server together with friends.
## Deployment
The recommended and easiest way of deploying the OpenSoundStream Server is to use the available docker container.

    docker run -d -p 8099:8000 \
        --mount source=oss-server-db,target=/oss_server/db \
         --name oss-server \
         opensoundstream/oss-server:alpine

##### Parameter Explanation:
- `-d` Run the server in detached mode (-> in Background)
- `-p 8099:8000` Expose port 8000 (HTTP Interface) of container to local port 8099, the local port can be changed to any free port.
- `--mount source=oss-server-db,target=/oss_server/db` A docker volume is used to persist the sqlite-database: If the container is deleted and instanciated again the Volume and therefore teh Database is used again.
- `--name oss-server` Name the container 'oss-server' for future reference
- `opensoundstream/oss-server:alpine` Specifies to use the alpine image of the oss-server and pulls it from dockerhub if not available locally

#### Additional Parameters (that might be useful)
- `-e DJANGO_HOST=my-domain.tld` Add example.com to the allowed host if exposing the Port directly (not recommend!).  The recommended way is to use a reverse proxy The allowed ports include `localhost` and `127.0.0.1` by default.

#### Reverse Proxy Config for Apache

    <VirtualHost *:443> #Using TLS-Encryption is strongly recommended 
	    ServerName my-domain.tld  
	    ProxyPass / http://localhost:8099/  
	    ProxyPassReverse / http://localhost:8099/
	    
	    #For Let's Encrypt confifguration
	    Include /etc/letsencrypt/options-ssl-apache.conf SSLCertificateFile
	    /etc/letsencrypt/live/my-domain.tld-0001/fullchain.pem SSLCertificateKeyFile
	    /etc/letsencrypt/live/my-domain.tld-0001/privkey.pem
	</VirtualHost>

#### API-Documentation
Can be found [here](https://github.com/Open-Sound-Stream-Organization/oss-server/blob/master/api-doc.md).
