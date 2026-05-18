#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo "========================================="
echo "   Validando Ambiente de Aprendizado"
echo "========================================="

# 1. Validar Docker CLI e Daemon
if docker --version > /dev/null 2>&1; then
    echo -e "[ ${GREEN}OK${NC} ] Docker CLI instalado: $(docker --version)"
    if docker ps > /dev/null 2>&1; then
        echo -e "[ ${GREEN}OK${NC} ] Serviço Docker ativo."
    else
        echo -e "[ ${RED}FALHOU${NC} ] Serviço Docker inativo."
    fi
else
    echo -e "[ ${RED}FALHOU${NC} ] Docker não instalado."
fi

# 2. Validar Docker Compose
if docker compose version > /dev/null 2>&1; then
    echo -e "[ ${GREEN}OK${NC} ] Docker Compose instalado: $(docker compose version)"
else
    echo -e "[ ${RED}FALHOU${NC} ] Docker Compose não instalado."
fi

# 3. Validar Ferramentas Kubernetes (Kubectl e Helm)
if kubectl version --client > /dev/null 2>&1; then
    echo -e "[ ${GREEN}OK${NC} ] Kubectl instalado."
else
    echo -e "[ ${RED}FALHOU${NC} ] Kubectl não instalado."
fi

if helm version > /dev/null 2>&1; then
    echo -e "[ ${GREEN}OK${NC} ] Helm instalado."
else
    echo -e "[ ${RED}FALHOU${NC} ] Helm não instalado."
fi

# 4. Validar Cluster Local (Minikube)
if minikube status | grep -q "Running"; then
    echo -e "[ ${GREEN}OK${NC} ] Cluster Kubernetes ativo."
else
    echo -e "[ ${YELLOW}AVISO${NC} ] Cluster inativo. Iniciando via terminal..."
    minikube start --driver=docker
    if minikube status | grep -q "Running"; then
        echo -e "[ ${GREEN}OK${NC} ] Cluster Kubernetes iniciado com sucesso."
    else
        echo -e "[ ${RED}FALHOU${NC} ] Não foi possível iniciar o Kubernetes."
    fi
fi

echo "========================================="
