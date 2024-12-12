
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

<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_4/screenshots/photo_1_2024-12-13_01-59-55.jpg" />
</p>
<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_4/screenshots/photo_3_2024-12-13_01-59-55.jpg" />
</p>
<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_4/screenshots/photo_2_2024-12-13_01-59-55.jpg" />
</p>
<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_4/screenshots/photo_1_2024-12-13_01-59-55.jpg" />
</p>
<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_4/screenshots/photo_4_2024-12-13_01-59-55.jpg" />
</p>
<p>
    <img src="https://github.com/maksiam/containers_itmo/blob/main/lab_4/screenshots/photo_5_2024-12-13_01-59-55.jpg" />
</p>

