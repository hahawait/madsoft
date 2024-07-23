from abc import ABC
from typing import Generic, Type, TypeVar

from tortoise import Model

TModel = TypeVar("TModel", bound=Model)


class BaseRepository(Generic[TModel], ABC):
    model: Type[TModel] = None

    async def get_all_filtering(
        self,
        limit: int = None,
        offset: int = None,
        **kwargs
    ) -> list[TModel]:
        query = self.model.filter(**kwargs)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return await query

    async def get_one_or_none(self, **kwargs) -> Type[TModel]:
        return await self.model.get_or_none(**kwargs)

    async def create(self, **kwargs) -> Type[TModel]:
        model = await self.model.create(**kwargs)
        return model

    async def update_one(self, item_id: int, **kwargs) -> None:
        model = await self.model.get_or_none(id=item_id)
        await model.update_from_dict(kwargs)
        await model.save()

    async def delete(self, **kwargs) -> Type[TModel]:
        model = await self.model.get_or_none(**kwargs)
        if not model:
            return None
        await model.delete()
        return model
