from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from models.posts import DeletePostResponse, Post, UpdatePost
from repositories.post_repository import (
    post_create,
    post_delete,
    post_get_one,
    post_update,
    posts_get_all,
)
router = APIRouter(tags=["posts"])
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: Post, db: Session = Depends(get_db)):
    return post_create(db=db, post=post)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Post])
async def get_all_posts(db: Session = Depends(get_db)):
    return posts_get_all(db=db)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Post)
async def get_one_post(id, db: Session = Depends(get_db)):
    return post_get_one(db=db, id=id)

@router.delete(
    "/{id}", status_code=status.HTTP_200_OK, response_model=DeletePostResponse
)
async def delete_post(id, db: Session = Depends(get_db)):
    delete_status = post_delete(db=db, id=id)
    if delete_status.detail == "Doesnt Exist":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found"
        )
    else:
        return delete_status

@router.put("/", status_code=status.HTTP_200_OK, response_model=Post)
async def update_post(post: UpdatePost, db: Session = Depends(get_db)):
    return post_update(db=db, post=post)
