from fastapi import Header
from typing import Optional


# Simplă funcție care returnează owner-ul din header X-User (opțional)
async def get_current_user(x_user: Optional[str] = Header(None)) -> Optional[str]:
    return x_user