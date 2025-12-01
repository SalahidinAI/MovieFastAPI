from movie_app.db.models import Director
from movie_app.db.schema import DirectorSchema
from movie_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException


director_router = APIRouter(prefix='/director', tags=['Directors'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@director_router.post('/', response_model=DirectorSchema)
async def director_create(director: DirectorSchema, db: Session = Depends(get_db)):
    director_db = Director(**director.dict())
    db.add(director_db)
    db.commit()
    db.refresh(director_db)
    return director_db


@director_router.get('/', response_model=List[DirectorSchema])
async def director_list(db: Session = Depends(get_db)):
    return db.query(Director).all()


@director_router.get('/{director_id}/', response_model=DirectorSchema)
async def director_detail(director_id: int, db: Session = Depends(get_db)):
    director_db = db.query(Director).filter(Director.id == director_id).first()
    if director_db is None:
        raise HTTPException(status_code=404, detail='Director not found')
    return director_db


@director_router.put('/{director_id}/', response_model=DirectorSchema)
async def director_update(director_id: int, director: DirectorSchema, db: Session = Depends(get_db)):
    director_db = db.query(Director).filter(Director.id == director_id).first()
    if director_db is None:
        raise HTTPException(status_code=404, detail='Director not found')

    for director_key, director_value in director.dict().items():
        setattr(director_db, director_key, director_value)

    db.add(director_db)
    db.commit()
    db.refresh(director_db)
    return director_db


@director_router.delete('/{director_id}/')
async def director_delete(director_id: int, db: Session = Depends(get_db)):
    director_db = db.query(Director).filter(Director.id == director_id).first()
    if director_db is None:
        raise HTTPException(status_code=404, detail='Director not found')

    db.delete(director_db)
    db.commit()
    return {'message': 'Director is deleted'}