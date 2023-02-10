from json import dumps as json_dumps
from fastapi import Response


from constants import CONTENT_TYPE
from content_types import TEXT_JSON_CONTENT_TYPE, TEXT_PLAIN_CONTENT_TYPE
from status_codes import OK_STATUS_CODE


def json_response(json, status_code = OK_STATUS_CODE):
    headers = {CONTENT_TYPE: TEXT_JSON_CONTENT_TYPE}

    content = json_dumps(json)

    response = Response(status_code=status_code, headers=headers, content=content)

    return response


def plain_response(text, status_code = OK_STATUS_CODE):
    headers = {CONTENT_TYPE: TEXT_PLAIN_CONTENT_TYPE}

    content = text

    response = Response(status_code=status_code, headers=headers, content=content)

    return response
