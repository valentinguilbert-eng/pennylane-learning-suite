from passlib.context import CryptContext
from jose import jwt, JWTError
from litestar.exceptions import HTTPException
from app.config import SECRET_KEY
from datetime import datetime, timedelta, timezone

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
EXPIRE_DAYS = 30


def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)


def create_token(data: dict) -> str:
    payload = {**data, "exp": datetime.now(timezone.utc) + timedelta(days=EXPIRE_DAYS)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")


def require_auth(request) -> dict:
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Non authentifié")
    return decode_token(auth[7:])


def require_admin(request) -> dict:
    payload = require_auth(request)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Accès réservé aux admins")
    return payload
