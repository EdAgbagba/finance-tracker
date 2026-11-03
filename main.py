from fastapi import FastAPI
from parsers import route
from contextlib import asynccontextmanager
from .database import create_db_and_tables
from .routers.transactions import router as transaction_router


# to set up what the code should do on start up--database
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(transaction_router)
