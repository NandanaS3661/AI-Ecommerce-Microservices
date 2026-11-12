# AI E-Commerce Microservices

Six FastAPI microservices + API gateway + Streamlit frontend. MySQL stores users, products, orders and stock. MongoDB stores assistant chat history and uploaded knowledge documents. Scikit-learn TF-IDF powers similar-product recommendations.

## Run on your Windows machine

Your current PowerShell location is:
`C:\Users\Administrator\Desktop\Numpy`

Extract this ZIP, then open the extracted `ai_ecommerce_microservices` folder in VS Code. In the VS Code terminal:

```powershell
cd "C:\Users\Administrator\Desktop\Numpy\ai_ecommerce_microservices"
dir
docker compose up --build
```

Docker Desktop must be running. Open http://localhost:8501 for the app and http://localhost:8000/docs for the gateway API docs. Stop with `docker compose down`.

## Services
- User service: registration and lookup
- Product service: catalogue and search
- Order service: order creation/listing
- Inventory service: stock lookup/update
- Recommendation service: TF-IDF similarity recommendations
- AI service: document upload, retrieval-based Q&A, chat history
- API gateway: routes requests to services

## GitHub
Create an empty GitHub repository, then run from this folder:

```powershell
git init
git add .
git commit -m "Initial AI e-commerce microservices"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ai-ecommerce-microservices.git
git push -u origin main
```
Replace `YOUR-USERNAME`.

## Kubernetes
For Docker Desktop Kubernetes, build local images first (commands are listed below), then:

```powershell
kubectl apply -f k8s/00-config.yaml
kubectl apply -f k8s/01-databases.yaml
kubectl apply -f k8s/02-services.yaml
kubectl apply -f k8s/03-ml-deployment.yaml
kubectl get pods -n ai-ecommerce
kubectl get services -n ai-ecommerce
kubectl port-forward -n ai-ecommerce service/frontend 8501:8501
```

Build images before applying:
```powershell
docker build -t ai-ecommerce-api-gateway:latest ./services/api-gateway
docker build -t ai-ecommerce-user-service:latest ./services/user-service
docker build -t ai-ecommerce-product-service:latest ./services/product-service
docker build -t ai-ecommerce-order-service:latest ./services/order-service
docker build -t ai-ecommerce-inventory-service:latest ./services/inventory-service
docker build -t ai-ecommerce-recommendation-service:latest ./services/recommendation-service
docker build -t ai-ecommerce-ai-service:latest ./services/ai-service
docker build -t ai-ecommerce-frontend:latest ./frontend
```

## Notes
This is a learning/demo baseline, not production-ready. The chatbot uses document retrieval rather than a hosted generative LLM. Add an LLM API integration, authentication, database migrations, persistent Kubernetes volumes, health probes, resource limits and proper secrets management before production. Change development passwords before deployment.
