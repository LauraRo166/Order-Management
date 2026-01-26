"""
Unit tests for service layer.
Tests business logic with mocked dependencies.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from app.services.transition_service import TransitionService
from app.models.order import Order


class TestTransitionService:
    """Test suite for TransitionService."""

    @pytest.fixture
    def mock_order_repo(self):
        """Create a mock order repository."""
        return AsyncMock()

    @pytest.fixture
    def mock_log_repo(self):
        """Create a mock log repository."""
        repo = AsyncMock()
        repo.db = AsyncMock()
        return repo

    @pytest.fixture
    def service(self, mock_order_repo, mock_log_repo):
        """Create TransitionService with mocked dependencies."""
        return TransitionService(mock_order_repo, mock_log_repo)

    @pytest.mark.asyncio
    async def test_transition_order_success(self, service, mock_order_repo, mock_log_repo):
        """Test successful order transition."""
        order_id = uuid4()
        mock_order = MagicMock(spec=Order)
        mock_order.id = order_id
        mock_order.current_state = "pending"
        mock_order.amount = 500.0

        mock_order_repo.get_by_id.return_value = mock_order

        result = await service.transition_order(order_id, "start_preparation")

        assert result["previous_state"] == "pending"
        assert result["new_state"] == "in_preparation"
        mock_log_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_transition_order_not_found(self, service, mock_order_repo):
        """Test transition fails when order not found."""
        mock_order_repo.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Order not found"):
            await service.transition_order(uuid4(), "start_preparation")

    @pytest.mark.asyncio
    async def test_order_over_threshold_requires_review(self, service, mock_order_repo):
        """Test business rule: orders over $1000 must go through review."""
        order_id = uuid4()
        mock_order = MagicMock(spec=Order)
        mock_order.id = order_id
        mock_order.current_state = "pending"
        mock_order.amount = 1500.0

        mock_order_repo.get_by_id.return_value = mock_order

        with pytest.raises(ValueError, match="require review"):
            await service.transition_order(order_id, "start_preparation")

    @pytest.mark.asyncio
    async def test_cannot_cancel_after_shipped(self, service, mock_order_repo):
        """Test business rule: cannot cancel after shipping."""
        order_id = uuid4()
        mock_order = MagicMock(spec=Order)
        mock_order.id = order_id
        mock_order.current_state = "shipped"
        mock_order.amount = 500.0

        mock_order_repo.get_by_id.return_value = mock_order

        with pytest.raises(ValueError):
            await service.transition_order(order_id, "cancel")

