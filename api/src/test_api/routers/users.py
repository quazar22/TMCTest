from fastapi import APIRouter, Depends
from test_api.schemas.user import UserResponse
from test_api.services.users import get_users_db
from test_api.dependencies import AsyncSession, get_db
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse], status_code=200)
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await get_users_db(db)
    return users