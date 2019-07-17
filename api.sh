#!/bin/bash

sudo rm /home/ubuntu/venv/mmp/aws/son-key.txt
sudo rm /home/ubuntu/venv/mmp/aws/api.txt

curl --data "name=sample&login=admin" $(cat /home/ubuntu/venv/mmp/aws/sonarqube.txt):8082/api/user_tokens/generate -u admin:admin > /home/ubuntu/venv/mmp/aws/son-key.txt

sed -e 's/.*token":"\(.*\)","creat.*/\1/' son-key.txt > /home/ubuntu/venv/mmp/aws/api.txt
