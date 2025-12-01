from movie_app.db.models import Movie
from movie_app.db.schema import MovieSchema
from movie_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException

movie_router = APIRouter(prefix='/movie', tags=['Movies'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@movie_router.post('/', response_model=MovieSchema)
async def movie_create(movie: MovieSchema, db: Session = Depends(get_db)):
    movie_db = Movie(**movie.dict())
    db.add(movie_db)
    db.commit()
    db.refresh(movie_db)
    return movie_db


@movie_router.get('/', response_model=List[MovieSchema])
async def movie_list(db: Session = Depends(get_db)):
    return db.query(Movie).all()


@movie_router.get('/{movie_id}/', response_model=MovieSchema)
async def movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie_db = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie_db is None:
        raise HTTPException(status_code=404, detail='Movie not found')
    return movie_db


@movie_router.put('/{movie_id}/', response_model=MovieSchema)
async def movie_update(movie_id: int, movie: MovieSchema, db: Session = Depends(get_db)):
    movie_db = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie_db is None:
        raise HTTPException(status_code=404, detail='Movie not found')

    for movie_key, movie_value in movie.dict().items():
        setattr(movie_db, movie_key, movie_value)

    db.add(movie_db)
    db.commit()
    db.refresh(movie_db)
    return movie_db


@movie_router.delete('/{movie_id}/')
async def movie_delete(movie_id: int, db: Session = Depends(get_db)):
    movie_db = db.query(Movie).filter(Movie.id == movie_id).first()
    if movie_db is None:
        raise HTTPException(status_code=404, detail='Movie not found')

    db.delete(movie_db)
    db.commit()
    return {'message': 'Movie is deleted'}


# unique together logic for user and movie in rating

# @app.post("/reviews/")
# async def create_review(review: ReviewSchema, db: Session = Depends(get_db)):
#     # Check if the user has already rated the movie
#     existing_review = db.query(Review).filter(Review.user_id == review.user_id, Review.movie_id == review.movie_id).first()
#
#     if existing_review:
#         raise HTTPException(status_code=400, detail="You have already rated this movie.")
#
#     # If no review exists, create a new one
#     new_review = Review(**review.dict())
#     db.add(new_review)
#     db.commit()
#     db.refresh(new_review)
#     return new_review
