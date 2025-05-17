# Mini Project : Richdale AI Summer Internship test

## 🌿 A bref about Health Leaf Classifier

A **FastAPI** web service for classifying healthy and diseased leaves using **MobileNetV1**, containerized with **Docker** and deployed on **Kubernetes** (**Minikube**).

## Training Model with MobileNetV1

The source code for training the model is located in: [Train_Model/Train_Model_with_MobileNetV1.ipynb](Train_Model/Train_Model_with_MobileNetV1.ipynb)

## Available URLs

| URL        | Description                                    |
| ---------- | ---------------------------------------------- |
| `/`        | Main page of the web app                       |
| `/debug`   | Checks if frontend files exist (HTML, CSS, JS) |
| `/predict` | Accepts a POST image and returns prediction    |

### Example Response from `/predict`

```json
{
  "result": "Healthy leaf or Diseased leaf",
  "confidence": "99 %",
  "image": "the  image  you upload"
}
```

## FastAPI Server

Start the FastAPI server locally on 7000 port using:

```bash
uvicorn main:app --host 0.0.0.0 --port 7000
```

## Docker Setup

### Build Docker Container

```bash
docker build -t health-leaf-classifier:1.0 .
```

### Run Container Locally

```bash
docker run -p 5000:5000 health-leaf-classifier:1.0
```

## Kubernetes Deployment with Minikube

### Prerequisites

- Install Minikube from: https://github.com/kubernetes/minikube/releases
  - For Windows: Download `minikube-windows-amd64.exe`
  - Other operating systems: Select appropriate version from releases

### Start Minikube

```bash
minikube start --driver=docker
```

### Configure Docker to Use Minikube's Docker Daemon

For Windows Command Prompt:

```cmd
minikube docker-env | Invoke-Expression
```

Verify configuration:

```bash
docker ps
```

### Deploy to Kubernetes

1. Build the Docker image:

```bash
docker build -t health-leaf-classifier:1.0 .
```

2. Apply Kubernetes configuration files:

```bash
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

3. Start the service:

```bash
minikube service health-leaf-classifier-service
```

### Verification

Check the deployment status:

```bash
kubectl get pods
kubectl get deployment
kubectl get service
```

### Scaling

To scale the deployment:

```bash
kubectl scale deployment --replicas=5 health-leaf-classifier-deployment
```

### HPA Configuration
Apply the HPA configuration:
```bash
kubectl apply -f hpa.yml
```
Verify HPA is running:
```bash
kubectl get hpa
```
Monitor autoscaling behavior:
```bash
watch kubectl get hpa
```
View detailed HPA status:
```bash
kubectl describe hpa health-leaf-classifier-hpa
```
### Testing Autoscaling

Watch scaling in action:
```bash
kubectl get pods -w
```



## Important Notes

⚠️ **After making changes to the application:**

1. Rebuild the Docker image:

```bash
docker build -t health-leaf-classifier:1.0 .
```

2. Restart the deployment:

```bash
kubectl rollout restart deployment health-leaf-classifier-deployment
```

⚠️ **To use the application:**

1. Start the service:

```bash
minikube service health-leaf-classifier-service
```

2. Set up port forwarding (if needed):

```bash
kubectl port-forward svc/health-leaf-classifier 7000:7000
```

This ensures that POST requests to the API work correctly.
