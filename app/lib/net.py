import asyncio
import json
import socket
from http import client
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class ReturnData:
    error: bool = False
    reson: str = ''
    data: Any = None


async def a_request(url: str) -> client.HTTPResponse:
    loop = asyncio.get_event_loop()
    res: client.HTTPResponse = await loop.run_in_executor(
        None,
        urllib.request.urlopen, url
    )
    return res


def request(url: str) -> ReturnData:
    return_data = ReturnData()
    res: Optional[client.HTTPResponse] = None
    try:
        res = urllib.request.urlopen(url, timeout=10)
    except urllib.error.URLError as uerror:
        return_data.error = True
        if isinstance(uerror.reason, socket.timeout):
            return_data.reson = 'time out error'
        else:
            return_data.reson = 'bad request error'
        res = None
    if res is None or return_data.error:
        return return_data
    with res:
        if res.status != 200:
            return_data.error = True
            return_data.reson = res.reason
        else:
            return_data.data = json.loads(res.read())
    return return_data
