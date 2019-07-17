#!/bin/bash
curl -u admin:admin123 -X POST --header 'Content-Type: application/json' http://$1:8081/service/rest/v1/script -d @maven.json
curl -u admin:admin123 -X POST --header 'Content-Type: application/json' http://$1:8081/service/rest/v1/script -d @raw.json
curl -u admin:admin123 -X POST --header 'Content-Type: text/plain' http://$1:8081/service/rest/v1/script/maven/run
curl -u admin:admin123 -X POST --header 'Content-Type: text/plain' http://$1:8081/service/rest/v1/script/raw/run

