from typing import Dict, List, Optional
from app.models.enums import OrderState, OrderAction


class OrderStateMachine:
    REVIEW_THRESHOLD = 1000.0

    TRANSITIONS: Dict[OrderState, Dict[OrderAction, OrderState]] = {
        OrderState.PENDING: {
            OrderAction.START_PREPARATION: OrderState.IN_PREPARATION,
            OrderAction.SUBMIT_FOR_REVIEW: OrderState.REVIEW,
            OrderAction.CANCEL: OrderState.CANCELLED,
        },
        OrderState.REVIEW: {
            OrderAction.APPROVE: OrderState.IN_PREPARATION,
            OrderAction.CANCEL: OrderState.CANCELLED,
        },
        OrderState.IN_PREPARATION: {
            OrderAction.SHIP: OrderState.SHIPPED,
            OrderAction.CANCEL: OrderState.CANCELLED,
        },
        OrderState.SHIPPED: {
            OrderAction.DELIVER: OrderState.DELIVERED,
        },
        OrderState.DELIVERED: {},
        OrderState.CANCELLED: {},
    }

    @classmethod
    def is_valid_transition(
        cls,
        current_state: str,
        action: str,
        order_amount: float
    ) -> tuple[bool, Optional[str], Optional[str]]:
        try:
            current = OrderState(current_state)
            action_enum = OrderAction(action)
        except ValueError:
            return False, None, "Invalid state or action"

        if (current == OrderState.PENDING and
            action_enum == OrderAction.START_PREPARATION and
            order_amount > cls.REVIEW_THRESHOLD):
            return False, None, f"Orders over ${cls.REVIEW_THRESHOLD} require review"

        if current not in cls.TRANSITIONS:
            return False, None, f"State {current_state} not recognized"

        allowed_actions = cls.TRANSITIONS[current]

        if action_enum not in allowed_actions:
            return False, None, f"Action '{action}' is not valid from state '{current_state}'"

        new_state = allowed_actions[action_enum]
        return True, new_state.value, None

    @classmethod
    def get_allowed_actions(cls, current_state: str) -> List[str]:
        try:
            state = OrderState(current_state)
            return [action.value for action in cls.TRANSITIONS.get(state, {}).keys()]
        except ValueError:
            return []