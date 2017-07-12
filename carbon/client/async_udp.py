import asyncio
import socket
import logging
from .udp import UDPClient as BaseUDPClient


log = logging.getLogger(__name__)


def create_future(loop):
    if hasattr(loop, 'create_future'):
        return loop.create_future()
    else:
        return asyncio.Future(loop=loop)


class AsyncUDPSocket:

    __slots__ = '__loop', '__sock', '__address', '__futures', '__closed'

    def __init__(self, loop=None):
        self.__loop = asyncio.get_event_loop() if loop is None else loop
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.setblocking(False)

        self.__futures = list()
        self.__closed = False
        self.__loop.add_writer(self.__sock.fileno(), self.__sender)

    def sendto(self, data, host, port):
        data = data if isinstance(data, bytes) else str(data).encode('utf-8')
        future = create_future(self.__loop)

        destination = (data, host, port)
        self.__futures.append((destination, future))

        return future

    def __sender(self):
        if not self.__futures:
            return

        destination, future = self.__futures[0]
        data, host, port = destination

        try:
            self.__sock.sendto(data, (host, port))
        except (BlockingIOError, InterruptedError):
            return
        except Exception as exc:
            self.__abort(exc)
        else:
            self.__futures.pop(0)
            future.set_result(True)

    def __abort(self, exc):
        for future in (f for _, f in self.__futures if not f.done()):
            future.set_exception(exc)

        self.close()

    @property
    def is_closed(self):
        return self.__closed

    def close(self):
        if self.__closed:
            raise RuntimeError("Socket already closed")

        self.__closed = True
        self.__loop.remove_writer(self.__sock.fileno())
        self.__sock.close()

        for future in (f for _, f in self.__futures if not f.done()):
            future.set_exception(ConnectionError("Connection closed"))


class UDPClient(BaseUDPClient):
    def __init__(self, hosts='127.0.0.1', ns='carbon.client', loop=None):
        super().__init__(hosts=hosts, ns=ns)

        self.__loop = loop or asyncio.get_event_loop()
        self.__socket = AsyncUDPSocket(loop=self.__loop)

    @property
    def socket(self):
        return self.__socket

    def _sender(self, packet, host, port):
        self.__loop.create_task(self.socket.sendto(packet, host, port))
