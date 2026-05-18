# Utiliza uma imagem Linux leve
FROM alpine:3.18

# Instala o Python 3 para servir a página
RUN apk add --no-cache python3

# Cria o diretório da aplicação
WORKDIR /app

# Cria uma página HTML lúdica de boas-vindas
RUN echo '<html><body style="font-family:sans-serif; text-align:center; padding-top:50px; background-color:#e6f7ff;">' > index.html && \
    echo '<h1 style="color:#0050b3;">🐳 Docker Funcionando com Sucesso!</h1>' >> index.html && \
    echo '<p style="color:#002c8c;">Parabéns, você acabou de buildar e rodar sua primeira imagem.</p>' >> index.html && \
    echo '</body></html>' >> index.html

# Expõe a porta interna do container
EXPOSE 8000

# Executa o servidor HTTP nativo do Python
CMD ["python3", "-m", "http.server", "8000"]
