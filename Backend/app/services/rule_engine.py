from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class RuleConditionType(str, Enum):
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    EQUALS = "equals"
    IN_LIST = "in_list"
    CONTAINS = "contains"
    AND = "and"
    OR = "or"


class RuleActionType(str, Enum):
    REQUIRE_REVIEW = "require_review"
    CALCULATE_TAX = "calculate_tax"
    BLOCK_TRANSITION = "block_transition"
    ADD_METADATA = "add_metadata"
    SEND_NOTIFICATION = "send_notification"


@dataclass
class RuleCondition:
    """Representa una condición que debe evaluarse"""
    condition_type: RuleConditionType
    field: str  # Campo del objeto a evaluar (ej: "amount", "product_type")
    value: Any  # Valor a comparar
    operator: Optional[str] = None  # Para condiciones complejas
    sub_conditions: Optional[List['RuleCondition']] = None  # Para AND/OR


@dataclass
class RuleAction:
    """Representa una acción a ejecutar cuando se cumple una regla"""
    action_type: RuleActionType
    parameters: Dict[str, Any]
    priority: int = 0  # Prioridad de ejecución (menor = mayor prioridad)


@dataclass
class Rule:
    """Representa una regla de negocio"""
    id: str
    name: str
    description: str
    event: str  # Evento que dispara la regla (ej: "order_transition", "order_creation")
    conditions: List[RuleCondition]
    actions: List[RuleAction]
    enabled: bool = True
    priority: int = 0


class RuleEngine:
    """Motor de evaluación de reglas de negocio"""

    def __init__(self, rule_repository):
        self.rule_repository = rule_repository

    def evaluate(self, order: Any, event: str, action: Optional[str] = None) -> List[RuleAction]:
        """
        Evalúa todas las reglas aplicables para un evento y retorna las acciones a ejecutar

        Args:
            order: Objeto order a evaluar
            event: Evento que dispara la evaluación (ej: "order_transition")
            action: Acción específica que se está intentando (opcional)

        Returns:
            Lista de RuleActions a ejecutar
        """
        applicable_rules = self.rule_repository.get_rules_by_event(event)
        actions_to_execute = []

        for rule in applicable_rules:
            if not rule.enabled:
                continue

            # Evaluar las condiciones de la regla
            if self._evaluate_conditions(order, rule.conditions, action):
                actions_to_execute.extend(rule.actions)

        # Ordenar por prioridad
        actions_to_execute.sort(key=lambda x: x.priority)
        return actions_to_execute

    def _evaluate_conditions(
        self,
        order: Any,
        conditions: List[RuleCondition],
        action: Optional[str] = None
    ) -> bool:
        """Evalúa una lista de condiciones"""
        if not conditions:
            return True

        # Si hay múltiples condiciones en el nivel raíz, se evalúan como AND
        for condition in conditions:
            if not self._evaluate_single_condition(order, condition, action):
                return False
        return True

    def _evaluate_single_condition(
        self,
        order: Any,
        condition: RuleCondition,
        action: Optional[str] = None
    ) -> bool:
        """Evalúa una condición individual"""

        # Condiciones lógicas compuestas
        if condition.condition_type == RuleConditionType.AND:
            return all(
                self._evaluate_single_condition(order, sub_cond, action)
                for sub_cond in condition.sub_conditions or []
            )

        if condition.condition_type == RuleConditionType.OR:
            return any(
                self._evaluate_single_condition(order, sub_cond, action)
                for sub_cond in condition.sub_conditions or []
            )

        # Obtener el valor del campo a evaluar
        field_value = self._get_field_value(order, condition.field, action)

        # Evaluar según el tipo de condición
        if condition.condition_type == RuleConditionType.GREATER_THAN:
            return field_value > condition.value

        elif condition.condition_type == RuleConditionType.LESS_THAN:
            return field_value < condition.value

        elif condition.condition_type == RuleConditionType.EQUALS:
            return field_value == condition.value

        elif condition.condition_type == RuleConditionType.IN_LIST:
            return field_value in condition.value

        elif condition.condition_type == RuleConditionType.CONTAINS:
            return condition.value in field_value

        return False

    def _get_field_value(self, order: Any, field: str, action: Optional[str] = None) -> Any:
        """Obtiene el valor de un campo del objeto order"""

        # Campos especiales
        if field == "action":
            return action

        if field == "current_state":
            return order.current_state

        # Campos simples del order
        if hasattr(order, field):
            return getattr(order, field)

        # Campos anidados (ej: "customer.name")
        if "." in field:
            parts = field.split(".")
            value = order
            for part in parts:
                if hasattr(value, part):
                    value = getattr(value, part)
                else:
                    return None
            return value

        # Campos calculados
        if field == "total_products":
            return len(order.order_products) if hasattr(order, 'order_products') else 0

        if field == "has_high_value_product":
            if hasattr(order, 'order_products'):
                for op in order.order_products:
                    if hasattr(op, 'unit_price') and op.unit_price > 500:
                        return True
            return False

        return None

    def execute_actions(self, actions: List[RuleAction], order: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta las acciones retornadas por el motor de reglas

        Args:
            actions: Lista de acciones a ejecutar
            order: Objeto order
            context: Contexto adicional (puede incluir resultados de acciones anteriores)

        Returns:
            Diccionario con resultados de las acciones ejecutadas
        """
        results = {
            "blocked": False,
            "block_reason": None,
            "metadata": {},
            "calculations": {}
        }

        for action in actions:
            if action.action_type == RuleActionType.REQUIRE_REVIEW:
                results["blocked"] = True
                results["block_reason"] = action.parameters.get("reason", "Review required")

            elif action.action_type == RuleActionType.CALCULATE_TAX:
                tax_rate = action.parameters.get("rate", 0.0)
                tax_amount = order.amount * tax_rate
                results["calculations"]["tax"] = {
                    "rate": tax_rate,
                    "amount": tax_amount,
                    "total_with_tax": order.amount + tax_amount
                }

            elif action.action_type == RuleActionType.BLOCK_TRANSITION:
                results["blocked"] = True
                results["block_reason"] = action.parameters.get("reason", "Transition not allowed")

            elif action.action_type == RuleActionType.ADD_METADATA:
                results["metadata"].update(action.parameters.get("data", {}))

            elif action.action_type == RuleActionType.SEND_NOTIFICATION:
                # Aquí se podría integrar con un servicio de notificaciones
                results["metadata"]["notification_sent"] = True
                results["metadata"]["notification_type"] = action.parameters.get("type", "email")

        return results
