import ssl

import socketpool


class SSLServerSocketPool:
    def __init__(self, pool: socketpool.SocketPool, ssl_context: ssl.SSLContext):
        self._pool = pool
        self._ssl_context = ssl_context

    @property
    def AF_INET(self) -> int:
        return self._pool.AF_INET

    @property
    def AF_INET6(self) -> int:
        return self._pool.AF_INET6

    @property
    def SOCK_STREAM(self) -> int:
        return self._pool.SOCK_STREAM

    @property
    def SOCK_DGRAM(self) -> int:
        return self._pool.SOCK_DGRAM

    @property
    def SOCK_RAW(self) -> int:
        return self._pool.SOCK_RAW

    @property
    def EAI_NONAME(self) -> int:
        return self._pool.EAI_NONAME

    @property
    def TCP_NODELAY(self) -> int:
        return self._pool.TCP_NODELAY

    @property
    def IPPROTO_TCP(self) -> int:
        return self._pool.IPPROTO_TCP

    def socket(self, family: int = None, type: int = None) -> ssl.SSLSocket:
        socket = self._pool.socket(family, type)
        return self._ssl_context.wrap_socket(socket, server_side=True)

    def getaddrinfo(self, *args, **kwargs):
        return self._pool.getaddrinfo(*args, **kwargs)
