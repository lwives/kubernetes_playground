#!/bin/bash
# Para o Serviço de Produtos
docker build -t product-service:latest ./product_service

# Para o Serviço de Pedidos
docker build -t order-service:latest ./order_service

# Para o GraphQL API Gateway
docker build -t graphql-api-gateway:latest ./graphql_api_gateway
