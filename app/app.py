from fastapi import FastAPI
from contextlib import asynccontextmanager
from tortoise import Tortoise
from config import Config
from app.openai import write_openai_schema
from app.routers.pablo import router as pablo_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect and (optionally) create schema
    await Tortoise.init(config=Config.TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)  # remove if you only want migrations
    write_openai_schema(app)
    print("✅ Generated openai_tools.json")
    yield
    # Shutdown: close DB connections
    await Tortoise.close_connections()

def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI + Tortoise + Postgres + GCP Auth", lifespan=lifespan)
    app.include_router(pablo_router)

    @app.get("/")
    async def root():
        return {"status": "ok"}

    return app

app = create_app()
