import threading
import time
import logging
import signal
import asyncio
import os

from functools import partial

log = logging.getLogger(__name__)


def shutdown(wait_seconds, before_shutdown, _signo, _stack_frame):
    log.warning("shutdown signal received. waiting..")

    if before_shutdown:
        log.debug("Calling before_shutdown function..")
        before_shutdown()

    thread = threading.Thread(target=lambda: time.sleep(wait_seconds))
    thread.start()
    thread.join()

    # Send signal for framework to do it's thing~
    os.kill(os.getpid(), signal.SIGINT)


class GracefulShutdown:

    def __init__(self, before_shutdown=None, wait_seconds=5):
        self._before_shutdown = before_shutdown
        self._wait_seconds = wait_seconds

    def __enter__(self):
        if os.environ.get('docker'):
            signal.signal(signal.SIGHUP, partial(shutdown, self._wait_seconds, self._before_shutdown))

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_val:
            log.exception(exc_val)
