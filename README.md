# Kubernetes DevOps Starter

This small example has two parts:

1. `k8s/` declares a two-replica HTTP service for Kubernetes.
2. `deploy.py` waits until Kubernetes reports that the Deployment is ready — a useful step in CI/CD.

## Try it

```bash
kubectl apply -f k8s/
python -m pip install -r requirements.txt
python deploy.py hello-api --namespace default
kubectl get pods
```

The script reads your normal `kubectl` configuration, checks the Deployment every five seconds, and exits with code `0` when enough replicas are available. It exits with a non-zero code if the deployment cannot become ready within the timeout, letting a CI pipeline fail safely.
