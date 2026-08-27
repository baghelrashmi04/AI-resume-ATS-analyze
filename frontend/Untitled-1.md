
#readme 

i built two docker images one for backend anoher for frontend , backend includes
every file that is required to process the program and frontend includes files which 
displayed to end user and some dependcies like requirement.txt and dockerfile which holds the image 

made two separate docker files , ran them and build images by 
docker build -t reumse-backend , reumse-frontend 

now because we have two seprate files of same projects they must have a network to contact with ech other 
so built a network using docker network create resume-net
and now going inside backend and using docker run -d --name backend-container --network resume-net -p 8000:8000 --env-file .env resume-backend
docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
and then going inside frontend and using docker run -d --name frontend-container --network resume-net -p 3000:3000 --env-file .env resume-frontend