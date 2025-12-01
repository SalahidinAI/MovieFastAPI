from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.testing.config import db_url

from movie_app.db.models import Genre
from movie_app.db.schema import GenreSchema
from movie_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


genre_router = APIRouter(prefix='/genre', tags=['Genres'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@genre_router.post('/', response_model=GenreSchema)
async def genre_create(genre: GenreSchema, db: Session = Depends(get_db)):
    genre_db = Genre(genre_name=genre.genre_name)
    db.add(genre_db)
    db.commit()
    db.refresh(genre_db)
    return genre_db


@genre_router.get('/', response_model=List[GenreSchema])
async def genre_list(db: Session = Depends(get_db)):
    return db.query(Genre).all()


@genre_router.get('/{genre_id}/', response_model=GenreSchema)
async def genre_detail(genre_id: int, db: Session = Depends(get_db)):
    genre_db = db.query(Genre).filter(Genre.id == genre_id).first()
    if genre_db is None:
        raise HTTPException(status_code=404, detail='Genre not found')
    return genre_db


@genre_router.put('/{genre_id}/', response_model=GenreSchema)
async def genre_update(genre_id: int, genre: GenreSchema, db: Session = Depends(get_db)):
    genre_db = db.query(Genre).filter(Genre.id == genre_id).first()
    if genre_db is None:
        raise HTTPException(status_code=404, detail='Genre not found')

    genre_db.genre_name = genre.genre_name
    db.add(genre_db)
    db.commit()
    db.refresh(genre_db)
    return genre_db


@genre_router.delete('/{genre_id}/')
async def genre_delete(genre_id: int, db: Session = Depends(get_db)):
    genre_db = db.query(Genre).filter(Genre.id == genre_id).first()
    if genre_db is None:
        raise HTTPException(status_code=404, detail='Genre not found')

    db.delete(genre_db)
    db.commit()
    return {'message': 'Genre is deleted'}
