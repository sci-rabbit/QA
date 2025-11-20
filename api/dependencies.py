from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session

db_session = Annotated[AsyncSession, Depends(get_session)]