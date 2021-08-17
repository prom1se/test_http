from hashlib import sha256
from pathlib import Path
from os import makedirs, remove

from modules.db import DataBase
from modules.authentification import  authenticate_user


class FilesWorker:
    def __init__(self, database: DataBase):
        self.db = database
        self.store_folder = Path('../store')
        self.folder_name_length = 2

    @staticmethod
    async def _get_hash(data: bytes) -> str:
        return sha256(data).hexdigest()

    @authenticate_user()
    async def upload(self, user: str, content: bytes):
        file_hash = await self._get_hash(content)
        file = self.store_folder.joinpath(file_hash[:self.folder_name_length], file_hash)
        if not file.parent.exists():
            makedirs(file.parent)
        file.write_bytes(content)
        await self.db.add_user_file(user, file_hash)
        return True, file_hash

    @authenticate_user()
    async def delete(self, user: str, file_hash: str):
        if await self.db.is_file_exists(user, file_hash):
            remove(self.store_folder.joinpath(file_hash[:self.folder_name_length], file_hash))
            return True, None
        else:
            return False, 'File not found'

    @authenticate_user()
    async def download(self, user: str, file_hash: str):
        if await self.db.is_file_exists(user, file_hash):
            return True, self.store_folder.joinpath(file_hash[:self.folder_name_length], file_hash).read_bytes()
        else:
            return False, 'File not found'
