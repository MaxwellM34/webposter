from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from app.models import User, Post, Upload
from app.auth.authenticate import authenticate
from datetime import datetime
import os
import shutil
import tempfile
from pydantic import BaseModel
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions


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
    user_id: int
    caption: str
    url: str | None
    file_type: str | None
    file_name: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class FeedPost(BaseModel):
    id: int
    user_id: int
    caption: str
    url: str | None
    file_type: str | None
    file_name: str | None
    created_at: datetime
    is_owner: bool
    email: str


class FeedResponse(BaseModel):
    posts: list[FeedPost]



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
    caption: str = Form(""),
):
    temp_file_path: str | None = None

    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="Missing filename")

        _, ext = os.path.splitext(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

        with open(temp_file_path, "rb") as upload_fp:
            upload_result = imagekit.upload_file(
                file=upload_fp,
                file_name=file.filename,
                options=UploadFileRequestOptions(
                    use_unique_file_name=True,
                    tags=["backend-upload"],
                ),
            )

        if upload_result.response_metadata.http_status_code != 200:
            raise HTTPException(status_code=502, detail="ImageKit upload failed")

        upload = await Upload.create(
            user_id=user.id,
            caption=caption,
            url=upload_result.url,
            file_type="video" if (file.content_type or "").startswith("video/") else "image",
            file_name=upload_result.name,
        )
        return upload
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        try:
            file.file.close()
        except Exception:
            pass

@router.get(
    "/feed",
    response_model=FeedResponse,
    summary="Get feed",
)
async def get_feed(
):
    uploads = await Upload.all().order_by("-created_at")
    users = await User.all()
    user_dict = {u.id: u.email for u in users}

    posts_data: list[FeedPost] = []
    for upload in uploads:
        posts_data.append(
            FeedPost(
                id=upload.id,
                user_id=upload.user_id,
                caption=upload.caption,
                url=upload.url,
                file_type=upload.file_type,
                file_name=upload.file_name,
                created_at=upload.created_at,
                is_owner=upload.user_id == user.id,
                email=user_dict.get(upload.user_id, "Unknown"),
            )
        )

    return FeedResponse(posts=posts_data)
    


   
