from contextlib import AsyncExitStack
from io import BytesIO
from typing import IO

from aioboto3.session import Session

from config import Config


class Storage:
    """Менеджер хранилища"""

    def __init__(
        self,
        config: Config,
    ):
        self._bucket_name = config.storage.AWS_BUCKET_NAME
        self._exit_stack = AsyncExitStack()
        self._storage_params = dict(
            service_name="s3",
            # region_name="ru-central1",
            aws_secret_access_key=config.storage.AWS_SECRET_ACCESS_KEY,
            aws_access_key_id=config.storage.AWS_ACCESS_KEY_ID,
            endpoint_url=config.storage.AWS_URL,
        )

    async def __aenter__(self):
        session = Session()

        client = session.client(**self._storage_params)
        resource = session.resource(**self._storage_params)
        self.client = await self._exit_stack.enter_async_context(client)
        self.resource = await self._exit_stack.enter_async_context(resource)

        self.bucket = await self.resource.Bucket(self._bucket_name)

        # Проверка и создание бакета, если его нет
        try:
            await self.client.head_bucket(Bucket=self._bucket_name)
        except self.client.exceptions.ClientError:
            await self.client.create_bucket(Bucket=self._bucket_name)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

    async def save(self, file: IO, file_key: str, is_public=False) -> str:
        """Залить файл на бакет"""

        file.seek(0)  # убедимся что курсор стоит на начале файла
        await self.client.upload_fileobj(
            Fileobj=file,
            Bucket=self._bucket_name,
            Key=file_key,
        )
        if is_public:
            object_acl = await self.resource.ObjectAcl(self._bucket_name, file_key)
            await object_acl.put(ACL="public-read")

        return file_key

    async def get(self, key: str) -> IO:
        """Получает файл объект из облака"""
        fh = BytesIO()
        await self.client.download_fileobj(self._bucket_name, key, fh)
        fh.seek(0)
        return fh

    async def delete(self, key: str) -> None:
        """Удаляет файл из облака"""
        await self.client.delete_object(Bucket=self._bucket_name, Key=key)
