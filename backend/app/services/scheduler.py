"""APScheduler jobs: convocations 15min avant, enquête froid J+30, rappels."""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from app.models.db import get_pool
from app.services.email import send_convocation, send_enquete_froid, send_rappel_enquete
import logging
import secrets
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

_scheduler: AsyncIOScheduler | None = None


def get_scheduler() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = AsyncIOScheduler(timezone="Europe/Paris")
    return _scheduler


async def schedule_convocations(session_id: str):
    """Planifie les convocations pour tous les inscrits à une session."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        session = await conn.fetchrow(
            "SELECT date_debut, heure_debut FROM sessions WHERE id=$1", session_id
        )
        if not session or not session["date_debut"] or not session["heure_debut"]:
            return
        inscrits = await conn.fetch(
            "SELECT stagiaire_id FROM inscriptions WHERE session_id=$1 AND statut != 'annule'", session_id
        )

    heure = str(session["heure_debut"])
    date_str = str(session["date_debut"])
    # Parse datetime Europe/Paris → UTC for scheduler
    from zoneinfo import ZoneInfo
    paris = ZoneInfo("Europe/Paris")
    dt_debut = datetime.fromisoformat(f"{date_str}T{heure}:00").replace(tzinfo=paris)
    dt_convocation = dt_debut - timedelta(minutes=15)

    scheduler = get_scheduler()
    for row in inscrits:
        job_id = f"conv_{session_id}_{row['stagiaire_id']}"
        if not scheduler.get_job(job_id):
            scheduler.add_job(
                send_convocation,
                trigger=DateTrigger(run_date=dt_convocation),
                args=[session_id, str(row["stagiaire_id"])],
                id=job_id,
                replace_existing=True,
                misfire_grace_time=600,
            )
    logger.info(f"Convocations planifiées pour session {session_id}: {len(inscrits)} inscrits")


async def schedule_enquete_froid(session_id: str):
    """Planifie les enquêtes à froid J+30 après la fin de session."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        session = await conn.fetchrow(
            "SELECT date_fin FROM sessions WHERE id=$1", session_id
        )
        if not session or not session["date_fin"]:
            return
        inscrits = await conn.fetch(
            "SELECT stagiaire_id FROM inscriptions WHERE session_id=$1 AND statut != 'annule'", session_id
        )

    from zoneinfo import ZoneInfo
    paris = ZoneInfo("Europe/Paris")
    dt_fin = datetime.fromisoformat(str(session["date_fin"])).replace(tzinfo=paris)
    dt_froid = dt_fin + timedelta(days=30)
    dt_rappel = dt_froid + timedelta(days=7)

    scheduler = get_scheduler()
    for row in inscrits:
        stagiaire_id = str(row["stagiaire_id"])
        token = secrets.token_urlsafe(32)

        # Store token in DB
        async with pool.acquire() as conn:
            await conn.execute(
                """INSERT INTO enquetes (session_id, stagiaire_id, type, token, reponses)
                   VALUES ($1,$2,'froid',$3,'{}')
                   ON CONFLICT (session_id, stagiaire_id, type) DO UPDATE SET token=$3""",
                session_id, stagiaire_id, token
            )

        job_id = f"enquete_froid_{session_id}_{stagiaire_id}"
        if not scheduler.get_job(job_id):
            scheduler.add_job(
                send_enquete_froid,
                trigger=DateTrigger(run_date=dt_froid),
                args=[session_id, stagiaire_id, token],
                id=job_id,
                replace_existing=True,
                misfire_grace_time=86400,
            )

        rappel_id = f"rappel_froid_{session_id}_{stagiaire_id}"
        if not scheduler.get_job(rappel_id):
            scheduler.add_job(
                _rappel_si_pas_reponse,
                trigger=DateTrigger(run_date=dt_rappel),
                args=[session_id, stagiaire_id, "froid", token],
                id=rappel_id,
                replace_existing=True,
                misfire_grace_time=86400,
            )

    logger.info(f"Enquêtes froid planifiées pour session {session_id}: {len(inscrits)} inscrits")


async def _rappel_si_pas_reponse(session_id: str, stagiaire_id: str, type_enquete: str, token: str):
    """Envoie un rappel uniquement si l'enquête n'a pas encore été remplie."""
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT reponses FROM enquetes WHERE session_id=$1 AND stagiaire_id=$2 AND type=$3",
            session_id, stagiaire_id, type_enquete
        )
    if row and (row["reponses"] is None or row["reponses"] in ("{}", "")):
        await send_rappel_enquete(session_id, stagiaire_id, type_enquete, token)
