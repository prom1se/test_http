"""
The stub class for working with the database.
Based on it, you can implement real work with a database or a file as a database.
"""


class DataBase:
    my_db = {
        'known_users': ['dGVzdF91c2VyOnRlc3RfcHdk'],
        'user_files': {}
    }

    async def check_user_info(self, info: str) -> bool:
        return info in self.my_db['known_users']

    async def is_file_exists(self, user: str,  file_hash: str) -> bool:
        return file_hash in self.my_db['user_files'][user]

    async def add_user_file(self, username: str, file_hash: str):
        if user_files := self.my_db['user_files'].get(username):
            user_files.append(file_hash)
        else:
            self.my_db['user_files'][username] = [file_hash]
