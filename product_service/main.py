from fastapi import FastAPI, HTTPException, status, Depends 
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os

app = FastAPI(
    title="Serviço de Produtos",
    description="Gerencia produtos e seu estoque com persistência em PostgreSQL."
)

# Configuração do Banco de Dados PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres-service:5432/mydatabase")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de Dados do Produto
class ProductDB(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    preco = Column(Float)
    quantidade = Column(Integer)

# Esquema Pydantic para validação e serialização
class ProductBase(BaseModel):
    nome: str
    preco: float
    quantidade: int

class ProductCreate(ProductBase):
    id: int 

class Product(ProductCreate):
    class Config:
        from_attributes = True 

# Criar tabelas (se não existirem)
def create_db_tables():
    Base.metadata.create_all(bind=engine)
    # Popular dados iniciais se o banco estiver vazio (apenas para exemplo)
    db = SessionLocal()
    try:
        if db.query(ProductDB).count() == 0:
            print("Populating initial product data...")
            db.add_all([
                ProductDB(id=1, nome="Smartphone X", preco=1200.00, quantidade=50),
                ProductDB(id=2, nome="Notebook Pro", preco=4500.00, quantidade=20),
                ProductDB(id=3, nome="Fone de Ouvido Z", preco=250.00, quantidade=100),
            ])
            db.commit()
            print("Dados iniciais de produtos inseridos com sucesso.")
    finally:
        db.close()

# Executar criação e inserção ao iniciar o app
@app.on_event("startup")
async def startup_event():
    create_db_tables()
    print(f"Service de Produtos conectado ao Banco de Dados: {DATABASE_URL}")

# Dependência para obter a sessão do DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo para a requisição de diminuir estoque 
class DecreaseStockRequest(BaseModel):
    quantidade: int
    
@app.get("/produto/{product_id}", response_model=Product)
def get_product(product_id: int, db: SessionLocal = Depends(get_db)):
    """
    Retorna os detalhes de um produto específico.
    """
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product

@app.put("/produto/{product_id}/diminuir_estoque")
def decrease_stock(product_id: int, request_body: DecreaseStockRequest, db: SessionLocal = Depends(get_db)):
    """
    Diminui a quantidade em estoque de um produto.
    """
    quantidade_a_diminuir = request_body.quantidade

    product = db.query(ProductDB).filter(ProductDB.id == product_id).with_for_update().first() # Adiciona lock para concorrência
    if product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if product.quantidade < quantidade_a_diminuir:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    product.quantidade -= quantidade_a_diminuir
    db.add(product)
    db.commit()
    db.refresh(product) # Atualiza o objeto com os dados mais recentes do DB
    return {"message": "Estoque atualizado com sucesso", "nova_quantidade": product.quantidade}

@app.get("/produtos", response_model=list[Product])
def list_products(db: SessionLocal = Depends(get_db)):
    """
    Lista todos os produtos disponíveis.
    """
    return db.query(ProductDB).all()

@app.post("/produto", status_code=201, response_model=Product)
def create_product(product: ProductCreate, db: SessionLocal = Depends(get_db)):
    """
    Adiciona um novo produto.
    """
    db_product = db.query(ProductDB).filter(ProductDB.id == product.id).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Produto com este ID já existe")

    new_product = ProductDB(**product.model_dump()) 
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product