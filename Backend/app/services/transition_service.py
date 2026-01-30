from app.repositories.order_repository import OrderRepository
from app.repositories.transition_log_repository import TransitionLogRepository
from app.repositories.ticket_repository import TicketRepository
from app.repositories.rule_repository import RuleRepository
from app.services.state_machine import OrderStateMachine
from app.services.rule_engine import RuleEngine, RuleActionType
from app.schemas.transition import TransitionLogResponse
from typing import List, Optional, Dict, Any
from uuid import UUID


class TransitionService:
    def __init__(
        self,
        order_repo: OrderRepository,
        log_repo: TransitionLogRepository,
        ticket_repo: Optional[TicketRepository] = None,
        rule_repository: Optional[RuleRepository] = None
    ):
        self.order_repo = order_repo
        self.log_repo = log_repo
        self.ticket_repo = ticket_repo

        self.rule_repository = rule_repository or RuleRepository()
        self.rule_engine = RuleEngine(self.rule_repository)

    async def transition_order(
        self,
        order_id: UUID,
        action: str,
        cancellation_reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Performs a state transition in one command.

        This operation is atomic: if it fails, neither the state change nor the transition log is saved.
        If the action is 'cancel', a ticket is created with the cancellation reason.
        Now includes rule engine evaluation before transition.
        """

        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        rule_actions = self.rule_engine.evaluate(order, event="order_transition", action=action)

        rule_results = self.rule_engine.execute_actions(
            rule_actions,
            order,
            context={"action": action, "cancellation_reason": cancellation_reason}
        )

        if rule_results.get("blocked", False):
            raise ValueError(rule_results.get("block_reason", "Transition blocked by business rules"))

        is_valid, new_state, error_msg = OrderStateMachine.is_valid_transition(
            current_state=order.current_state,
            action=action,
            order_amount=order.amount
        )

        if not is_valid:
            raise ValueError(error_msg)

        if action == "cancel":
            if not cancellation_reason or not cancellation_reason.strip():
                raise ValueError("Cancellation reason is required when cancelling an order")

        previous_state = order.current_state

        order.current_state = new_state

        log_data = {
            "order_id": order.id,
            "previous_state": previous_state,
            "new_state": new_state,
            "action_taken": action
        }
        await self.log_repo.create(log_data)

        if action == "cancel" and self.ticket_repo:
            ticket_data = {
                "order_id": order.id,
                "cancellation_reason": cancellation_reason
            }
            await self.ticket_repo.create(ticket_data)

        await self.log_repo.db.commit()
        await self.log_repo.db.refresh(order)

        return {
            "order_id": order.id,
            "previous_state": previous_state,
            "new_state": new_state,
            "action_taken": action,
            "rule_metadata": rule_results.get("metadata", {}),
            "calculations": rule_results.get("calculations", {})
        }

    async def get_order_logs(self, order_id: UUID) -> List[TransitionLogResponse]:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("Order not found")

        logs = await self.log_repo.get_by_order_id(order_id)
        return [TransitionLogResponse.model_validate(log) for log in logs]