from http.server import SimpleHTTPRequestHandler
import socket
import socketserver
from threading import Thread
from select import select
from time import sleep
import sys


def print_help():
    print('INFORMATION:')
    print('This programme block access to chosen site.')
    print('Made by Roman Yaschenko MO-202')
    print('How to run: in cmd or bash type "python proxy.py [site]"')
    print('Set up proxy in os settings.')
    print('Run example: python proxy.py site.com')


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.socket_idle = 0
        super().__init__(request, client_address, server)

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            path_parts = self.path.split(':')
            host, port = path_parts[0], int(path_parts[-1])
            try:
                if check(host):
                    self.send_error(423)
                    return
                sock.connect((host, port))
                self.send_response(200)
                self.send_header('Proxy-agent', 'Simple HTTP proxy')
                self.end_headers()
                self.send(sock)
            except socket.error:
                self.send_error(404)
            except ConnectionError:
                pass
            finally:
                self.connection.close()

    def send(self, sock):
        socks = [self.connection, sock]
        while True:
            input_ready, output_ready, exception_ready = select(socks, [], socks, 0.1)
            if exception_ready:
                return
            if input_ready:
                for item in input_ready:
                    data = item.recv(8192)
                    if data:
                        current_sock = self.connection if item is sock else sock
                        current_sock.send(data)
                    elif self._socket_max_idle:
                        return
            elif self._socket_max_idle:
                return


@property
def _socket_max_idle(self):
    if self.socket_idle < 10:
        sleep(1)
        self.socket_idle += 1
        return False
    else:
        return True


def check(host):
    if blocked in host:
        return True
    return False


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def main():
    if len(sys.argv) != 2:
        print_help()
        return

    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print_help()
        return

    global blocked
    blocked = sys.argv[1]
    print(blocked + ' is blocked!')
    server = ThreadedTCPServer(('127.0.0.1', 8080), Handler)
    thread = Thread(target=server.serve_forever)
    thread.start()


if __name__ == '__main__':
    main()