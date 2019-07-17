#!/bin/sh
response=$(curl -s -o /dev/null -w "%{http_code}\n" http://sampath:xyz@184.72.174.202:30003)
if [ "$response" != "200" ]
then
 echo "Response code: $response , Jenkins url is not accessible"
 else
         echo "Response code is $response , Jenkins url is accessible"
         configfile=$(curl -X GET http://sampath:xyz@184.72.174.202:30003/job/gitlab-integration/config.xml -o jobconfig.xml)
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
         file1=repocnf.xml
         file2=credcnf.xml
         xmlstarlet ed -u '/maven2-moduleset/scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url' -v "$1" $file > $file1
         echo "Repo value added..."
         sleep 2s
         xmlstarlet ed -u '/maven2-moduleset/scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/credentialsId' -v "$2" $file1 > $file2
         echo "Git Credentials added.."

         echo "Giving exec permission for updated config file"
         sudo chmod 777 $file2
         echo "Permission given"

        # echo "Getting jenkins crumb for uploading config file.. "
        # jencrumb=  wget -q --auth-no-challenge --user sampath --password xyz --output-document - 'http://184.72.174.202:30003/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'
         #echo $jencrumb
         #sleep 5s

         echo "Uploading the job config file to Jenkins.."
         #uploadresponse=$(curl -s -o /dev/null -w "%{http_code}\n" -H "$jencrumb" -X POST http://sampath:xyz@184.72.174.202:30003/job/gitlab-integration/config.xml --data-binary "@$file2")
         uploadresponse=$(curl -s -o /dev/null -w "%{http_code}\n" -X POST http://sampath:xyz@184.72.174.202:30003/job/gitlab-integration/config.xml --data-binary "@$file2")
         echo $uploadresponse
         if [ "$uploadresponse" != "200" ]
         then
                 echo "Error in uploading Config file.."
         else
                 echo "Config file uploaded successfully!!"
         fi

         echo "Triggering Jenkins Build remotedly..."
         jenbuild=$(curl -s -o /dev/null -w "%{http_code}\n" -X POST http://sampath:xyz@184.72.174.202:30003/job/gitlab-integration/build)
         echo $jenbuild
         if [ "$jenbuild" != "201" ]
         then
                 echo "Unable to trigger build remotedly.."
         else
                 echo "Build triggered successfully..!!"
         fi

fi

