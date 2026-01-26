from enum import Enum


class OrderState(str, Enum):
    PENDING = "pending"
    REVIEW = "review"
    IN_PREPARATION = "in_preparation"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderAction(str, Enum):
    SUBMIT_FOR_REVIEW = "submit_for_review"
    APPROVE = "approve"
    START_PREPARATION = "start_preparation"
    SHIP = "ship"
    DELIVER = "deliver"
    CANCEL = "cancel"