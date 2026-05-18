from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, declarative_base
import requests 
import os

app = FastAPI(
    title="Serviço de Pedidos",
    description="Gerencia pedidos e interage com o Serviço de Produtos."
)

# Configuração do Banco de Dados PostgreSQL
# Variável de ambiente para URL do DB, com fallback para localhost em desenvolvimento
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy para o Banco de Dados (tabela 'orders')
class OrderDB(Base):
    __tablename__ = "orders"
    # ID será auto-incrementado pelo PostgreSQL, pois é primary_key
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    quantidade = Column(Integer)

# Esquemas Pydantic para validação e serialização de dados
# PedidoCreate: Usado para receber dados na criação de um novo pedido (não inclui o ID)
class PedidoCreate(BaseModel):
    product_id: int
    quantidade: int

# Pedido: Usado para retornar um pedido completo (inclui o ID gerado)
class Pedido(PedidoCreate):
    id: int # O ID será preenchido após o commit e refresh do banco de dados
    class Config:
        from_attributes = True # Habilita o mapeamento ORM para Pydantic v2+

# Dependência para obter e fechar a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar as tabelas do banco de dados na inicialização
def create_db_tables():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Neste serviço, não populamos dados iniciais, pois pedidos são criados via API.
        if db.query(OrderDB).count() == 0:
            print("Tabela 'orders' criada ou vazia. Aguardando criação de pedidos via API.")
        else:
            print("Tabela 'orders' já existe e pode conter dados.")
    finally:
        db.close()

# Rota para verificar se o serviço está no ar
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Serviço de Pedidos"}

# Endpoint para criar pedidos
@app.post("/pedido", response_model=Pedido, status_code=status.HTTP_201_CREATED)
def create_order(pedido: PedidoCreate, db: SessionLocal = Depends(get_db)):
    # URL do serviço de produtos (ajustar para o nome do serviço no Kubernetes)
    # Usa variável de ambiente para flexibilidade, com fallback para dev local
    PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8002")

    # 1. Verificar estoque do produto no Serviço de Produtos
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/produto/{pedido.product_id}")
        response.raise_for_status() # Gera um HTTPError para respostas 4xx/5xx
        product_data = response.json()
    except requests.exceptions.RequestException as e:
        # Se houver erro de conexão ou resposta do Serviço de Produtos
        raise HTTPException(status_code=500, detail=f"Erro ao conectar/consultar Serviço de Produtos: {e}")

    if not product_data:
        raise HTTPException(status_code=404, detail="Produto não encontrado no Serviço de Produtos.")

    if product_data["quantidade"] < pedido.quantidade:
        raise HTTPException(status_code=400, detail="Estoque insuficiente para este produto.")

    # 2. Diminuir estoque no Serviço de Produtos (requisição PUT)
    try:
        response = requests.put(
            f"{PRODUCT_SERVICE_URL}/produto/{pedido.product_id}/diminuir_estoque",
            json={"quantidade": pedido.quantidade}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Se houver erro ao diminuir o estoque
        raise HTTPException(status_code=500, detail=f"Erro ao diminuir estoque no Serviço de Produtos: {e}")

    # 3. Criar pedido no Banco de Dados local
    try:
        # Cria uma nova instância de OrderDB.
        # Não passamos o 'id' pois ele é auto-incrementado pelo DB.
        new_order = OrderDB(product_id=pedido.product_id, quantidade=pedido.quantidade)

        db.add(new_order) # Adiciona o objeto à sessão
        db.commit()       # Salva as mudanças no banco de dados
        db.refresh(new_order) # Atualiza o objeto 'new_order' com os dados do DB (incluindo o ID gerado)

        print(f"Pedido criado com sucesso no Serviço de Pedidos: ID={new_order.id}, Produto ID={new_order.product_id}, Quantidade={new_order.quantidade}. Estoque atualizado.")
        # DEBUG: Imprimir o objeto ANTES de retornar para verificar seu conteúdo
        # Isso é importante para vermos o que o FastAPI está tentando serializar.
        print(f"DEBUG - Objeto Pedido sendo retornado (Serviço de Pedidos): ID={new_order.id}, Product_ID={new_order.product_id}, Quantidade={new_order.quantidade}")

        return new_order # Retorna o objeto OrderDB atualizado, que será serializado para Pedido Pydantic

    except Exception as e:
        db.rollback() # Em caso de erro, desfaz a transação
        print(f"Erro interno ao criar pedido no DB do Serviço de Pedidos: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar pedido: {e}")

# Endpoint para listar todos os pedidos
@app.get("/pedidos", response_model=list[Pedido])
def list_orders(db: SessionLocal = Depends(get_db)):
    orders = db.query(OrderDB).all()
    return orders

# Inicializa as tabelas do banco de dados na inicialização da aplicação
@app.on_event("startup")
def startup_event():
    create_db_tables()