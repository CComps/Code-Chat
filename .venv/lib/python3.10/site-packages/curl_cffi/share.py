import asyncio as aio
import threading
from typing import Any
from .const import CurlShareOpt, CurlLockData
from ._wrapper import ffi, lib  # type: ignore


@ffi.def_extern()
def lock_cb(curl, curl_lock_data: int, access, clientp: Any):
    share_handle = ffi.from_handle(clientp)
    share_handle._locks[curl_lock_data].lock()


@ffi.def_extern()
def unlock_cb(curl, curl_lock_data: int, access, clientp: Any):
    share_handle = ffi.from_handle(clientp)
    share_handle._locks[curl_lock_data].unlock()


class CurlShare:
    def __init__(self, asyncio: bool = False):
        self._share = lib.curl_share_init()
        if asyncio:
            Lock = aio.Lock
        else:
            Lock = threading.Lock
        self._locks = {
            CurlLockData.COOKIE: Lock(),
            CurlLockData.DNS: Lock(),
            CurlLockData.SSL_SESSION: Lock(),
            CurlLockData.CONNECT: Lock(),
            CurlLockData.PSL: Lock(),
        }

    def setopt(self, option: CurlShareOpt, value: int):
        lib.curl_share_setopt(option, value)
