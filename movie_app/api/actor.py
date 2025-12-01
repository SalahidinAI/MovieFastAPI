from movie_app.db.models import Actor
from movie_app.db.schema import ActorSchema
from movie_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, HTTPException, Depends

actor_router = APIRouter(prefix='/actor', tags=['Actors'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@actor_router.post('/', response_model=ActorSchema)
async def actor_create(actor: ActorSchema, db: Session = Depends(get_db)):
    actor_db = Actor(**actor.dict())
    db.add(actor_db)
    db.commit()
    db.refresh(actor_db)
    return actor_db


@actor_router.get('/', response_model=List[ActorSchema])
async def actor_list(db: Session = Depends(get_db)):
    return db.query(Actor).all()


@actor_router.get('/{actor_id}/', response_model=ActorSchema)
async def actor_detail(actor_id: int, db: Session = Depends(get_db)):
    actor_db = db.query(Actor).filter(Actor.id == actor_id).first()
    if actor_db is None:
        raise HTTPException(status_code=404, detail='Actor not found')
    return actor_db


@actor_router.put('/{actor_id}/', response_model=ActorSchema)
async def actor_update(actor_id: int, actor: ActorSchema, db: Session = Depends(get_db)):
    actor_db = db.query(Actor).filter(Actor.id == actor_id).first()
    if actor_db is None:
        raise HTTPException(status_code=404, detail='Actor not found')

    for actor_key, actor_value in actor.dict().items():
        setattr(actor_db, actor_key, actor_value)

    db.add(actor_db)
    db.commit()
    db.refresh(actor_db)
    return actor_db


@actor_router.delete('/{actor_id}/')
async def actor_delete(actor_id: int, db: Session = Depends(get_db)):
    actor_db = db.query(Actor).filter(Actor.id == actor_id).first()
    if actor_db is None:
        raise HTTPException(status_code=404, detail='Actor not found')

    db.delete(actor_db)
    db.commit()
    return {'message': 'Actor is deleted'}
