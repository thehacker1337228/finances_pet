from services.models import async_session
from services.models import Wastes
from sqlalchemy import select, func
import time
import asyncio

class WastesRequests:
    async def add(self, wastes_dto):  # принимает DTO object
        async with async_session() as session:
            waste = Wastes(wastes_dto.category_id, wastes_dto.amount, wastes_dto.created_at)  # типа to_model
            session.add(waste)
            await session.commit()





class WastesDto:
    def __init__(self, category_id, amount, created_at, id = None):
        self.category_id = category_id
        self.amount = amount
        self.created_at = created_at


