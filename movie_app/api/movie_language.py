from movie_app.db.models import MovieLanguage, Movie
from movie_app.db.schema import MovieLanguageSchema
from movie_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException

movie_lang_router = APIRouter(prefix='/movie_lang', tags=['Movie Languages'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@movie_lang_router.post('/', response_model=MovieLanguageSchema)
async def movie_lang_create(movie_lang: MovieLanguageSchema, db: Session = Depends(get_db)):
    movie_lang_db = MovieLanguage(**movie_lang.dict())
    db.add(movie_lang_db)
    db.commit()
    db.refresh(movie_lang_db)
    return movie_lang_db


@movie_lang_router.get('/', response_model=List[MovieLanguageSchema])
async def movie_lang_list(db: Session = Depends(get_db)):
    return db.query(MovieLanguage).all()


@movie_lang_router.get('/{movie_lang_id}/', response_model=MovieLanguageSchema)
async def movie_lang_detail(movie_lang_id: int, db: Session = Depends(get_db)):
    movie_lang_db = db.query(MovieLanguage).filter(MovieLanguage.id == movie_lang_id).first()
    if movie_lang_db is None:
        raise HTTPException(status_code=404, detail='Movie language not found')
    return movie_lang_db


@movie_lang_router.put('/{movie_lant_id}/', response_model=MovieLanguageSchema)
async def movie_lang_update(movie_lang_id: int, movie_lang: MovieLanguageSchema, db: Session = Depends(get_db)):
    movie_lang_db = db.query(MovieLanguage).filter(MovieLanguage.id == movie_lang_id).first()
    if movie_lang_db is None:
        raise HTTPException(status_code=404, detail='Movie language not found')

    for movie_lang_key, movie_lang_value in movie_lang.dict().items():
        setattr(movie_lang_db, movie_lang_key, movie_lang_value)

    db.add(movie_lang_db)
    db.commit()
    db.refresh(movie_lang_db)
    return movie_lang_db


@movie_lang_router.delete('/{movie_lant_id}/')
async def movie_lang_delete(movie_lant_id: int, db: Session = Depends(get_db)):
    movie_lant_db = db.query(MovieLanguage).filter(MovieLanguage.id == movie_lant_id).first()
    if movie_lant_db is None:
        raise HTTPException(status_code=404, detail='Movie language not found')

    db.delete(movie_lant_db)
    db.commit()
    return {'message': 'Movie language is deleted'}
