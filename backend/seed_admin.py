"""Create the first admin user. Run once: uv run python seed_admin.py"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


async def main():
    import asyncpg
    from app.services.auth import hash_password

    db_url = os.environ["DATABASE_URL"]
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    email = input("Email: ")
    password = input("Mot de passe: ")

    conn = await asyncpg.connect(db_url)
    await conn.execute(
        """INSERT INTO utilisateurs (email, nom, prenom, role, password_hash)
           VALUES ($1,$2,$3,'admin',$4)
           ON CONFLICT (email) DO UPDATE SET password_hash=$4""",
        email, nom, prenom, hash_password(password)
    )
    await conn.close()
    print(f"Admin créé : {prenom} {nom} <{email}>")


asyncio.run(main())
