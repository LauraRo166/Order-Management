from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductResponse
from typing import List
from uuid import UUID

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        repository = ProductRepository(db)
        service = ProductService(repository)
        return await service.create_product(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    repository = ProductRepository(db)
    service = ProductService(repository)
    return await service.get_all_products()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    try:
        repository = ProductRepository(db)
        service = ProductService(repository)
        return await service.get_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))