from traceback import format_exc
import logging as log
from base64 import b64decode
from aiohttp.web_request import Request
from aiohttp.web_response import Response


class RequestDataException(Exception):
    pass


def _get_user_from_data(data: str) -> str:
    return b64decode(data).decode().split(':')[0]


async def get_data_for_func(user: str, request: Request) -> dict:
    if request.method == 'POST':
        if request.body_exists:
            return {'user': user, 'content': request.content}
        else:
            raise RequestDataException('An empty body is not allowed for this request.')
    elif request.rel_url.query_string == '':
        raise RequestDataException('An empty parameter is not allowed.')
    elif request.method == 'GET':
        return {'user': user, 'file_hash': request.rel_url.query_string}
    elif request.method == 'DELETE':
        return {'user': user, 'file_hash': request.rel_url.query_string}


def authenticate_user():
    def wrap(func):
        async def authenticate(cls, request: Request) -> Response:
            try:
                auth_type, auth_data = request.headers['Authorization'].split(' ')
                if auth_type.lower() != 'basic':
                    Response(reason='The authorization type is not supported.', status=401)
                if not await cls.db.check_user_info(auth_data):
                    return Response(reason='User not found', status=401)
            except KeyError:
                return Response(reason='Available only to authorized users.', status=401)
            try:
                data = await get_data_for_func(_get_user_from_data(auth_data), request)
                try:
                    status, result = await func(cls, **data)
                    if not status:
                        return Response(status=400, reason=result)
                    else:
                        return Response(status=200, body=result)
                except Exception as e:
                    log.error(format_exc())
                    return Response(status=500, reason=str(e))
            except RequestDataException as ex:
                return Response(status=400, reason=str(ex))
        return authenticate
    return wrap
