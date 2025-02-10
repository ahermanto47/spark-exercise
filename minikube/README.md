# spark-exercise on minikube

> One option to run spark is to use JupyterHub running in kubernetes. In this case we can use google's minikube platform. You can try this setup if your machine have at least 4 cores and 16GB RAM. As a prerequisite, you need to install minikube. See here for information on how to install and configure minikube - [minikube](https://minikube.sigs.k8s.io/docs/). Once minikube is installed, here are the steps to build your spark playground;

1. Start minikube with 4 cpus and 16GB ram

```
minikube start --cpus=4 --memory=16384
```

2. Enable internal minikube docker registry

```
minikube addons enable registry
```

3. Build and push docker images(pyspark, spark, singleuser) to minikube registry

```
docker build -t $(minikube ip):5000/pyspark:test -f kubernetes/dockerfiles/pyspark/Dockerfile .

docker push --tls-verify=false $(minikube ip):5000/pyspark:test
```

4. apply spark resources

```
kubectl apply -f spark_ns.yaml

kubectl apply -f spark_sa.yaml

kubectl apply -f spark_sa_role.yaml
```

5. test with spark-submit

```
/opt/spark/bin/spark-submit --master k8s://https://$(minikube ip):8443 --deploy-mode cluster --driver-memory 1g --conf spark.kubernetes.memoryOverheadFactor=0.5 --name sparkpi-test1 --class org.apache.spark.examples.SparkPi --conf spark.kubernetes.container.image=spark:latest  --conf spark.kubernetes.driver.pod.name=spark-test1-pi  --conf spark.kubernetes.namespace=spark --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark  --verbose  local:///opt/spark/examples/jars/spark-examples_2.12-3.5.3.jar 1000
```

6. apply spark driver resource

```
kubectl apply -f driver_service.yaml
```

7. apply jupyterhub resource

```
kubectl apply -f jupyterhub_ns.yaml

kubectl apply -f jupyperhub_sa.yaml

kubectl apply -f jupyterhub_sa_role.yaml
```

8. install jupyterhub using jhub_values.yaml

```        
helm upgrade --cleanup-on-fail --install jupyterhub jupyterhub/jupyterhub --namespace jupyterhub --create-namespace --version=3.3.8 --values jhub_values.yaml
```

9. test using pyspark_k8s_example.ipynb

## known issues:
1. unable to read downloaded files
2. it seems like it wants a hadoop like system to work with files
