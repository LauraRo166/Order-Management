"""
Unit tests for OrderStateMachine.
Tests the core state machine logic and business rules.
"""
import pytest
from app.services.state_machine import OrderStateMachine


class TestOrderStateMachine:
    """Test suite for OrderStateMachine business logic."""

    def test_pending_to_in_preparation_under_threshold(self):
        """Orders under $1000 can go directly to preparation."""
        is_valid, new_state, error = OrderStateMachine.is_valid_transition(
            current_state="pending",
            action="start_preparation",
            order_amount=500.0
        )

        assert is_valid is True
        assert new_state == "in_preparation"
        assert error is None

    def test_pending_requires_review_over_threshold(self):
        """Orders over $1000 must go through review."""
        is_valid, new_state, error = OrderStateMachine.is_valid_transition(
            current_state="pending",
            action="start_preparation",
            order_amount=1500.0
        )

        assert is_valid is False
        assert "require review" in error.lower()

    def test_cancel_from_pending(self):
        """Can cancel from pending state."""
        is_valid, new_state, error = OrderStateMachine.is_valid_transition(
            current_state="pending",
            action="cancel",
            order_amount=500.0
        )

        assert is_valid is True
        assert new_state == "cancelled"

    def test_cannot_cancel_from_shipped(self):
        """Cannot cancel after shipping."""
        is_valid, new_state, error = OrderStateMachine.is_valid_transition(
            current_state="shipped",
            action="cancel",
            order_amount=500.0
        )

        assert is_valid is False

    def test_full_flow_under_threshold(self):
        """Test complete flow for order under $1000."""
        # pending -> in_preparation
        is_valid, state, _ = OrderStateMachine.is_valid_transition("pending", "start_preparation", 500.0)
        assert is_valid and state == "in_preparation"

        # in_preparation -> shipped
        is_valid, state, _ = OrderStateMachine.is_valid_transition("in_preparation", "ship", 500.0)
        assert is_valid and state == "shipped"

        # shipped -> delivered
        is_valid, state, _ = OrderStateMachine.is_valid_transition("shipped", "deliver", 500.0)
        assert is_valid and state == "delivered"

    def test_get_allowed_actions(self):
        """Test getting allowed actions per state."""
        # Pending state
        actions = OrderStateMachine.get_allowed_actions("pending")
        assert "start_preparation" in actions
        assert "cancel" in actions

        # Shipped state - no cancel allowed
        actions = OrderStateMachine.get_allowed_actions("shipped")
        assert "deliver" in actions
        assert "cancel" not in actions

        # Delivered - no actions
        actions = OrderStateMachine.get_allowed_actions("delivered")
        assert len(actions) == 0

