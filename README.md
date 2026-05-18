# 🐳 Laboratório de Kubernetes

Bem-vindo ao seu ambiente prático de desenvolvimento! Este repositório utiliza o **GitHub Codespaces** para fornecer uma máquina Linux virtual completa na nuvem, com todas as ferramentas necessárias já instaladas e configuradas.

---

## 🚀 Como Iniciar o Seu Ambiente

Não é necessário instalar nada no seu computador pessoal. Siga os passos:

1. Clique no botão verde **<> Code** (no topo desta página).
2. Selecione a aba **Codespaces**.
3. Clique em **Create codespace on main**.
4. Aguarde cerca de 2 minutos até que o terminal e o editor carreguem completamente no seu navegador.

---

## 🔍 Passo 1: Validar o Ambiente

Assim que o terminal do Codespaces abrir, execute o script de testes automatizado para garantir que todos os serviços estão ativos:

```bash
source ./test-env.sh
```

> 💡 **Nota:** Se todos os itens exibirem `[ OK ]` em verde, seu ambiente está pronto!

---

## 🛠️ Exercícios Práticos (Subir Tudo no Kubernetes)

Siga exatamente esta sequência para evitar erros comuns de `ImagePullBackOff` e de conexão com o cluster.

1. Inicie o cluster local:

```bash
minikube start --driver=docker
```

2. Confirme que o Kubernetes está acessível:

```bash
kubectl cluster-info
```

3. Gere as imagens Docker dos serviços:

```bash
source create_images.sh
```

4. Carregue as imagens locais no Minikube (passo obrigatório neste ambiente):

```bash
minikube image load product-service:latest order-service:latest graphql-api-gateway:latest
```

5. Aplique toda a infraestrutura Kubernetes:

```bash
source init_containers.sh
```

6. Verifique se os pods ficaram `Running`:

```bash
kubectl get pods,svc
```

7. Abra acesso local ao gateway GraphQL (mantenha este terminal aberto):

```bash
kubectl port-forward service/graphql-gateway-nodeport 9004:9004
```

8. Em outro terminal, teste consultas GraphQL:

```bash
curl -sS -X POST 'http://127.0.0.1:9004/graphql/' \
	-H 'Content-Type: application/json' \
	--data '{"query":"{ products { id nome preco } orders { id product_id quantidade } }"}'
```

9. Teste mutation + leitura (escrita no banco + confirmação):

```bash
curl -sS -X POST 'http://127.0.0.1:9004/graphql/' \
	-H 'Content-Type: application/json' \
	--data '{"query":"mutation { createOrder(input: { product_id: 1, quantidade: 2 }) { message pedido { id product_id quantidade } } }"}'

curl -sS -X POST 'http://127.0.0.1:9004/graphql/' \
	-H 'Content-Type: application/json' \
	--data '{"query":"{ orders { id product_id quantidade } }"}'
```

### Problemas comuns

- `no route to host` ao executar `kubectl apply`:
	Cluster Minikube parado. Rode `minikube start` e tente novamente.

- `ImagePullBackOff` nos pods de aplicação:
	As imagens não foram carregadas no Minikube. Rode novamente:

```bash
minikube image load product-service:latest order-service:latest graphql-api-gateway:latest
kubectl rollout restart deployment product-service-deployment order-service-deployment graphql-gateway-deployment
```

- `curl` sem resposta em `/graphql`:
	Use `/graphql/` (com barra final), ou siga redirecionamento HTTP.

---

## ⚠️ Regras Importantes (Consumo de Horas)

O GitHub Codespaces possui um limite mensal de horas gratuitas por estudante. Para não esgotar sua cota:
* **Sempre feche o ambiente:** Ao terminar de estudar, feche a aba do navegador.
* **Desligamento Automático:** A máquina possui um temporizador de inatividade e desligará automaticamente após 20 minutos sem uso. Seus arquivos salvos não serão perdidos.
