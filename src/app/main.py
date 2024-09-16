from contextlib import asynccontextmanager

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI

load_dotenv(find_dotenv())


from app.db_and_models.session import create_db_and_tables
from app.routers.followers import router as follower_router
from app.routers.likes import router as like_router
from app.routers.posts import router as post_router
from app.routers.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    # drop_tables()


app = FastAPI(
    lifespan=lifespan,
    title="Twitter Clone",
    description="Unsere App im Kurs",
    version="1.0.0",
    contact={"name": "Coding Crashkurs", "email": "blbla@aaa.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/license/mit"},
)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(like_router)
app.include_router(follower_router)
