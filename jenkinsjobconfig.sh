#!/bin/sh
# Run the shell script by passing parameters
# $1= jenkins url
# $2=  Git repo url
# $3= Git Credentials
# $4= Nexus url

# ./jenkinsconfig.sh "a64f4bd9c35ca11e9839502028b7c8da-1489108259.us-west-2.elb.amazonaws.com" "https://github.com/kenych/berlin-clock.git" "" "aad7d68c038ef11e9839502028b7c8da-1586505699.us-west-2.elb.amazonaws.com"

response=$(curl -s -o /dev/null -w "%{http_code}\n" http://cfs:capgemini@$1:8080)
if [ "$response" != "200" ]
then
 echo "Response code: $response , Jenkins url is not accessible"
 else
         echo "Response code is $response , Jenkins url is accessible"
         echo "Creating Jenkins job..."

         createjob=$(curl -s -XPOST http://$1:8080/createItem?name=CICDjob -u cfs:capgemini --data-binary @initialjobconfig.xml -H "Content-Type:text/xml")

         echo $createjob

         configfile=$(curl -X GET http://cfs:capgemini@$1:8080/job/CICDjob/config.xml -o jobconfig.xml)
         echo $configfile
         echo "Jenkins config file downloaded...."
         echo "Checking config file permission...."
         file=jobconfig.xml
         if [ -x $file ]
         then
                 echo "file is writable."
         else
                 echo "file does not have write permission. changing the permission.."
                 sudo chmod 777 $file
                 echo "Write permission given.."
         fi
         echo "Configuring Git Repo details to Jenkins job.."
         file1=buildcnf.xml
         
         xmlstarlet ed -u '/maven2-moduleset/scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url' -v "$2" \
                -u '/maven2-moduleset/scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/credentialsId' -v "$3" \
                -s /maven2-moduleset -t elem -n goals -v "clean package" \
                -s /maven2-moduleset/postbuilders -t elem -n hudson.tasks.Shell -v "" \
                -s /maven2-moduleset/postbuilders/hudson.tasks.Shell -t elem -n command -v "#!/bin/bash&#xa;curl --upload-file "'$WORKSPACE'"/webapp/target/*.war -v -u admin:admin123 -v http://$4:8081/repository/nexusraw/" \
               -u 'maven2-moduleset/runPostStepsIfResult/name' -v "SUCCESS" \
               -u 'maven2-moduleset/runPostStepsIfResult/ordinal' -v "0" \
               -u 'maven2-moduleset/runPostStepsIfResult/color' -v "BLUE" \
               -u 'maven2-moduleset/runPostStepsIfResult/completeBuild' -v "true" $file > $file1
         echo "Configuration changes have been added.."


         echo "Giving exec permission for updated config file"
         sudo chmod 777 $file1
         echo "Permission given"

        # echo "Getting jenkins crumb for uploading config file.. "
        # jencrumb=  wget -q --auth-no-challenge --user sampath --password xyz --output-document - 'http://184.72.174.202:30003/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'
         #echo $jencrumb
         #sleep 5s

         echo "Uploading the job config file to Jenkins.."
         #uploadresponse=$(curl -s -o /dev/null -w "%{http_code}\n" -H "$jencrumb" -X POST http://sampath:xyz@184.72.174.202:30003/job/gitlab-integration/config.xml --data-binary "@$file2")
         uploadresponse=$(curl -s -o /dev/null -w "%{http_code}\n" -X POST http://cfs:capgemini@$1:8080/job/CICDjob/config.xml --data-binary "@$file1")
         echo $uploadresponse
         if [ "$uploadresponse" != "200" ]
         then
                 echo "Error in uploading Config file.."
         else
                 echo "Config file uploaded successfully!!"
         fi

         echo "Triggering Jenkins Build remotedly..."
         jenbuild=$(curl -s -o /dev/null -w "%{http_code}\n" -X POST http://cfs:capgemini@$1:8080/job/CICDjob/build)
         echo $jenbuild
         if [ "$jenbuild" != "201" ]
         then
                 echo "Unable to trigger build remotedly.."
         else
                 echo "Build triggered successfully..!!"
         fi

         sleep 25s

         echo "Checking Build Status..."
         lastbuild= $(curl -X GET http://cfs:capgemini@$1:8080/job/CICDjob/lastBuild/api/xml -o lastbuild.xml)

         sleep 5s

         buildnum=$(xmlstarlet sel -t -m "/mavenModuleSetBuild" -v "number" lastbuild.xml)
         echo "Build number is $buildnum "

         buildinprogress=$(xmlstarlet sel -t -m "/mavenModuleSetBuild" -v "building" lastbuild.xml)
         #echo $buildinprogress

         if [ "$buildinprogress" != "false" ]
         then
                 echo "Build is in Progress..."
         else
                  buildresult=$(xmlstarlet sel -t -m "/mavenModuleSetBuild" -v "result" lastbuild.xml)
                  if [ "$buildresult" != "SUCCESS" ]
                  then
                          echo "------Job Execution Failed----"
                  else
                          echo "------Job Executed Successfully-----"
                  fi
         fi
         echo "Fetching the Console output from Jenkins.."
         buildlog=$(curl -s -S -u cfs:capgemini "http://$1:8080/job/CICDjob/$buildnum/logText/progressiveText?start=0")
         echo "------Jenkins Build log------------------"
         echo "$buildlog"
fi

