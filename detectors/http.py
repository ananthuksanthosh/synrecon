import socket

from .base import ServiceDetector


class HTTPDetector(ServiceDetector):

    name = "HTTP"

    ports = {
        80,
        8000,
        8008,
        8080,
        8081,
        8888
    }

    def detect(
        self,
        target: str,
        port: int,
        timeout: float = 2.0
    ):

        try:

            request = (
                f"HEAD / HTTP/1.0\r\n"
                f"Host: {target}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            ).encode()

            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.sendall(request)

                response = sock.recv(
                    4096
                ).decode(
                    errors="replace"
                )

            lines = response.splitlines()

            server = None

            for line in lines:

                if line.lower().startswith(
                    "server:"
                ):

                    server = line.strip()

                    break

            if server:

                return (
                    "HTTP",
                    server
                )

            if response.startswith(
                "HTTP/"
            ):

                status = lines[0] if lines else "HTTP response"

                return (
                    "HTTP",
                    status
                )

            return (
                "UNKNOWN",
                "Port responded but HTTP was not confirmed"
            )

        except Exception:

            return (
                "UNKNOWN",
                None
            )
