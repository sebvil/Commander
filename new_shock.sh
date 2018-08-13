#!/bin/bash

#creates network if it does not exist
sudo docker network create mongo-shock

#creates mongo container if it does not exist

sudo docker run -d --name mongo --network mongo-shock -v mongo:/data/db mongo:3.6

#create shock container

sudo docker run -d -ti --name shock-server --network mongo-shock -v shock:/usr/local/shock mgrast/shock

