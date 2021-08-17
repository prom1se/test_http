import uuid
from hashlib import sha256
from pathlib import Path
from os import makedirs, remove
from aiohttp.streams import StreamReader
from uuid import uuid4

from modules.db import DataBase
from modules.authentification import  authenticate_user


class FilesWorker:
    def __init__(self, database: DataBase):
        self.db = database
        self.store_folder = Path('../store')
        self.folder_name_length = 2

    async def _get_hash_save_tmp(self, data: StreamReader) -> (Path, str):
        tmp_file = Path(self.store_folder.joinpath(f'tmp_{uuid4()}'))
        makedirs(tmp_file.parent, exist_ok=True)
        file_hash = sha256()
        with tmp_file.open('ab') as w_file:
            async for chunk in data.iter_chunked(2048):
                file_hash.update(chunk)
                w_file.write(chunk)
        return tmp_file, file_hash.hexdigest()

    @authenticate_user()
    async def upload(self, user: str, content: StreamReader):
        tmp_file, file_hash = await self._get_hash_save_tmp(content)
        file = self.store_folder.joinpath(file_hash[:self.folder_name_length], file_hash)
        makedirs(file.parent, exist_ok=True)
        tmp_file.replace(file)
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
