import base64
from fastapi import UploadFile

from apps.memes.exceptions import MemeNotFoundException
from apps.memes.models import Meme
from apps.memes.schemas import MemeCreateSchema, MemeUpdateSchema, MemeResponceSchema
from apps.memes.uow import MemeUOW

from apps.base.service import BaseService
from apps.base.storage import Storage
from config import Config


class MemeService(BaseService):
    def __init__(
            self,
            config: Config,
            uow: MemeUOW,
            storage: Storage
    ) -> None:
        self._uow = uow
        self._storage = storage
        super().__init__(config=config)

    async def get_all(
        self,
        offset: int = None,
        limit: int = None
    ) -> list[Meme]:
        memes = await self._uow.memes_repo.get_all_filtering(
            offset=offset,
            limit=limit,
        )
        async with self._storage as storage:
            images = [await storage.get(str(meme.id)) for meme in memes]

        return [
            MemeResponceSchema(
                meme=meme,
                image=base64.b64encode(image.read())
            ) for meme, image in zip(memes, images)
        ]

    async def get_by_id(self, meme_id: int) -> MemeResponceSchema:
        meme = await self._uow.memes_repo.get_one_or_none(id=meme_id)
        if not meme:
            raise MemeNotFoundException
        async with self._storage as storage:
            image = await storage.get(str(meme.id))
        return MemeResponceSchema(
            meme=meme,
            image=base64.b64encode(image.read())
        )

    async def create(self, entity: MemeCreateSchema, image: UploadFile) -> Meme:
        meme = await self._uow.memes_repo.create(**entity.model_dump(exclude={"image"}))
        async with self._storage as storage:
            await storage.save(image.file, str(meme.id))
        return meme

    async def update(self, meme_id: int, entity: MemeUpdateSchema, image: UploadFile) -> Meme:
        if image:
            async with self._storage as storage:
                await storage.save(image.file, str(meme_id))
        return await self._uow.memes_repo.update_one(
            item_id=meme_id,
            **entity.model_dump(exclude_none=True)
        )

    async def delete(self, meme_id: int) -> Meme:
        meme = await self._uow.memes_repo.delete(id=meme_id)
        async with self._storage as storage:
            await storage.delete(str(meme_id))
        return meme
