from test_api.db.connection import AsyncSession, async_session
from collections.abc import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session