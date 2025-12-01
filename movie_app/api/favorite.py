from movie_app.db.models import Favorite, UserProfile, Movie, FavoriteItem
from movie_app.db.schema import FavoriteItemSchema, FavoriteItemCreateSchema, FavoriteSchema
from movie_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException

favorite_router = APIRouter(prefix='/favorite', tags=['Favorite'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@favorite_router.get('/', response_model=FavoriteSchema)
async def favorite_list(user_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite_db:
        raise HTTPException(status_code=404, detail='Favorite not found')

    return favorite_db


@favorite_router.post('/')
async def favorite_add(movie_id: int, user_id: int, db: Session = Depends(get_db)):
    movie_db = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie_db:
        raise HTTPException(status_code=404, detail='Movie not found')

    favorite_db = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite_db:
        raise HTTPException(status_code=404, detail='User not found')

    movie_item = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite_db.id,
                                               FavoriteItem.movie_id == movie_id).first()
    if movie_item:
        raise HTTPException(status_code=400, detail='Movie already exists in favorite')

    favorite_item_db = FavoriteItem(favorite_id=favorite_db.id, movie_id=movie_id)
    db.add(favorite_item_db)
    db.commit()
    db.refresh(favorite_item_db)
    return favorite_item_db


@favorite_router.delete('/{movie_id}/')
async def movie_delete(movie_id: int, user_id: int, db: Session = Depends(get_db)):
    favorite_db = db.query(Favorite).filter(Favorite.user_id == user_id).first()
    if not favorite_db:
        raise HTTPException(status_code=404, detail='Favorite not found')

    favorite_item_db = db.query(FavoriteItem).filter(FavoriteItem.favorite_id == favorite_db.id,
                                                     FavoriteItem.movie_id == movie_id).first()
    if not favorite_item_db:
        raise HTTPException(status_code=404, detail='Favorite item not found')

    db.delete(favorite_item_db)
    db.commit()
    return {'message': 'Movie is deleted'}
