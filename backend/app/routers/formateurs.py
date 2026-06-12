from litestar import Router, get, post, put, delete
from litestar.connection import Request
from litestar.exceptions import HTTPException
from app.models.db import get_pool
from app.models.types import Formateur
from app.services.auth import require_auth


@get("/")
async def list_formateurs(request: Request) -> list[dict]:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM formateurs WHERE actif=TRUE ORDER BY nom")
    return [dict(r) for r in rows]


@post("/")
async def create_formateur(data: Formateur, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO formateurs (nom, prenom, email, tel, type, siret, adresse, actif)
               VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING *""",
            data.nom, data.prenom, data.email, data.tel, data.type, data.siret, data.adresse, data.actif
        )
    return dict(row)


@put("/{id:str}")
async def update_formateur(id: str, data: Formateur, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """UPDATE formateurs SET nom=$1, prenom=$2, email=$3, tel=$4, type=$5, siret=$6, adresse=$7, actif=$8
               WHERE id=$9 RETURNING *""",
            data.nom, data.prenom, data.email, data.tel, data.type, data.siret, data.adresse, data.actif, id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Formateur introuvable")
    return dict(row)


@delete("/{id:str}", status_code=204)
async def delete_formateur(id: str, request: Request) -> None:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("UPDATE formateurs SET actif=FALSE WHERE id=$1", id)


formateurs_router = Router(path="/formateurs", route_handlers=[
    list_formateurs, create_formateur, update_formateur, delete_formateur
])
