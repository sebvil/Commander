#!/bin/bash

#creates network if it does not exist
sudo docker network create mongo-shock

sudo docker rm -f mongo
sudo docker rm -f shock-server

#creates mongo container if it does not exist

sudo docker run -d --name mongo --network mongo-shock -v mongo:/data/db mongo:3.6

#create shock container

sudo docker run -d -ti --name shock-server --network mongo-shock --rm -p 7445:7445 -v shock:/usr/local/shock mgrast/shock

