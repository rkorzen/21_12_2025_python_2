from __future__ import annotations

import time
from contextlib import contextmanager
from decimal import Decimal

from django.conf import settings
from django.db import connection, reset_queries


@contextmanager
def query_debugger():
    if settings.DEBUG:
        reset_queries()
        start_queries = len(connection.queries)
    else:
        start_queries = 0

    started_at = time.perf_counter()
    payload: dict[str, int | float] = {}
    try:
        yield payload
    finally:
        payload["elapsed_ms"] = round((time.perf_counter() - started_at) * 1000, 2)
        payload["query_count"] = len(connection.queries) - start_queries if settings.DEBUG else -1


def to_plain_value(value):
    if isinstance(value, Decimal):
        return float(value)
    return value
