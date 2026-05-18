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

## 🛠️ Exercícios Práticos

1. Execute create_images.sh (source create_images.sh)
2. Inicialize a infraestrutura (source init_containers.sh).

---

## ⚠️ Regras Importantes (Consumo de Horas)

O GitHub Codespaces possui um limite mensal de horas gratuitas por estudante. Para não esgotar sua cota:
* **Sempre feche o ambiente:** Ao terminar de estudar, feche a aba do navegador.
* **Desligamento Automático:** A máquina possui um temporizador de inatividade e desligará automaticamente após 20 minutos sem uso. Seus arquivos salvos não serão perdidos.
