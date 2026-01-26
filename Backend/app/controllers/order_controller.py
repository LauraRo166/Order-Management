from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.repositories.order_repository import OrderRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreate, OrderResponse
from uuid import UUID

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=201)  # Sin barra
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    order_repo = OrderRepository(db)
    customer_repo = CustomerRepository(db)
    product_repo = ProductRepository(db)

    customer = await customer_repo.get_by_id(order_data.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for product_data in order_data.products:
        product = await product_repo.get_by_id(product_data.product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {product_data.product_id} not found"
            )

    order = await order_repo.create(
        order_data=order_data.dict(exclude={'products'}),
        products=[p.dict() for p in order_data.products]
    )

    return order


@router.get("", response_model=list[OrderResponse])  # Sin barra
async def get_orders(db: AsyncSession = Depends(get_db)):
    order_repo = OrderRepository(db)
    orders = await order_repo.get_all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    order_repo = OrderRepository(db)
    order = await order_repo.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: UUID, db: AsyncSession = Depends(get_db)):
    order_repo = OrderRepository(db)
    success = await order_repo.delete(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")