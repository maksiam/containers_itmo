apiVersion: apps/v1
kind: Deployment
metadata:
  name: faiss-db
  labels:
    app: faiss-db
    tier: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: faiss-db
  template:
    metadata:
      labels:
        app: faiss-db
        tier: backend
    spec:
      containers:
      - name: faiss-db
        image: lab_2-faiss_db:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 5000
        volumeMounts:
        - name: faiss-data
          mountPath: /app/faiss_index
      volumes:
      - name: faiss-data
        persistentVolumeClaim:
          claimName: faiss-pvc
