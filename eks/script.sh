#!/bin/bash
sed -i '/- cluster:/r output.txt' ~/.kube/config-sample-eks
sed -i -e '6,7d' ~/.kube/config-sample-eks