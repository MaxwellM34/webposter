from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "upload" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "caption" TEXT NOT NULL
);
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "firstname" VARCHAR(100) NOT NULL,
    "lastname" VARCHAR(100),
    "can_review" BOOL NOT NULL  DEFAULT False,
    "disabled" BOOL NOT NULL  DEFAULT False
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "users";
        DROP TABLE IF EXISTS "upload";"""
