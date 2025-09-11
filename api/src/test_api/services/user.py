from test_api.models.user import User
from test_api.schemas.user import UserCreate
from test_api.db.connection import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

async def get_user_db(db: AsyncSession, user_id: int):
    try:
        user = await db.get_one(User, user_id)
        if not user:
            return None
        return user
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Database error: {e}")
        return None

async def create_user_db(db: AsyncSession, user: UserCreate):
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Database error: {e}")
        return None

async def delete_user_db(db: AsyncSession, user_id: int):
    try:
        user = await db.get(User, user_id)
        if user:
            await db.delete(user)
            await db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Database error: {e}")
        return None