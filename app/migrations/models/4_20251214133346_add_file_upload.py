from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "upload" ADD "file_type" VARCHAR(255);
        ALTER TABLE "upload" ADD "url" TEXT;
        ALTER TABLE "upload" ADD "file_name" VARCHAR(255);
        ALTER TABLE "upload" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "upload" DROP COLUMN "file_type";
        ALTER TABLE "upload" DROP COLUMN "url";
        ALTER TABLE "upload" DROP COLUMN "file_name";
        ALTER TABLE "upload" DROP COLUMN "created_at";"""
