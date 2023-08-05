'''
Entry point. Init logging, initialize component factory,
start asyncio event loop, manage components lifecycle
'''

from .worker import BFG
from .config import ComponentFactory
import time
import numpy as np
import asyncio
import logging
import sys


LOG = logging.getLogger(__name__)


def init_logging(debug=False, filename='bfg.log'):
    ''' Configure logging: verbose or not '''
    default_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s", "%H:%M:%S")
    dbg_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    dbg_handler = logging.FileHandler(filename)
    dbg_handler.setLevel(debug)
    dbg_handler.setFormatter(dbg_formatter)

    cmd_handler = logging.StreamHandler(sys.stdout)
    cmd_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    cmd_handler.setFormatter(dbg_formatter if debug else default_formatter)

    warn_handler = logging.StreamHandler(sys.stdout)
    warn_handler.setLevel(logging.WARN)
    warn_handler.setFormatter(dbg_formatter)

    logger = logging.getLogger("hyper")
    logger.setLevel(logging.WARNING)

    logger = logging.getLogger("")  # configure root logger
    logger.setLevel(logging.DEBUG)
    logger.addHandler(cmd_handler)
    logger.addHandler(dbg_handler)
    logging.getLogger().addHandler(dbg_handler)


def main():
    ''' Run event loop '''
    init_logging()
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main_coro(event_loop))
    event_loop.close()


@asyncio.coroutine
def main_coro(event_loop):
    ''' Main coroutine. Manage components' lifecycle '''

    # Configure factories using config files
    LOG.info("Configuring component factory")
    cf = ComponentFactory("tmp/load.toml", event_loop)

    # Create workers using 'bfg' section from config
    LOG.info("Creating workers")
    workers = [
        cf.get_factory('bfg', bfg_name)
        for bfg_name in cf.get_config('bfg')]

    # Start workers and wait for them asyncronously
    LOG.info("Starting workers")
    [worker.start() for worker in workers]
    LOG.info("Waiting for workers")
    while any(worker.running() for worker in workers):
        yield from asyncio.sleep(1)
    LOG.info("All workers finished")

    # Stop aggregator
    rs = cf.get_factory('aggregator', 'lunapark')
    yield from rs.stop()


if __name__ == '__main__':
    main()
