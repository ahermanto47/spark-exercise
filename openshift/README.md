# spark-exercise

oc apply -f manifest\operator-cm.yaml

oc apply -f manifest\cluster-cm.yaml

# login to master

oc exec --stdin --tty my-spark-cluster-m-jtr5c -- /bin/bash

spark-shell

# key in contents in src/test/test.scala

