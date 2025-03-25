# ATS Resume Scoring System - Deployment Guide

## Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Running Locally (Docker Compose)](#running-locally-docker-compose)
- [Deploying on Kubernetes (Minikube)](#deploying-on-kubernetes-minikube)
- [Deploying on AWS EKS](#deploying-on-aws-eks)
- [Managing Kubernetes Resources](#managing-kubernetes-resources)

---

## Project Overview  
This project consists of three main services:  
- **Ollama** (LLM Model Server)  
- **FastAPI** (Backend API)  
- **Streamlit** (Frontend UI)  

Each service runs inside a **Docker container** and is deployed using **Kubernetes**.

---

## Prerequisites  
- **Docker** and **Minikube** installed  
- **kubectl** and **eksctl** configured  
- **AWS CLI** with access to **EKS**  
- **ECR Repository** (if using AWS)

---

## Running Locally (Docker Compose)  

### **1️⃣ Build and Run Containers**  
```sh
docker-compose up --build
```
Now, you can locally test 
 - Streamlit UI: http://localhost:8501
 - FastAPI API: http://localhost:8000/
 - Ollama API: http://localhost:11434

### **3️⃣ Stop Services **
```sh
docker compose down
```
---

## Deploying on AWS or Locally
For running on AWS or any other Cloud services you can follow the documentation. Here, I will show how to do on local, it will be exactly same for Clouds also only difference is that you have to 
 - Created Image Repository on Cloud
 - Push the images
 - Create tag for each images
 - Reference the same tag in the Deplyoment file as shown here
```yaml
spec:
      containers:
        - name: ollama
          image: <cloud-platorm-image-path>
```

### **3️⃣ Apply Kubernetes Deployments**
```sh
docker-compose up
```
Above command should already have created image locally, in case of cloud tag the created images and push to repository. 
On LOCAL you can directly access this image as shown in Deployment.yaml file -
```yaml
    spec:
      containers:
        - name: ollama
          image: atspass-ollama-service:latest
          imagePullPolicy: Never
```
Make sure to use imagePullPolicy: Never for running on Local else it will create issue.

Finally apply the deployments - 
```sh
kubectl apply -f Ollama/ollama-deployment.yaml
kubectl apply -f FastAPI/fastapi-deployment.yaml
kubectl apply -f StreamlitUI/streamlit-deployment.yaml
```
### **4️⃣ Check Running Services**
Finally check if the services are running using -
```sh
kubectl get pods
kubectl get services
```
