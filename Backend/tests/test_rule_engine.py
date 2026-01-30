import pytest
from app.repositories.rule_repository import RuleRepository
from app.services.rule_engine import RuleEngine, RuleActionType


class MockOrder:
    """Mock Order object for testing"""
    def __init__(self, amount, current_state, order_products=None):
        self.id = "test-order-123"
        self.amount = amount
        self.current_state = current_state
        self.order_products = order_products or []


class MockProduct:
    """Mock Product object for testing"""
    def __init__(self, product_id, unit_price):
        self.product_id = product_id
        self.unit_price = unit_price


class TestRuleEngine:
    """Tests for the rule engine"""

    def setup_method(self):
        """Setup executed before each test"""
        self.rule_repo = RuleRepository()
        self.rule_engine = RuleEngine(self.rule_repo)

    def test_high_value_order_blocks_direct_preparation(self):
        """Test: Orders > $1000 should be blocked when attempting direct preparation"""
        order = MockOrder(amount=1500.0, current_state="pending")
        action = "start_preparation"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)
        results = self.rule_engine.execute_actions(actions, order, {"action": action})

        assert results["blocked"] is True
        assert "review" in results["block_reason"].lower()
        assert results["metadata"]["requires_review"] is True

    def test_standard_order_passes_direct_preparation(self):
        """Test: Orders < $1000 can go directly to preparation"""
        order = MockOrder(amount=500.0, current_state="pending")
        action = "start_preparation"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)
        results = self.rule_engine.execute_actions(actions, order, {"action": action})

        assert results["blocked"] is False

    def test_standard_tax_calculation(self):
        """Test: Orders between $100 and $1000 have 10% tax"""
        order = MockOrder(amount=500.0, current_state="pending")
        action = "start_preparation"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)
        results = self.rule_engine.execute_actions(actions, order, {"action": action})

        assert "tax" in results["calculations"]
        assert results["calculations"]["tax"]["rate"] == 0.10
        assert results["calculations"]["tax"]["amount"] == 50.0
        assert results["calculations"]["tax"]["total_with_tax"] == 550.0

    def test_premium_tax_calculation(self):
        """Test: Orders > $1000 have 15% tax"""
        order = MockOrder(amount=2000.0, current_state="review")
        action = "approve"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)
        results = self.rule_engine.execute_actions(actions, order, {"action": action})

        assert "tax" in results["calculations"]
        assert results["calculations"]["tax"]["rate"] == 0.15
        assert results["calculations"]["tax"]["amount"] == 300.0

    def test_luxury_product_additional_tax(self):
        """Test: High-value products (>$500) have additional 5% tax"""
        products = [
            MockProduct("p1", 600.0),
            MockProduct("p2", 200.0)
        ]
        order = MockOrder(amount=800.0, current_state="pending", order_products=products)
        action = "start_preparation"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)
        results = self.rule_engine.execute_actions(actions, order, {"action": action})

        # Should have luxury items metadata
        assert results["metadata"].get("luxury_items") is True
        assert results["metadata"].get("additional_tax_applied") is True

    def test_cancellation_triggers_notification(self):
        """Test: Cancellation triggers notification"""
        order = MockOrder(amount=500.0, current_state="pending")
        action = "cancel"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)
        results = self.rule_engine.execute_actions(actions, order, {"action": action})

        assert results["metadata"].get("notification_sent") is True
        assert results["metadata"].get("cancellation_processed") is True

    def test_large_order_metadata(self):
        """Test: Orders with more than 10 products add metadata"""
        products = [MockProduct(f"p{i}", 50.0) for i in range(15)]
        order = MockOrder(amount=750.0, current_state="pending", order_products=products)
        action = "start_preparation"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)
        results = self.rule_engine.execute_actions(actions, order, {"action": action})

        assert results["metadata"].get("large_order") is True

    def test_multiple_rules_can_activate(self):
        """Test: Multiple rules can activate simultaneously"""
        # Order with luxury products between $100 and $1000
        products = [MockProduct("p1", 600.0)]
        order = MockOrder(amount=600.0, current_state="pending", order_products=products)
        action = "start_preparation"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)

        # Should activate:
        # - Standard Tax (10%)
        # - Luxury Product Tax (5%)
        assert len(actions) >= 2

        tax_actions = [a for a in actions if a.action_type == RuleActionType.CALCULATE_TAX]
        assert len(tax_actions) >= 2

    def test_rule_priority_ordering(self):
        """Test: Actions are ordered by priority"""
        order = MockOrder(amount=1500.0, current_state="pending")
        action = "start_preparation"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)

        # Verify actions are ordered by priority
        priorities = [a.priority for a in actions]
        assert priorities == sorted(priorities)

    def test_no_rules_for_delivered_state(self):
        """Test: No rules activate for delivered orders"""
        order = MockOrder(amount=500.0, current_state="delivered")
        action = "some_action"

        actions = self.rule_engine.evaluate(order, event="order_transition", action=action)

        # Should have no actions because state is delivered
        assert len(actions) == 0

    def test_get_field_value_nested(self):
        """Test: Get values from nested fields"""
        class MockCustomer:
            def __init__(self, name):
                self.name = name

        order = MockOrder(amount=500.0, current_state="pending")
        order.customer = MockCustomer("John Doe")

        # Test nested field access
        value = self.rule_engine._get_field_value(order, "customer.name", None)
        assert value == "John Doe"

    def test_rule_repository_crud_operations(self):
        """Test: CRUD operations of the rule repository"""
        initial_count = len(self.rule_repo.get_all_rules())

        # Test get_rule_by_id
        rule = self.rule_repo.get_rule_by_id("rule_001")
        assert rule is not None
        assert rule.id == "rule_001"

        # Test toggle_rule
        original_state = rule.enabled
        self.rule_repo.toggle_rule("rule_001", not original_state)
        rule = self.rule_repo.get_rule_by_id("rule_001")
        assert rule.enabled == (not original_state)

        # Restore original state
        self.rule_repo.toggle_rule("rule_001", original_state)


class TestRuleConditionEvaluation:
    """Specific tests for condition evaluation"""

    def setup_method(self):
        self.rule_repo = RuleRepository()
        self.rule_engine = RuleEngine(self.rule_repo)

    def test_greater_than_condition(self):
        """Test: GREATER_THAN condition"""
        from app.services.rule_engine import RuleCondition, RuleConditionType

        order = MockOrder(amount=1500.0, current_state="pending")
        condition = RuleCondition(
            condition_type=RuleConditionType.GREATER_THAN,
            field="amount",
            value=1000.0
        )

        result = self.rule_engine._evaluate_single_condition(order, condition, None)
        assert result is True

    def test_equals_condition(self):
        """Test: EQUALS condition"""
        from app.services.rule_engine import RuleCondition, RuleConditionType

        order = MockOrder(amount=1000.0, current_state="pending")
        condition = RuleCondition(
            condition_type=RuleConditionType.EQUALS,
            field="current_state",
            value="pending"
        )

        result = self.rule_engine._evaluate_single_condition(order, condition, None)
        assert result is True

    def test_in_list_condition(self):
        """Test: IN_LIST condition"""
        from app.services.rule_engine import RuleCondition, RuleConditionType

        order = MockOrder(amount=500.0, current_state="pending")
        condition = RuleCondition(
            condition_type=RuleConditionType.IN_LIST,
            field="action",
            value=["start_preparation", "approve"]
        )

        result = self.rule_engine._evaluate_single_condition(
            order, condition, "start_preparation"
        )
        assert result is True

    def test_and_condition(self):
        """Test: Compound AND condition"""
        from app.services.rule_engine import RuleCondition, RuleConditionType

        order = MockOrder(amount=500.0, current_state="pending")
        condition = RuleCondition(
            condition_type=RuleConditionType.AND,
            field="amount",
            value=None,
            sub_conditions=[
                RuleCondition(
                    condition_type=RuleConditionType.GREATER_THAN,
                    field="amount",
                    value=100.0
                ),
                RuleCondition(
                    condition_type=RuleConditionType.LESS_THAN,
                    field="amount",
                    value=1000.0
                )
            ]
        )

        result = self.rule_engine._evaluate_single_condition(order, condition, None)
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
