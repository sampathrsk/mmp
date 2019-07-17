#!/bin/bash
echo 'Artifact deployment started'
rm webapp.war*
wget http://$(cat nexus.txt):8081/repository/nexusraw/webapp.war 


kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}' | grep "tomcat" > /home/ubuntu/venv/mmp/aws/pods.txt

kubectl cp webapp.war $(cat pods.txt):/usr/local/tomcat/webapps/

echo ' artifact has been successfully deployed to Tomcat'

