from typing import List
from app.services.rule_engine import (
    Rule,
    RuleCondition,
    RuleAction,
    RuleConditionType,
    RuleActionType
)


class RuleRepository:

    def __init__(self):
        self._rules = self._initialize_rules()

    def _initialize_rules(self) -> List[Rule]:
        return [
            # Rule 1: Threshold Review - orders > $1000 require review
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

            # Rule 2: High tax for high value orders
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

            # Rule 3: Notification for cancelled orders
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
