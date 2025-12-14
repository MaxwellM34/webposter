from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import postCreate, postResponse, userCreate
from app.models.posts import Post
from app.models.user import User
from app.auth.authenticate import authenticate



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

        


   
