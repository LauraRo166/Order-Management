from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.transition_log import TransitionLog
from typing import List, Dict
from uuid import UUID, uuid4


class TransitionLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, log_data: Dict) -> TransitionLog:
        log = TransitionLog(
            id=uuid4(),
            order_id=log_data["order_id"],
            previous_state=log_data["previous_state"],
            new_state=log_data["new_state"],
            action_taken=log_data["action_taken"]
        )
        self.db.add(log)
        await self.db.flush()
        return log

    async def get_by_order_id(self, order_id: UUID) -> List[TransitionLog]:
        result = await self.db.execute(
            select(TransitionLog)
            .where(TransitionLog.order_id == order_id)
            .order_by(TransitionLog.transition_date.asc())
        )
        return list(result.scalars().all())

    async def get_all(self, limit: int = 100) -> List[TransitionLog]:
        result = await self.db.execute(
            select(TransitionLog)
            .order_by(TransitionLog.transition_date.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
