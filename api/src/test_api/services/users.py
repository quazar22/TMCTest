from sqlalchemy import select
from test_api.dependencies import AsyncSession
from test_api.models.user import User

async def get_users_db(db: AsyncSession):
    users = (await db.scalars(select(User))).all()
    return users