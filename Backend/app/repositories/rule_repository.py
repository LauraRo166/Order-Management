from typing import List
from app.services.rule_engine import (
    Rule,
    RuleCondition,
    RuleAction,
    RuleConditionType,
    RuleActionType
)


class RuleRepository:
    """Repositorio de reglas de negocio (mockeado)"""

    def __init__(self):
        self._rules = self._initialize_rules()

    def _initialize_rules(self) -> List[Rule]:
        """Inicializa las reglas de negocio mockeadas"""
        return [
            # Regla 1: Threshold Review - Órdenes > $1000 requieren revisión
            Rule(
                id="rule_001",
                name="High Value Order Review",
                description="Orders over $1000 must go through review process",
                event="order_transition",
                conditions=[
                    RuleCondition(
                        condition_type=RuleConditionType.GREATER_THAN,
                        field="amount",
                        value=1000.0
                    ),
                    RuleCondition(
                        condition_type=RuleConditionType.EQUALS,
                        field="action",
                        value="start_preparation"
                    ),
                    RuleCondition(
                        condition_type=RuleConditionType.EQUALS,
                        field="current_state",
                        value="pending"
                    )
                ],
                actions=[
                    RuleAction(
                        action_type=RuleActionType.BLOCK_TRANSITION,
                        parameters={
                            "reason": "Orders over $1000 require review"
                        },
                        priority=1
                    ),
                    RuleAction(
                        action_type=RuleActionType.ADD_METADATA,
                        parameters={
                            "data": {
                                "requires_review": True,
                                "review_threshold": 1000.0
                            }
                        },
                        priority=2
                    )
                ],
                enabled=True,
                priority=1
            ),

            # Regla 2: Tax Calculation basada en monto total
            Rule(
                id="rule_002",
                name="Standard Tax Calculation",
                description="Apply 10% tax for orders between $100 and $1000",
                event="order_transition",
                conditions=[
                    RuleCondition(
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
                    ),
                    RuleCondition(
                        condition_type=RuleConditionType.IN_LIST,
                        field="action",
                        value=["start_preparation", "approve"]
                    )
                ],
                actions=[
                    RuleAction(
                        action_type=RuleActionType.CALCULATE_TAX,
                        parameters={
                            "rate": 0.10,
                            "description": "Standard tax rate"
                        },
                        priority=3
                    )
                ],
                enabled=True,
                priority=2
            ),

            # Regla 3: High Tax for High Value Orders
            Rule(
                id="rule_003",
                name="Premium Tax Calculation",
                description="Apply 15% tax for orders over $1000",
                event="order_transition",
                conditions=[
                    RuleCondition(
                        condition_type=RuleConditionType.GREATER_THAN,
                        field="amount",
                        value=1000.0
                    ),
                    RuleCondition(
                        condition_type=RuleConditionType.IN_LIST,
                        field="action",
                        value=["approve", "start_preparation"]
                    )
                ],
                actions=[
                    RuleAction(
                        action_type=RuleActionType.CALCULATE_TAX,
                        parameters={
                            "rate": 0.15,
                            "description": "Premium tax rate for high-value orders"
                        },
                        priority=3
                    )
                ],
                enabled=True,
                priority=2
            ),

            # Regla 4: Tax basada en productos de alto valor
            Rule(
                id="rule_004",
                name="Luxury Product Tax",
                description="Apply additional 5% tax if order contains high-value products",
                event="order_transition",
                conditions=[
                    RuleCondition(
                        condition_type=RuleConditionType.EQUALS,
                        field="has_high_value_product",
                        value=True
                    ),
                    RuleCondition(
                        condition_type=RuleConditionType.IN_LIST,
                        field="action",
                        value=["start_preparation", "approve"]
                    )
                ],
                actions=[
                    RuleAction(
                        action_type=RuleActionType.CALCULATE_TAX,
                        parameters={
                            "rate": 0.05,
                            "description": "Luxury product additional tax"
                        },
                        priority=4
                    ),
                    RuleAction(
                        action_type=RuleActionType.ADD_METADATA,
                        parameters={
                            "data": {
                                "luxury_items": True,
                                "additional_tax_applied": True
                            }
                        },
                        priority=5
                    )
                ],
                enabled=True,
                priority=3
            ),

            # Regla 5: Notification for cancelled orders
            Rule(
                id="rule_005",
                name="Cancellation Notification",
                description="Send notification when order is cancelled",
                event="order_transition",
                conditions=[
                    RuleCondition(
                        condition_type=RuleConditionType.EQUALS,
                        field="action",
                        value="cancel"
                    )
                ],
                actions=[
                    RuleAction(
                        action_type=RuleActionType.SEND_NOTIFICATION,
                        parameters={
                            "type": "email",
                            "template": "order_cancelled",
                            "recipients": ["customer", "admin"]
                        },
                        priority=1
                    ),
                    RuleAction(
                        action_type=RuleActionType.ADD_METADATA,
                        parameters={
                            "data": {
                                "notification_sent": True,
                                "cancellation_processed": True
                            }
                        },
                        priority=2
                    )
                ],
                enabled=True,
                priority=1
            ),

            # Regla 6: Large order review (more than 10 products)
            Rule(
                id="rule_006",
                name="Large Order Review",
                description="Orders with more than 10 products require additional review",
                event="order_transition",
                conditions=[
                    RuleCondition(
                        condition_type=RuleConditionType.GREATER_THAN,
                        field="total_products",
                        value=10
                    ),
                    RuleCondition(
                        condition_type=RuleConditionType.EQUALS,
                        field="action",
                        value="start_preparation"
                    )
                ],
                actions=[
                    RuleAction(
                        action_type=RuleActionType.ADD_METADATA,
                        parameters={
                            "data": {
                                "large_order": True,
                                "requires_additional_review": True
                            }
                        },
                        priority=2
                    )
                ],
                enabled=True,
                priority=2
            )
        ]

    def get_all_rules(self) -> List[Rule]:
        """Retorna todas las reglas"""
        return self._rules

    def get_rules_by_event(self, event: str) -> List[Rule]:
        """Retorna las reglas aplicables a un evento específico"""
        return [rule for rule in self._rules if rule.event == event and rule.enabled]

    def get_rule_by_id(self, rule_id: str) -> Rule:
        """Retorna una regla por su ID"""
        for rule in self._rules:
            if rule.id == rule_id:
                return rule
        return None

    def add_rule(self, rule: Rule) -> None:
        """Agrega una nueva regla"""
        self._rules.append(rule)

    def update_rule(self, rule_id: str, updated_rule: Rule) -> bool:
        """Actualiza una regla existente"""
        for i, rule in enumerate(self._rules):
            if rule.id == rule_id:
                self._rules[i] = updated_rule
                return True
        return False

    def delete_rule(self, rule_id: str) -> bool:
        """Elimina una regla"""
        for i, rule in enumerate(self._rules):
            if rule.id == rule_id:
                self._rules.pop(i)
                return True
        return False

    def toggle_rule(self, rule_id: str, enabled: bool) -> bool:
        """Habilita o deshabilita una regla"""
        for rule in self._rules:
            if rule.id == rule_id:
                rule.enabled = enabled
                return True
        return False
