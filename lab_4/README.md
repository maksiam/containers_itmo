
```bash
eval $(minikube docker-env)

cd ../lab2

docker compose build

cd ../lab_4

kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f faiss_pvc.yaml
kubectl apply -f faiss_deployment.yaml
kubectl apply -f faiss_service.yaml
kubectl apply -f bot_deployment.yaml
```

