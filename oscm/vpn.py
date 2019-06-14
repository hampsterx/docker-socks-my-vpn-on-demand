import os
import re
import asyncio
import logging
from asyncio.subprocess import PIPE

OVNP_CONFIG_PATH = os.environ['OVNP_CONFIG_PATH']

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class VPN:
    OPTIONS = {
        "status-version": "3",
        #  "management": ["127.0.0.1", "9500"],
        #  "management-up-down": None,
        "verb": "3",
        "ping": "15",
        "ping-exit": "90",
        "ping-restart": "30",
        "machine-readable-output": None,
        "inactive": "300",
        "config": OVNP_CONFIG_PATH

    }

    def __init__(self):

        self.process = None
        self.watcher_task = None
        self.is_active = False

    @classmethod
    def format_options(cls):
        args = []
        for k, v in cls.OPTIONS.items():
            args.append("--{}".format(k))
            if v:
                if isinstance(v, list):
                    args += v
                else:
                    args.append(v)
        return args

    @classmethod
    def log(cls, line):
        # Eg "1560475213.659239 22000003 OPTIONS IMPORT: timers and/or timeouts modified"
        match = re.findall("^(\d+\.\d+) (\d+) (.*?)$", line)

        if not match:
            return

        ts = match[0][0]
        level = int(match[0][1])
        msg = match[0][2]

        log_level = "debug"
        if level == 1:
            log_level = "info"
        elif level == [2, 3]:
            log_level = "warn"
        elif level in [110]:
            log_level = "error"
            msg = msg.strip("ERROR: ")

        getattr(log, log_level)(msg)

        return msg

    async def watcher(self):
        try:
            while True:

                line = await self.process.stdout.readline()

                if line:
                    line = self.log(line.decode('utf-8').strip("\n"))

                    if line == "Initialization Sequence Completed":
                        self.is_active = True

                else:
                    self.is_active = False
                    log.info("Stopped with exit {}".format(self.process.returncode))
                    self.process = None
                    break

        except Exception as e:
            log.exception(e)

    async def start(self):

        if self.process:
            if self.process.returncode is None:
                log.info("Already Started..")
                # todo: ensure OK/Ping it
                return True

            log.debug("Process has {} return code".format(self.process.returncode))
            return False

        log.info("Starting OpenVPN")

        cmd = ["openvpn"] + self.format_options()

        self.process = await asyncio.create_subprocess_shell(" ".join(cmd), stderr=PIPE, stdout=PIPE)

        self.watcher_task = asyncio.create_task(self.watcher())

        for i in range(0, 30):
            if self.is_active:
                return True
            await asyncio.sleep(1)

        return False

    async def stop(self):
        # todo send Sigterm or use management service to halt it cleanly
        pass
