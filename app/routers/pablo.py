from fastapi import APIRouter, Depends, File, UploadFile, Form 
from typing import Optional
from fastapi import FastAPI, HTTPException
from app.models.schemas import postCreate, postResponse
from app.models.posts import Post


router = APIRouter(prefix='', tags=['posts'])

@router.get("/posts", response_model=list[postResponse])
async def getAllPosts():
    posts = await Post.all()
    return posts


@router.get("/posts/{id}",  response_model=postResponse)
async def getPost(id: int):
    post = await Post.get_or_none(id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/post",  response_model=postResponse)
async def createPost(post: postCreate):
    newPost = await Post.create(
        caption=post.caption,
        content=post.content
    )
    return newPost

