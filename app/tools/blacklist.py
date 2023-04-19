from typing import Literal

from app.db.storage import Storage


async def move_to_blacklist(id_: str, type_: Literal["user", "key"]) -> None:
    kds_db = Storage().get_connection()
    await kds_db.set(f"blacklist:{type_}:{id_}", 1)
