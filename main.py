# import routes
from routes.users import user_router
from routes.books import book_router
from exceptions import NotFoundException, not_found_exception_handler, BadRequestException, bad_request_exception_handler, InternalServerException, internal_server_exception_handler
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



# routes
app.include_router(user_router)
app.include_router(book_router)



#exceptions


app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(InternalServerException, internal_server_exception_handler)   


@app.get("/")
async def root():
    return {"message": "Hello World"}
