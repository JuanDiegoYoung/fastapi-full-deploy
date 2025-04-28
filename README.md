# ML API - FastAPI Deployment on AWS

This project implements a REST API using **FastAPI** to expose a Machine Learning model.  
It is designed to be packaged with **Docker**, pushed to **AWS ECR**, and deployed to **Kubernetes (EKS)** using an automated **GitHub Actions** CI/CD workflow.

## Project Structure



Estructura del proyecto:
```
app/
├── main.py
├── train_model.py

configs/
├── fastapi-deployment.yaml
├── fastapi-service.yaml
├── prometheus-deployment.yaml
├── prometheus-configmap.yaml

tests/
├── test_api.py

.github/
└── workflows/
    └── deploy.yml

README.md
requirements.txt
Dockerfile
.gitignore

```


## Technologies Used

- FastAPI
- Docker
- AWS ECR
- Kubernetes (EKS)
- GitHub Actions
- Prometheus and Grafana for monitoring (optional)

## Workflow

1. **Local development**: test the code and the API using pytest.
2. **Automated CI/CD**:
    - Every push to `main` triggers the GitHub Actions workflow.
    - Automatic testing runs.
    - Docker image is built.
    - Image is pushed to AWS ECR.
    - (Coming soon) Automatic deployment to Kubernetes.

## How to Run Locally

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API locally
uvicorn app.main:app --reload
