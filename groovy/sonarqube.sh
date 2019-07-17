sh /home/ubuntu/venv/mmp/aws/api.sh
rm /home/ubuntu/venv/mmp/aws/groovy/new.groovy
rm /home/ubuntu/venv/mmp/aws/groovy/some.groovy
rm /home/ubuntu/venv/mmp/aws/jen-pod.txt
cp /home/ubuntu/venv/mmp/aws/groovy/sonarqube.groovy /home/ubuntu/venv/mmp/aws/groovy/so.groovy

sed "s/URL/http:\/\/$(cat /home/ubuntu/venv/mmp/aws/sonarqube.txt):8083/" /home/ubuntu/venv/mmp/aws/groovy/so.groovy > /home/ubuntu/venv/mmp/aws/groovy/new.groovy
sed "s/API/$(cat /home/ubuntu/venv/mmp/aws/api.txt)/" /home/ubuntu/venv/mmp/aws/groovy/new.groovy > /home/ubuntu/venv/mmp/aws/groovy/some.groovy


kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}' | grep "jenkins" > /home/ubuntu/venv/mmp/aws/jen-pod.txt

kubectl cp /home/ubuntu/venv/mmp/aws/groovy/some.groovy $(cat jen-pod.txt):/var/jenkins_home/init.groovy.d/

curl -X POST -u cfs:capgemini $(cat /home/ubuntu/venv/mmp/aws/jenkins.txt):8080/restart
