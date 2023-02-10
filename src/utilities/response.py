from json import dumps as json_dumps
from fastapi import Response


from constants import CONTENT_TYPE
from content_types import TEXT_JSON_CONTENT_TYPE, TEXT_PLAIN_CONTENT_TYPE


def plain_response(text):
    headers = {CONTENT_TYPE: TEXT_PLAIN_CONTENT_TYPE}

    content = text

    response = Response(content=content, headers=headers)

    return response


def json_response(json):
    headers = {CONTENT_TYPE: TEXT_JSON_CONTENT_TYPE}

    content = json_dumps(json)

    response = Response(content=content, headers=headers)

    return response
