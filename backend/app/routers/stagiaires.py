from litestar import Router, get, post, put, delete
from litestar.connection import Request
from litestar.exceptions import HTTPException
from app.models.db import get_pool
from app.models.types import Stagiaire
from app.services.auth import require_auth


@get("/")
async def list_stagiaires(request: Request) -> list[dict]:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT s.*, e.nom as entreprise_nom FROM stagiaires s
               LEFT JOIN entreprises e ON e.id = s.entreprise_id
               ORDER BY s.nom"""
        )
    return [dict(r) for r in rows]


@get("/{id:str}")
async def get_stagiaire(id: str, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """SELECT s.*, e.nom as entreprise_nom FROM stagiaires s
               LEFT JOIN entreprises e ON e.id = s.entreprise_id
               WHERE s.id=$1""", id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Stagiaire introuvable")
        sessions = await conn.fetch(
            """SELECT se.id, se.code, se.titre, se.date_debut, se.statut, i.statut as inscription_statut
               FROM inscriptions i JOIN sessions se ON se.id = i.session_id
               WHERE i.stagiaire_id=$1 ORDER BY se.date_debut DESC""", id
        )
    return {**dict(row), "sessions": [dict(s) for s in sessions]}


@post("/")
async def create_stagiaire(data: Stagiaire, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO stagiaires (entreprise_id, nom, prenom, email, tel, poste, notes)
               VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING *""",
            data.entreprise_id, data.nom, data.prenom, data.email, data.tel, data.poste, data.notes
        )
    return dict(row)


@put("/{id:str}")
async def update_stagiaire(id: str, data: Stagiaire, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """UPDATE stagiaires SET entreprise_id=$1, nom=$2, prenom=$3, email=$4, tel=$5, poste=$6, notes=$7
               WHERE id=$8 RETURNING *""",
            data.entreprise_id, data.nom, data.prenom, data.email, data.tel, data.poste, data.notes, id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Stagiaire introuvable")
    return dict(row)


@delete("/{id:str}", status_code=204)
async def delete_stagiaire(id: str, request: Request) -> None:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM stagiaires WHERE id=$1", id)


stagiaires_router = Router(path="/stagiaires", route_handlers=[
    list_stagiaires, get_stagiaire, create_stagiaire, update_stagiaire, delete_stagiaire
])
