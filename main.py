import os
import logging
import uvicorn
import asyncio
from dotenv import load_dotenv
load_dotenv()

from oscm.utils import GracefulShutdown

debug = os.environ.get('APP_DEBUG', '') == "true"

if debug:
    import coloredlogs
    coloredlogs.install(level='DEBUG')

loop = asyncio.get_event_loop()

log = logging.getLogger()

async def shutdown():
    from oscm.routes import vpn
    await vpn.stop()


if __name__ == '__main__':

    log.info("Starting up..")

    try:
        with GracefulShutdown(before_shutdown=shutdown):
            loop = asyncio.get_event_loop()
            uvicorn.run("oscm:app", host='0.0.0.0', port=8080, debug=debug, reload=debug, timeout_keep_alive=120,
                        access_log=False)

    except Exception as e:
        log.exception(e)
        exit(e)

