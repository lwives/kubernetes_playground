// Criado com auxílio do Google Gemini
from fastapi import FastAPI, HTTPException
from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path
from ariadne.graphql import GraphQLError
from ariadne.asgi import GraphQL 
import os 
import requests 

# Cria a instância da aplicação FastAPI
app = FastAPI(
    title="GraphQL API Gateway",
    description="Gateway que agrega APIs de Produtos e Pedidos."
)

# Carrega o esquema GraphQL 
type_defs = load_schema_from_path("schema.graphql")

# Define as URLs base dos microserviços de Pedidos e Produtos.
# Usa variáveis de ambiente para flexibilidade em diferentes ambientes (produção, desenvolvimento).
# Se as variáveis de ambiente não estiverem definidas, usa URLs de localhost como padrão.
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://localhost:8001") 
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8002")

# --- Definição dos Resolvers para Queries (Consultas) ---

# Cria um objeto QueryType para agrupar todos os resolvers de consulta
query = QueryType()

# Resolver para a query 'products' (busca todos os produtos do Serviço de Produtos)
@query.field("products")
async def resolve_products(_, info):
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/produtos")
        response.raise_for_status() # Gera HTTPError para respostas 4xx/5xx
        return response.json() # Retorna os dados JSON dos produtos
    except requests.exceptions.RequestException as e:
        # Captura erros de rede ou de status HTTP do Serviço de Produtos
        raise GraphQLError(f"Erro ao buscar produtos: {e}")

# Resolver para a query 'orders' (busca todos os pedidos do Serviço de Pedidos)
@query.field("orders")
async def resolve_orders(_, info):
    try:
        response = requests.get(f"{ORDER_SERVICE_URL}/pedidos")
        response.raise_for_status()
        return response.json() # Retorna os dados JSON dos pedidos
    except requests.exceptions.RequestException as e:
        # Captura erros de rede ou de status HTTP do Serviço de Pedidos
        raise GraphQLError(f"Erro ao buscar pedidos: {e}")

# --- Definição dos Resolvers para Mutations (Operações de Escrita) ---

# Cria um objeto MutationType para agrupar todos os resolvers de mutação
mutation = MutationType()

# Resolver para a mutação 'createOrder'
@mutation.field("createOrder")
async def resolve_create_order(_, info, input):
    product_id = input["product_id"]
    quantidade = input["quantidade"]
    try:
        # Faz uma requisição POST para o endpoint /pedido do Serviço de Pedidos para criar um pedido
        response = requests.post(
            f"{ORDER_SERVICE_URL}/pedido",
            json={"product_id": product_id, "quantidade": quantidade}
        )
        response.raise_for_status() # Gera HTTPError para respostas 4xx/5xx
        order_data = response.json() # Converte a resposta JSON do Serviço de Pedidos

        print(f"DEBUG - GraphQL Gateway: Recebeu do Serviço de Pedidos: {order_data}")
        
        # Constroi o payload que será retornado pelo GraphQL
        payload = {
            "message": "Pedido criado com sucesso.",
            "pedido": order_data # Este é o objeto que o GraphQL tenta mapear para o tipo 'Pedido'
        }
        print(f"DEBUG - GraphQL Gateway: Retornando payload: {payload}")
        return payload # Retorna o payload para o cliente GraphQL 
    except requests.exceptions.RequestException as e:
        # Captura erros de rede ou de status HTTP (ex: 400 Bad Request, 500 Internal Server Error)
        # do serviço de pedidos e os encapsula como um GraphQLError.
        raise GraphQLError(f"Erro ao criar pedido (comunicação com Serviço de Pedidos): {e}")
    except Exception as e:
        # Captura quaisquer outros erros inesperados que ocorram no próprio gateway durante o processamento.
        raise GraphQLError(f"Erro interno no GraphQL Gateway: {e}")

# Cria o esquema executável do GraphQL, combinando as definições de tipo (type_defs)
# com os resolvers (query e mutation).
schema = make_executable_schema(type_defs, query, mutation)

# Adiciona o Endpoint GraphQL ao FastAPI 
app.mount("/graphql", GraphQL(schema, debug=True)) # debug=True para habilitar o GraphQL IDE
