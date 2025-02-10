# spark-exercise on minikube

> One option to run spark is to use JupyterHub running in kubernetes. In this case we can use google's minikube platform. You can try this setup if your machine have at least 4 cores and 16GB RAM. As a prerequisite, you need to install minikube. See here for information on how to install and configure minikube - [title](https://minikube.sigs.k8s.io/docs/). Once minikube is installed, here are the steps to build your spark playground;

1. Start minikube

```
minikube start --cpus=4 --memory=16384
```

2. minikube addons enable registry
3. build and push docker images(pyspark, spark, singleuser) to minikube registry:
        a. docker build -t $(minikube ip):5000/pyspark:test -f kubernetes/dockerfiles/pyspark/Dockerfile .
        b. docker push --tls-verify=false $(minikube ip):5000/pyspark:test
4. apply spark resources
        a. kubectl apply -f spark_ns.yaml
        b. kubectl apply -f spark_sa.yaml
        c. kubectl apply -f spark_sa_role.yaml
5. test with spark-submit
        a. /opt/spark/bin/spark-submit --master k8s://https://$(minikube ip):8443 --deploy-mode cluster --driver-memory 1g --conf spark.kubernetes.memoryOverheadFactor=0.5 --name sparkpi-test1 --class org.apache.spark.examples.SparkPi --conf spark.kubernetes.container.image=spark:latest  --conf spark.kubernetes.driver.pod.name=spark-test1-pi  --conf spark.kubernetes.namespace=spark --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark  --verbose  local:///opt/spark/examples/jars/spark-examples_2.12-3.5.3.jar 1000
6. apply spark driver resource
        a. kubectl apply -f driver_service.yaml
7. apply jupyterhub resource
        a. kubectl apply -f jupyterhub_ns.yaml
        b. kubectl apply -f jupyperhub_sa.yaml
        c. kubectl apply -f jupyterhub_sa_role.yaml
8. install jupyterhub using jhub_values.yaml
        a. helm upgrade --cleanup-on-fail --install jupyterhub jupyterhub/jupyterhub --namespace jupyterhub --create-namespace --version=3.3.8 --values jhub_values.yaml
9. test using pyspark_k8s_example.ipynb
10. issues:
        1. unable to read downloaded files
        2. it seems like it wants a hadoop like system to work with files
