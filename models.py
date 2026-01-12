from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

#cria a conexão com o banco de dados SQLite
db = create_engine("sqlite:///banco.db")

# cria a base do banco de dados
Base = declarative_base()

#criar as classes/tabelas do banco de dados
class Usuario(Base):
    __tablename__ = "usuarios"
    from sqlalchemy import Column, Integer, String

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome",String, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo",Boolean)
    admin = Column("admin",Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("EM_ANDAMENTO", "EM_ANDAMENTO"),
    #     ("FINALIZADO", "FINALIZADO"),
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String, nullable=False)
    usuario = Column("usuario", ForeignKey("usuarios.id"), nullable=False)
    preco = Column("preco", Float, nullable=False)
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.status = status
        self.usuario = usuario
        self.preco = preco

    def calcular_preco(self):
        # preco_pedido = 0
        # for item in self.itens:
        #     preco_item = item.preco_unitario * item.quantidade
        #     preco_pedido += preco_item
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer, nullable=False)
    sabor = Column("sabor", String, nullable=False)
    tamanho = Column("tamanho", String, nullable=False)
    preco_unitario = Column("preco_unitario", Float, nullable=False)
    pedido = Column("pedido", ForeignKey("pedidos.id"), nullable=False)

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido



#criar migração (tabelas) no banco de dados
# alembic revision --autogenerate -m "Criando tabelas iniciais"
#executar a migração
# alembic upgrade head