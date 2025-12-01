from pydantic import BaseModel, EmailStr, field_validator, conint
from datetime import datetime, date, time
from typing import List, Optional
from .models import StatusChoices, TypeChoices


class UserProfileSchema(BaseModel):
    first_name: str
    last_name: Optional[str]
    username: str
    password: str
    email: EmailStr
    phone: str
    age: conint(ge=15, le=100)
    status: StatusChoices

    class Config:
        from_attributes = True

    @field_validator('age')
    def check_age(cls, v):
        if not (15 <= v <= 100):
            raise ValueError('Age must be between 15 and 100')
        return v


class CountrySchema(BaseModel):
    country_name: str

    class Config:
        from_attributes = True


class DirectorSchema(BaseModel):
    director_name: str
    bio: str
    age: conint(ge=15, le=100)
    director_image: str

    class Config:
        from_attributes = True

    @field_validator('age')
    def check_age(cls, v):
        if not (15 <= v <= 100):
            raise ValueError('Age should be between 15 and 100')
        return v


# class MovieActorSchema(BaseModel):
#     movie_id: int
#     actor_id: int
#
#     class Config:
#         from_attributes = True


class ActorSchema(BaseModel):
    actor_name: str
    bio: str
    age: conint(ge=15, le=100)
    actor_image: str

    class Config:
        from_attributes = True

    @field_validator('age')
    def check_age(cls, v):
        if not (15 <= v <= 100):
            raise ValueError('Age must be between 15 and 100')
        return v


# class MovieGenreSchema(BaseModel):
#     movie_id: int
#     genre_id: int
#
#     class Config:
#         from_attributes = True


class GenreSchema(BaseModel):
    genre_name: str

    class Config:
        from_attributes = True


class MovieSchema(BaseModel):
    movie_name: str
    movie_trailer: str
    movie_image: str
    status_movie: str
    year: date
    type: List[TypeChoices]
    movie_time: time
    description: str
    country_id: int
    director_id: Optional[int]

    @field_validator('year')
    def check_year_not_in_future(cls, v):
        if v > date.today():
            raise ValueError("The year cannot be in the future")
        return v

    class Config:
        from_attributes = True


class MovieLanguageSchema(BaseModel):
    language: str
    video: str

    class Config:
        from_attributes = True


class MomentSchema(BaseModel):
    moment_image: str
    movie_id: int

    class Config:
        from_attributes = True


class ReviewSchema(BaseModel):
    stars: Optional[conint(ge=1, le=5)]
    text: Optional[str]
    parent_id: Optional[int]
    user_id: int
    movie_id: int

    class Config:
        from_attributes = True

    # @field_validator('text', mode='before')
    # def check_stars_or_text(cls, v, values, field):
    #     stars = values.get('stars')
    #     if not stars and not v:
    #         raise ValueError('Either stars or text must be provided')
    #     return v

    @field_validator('text', mode='before')
    def validate_text(cls, v):
        if v is None or v.strip() == "":
            raise ValueError("Text cannot be empty.")
        return v


class FavoriteItemSchema(BaseModel):
    id: int
    movie_id: int

    class Config:
        from_attributes = True


class FavoriteSchema(BaseModel):
    user_id: int
    items: List[FavoriteItemSchema] = []

    class Config:
        from_attributes = True


class FavoriteItemCreateSchema(BaseModel):
    movie_id: int

    class Config:
        from_attributes = True

