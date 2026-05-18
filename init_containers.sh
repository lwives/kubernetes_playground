#!/bin/bash
kubectl apply -f k8s/postgres-pvc.yaml
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/product-service-deployment.yaml
kubectl apply -f k8s/product-service-clusterip.yaml
kubectl apply -f k8s/order-service-deployment.yaml
kubectl apply -f k8s/order-service-clusterip.yaml
kubectl apply -f k8s/graphql-gateway-deployment.yaml
kubectl apply -f k8s/graphql-gateway-nodeport.yaml