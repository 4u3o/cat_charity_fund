from datetime import datetime
from typing import Generic, List, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_multi(
        self,
        session: AsyncSession
    ) -> List[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        user: Optional[User] = None
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if db_obj.invested_amount == db_obj.full_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def is_not_fully_invested(
        self,
        session: AsyncSession,
    ) -> bool:
        db_obj = await session.execute(
            select(self.model).where(not_(self.model.fully_invested))
        )

        return bool(db_obj.scalars().first())

    async def get_multi_with_free_amount(
        self,
        session: AsyncSession
    ) -> List[ModelType]:
        db_objs_result = await session.execute(
            select(self.model).where(
                not_(self.model.fully_invested)
            ).order_by(self.model.id)
        )

        return db_objs_result.scalars().all()
