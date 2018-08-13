#!/bin/bash

sudo docker start mongo
sudo docker run -d -ti --name shock-server --network test --rm -p 7445:7445 -v shock:/usr/local/shock mgrast/shock
