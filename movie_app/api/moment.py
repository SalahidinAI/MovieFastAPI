from movie_app.db.models import Moment
from movie_app.db.schema import MomentSchema
from movie_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException

moment_router = APIRouter(prefix='/moment', tags=['Moments'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@moment_router.post('/', response_model=MomentSchema)
async def moment_create(moment: MomentSchema, db: Session = Depends(get_db)):
    moment_db = Moment(**moment.dict())
    db.add(moment_db)
    db.commit()
    db.refresh(moment_db)
    return moment_db


@moment_router.get('/', response_model=List[MomentSchema])
async def moment_list(db: Session = Depends(get_db)):
    return db.query(Moment).all()


@moment_router.get('/{moment_id}/', response_model=MomentSchema)
async def moment_detail(moment_id: int, db: Session = Depends(get_db)):
    moment_db = db.query(Moment).filter(Moment.id == moment_id).first()
    if moment_db is None:
        raise HTTPException(status_code=404, detail='Moment not found')
    return moment_db


@moment_router.put('/{moment_id}/', response_model=MomentSchema)
async def moment_update(moment_id: int, moment: MomentSchema, db: Session = Depends(get_db)):
    moment_db = db.query(Moment).filter(Moment.id == moment_id).first()
    if moment_db is None:
        raise HTTPException(status_code=404, detail='Moment not found')

    for moment_key, moment_value in moment.dict().items():
        setattr(moment_db, moment_key, moment_value)

    db.add(moment_db)
    db.commit()
    db.refresh(moment_db)
    return moment_db


@moment_router.delete('/{moment_id}/')
async def moment_delete(moment_id: int, db: Session = Depends(get_db)):
    moment_db = db.query(Moment).filter(Moment.id == moment_id).first()
    if moment_db is None:
        raise HTTPException(status_code=404, detail='Moment not found')

    db.delete(moment_db)
    db.commit()
    return {'message': 'Moment is deleted'}
