from litestar import Router, post, get
from litestar.exceptions import HTTPException
from litestar.connection import Request
from app.models.db import get_pool
from app.models.types import UserLogin
from app.services.auth import verify_password, create_token, decode_token
import msgspec


@post("/login")
async def login(data: UserLogin) -> dict:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, email, nom, prenom, role, password_hash FROM utilisateurs WHERE email=$1 AND actif=TRUE",
            data.email
        )
    if not row or not verify_password(data.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    token = create_token({"sub": str(row["id"]), "role": row["role"], "email": row["email"]})
    return {
        "token": token,
        "user": {"id": str(row["id"]), "email": row["email"], "nom": row["nom"], "prenom": row["prenom"], "role": row["role"]}
    }


@get("/me")
async def me(request: Request) -> dict:
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Non authentifié")
    payload = decode_token(auth[7:])
    return payload


auth_router = Router(path="/auth", route_handlers=[login, me])
