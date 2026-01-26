"""
Integration tests for API endpoints.
"""
import pytest
from httpx import AsyncClient


class TestMainEndpoint:
    """Test main app endpoint."""

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint returns welcome message."""
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestCustomerEndpoints:
    """Test customer CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_and_get_customer(self, client: AsyncClient, sample_customer_data):
        """Test creating and retrieving a customer."""
        # Create
        response = await client.post("/customers/", json=sample_customer_data)
        assert response.status_code == 201
        customer = response.json()
        assert "id" in customer
        assert customer["email"] == sample_customer_data["email"]

        # Get
        customer_id = customer["id"]
        response = await client.get(f"/customers/{customer_id}")
        assert response.status_code == 200
        assert response.json()["id"] == customer_id


class TestProductEndpoints:
    """Test product CRUD operations."""

    @pytest.mark.asyncio
    async def test_create_and_list_products(self, client: AsyncClient, sample_product_data):
        """Test creating a product and listing all products."""
        # Create
        response = await client.post("/products/", json=sample_product_data)
        assert response.status_code == 201
        product = response.json()
        assert product["name"] == sample_product_data["name"]

        # List
        response = await client.get("/products/")
        assert response.status_code == 200
        products = response.json()
        assert len(products) > 0


class TestOrderEndpoints:
    """Test order operations."""

    @pytest.mark.asyncio
    async def test_create_order(self, client: AsyncClient, sample_customer_data, sample_product_data):
        """Test creating an order with customer and product."""
        # Create customer
        customer_resp = await client.post("/customers/", json=sample_customer_data)
        customer_id = customer_resp.json()["id"]

        # Create product
        product_resp = await client.post("/products/", json=sample_product_data)
        product = product_resp.json()

        # Create order
        order_data = {
            "amount": 199.98,
            "current_state": "pending",
            "customer_id": customer_id,
            "products": [{
                "product_id": product["id"],
                "name": product["name"],
                "quantity": 2,
                "unit_price": product["unit_price"]
            }]
        }

        response = await client.post("/orders", json=order_data)
        assert response.status_code == 201
        order = response.json()
        assert order["customer"]["id"] == customer_id
        assert order["current_state"] == "pending"
        assert "products" in order

    @pytest.mark.asyncio
    async def test_list_orders(self, client: AsyncClient):
        """Test listing all orders."""
        response = await client.get("/orders")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestTransitionEndpoints:
    """Test state transition operations."""

    @pytest.mark.asyncio
    async def test_transition_order_success(self, client: AsyncClient, sample_customer_data, sample_product_data):
        """Test successful order state transition."""
        # Setup: create customer, product, and order
        customer_resp = await client.post("/customers/", json=sample_customer_data)
        customer_id = customer_resp.json()["id"]

        product_resp = await client.post("/products/", json=sample_product_data)
        product = product_resp.json()

        order_data = {
            "amount": 500.0,
            "current_state": "pending",
            "customer_id": customer_id,
            "products": [{
                "product_id": product["id"],
                "name": product["name"],
                "quantity": 5,
                "unit_price": 100.0
            }]
        }

        order_resp = await client.post("/orders", json=order_data)
        order_id = order_resp.json()["id"]

        # Test transition
        response = await client.post(
            f"/orders/{order_id}/transition",
            json={"action": "start_preparation"}
        )

        assert response.status_code == 200
        assert response.json()["current_state"] == "in_preparation"

    @pytest.mark.asyncio
    async def test_get_allowed_actions(self, client: AsyncClient, sample_customer_data, sample_product_data):
        """Test getting allowed actions for an order."""
        # Setup order
        customer_resp = await client.post("/customers/", json=sample_customer_data)
        customer_id = customer_resp.json()["id"]

        product_resp = await client.post("/products/", json=sample_product_data)
        product = product_resp.json()

        order_data = {
            "amount": 500.0,
            "current_state": "pending",
            "customer_id": customer_id,
            "products": [{
                "product_id": product["id"],
                "name": product["name"],
                "quantity": 1,
                "unit_price": 500.0
            }]
        }

        order_resp = await client.post("/orders", json=order_data)
        order_id = order_resp.json()["id"]

        # Test
        response = await client.get(f"/orders/{order_id}/allowed-actions")
        assert response.status_code == 200
        actions = response.json()
        assert isinstance(actions, list)
        assert "start_preparation" in actions

    @pytest.mark.asyncio
    async def test_get_logs(self, client: AsyncClient):
        """Test retrieving all logs."""
        response = await client.get("/orders/logs?limit=10")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

