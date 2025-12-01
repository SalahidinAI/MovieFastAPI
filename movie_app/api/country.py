from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from movie_app.db.schema import CountrySchema
from movie_app.db.models import Country
from movie_app.db.database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


country_router = APIRouter(prefix='/country', tags=['Countries'])


@country_router.post('/', response_model=CountrySchema)
async def country_create(country: CountrySchema, db: Session = Depends(get_db)):
    country_db = Country(country_name=country.country_name)
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db


@country_router.get('/', response_model=List[CountrySchema])
async def country_list(db: Session = Depends(get_db)):
    return db.query(Country).all()


@country_router.get('/{country_id}/', response_model=CountrySchema)
async def country_detail(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if country_db is None:
        raise HTTPException(status_code=404, detail='Country not found')
    return country_db


@country_router.put('/{country_id}/', response_model=CountrySchema)
async def country_update(country_id: int, country: CountrySchema, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if country_db is None:
        raise HTTPException(status_code=404, detail='Country not found')

    country_db.country_name = country.country_name
    db.add(country_db)
    db.commit()
    db.refresh(country_db)
    return country_db


@country_router.delete('/{country_id}/')
async def country_delete(country_id: int, db: Session = Depends(get_db)):
    country_db = db.query(Country).filter(Country.id == country_id).first()
    if country_db is None:
        raise HTTPException(status_code=404, detail='Counry not found')

    db.delete(country_db)
    db.commit()
    return {'message': 'This country is deleted'}
