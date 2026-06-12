from litestar import Router, get, post, put, delete
from litestar.connection import Request
from litestar.exceptions import HTTPException
from app.models.db import get_pool
from app.models.types import Entreprise
from app.services.auth import require_auth


@get("/")
async def list_entreprises(request: Request) -> list[dict]:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM entreprises ORDER BY nom")
    return [dict(r) for r in rows]


@get("/{id:str}")
async def get_entreprise(id: str, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM entreprises WHERE id=$1", id)
        if not row:
            raise HTTPException(status_code=404, detail="Entreprise introuvable")
        stagiaires = await conn.fetch(
            "SELECT id, nom, prenom, email, poste FROM stagiaires WHERE entreprise_id=$1 ORDER BY nom", id
        )
        sessions = await conn.fetch(
            "SELECT s.id, s.code, s.titre, s.date_debut, s.statut FROM sessions s WHERE s.entreprise_id=$1 ORDER BY s.date_debut DESC", id
        )
    return {**dict(row), "stagiaires": [dict(s) for s in stagiaires], "sessions": [dict(s) for s in sessions]}


@post("/")
async def create_entreprise(data: Entreprise, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO entreprises (nom, adresse, code_postal, ville, siret, contact_nom, contact_prenom, contact_email, contact_tel, notes)
               VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10) RETURNING *""",
            data.nom, data.adresse, data.code_postal, data.ville, data.siret,
            data.contact_nom, data.contact_prenom, data.contact_email, data.contact_tel, data.notes
        )
    return dict(row)


@put("/{id:str}")
async def update_entreprise(id: str, data: Entreprise, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """UPDATE entreprises SET nom=$1, adresse=$2, code_postal=$3, ville=$4, siret=$5,
               contact_nom=$6, contact_prenom=$7, contact_email=$8, contact_tel=$9, notes=$10
               WHERE id=$11 RETURNING *""",
            data.nom, data.adresse, data.code_postal, data.ville, data.siret,
            data.contact_nom, data.contact_prenom, data.contact_email, data.contact_tel, data.notes, id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Entreprise introuvable")
    return dict(row)


@delete("/{id:str}", status_code=204)
async def delete_entreprise(id: str, request: Request) -> None:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM entreprises WHERE id=$1", id)


entreprises_router = Router(path="/entreprises", route_handlers=[
    list_entreprises, get_entreprise, create_entreprise, update_entreprise, delete_entreprise
])
