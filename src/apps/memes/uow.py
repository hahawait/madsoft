from apps.memes.repository import MemesRepository
from apps.base.uow import BaseUOW


class MemeUOW(BaseUOW):
    def __init__(
            self,
            memes_repo: MemesRepository,
    ):
        self.memes_repo = memes_repo
        super().__init__()
