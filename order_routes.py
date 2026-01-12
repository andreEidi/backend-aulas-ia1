from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import ItemPedido, Pedido, Usuario

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    return {"mensagem": "Você está na rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": "Pedido criado com sucesso. Id do pedido: {}".format(novo_pedido.id)}


@order_router.get("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.usuario != usuario or not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar este pedido")
    session.status = "CANCELADO"
    session.commit()
    return {"mensagem": f"Pedido {pedido.id} cancelado com sucesso"}

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem listar todos os pedidos.")
    pedidos = session.query(Pedido).all()
    return pedidos

order_router.get("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_ao_pedido(id_pedido: int, 
                                   item_pedido_schema: ItemPedidoSchema, 
                                   session: Session = Depends(pegar_sessao), 
                                   usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    if pedido.usuario != usuario.id and not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para modificar este pedido")
    
    item_pedido = ItemPedido(
        quantidade=item_pedido_schema.quantidade,
        sabor=item_pedido_schema.sabor,
        tamanho=item_pedido_schema.tamanho,
        preco_unitario=item_pedido_schema.preco_unitario,
        pedido=id_pedido
    )
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": f"Item adicionado com sucesso.",
        "item": item_pedido.id,
        "preco_pedido": pedido.preco     
    }

order_router.get("/pedido/remover-item/{id_item_pedido}")
async def remover_item_ao_pedido(id_item_pedido: int, 
                                   session: Session = Depends(pegar_sessao), 
                                   usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(Pedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item no pedido não encontrado")
    if pedido.usuario != usuario.id and not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para modificar este pedido")
    
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "mensagem": f"Item removido com sucesso.",
        "preco_pedido": pedido.preco, 
        "pedido": item_pedido.pedido
    }