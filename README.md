# OpenSoundStream Server

OpenSoundStream is a system for managing and listening to songs from your private music collection. Beside it's website there are (native) client applications for Android and Windows available. It is meant to be used as a self-hosted application. It has a multi user system built in, so you can use your server together with friends.
## Deployment
The recommended and easiest way of deploying the OpenSoundStream Server is to use the available docker container with docker compose. Just get the [docker-compose.yml](https://raw.githubusercontent.com/Open-Sound-Stream-Organization/oss-server/master/docker-compose.yml), edit the environment variables and you're good to go. You need to [get a free API-Key from AcoustID for automatic music recognition](https://acoustid.org/new-application), its recommended but not mandatory, if you dont wish to use it please delete the line where the API-Key is set. Just start the container with `docker-compose up -d`. After the container has booted up you can access the app at port 8099 if you didn't change theport in the file.

#### Admin-Panel
To access the Admin-Panel you need a priveleged account. You can create one with issuing the following commands (execute them one at a time!)
    
    docker exec -it oss-server sh
    
    #Wait for the shell to attach to the container....
    
    python manage.py createsuperuser
    
    #You will be prompted interactively what the Account Data should be
    
    #To exit the container shell again:
    exit

After that you can access the Admin-Interface with the credentials at `/admin/` (pay attention to the latter slash!).

##### Alternative without compose:

Just run the 

    docker run -d -p 8099:8000 \
        --mount source=oss-server-db,target=/oss_server/db \
        --name oss-server \
        -e DJANGO_HOST=my-domain.tld \
        -e ACOUSTID_API_KEY=get-api-key-at-https://acoustid.org/new-application \
         opensoundstream/oss-server:alpine

##### Parameter Explanation:
- `-d` Run the server in detached mode (-> in Background)
- `-p 8099:8000` Expose port 8000 (HTTP Interface) of container to local port 8099, the local port can be changed to any free port.
- `--mount source=oss-server-db,target=/oss_server/db` A docker volume is used to persist the sqlite-database: If the container is deleted and instanciated again the Volume and therefore teh Database is used again.
- `--name oss-server` Name the container 'oss-server' for future reference
- `opensoundstream/oss-server:alpine` Specifies to use the alpine image of the oss-server and pulls it from dockerhub if not available locally
- `-e DJANGO_HOST=my-domain.tld` Add example.com to the allowed host if exposing the Port directly (not recommend!) or with a transparent reverse proxy like Caddy.  The recommended way is to use a reverse proxy The allowed ports include `localhost` and `127.0.0.1` by default.
- `-e ACOUSTID_API_KEY=get-api-key-at-https://acoustid.org/new-application`  Api-Key for automatic music recognition and metadata retrieval, get your own [here](https://acoustid.org/new-application). It also works without it, for that just delete this line.
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
