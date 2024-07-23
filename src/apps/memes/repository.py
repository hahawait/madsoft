from apps.memes.models import Meme
from apps.base.repository import BaseRepository


class MemesRepository(BaseRepository[Meme]):
    model = Meme
