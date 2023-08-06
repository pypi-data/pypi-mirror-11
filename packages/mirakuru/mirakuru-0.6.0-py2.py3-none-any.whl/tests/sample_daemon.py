"""
Daemon sample application for tests purposes.

Stopping this process is possible only by the SIGKILL signal.

Usage:

    python tests/sample_daemon.py

"""

import time

import daemon

from tests.signals import block_signals


with daemon.DaemonContext():
    block_signals()
    while True:
        print('Sleeping mirakuru daemon...')
        time.sleep(1)
