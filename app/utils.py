from fastapi import Header
from typing import Optional


# Simpla funcție care returneaza owner-ul din header X-User
async def get_current_user(x_user: Optional[str] = Header(None)) -> Optional[str]:
    return x_user