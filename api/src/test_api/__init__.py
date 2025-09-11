from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from test_api.routers import user, users
import argparse
import uvicorn
from test_api.db.connection import engine, Base
from test_api.metadata import tags_metadata
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    docs_url="/documentation", 
    openapi_tags=tags_metadata,
    title="Test API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(users.router)

def parse_args():
    parser = argparse.ArgumentParser(description="Test API")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()

def main():
    args = parse_args()
    print(f"Starting Test API on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port, reload=True if args.debug and args.host != "0.0.0.0" else False)

if __name__ == "__main__":
    main()