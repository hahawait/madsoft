from fastapi import Depends

from apps.memes.repository import MemesRepository
from apps.memes.service import MemeService
from apps.memes.uow import MemeUOW

from apps.base.storage import Storage

from config import Config, get_config


async def get_memes_service(config: Config = Depends(get_config)) -> MemeService:
    return MemeService(
        config=config,
        uow=MemeUOW(
            memes_repo=MemesRepository()
        ),
        storage=Storage(config)
    )
