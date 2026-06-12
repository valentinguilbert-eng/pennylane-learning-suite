from litestar import Router, get, post
from litestar.connection import Request
from litestar.exceptions import HTTPException
from app.models.db import get_pool
from app.models.types import QuestionnaireReponse
from app.services.auth import require_auth
import json


@post("/reponses")
async def save_reponses(data: QuestionnaireReponse, request: Request) -> dict:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT id FROM questionnaire_reponses WHERE session_id=$1 AND stagiaire_id=$2 AND type=$3",
            data.session_id, data.stagiaire_id, data.type
        )
        if existing:
            row = await conn.fetchrow(
                """UPDATE questionnaire_reponses SET questions=$1, reponses=$2, score=$3
                   WHERE id=$4 RETURNING *""",
                json.dumps(data.questions), json.dumps(data.reponses), data.score, existing["id"]
            )
        else:
            row = await conn.fetchrow(
                """INSERT INTO questionnaire_reponses (session_id, stagiaire_id, type, questions, reponses, score)
                   VALUES ($1,$2,$3,$4,$5,$6) RETURNING *""",
                data.session_id, data.stagiaire_id, data.type,
                json.dumps(data.questions), json.dumps(data.reponses), data.score
            )
    return dict(row)


@get("/session/{session_id:str}")
async def get_resultats_session(session_id: str, request: Request) -> list[dict]:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT qr.*, s.nom, s.prenom FROM questionnaire_reponses qr
               JOIN stagiaires s ON s.id = qr.stagiaire_id
               WHERE qr.session_id=$1 ORDER BY s.nom, qr.type""",
            session_id
        )
    return [dict(r) for r in rows]


@get("/session/{session_id:str}/stagiaire/{stagiaire_id:str}")
async def get_resultats_stagiaire(session_id: str, stagiaire_id: str, request: Request) -> list[dict]:
    require_auth(request)
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT * FROM questionnaire_reponses
               WHERE session_id=$1 AND stagiaire_id=$2 ORDER BY type""",
            session_id, stagiaire_id
        )
    return [dict(r) for r in rows]


questionnaires_router = Router(path="/questionnaires", route_handlers=[
    save_reponses, get_resultats_session, get_resultats_stagiaire
])
