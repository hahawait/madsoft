from fastapi import APIRouter, Depends, File, Form, UploadFile

from apps.memes.dependencies import get_memes_service
from apps.memes.schemas import MemeSchema, MemeCreateSchema, MemeUpdateSchema, MemeResponceSchema
from apps.memes.service import MemeService

from apps.base.schemas import ResponseSchema

memes_router = APIRouter(
    prefix="/memes",
    tags=["memes"]
)


@memes_router.get("")
async def get_memes(
    offset: int = None,
    limit: int = None,
    meme_service: MemeService = Depends(get_memes_service),
) -> list[MemeResponceSchema]:
    """
    Получение списка мемов с пагинацией
    """
    return await meme_service.get_all(offset=offset, limit=limit)


@memes_router.get("/{meme_id}")
async def get_meme(
    meme_id: int,
    meme_service: MemeService = Depends(get_memes_service),
) -> MemeResponceSchema:
    """
    Получение мема
    """
    return await meme_service.get_by_id(meme_id=meme_id)


@memes_router.post("")
async def create_meme(
    title: str = Form(...),
    description: str = Form(...),
    image: UploadFile = File(...),
    meme_service: MemeService = Depends(get_memes_service)
) -> MemeSchema:
    """
    Создание мема
    """
    meme = MemeCreateSchema(title=title, description=description)
    return await meme_service.create(entity=meme, image=image)


@memes_router.patch("/{meme_id}")
async def update_meme(
    meme_id: int,
    title: str = Form(None),
    description: str = Form(None),
    image: UploadFile = File(None),
    meme_service: MemeService = Depends(get_memes_service)
) -> ResponseSchema:
    """
    Обновление мема по id
    """
    meme = MemeUpdateSchema(title=title, description=description)
    await meme_service.update(meme_id=meme_id, entity=meme, image=image)
    return ResponseSchema(message="Meme updated successfully")


@memes_router.delete("/{meme_id}")
async def delete_meme(
    meme_id: int,
    meme_service: MemeService = Depends(get_memes_service)
) -> MemeSchema:
    """
    Удаление мема по id
    """
    return await meme_service.delete(meme_id=meme_id)
