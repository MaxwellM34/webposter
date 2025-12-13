from typing import Optional
from fastapi import FastAPI, HTTPException
from app.schemas import postCreate, postResponse
from tortoise.contrib.fastapi import register_tortoise
from app.models import Post

from app.config import TORTOISE_ORM

app = FastAPI()

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)


textPosts = {
    1: {"titles": "New Post", "content": "cool test post"},
    2: {"titles": "Second Post", "content": "more test content"},
    3: {"titles": "API Tips", "content": "keep endpoints simple"},
    4: {"titles": "FastAPI", "content": "auto docs are handy"},
    5: {"titles": "Reloading", "content": "uvicorn reload catches changes"},
    6: {"titles": "Routing", "content": "path params map to function args"},
    7: {"titles": "Errors", "content": "return 404 for missing items"},
    8: {"titles": "Data", "content": "this is placeholder text"},
    9: {"titles": "Testing", "content": "remember to add tests later"},
    10: {"titles": "Goodbye", "content": "last sample post"},
}


@app.get("/posts", response_model=list[postResponse])
async def getAllPosts():
    posts = await Post.all()
    return posts


@app.get("/posts/{id}",  response_model=postResponse)
async def getPost(id: int):
    post = await Post.get_or_none(id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/posts",  response_model=postResponse)
async def createPost(post: postCreate):
    newPost = await Post.create(
        title=post.title,
        content=post.content
    )
    return newPost

