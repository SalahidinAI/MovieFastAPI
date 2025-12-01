from datetime import datetime, time, date
from .database import Base
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Enum, ARRAY, Time, Date
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List, Optional
from enum import Enum as PyEnum, unique
from passlib.hash import bcrypt


class StatusChoices(str, PyEnum):
    pro = 'pro'
    simple = 'simple'


class TypeChoices(str, PyEnum):
    p144 = 'p144'
    p360 = 'p360'
    p480 = 'p480'
    p720 = 'p720'
    p1080 = 'p1080'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    phone: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    status: Mapped[List[StatusChoices]] = mapped_column(Enum(StatusChoices), default=[])

    user_favorite: Mapped['Favorite'] = relationship('Favorite', back_populates='user',
                                                     cascade='all, delete-orphan', uselist=False)

    def set_passwords(self, password: str):
        self.hashed_password = bcrypt.hash(password)

    def check_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))

    user: Mapped['UserProfile'] = relationship('UserProfile')


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)

    country_movie: Mapped[List['Movie']] = relationship('Movie', back_populates='country',
                                                        cascade='all, delete-orphan')


class Director(Base):
    __tablename__ = 'director'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    director_name: Mapped[str] = mapped_column(String(32), nullable=False)
    bio: Mapped[str] = mapped_column(Text)
    age: Mapped[int] = mapped_column(Integer)
    director_image: Mapped[str] = mapped_column(String)

    director_movie: Mapped['Movie'] = relationship('Movie', back_populates='director',
                                                   cascade='save-update', uselist=False)


class MovieActor(Base):
    __tablename__ = 'movie_actor'

    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'), primary_key=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey('actor.id'), primary_key=True)


class Actor(Base):
    __tablename__ = 'actor'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor_name: Mapped[str] = mapped_column(String(32), nullable=False)
    bio: Mapped[str] = mapped_column(Text)
    age: Mapped[int] = mapped_column(Integer)
    actor_image: Mapped[str] = mapped_column(String)

    actor_movie: Mapped[List['Movie']] = relationship('Movie', secondary='movie_actor', back_populates='actor')


class MovieGenre(Base):
    __tablename__ = 'movie_genre'

    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'), primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genre.id'), primary_key=True)


class Genre(Base):
    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    genre_name: Mapped[str] = mapped_column(String(64), nullable=False)

    genre_movie: Mapped[List['Movie']] = relationship('Movie', secondary='movie_genre', back_populates='genre')


class Movie(Base):
    __tablename__ = 'movie'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_name: Mapped[str] = mapped_column(String(32), nullable=False)
    movie_trailer: Mapped[str] = mapped_column(String, nullable=False)
    movie_image: Mapped[str] = mapped_column(String, nullable=False)
    status_movie: Mapped[str] = mapped_column(Enum(StatusChoices), default=StatusChoices.simple)
    year: Mapped[date] = mapped_column(Date)
    type: Mapped[List[TypeChoices]] = mapped_column(ARRAY(Enum(TypeChoices)), default=[])
    movie_time: Mapped[time] = mapped_column(Time)
    description: Mapped[str] = mapped_column(Text)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    director_id: Mapped[Optional[int]] = mapped_column(ForeignKey('director.id', ondelete='SET NULL'), nullable=True,
                                                       unique=True)

    country: Mapped['Country'] = relationship('Country', back_populates='country_movie')
    director: Mapped['Director'] = relationship('Director', back_populates='director_movie')
    actor: Mapped[List['Actor']] = relationship('Actor', secondary='movie_actor', back_populates='actor_movie')
    genre: Mapped[List['Genre']] = relationship('Genre', secondary='movie_genre', back_populates='genre_movie')
    movie_moment: Mapped[List['Moment']] = relationship('Moment', back_populates='movie',
                                                        cascade='all, delete-orphan')
    movie_review: Mapped[List['Review']] = relationship('Review', back_populates='movie',
                                                        cascade='all, delete-orphan')


class MovieLanguage(Base):
    __tablename__ = 'movie_language'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    language: Mapped[str] = mapped_column(String(32), nullable=False)
    video: Mapped[str] = mapped_column(String, nullable=False)


class Moment(Base):
    __tablename__ = 'moment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    moment_image: Mapped[str] = mapped_column(String, nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'))

    movie: Mapped['Movie'] = relationship('Movie', back_populates='movie_moment')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stars: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('review.id', ondelete='CASCADE'), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'))

    parent: Mapped[Optional['Review']] = relationship('Review', remote_side=[id])
    movie: Mapped['Movie'] = relationship('Movie', back_populates='movie_review')
    user: Mapped['UserProfile'] = relationship('UserProfile')


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='user_favorite')
    items: Mapped[List['FavoriteItem']] = relationship('FavoriteItem', back_populates='favorite',
                                                                cascade='all, delete-orphan')


class FavoriteItem(Base):
    __tablename__ = 'favorite_item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    favorite_id: Mapped[int] = mapped_column(ForeignKey('favorite.id'))
    movie_id: Mapped[int] = mapped_column(ForeignKey('movie.id'))

    favorite: Mapped['Favorite'] = relationship('Favorite', back_populates='items')
    movie: Mapped['Movie'] = relationship('Movie')
