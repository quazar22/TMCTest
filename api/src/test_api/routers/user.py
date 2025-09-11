from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from test_api.services.user import create_user_db, delete_user_db, get_user_db
from test_api.schemas.user import UserCreate, UserResponse
from test_api.dependencies import get_db

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_db(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await create_user_db(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_user_db(db, user_id)
    if deleted:
        return {"status": "User deleted", "user_id": user_id}
    raise HTTPException(status_code=404, detail="User not found")
