import logging
import os
import signal

from bottle import run

from webdriver_wharf import app, logging_init

logger = logging.getLogger(__name__)

loglevel = getattr(logging, os.environ.get('WEBDRIVER_WHARF_LOG_LEVEL', 'info').upper(), 'INFO')
listen_host = os.environ.get('WEBDRIVER_WHARF_LISTEN_HOST', '0.0.0.0')
listen_port = int(os.environ.get('WEBDRIVER_WHARF_LISTEN_PORT', 4899))


def handle_hup(signum, stackframe):
    app.pull_latest_image.trigger()

signal.signal(signal.SIGHUP, handle_hup)


def main():
    logging_init(loglevel)
    run(app.application, server=app.WharfServer, host=listen_host, port=listen_port, quiet=True)