#!/usr/bin/env python3
"""Wait for a Kubernetes deployment to become ready.

Prerequisites:
  pip install kubernetes
  kubectl config use-context <your-cluster-context>
"""

import argparse
import sys
import time

from kubernetes import client, config
from kubernetes.client.rest import ApiException


def deployment_is_ready(deployment: client.V1Deployment) -> bool:
    desired = deployment.spec.replicas or 1
    available = deployment.status.available_replicas or 0
    observed = deployment.status.observed_generation or 0
    return observed >= deployment.metadata.generation and available >= desired


def wait_for_deployment(namespace: str, name: str, timeout: int) -> None:
    config.load_kube_config()
    apps = client.AppsV1Api()
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        try:
            deployment = apps.read_namespaced_deployment(name, namespace)
        except ApiException as error:
            print(f"Could not read deployment: {error.reason}", file=sys.stderr)
            raise SystemExit(1) from error

        available = deployment.status.available_replicas or 0
        desired = deployment.spec.replicas or 1
        print(f"{name}: {available}/{desired} replicas available")
        if deployment_is_ready(deployment):
            print("Deployment is ready.")
            return
        time.sleep(5)

    print(f"Timed out after {timeout}s waiting for {name}.", file=sys.stderr)
    raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wait for a Kubernetes deployment.")
    parser.add_argument("name", help="deployment name")
    parser.add_argument("--namespace", default="default")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    wait_for_deployment(args.namespace, args.name, args.timeout)
