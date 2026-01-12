from main import ALGORITHM, SECRET_KEY, oauth2_schema
from models import Usuario, db
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        # yield session para usar como gerador
        yield session
    finally:
        #finally executa independente se deu erro ou não
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.token == token).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")   
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(payload.get("sub"))
        if id_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return id_usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado. Verifique a validade do token.")