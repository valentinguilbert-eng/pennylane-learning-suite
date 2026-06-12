from litestar import Router, get, put
from litestar.connection import Request
from app.models.db import get_pool
from app.services.auth import require_admin


@get("/")
async def list_parametres(request: Request) -> dict:
    require_admin(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT cle, valeur FROM parametres ORDER BY cle")
    return {r["cle"]: r["valeur"] for r in rows}


@put("/")
async def update_parametres(request: Request) -> dict:
    require_admin(request)
    body = await request.json()
    pool = await get_pool()
    async with pool.acquire() as conn:
        for cle, valeur in body.items():
            await conn.execute(
                """INSERT INTO parametres (cle, valeur) VALUES ($1,$2)
                   ON CONFLICT (cle) DO UPDATE SET valeur=$2, updated_at=NOW()""",
                cle, str(valeur)
            )
    return {"ok": True, "updated": list(body.keys())}


parametres_router = Router(path="/parametres", route_handlers=[list_parametres, update_parametres])
