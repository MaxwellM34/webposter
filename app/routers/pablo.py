from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from app.models import User, Post, Upload
from app.auth.authenticate import authenticate
from datetime import datetime
from pathlib import Path
import shutil
from uuid import uuid4
from pydantic import BaseModel


router = APIRouter(prefix='', tags=['posts'])




class postCreate(BaseModel):
    caption: str
    content: str


class postResponse(BaseModel):
    caption: str
    content: str
    created_at: datetime

class userCreate(BaseModel):
    email: str
    firstname: str
    lastname: str


class PostOut(BaseModel):
    id: int
    caption: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class UploadOut(BaseModel):
    id: int
    caption: str
    url: str | None
    file_type: str | None
    file_name: str | None
    created_at: datetime

    class Config:
        from_attributes = True



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


@router.post("/posts", response_model=postResponse)
async def createPost(post: postCreate, user=Depends(authenticate) ):
    newPost = await Post.create(
        caption=post.caption,
        content=post.content
    )
    return newPost

   
@router.post("/users", tags=["users"])
async def createUser(user: userCreate):
    newUser = await User.create(
        email=user.email,
        firstname=user.firstname,
        lastname=user.lastname
    )
    return  newUser



@router.post("/upload", response_model=UploadOut, summary="Upload file")
async def uploadFile(
    file: UploadFile = File(...),
    caption: str = Form("")
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    upload_dir = Path("uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    original_name = Path(file.filename).name
    ext = Path(original_name).suffix
    stored_name = f"{uuid4().hex}{ext}"
    dest_path = upload_dir / stored_name

    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    content_type = file.content_type or "application/octet-stream"

    upload = await Upload.create(
        caption=caption,
        url=f"/uploads/{stored_name}",
        file_type=content_type,
        file_name=original_name,
    )
    await file.close()
    return upload

@router.get(
    "/feed",
    response_model=list[UploadOut],
    summary="Get feed",
)
async def get_feed():
    return await Upload.all().order_by("-created_at")
    


   
