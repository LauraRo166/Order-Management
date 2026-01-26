from app.repositories.order_repository import OrderRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreate, OrderResponse
from app.schemas.product import ProductInOrder
from typing import List
from uuid import UUID


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        customer_repo: CustomerRepository,
        product_repo: ProductRepository
    ):
        self.order_repo = order_repo
        self.customer_repo = customer_repo
        self.product_repo = product_repo

    async def create_order(self, order_data: OrderCreate) -> OrderResponse:
        customer = await self.customer_repo.get_by_id(order_data.customer_id)
        if not customer:
            raise ValueError("Customer not found")

        products_with_prices = []
        for product_data in order_data.products:
            product = await self.product_repo.get_by_id(product_data.product_id)
            if not product:
                raise ValueError(f"Product {product_data.product_id} not found")

            products_with_prices.append({
                "product_id": product.id,
                "quantity": product_data.quantity,
                "unit_price": product.unit_price
            })

        order_dict = {
            "amount": order_data.amount,
            "current_state": order_data.current_state,
            "customer_id": order_data.customer_id,
            "notes": order_data.notes
        }

        order = await self.order_repo.create(order_dict, products_with_prices)

        return await self._build_order_response(order)

    async def get_order(self, order_id: UUID) -> OrderResponse:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        return await self._build_order_response(order)

    async def get_all_orders(self) -> List[OrderResponse]:
        orders = await self.order_repo.get_all()
        return [await self._build_order_response(order) for order in orders]

    async def delete_order(self, order_id: UUID) -> bool:
        deleted = await self.order_repo.delete(order_id)
        if not deleted:
            raise ValueError("Order not found")
        return True

    async def _build_order_response(self, order) -> OrderResponse:
        from app.schemas.customer import CustomerResponse

        products = [
            ProductInOrder(
                product_id=op.product.id,
                name=op.product.name,
                quantity=op.quantity,
                unit_price=op.unit_price
            )
            for op in order.order_products
        ]

        return OrderResponse(
            id=order.id,
            amount=order.amount,
            current_state=order.current_state,
            creation_date=order.creation_date,
            customer=CustomerResponse.model_validate(order.customer),
            products=products,
            notes=order.notes
        )