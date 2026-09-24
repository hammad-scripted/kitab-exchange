from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables
from colorama import init, Fore, Back, Style


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print(Fore.MAGENTA + "Database created")
    yield
    print(Fore.BLUE + "Database closed")


app = FastAPI(
    title="Kitab Exchange",
    description="Kitab Exchange API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
