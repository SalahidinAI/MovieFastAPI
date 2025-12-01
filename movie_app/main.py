from fastapi import FastAPI
import uvicorn
from movie_app.api import (country, genre, actor, director, movie, moment, movie_language, auth,
                           social_auth, favorite)
import redis.asyncio as aioredis
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from starlette.middleware.sessions import SessionMiddleware


async def init_redis():
    return aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


movie_app = FastAPI(title='Movie', lifespan=lifespan)
movie_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")  # for github or google

movie_app.include_router(auth.auth_router)
movie_app.include_router(country.country_router)
movie_app.include_router(genre.genre_router)
movie_app.include_router(actor.actor_router)
movie_app.include_router(director.director_router)
movie_app.include_router(movie.movie_router)
movie_app.include_router(moment.moment_router)
movie_app.include_router(movie_language.movie_lang_router)
movie_app.include_router(social_auth.social_router)
movie_app.include_router(favorite.favorite_router)

if __name__ == '__main__':
    uvicorn.run(movie_app, host='127.0.0.1', port=8000)
