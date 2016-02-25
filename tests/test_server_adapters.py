import os
import signal
import socket
import sys
import time
from subprocess import Popen, PIPE
from unittest import TestCase
from urllib.request import urlopen
from contextlib import closing

server_script = os.path.join(os.path.dirname(__file__), 'dummy_server.py')


def ping(host, port):
    """ Check if a server accepts connections on a specific TCP port. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
        try:
            sock.connect((host, port))
            return True
        except socket.error:
            return False


def warn(msg):
    sys.stderr.write('WARNING: %s\n' % msg.strip())


class ServerTests(TestCase):
    host = '127.0.0.1'
    server = 'wsgiref'
    port = 8001

    def setUp(self):
        cmd = [sys.executable, server_script, self.server, str(self.port)]
        cmd += sys.argv[1:]

        self.p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        for i in range(100):
            time.sleep(0.1)
            if ping(self.host, self.port):
                return
            if not self.p.poll() is None:
                break

        rv = self.p.poll()
        if rv is None:
            raise AssertionError("Server took too long to start up.")
        if rv is 128:  # import error
            raise ImportError("{} cannot import.".format(self.server))
        if rv is 3:
            raise AssertionError("{} port is already in use.".format(self.port))
        raise AssertionError("Skipping exited with error code {}".format(rv))

    def tearDown(self):
        if self.p.poll() is None:
            os.kill(self.p.pid, signal.SIGINT)
            time.sleep(0.5)
        while self.p.poll is None:
            os.kill(self.p.pid, signal.SIGTERM)
            time.sleep(1)

        for stream in (self.p.stdout, self.p.stderr):
            for line in stream:
                if 'warning'.encode('utf-8') in line.lower():
                    warn(line.strip().decode('utf-8'))
                elif 'error'.encode('utf-8') in line.lower():
                    raise AssertionError(line.strip().decode('utf-8'))

    def fetch(self, url):
        return urlopen('http://{host}:{port}/{url}'.format(host=self.host, port=self.port, url=url)).read()

    def test_simple(self):
        """ Test a simple static page with this server adapter. """
        self.assertEqual('OK'.encode('utf-8'), self.fetch('test'))


class GunicornServerTests(ServerTests):
    server = 'gunicorn'
