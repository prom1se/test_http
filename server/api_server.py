import asyncio
import logging as log
from os import environ
from aiohttp import web

from modules.files_worker import FilesWorker
from modules.db import DataBase

log.basicConfig(level=log.INFO, format='[%(asctime)s][%(levelname)s] %(message)s')

# read from environment variables to simplify the creation of a docker container
PORT = int(environ['PORT'])


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = web.Application()
    db = DataBase()
    filesWorker = FilesWorker(database=db)
    app.add_routes([
        web.post('/api/upload', filesWorker.upload),
        web.delete('/api/delete', filesWorker.delete),
        web.get('/api/download', filesWorker.download)
    ])
    web.run_app(app, port=PORT)
