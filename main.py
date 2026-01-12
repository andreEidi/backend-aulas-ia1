from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()




load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# O app deve estar criado antes de importar as rotas
app = FastAPI()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
from auth_routes import auth_router
from order_routes import order_router
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],               # Pode usar "*" no ambiente local
    allow_credentials=True,
    allow_methods=["*"],               # <-- PERMITE POST, GET, OPTIONS, etc
    allow_headers=["*"],               # <-- PERMITE Content-Type, Authorization, etc
)

# Incluindo os roteadores com prefixos e tags apropriados
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(order_router, prefix="/orders", tags=["orders"])

# To run the app, use the command:
#uvicorn main:app --reload
