# 🐳 Laboratório de Docker & Kubernetes

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
>
> O minikube (engine Kubernetes) está desligado por default, para não consumir memória nem perdermos tempo na inicialização.
> Para ativá-lo, digite o seguinte no terminal:

```bash
minikube start --driver=docker
```


---

## 🛠️ Exercícios Práticos

### Prática 1: Testando o Docker (CLI)
Crie e execute uma imagem Linux minimalista para validar o isolamento de contêineres:
```bash
docker build -t meu-primeiro-container .
docker run -d -p 8000:8000 meu-primeiro-container
```

### Prática 2: Testando o Docker Compose
Suba um servidor web Nginx estruturado em segundo plano:
```bash
docker compose up -d
```
* O VS Code exibirá uma notificação no canto inferior direito informando que a porta `8080` foi encaminhada.
* Clique em **Open in Browser** para acessar a página padrão do Nginx diretamente do seu navegador.
* Para derrubar o ambiente ao final do exercício: `docker compose down`

### Prática 3: Testando o Kubernetes (K8s)
O cluster local **Minikube** já inicia integrado ao Docker. Valide o estado do cluster:
```bash
kubectl get nodes
kubectl get pods -A
```

Crie um cluster com base no arquivo `k8s/pod.yaml`:
```bash
kubectl apply -f k8s/pod.yaml
kubectl get pods
```

---

## ⚠️ Regras Importantes (Consumo de Horas)

O GitHub Codespaces possui um limite mensal de horas gratuitas por estudante. Para não esgotar sua cota:
* **Sempre feche o ambiente:** Ao terminar de estudar, feche a aba do navegador.
* **Desligamento Automático:** A máquina possui um temporizador de inatividade e desligará automaticamente após 20 minutos sem uso. Seus arquivos salvos não serão perdidos.
