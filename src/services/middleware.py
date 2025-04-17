import logging
import time
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger(__name__)

ALLOW_ORIGINS = [
    'http://localhost:8000/',
    'http://localhost:3000/',
    "http://localhost:80/",
]

type CallNext = Callable[[Request], Awaitable[Response]]


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, *args, process_time_header_name: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.header_name = process_time_header_name

    async def dispatch(
        self,
        request: Request,
        call_next: CallNext,
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        proces_time = time.perf_counter() - start_time
        response.headers[self.header_name] = f"{proces_time:.5}"
        return response


def register_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_requests(
        request: Request,
        call_next: CallNext
    ) -> Response:
       log.info("Request %s to %s", request.url)
       return await call_next(request)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    app.add_middleware(
        ProcessTimeHeaderMiddleware,
        process_time_header_name="X-Procces-Time"
    )
