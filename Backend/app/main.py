from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.controllers.order_controller import router as order_router
from app.controllers.customer_controller import router as customer_router
from app.controllers.product_controller import router as product_router
from app.controllers.transition_controller import router as transition_router
from app.config.database import init_db, settings
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Orders Management API",
    version="1.0.0",
    lifespan=lifespan
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(transition_router)
app.include_router(order_router)
app.include_router(customer_router)
app.include_router(product_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Orders Management API"}