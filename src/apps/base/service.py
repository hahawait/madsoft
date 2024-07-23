from abc import ABC, abstractmethod

from config import Config


class BaseService(ABC):
    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    async def get_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, item_id: int):
        raise NotImplementedError

    @abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, item_id: int):
        raise NotImplementedError