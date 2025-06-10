import logging
import time
from contextlib import contextmanager
from logging import Logger
from typing import Generator, Optional

import humanize


@contextmanager
def benchmark(
    operation_name: Optional[str] = None, log: Optional[Logger] = None
) -> Generator[None, None, None]:
    """
    Function to benchmark a function
    """
    start: float = time.perf_counter()
    try:
        yield
    finally:
        elapsed: float = time.perf_counter() - start

        if not log:
            log = logging.getLogger(__name__)

        # Use humanize to format the time in a readable way
        # For very small times (< 1 second), show milliseconds
        if elapsed < 1:
            # Convert to milliseconds and format
            elapsed_ms = elapsed * 1000
            human_time = f"{humanize.intcomma(round(elapsed_ms))} ms"
        else:
            # For longer times, use precisedelta for a more readable format
            human_time = humanize.precisedelta(
                elapsed, minimum_unit="milliseconds", suppress=["microseconds"]
            )

        if operation_name:
            log.debug(f"* {operation_name} executed in {human_time}.")
        else:
            log.debug(f"* executed in {human_time}.")
