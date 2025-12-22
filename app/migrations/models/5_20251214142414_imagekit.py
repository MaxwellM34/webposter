from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "upload" ADD COLUMN IF NOT EXISTS "user_id" INT;
        UPDATE "upload" SET "user_id" = 0 WHERE "user_id" IS NULL;
        ALTER TABLE "upload" ALTER COLUMN "user_id" SET NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "upload" DROP COLUMN IF EXISTS "user_id";"""
