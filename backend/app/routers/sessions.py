from litestar import Router, get, post, put, delete, patch
from litestar.connection import Request
from litestar.exceptions import HTTPException
from app.models.db import get_pool
from app.models.types import Session, SessionCreneau, Inscription
from app.services.auth import require_auth, require_admin
import json


@get("/")
async def list_sessions(request: Request) -> list[dict]:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT s.*, e.nom as entreprise_nom,
               f.nom as formateur_nom, f.prenom as formateur_prenom,
               (SELECT count(*) FROM inscriptions i WHERE i.session_id=s.id) as nb_inscrits
               FROM sessions s
               LEFT JOIN entreprises e ON e.id = s.entreprise_id
               LEFT JOIN formateurs f ON f.id = s.formateur_id
               ORDER BY s.date_debut DESC NULLS LAST"""
        )
    return [dict(r) for r in rows]


@get("/{id:str}")
async def get_session(id: str, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """SELECT s.*, e.nom as entreprise_nom,
               f.nom as formateur_nom, f.prenom as formateur_prenom
               FROM sessions s
               LEFT JOIN entreprises e ON e.id = s.entreprise_id
               LEFT JOIN formateurs f ON f.id = s.formateur_id
               WHERE s.id=$1""", id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Session introuvable")
        creneaux = await conn.fetch(
            "SELECT * FROM sessions_creneaux WHERE session_id=$1 ORDER BY ordre, date", id
        )
        inscriptions = await conn.fetch(
            """SELECT i.*, st.nom, st.prenom, st.email, st.poste, e.nom as entreprise_nom
               FROM inscriptions i
               JOIN stagiaires st ON st.id = i.stagiaire_id
               LEFT JOIN entreprises e ON e.id = st.entreprise_id
               WHERE i.session_id=$1 ORDER BY st.nom""", id
        )
    return {
        **dict(row),
        "creneaux": [dict(c) for c in creneaux],
        "inscriptions": [dict(i) for i in inscriptions]
    }


@post("/")
async def create_session(data: Session, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO sessions (titre, entreprise_id, formateur_id, modules, format, modalite, lieu,
               date_debut, date_fin, heure_debut, heure_fin, participants_max, statut,
               prix_ht, tva_pct, opco_nom, opco_montant, acompte_pct, notes)
               VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19) RETURNING *""",
            data.titre, data.entreprise_id, data.formateur_id,
            json.dumps(data.modules), data.format, data.modalite, data.lieu,
            data.date_debut, data.date_fin, data.heure_debut, data.heure_fin,
            data.participants_max, data.statut,
            data.prix_ht, data.tva_pct, data.opco_nom, data.opco_montant, data.acompte_pct, data.notes
        )
        # Save creneaux if provided
        if data.creneaux:
            for i, c in enumerate(data.creneaux):
                await conn.execute(
                    """INSERT INTO sessions_creneaux (session_id, date, heure_debut, heure_fin, intervenant, ordre)
                       VALUES ($1,$2,$3,$4,$5,$6)""",
                    str(row["id"]), c.date, c.heure_debut, c.heure_fin, c.intervenant, i
                )
    return dict(row)


@put("/{id:str}")
async def update_session(id: str, data: Session, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """UPDATE sessions SET titre=$1, entreprise_id=$2, formateur_id=$3, modules=$4, format=$5,
               modalite=$6, lieu=$7, date_debut=$8, date_fin=$9, heure_debut=$10, heure_fin=$11,
               participants_max=$12, statut=$13, prix_ht=$14, tva_pct=$15, opco_nom=$16, opco_montant=$17,
               acompte_pct=$18, notes=$19, updated_at=NOW()
               WHERE id=$20 RETURNING *""",
            data.titre, data.entreprise_id, data.formateur_id,
            json.dumps(data.modules), data.format, data.modalite, data.lieu,
            data.date_debut, data.date_fin, data.heure_debut, data.heure_fin,
            data.participants_max, data.statut,
            data.prix_ht, data.tva_pct, data.opco_nom, data.opco_montant, data.acompte_pct, data.notes, id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Session introuvable")
        # Replace creneaux
        if data.creneaux is not None:
            await conn.execute("DELETE FROM sessions_creneaux WHERE session_id=$1", id)
            for i, c in enumerate(data.creneaux):
                await conn.execute(
                    """INSERT INTO sessions_creneaux (session_id, date, heure_debut, heure_fin, intervenant, ordre)
                       VALUES ($1,$2,$3,$4,$5,$6)""",
                    id, c.date, c.heure_debut, c.heure_fin, c.intervenant, i
                )
    return dict(row)


@patch("/{id:str}/statut")
async def update_statut(id: str, request: Request) -> dict:
    require_auth(request)
    body = await request.json()
    statut = body.get("statut")
    STATUTS = ["en_projet", "validee", "a_facturer", "terminee", "annulee"]
    if statut not in STATUTS:
        raise HTTPException(status_code=400, detail=f"Statut invalide. Valeurs: {STATUTS}")
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "UPDATE sessions SET statut=$1, updated_at=NOW() WHERE id=$2 RETURNING id, code, statut",
            statut, id
        )
        if not row:
            raise HTTPException(status_code=404, detail="Session introuvable")
    return dict(row)


@delete("/{id:str}", status_code=204)
async def delete_session(id: str, request: Request) -> None:
    require_admin(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM sessions WHERE id=$1", id)


# --- Inscriptions ---

@post("/{session_id:str}/inscriptions")
async def inscrire_stagiaire(session_id: str, data: Inscription, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT id FROM inscriptions WHERE session_id=$1 AND stagiaire_id=$2",
            session_id, data.stagiaire_id
        )
        if existing:
            raise HTTPException(status_code=409, detail="Stagiaire déjà inscrit à cette session")
        row = await conn.fetchrow(
            "INSERT INTO inscriptions (session_id, stagiaire_id, statut) VALUES ($1,$2,$3) RETURNING *",
            session_id, data.stagiaire_id, data.statut
        )
    return dict(row)


@delete("/{session_id:str}/inscriptions/{stagiaire_id:str}", status_code=204)
async def desinscrire_stagiaire(session_id: str, stagiaire_id: str, request: Request) -> None:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM inscriptions WHERE session_id=$1 AND stagiaire_id=$2",
            session_id, stagiaire_id
        )


sessions_router = Router(path="/sessions", route_handlers=[
    list_sessions, get_session, create_session, update_session,
    update_statut, delete_session,
    inscrire_stagiaire, desinscrire_stagiaire
])
