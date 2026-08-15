import socket
import ssl

from .base import ServiceDetector


class HTTPSDetector(ServiceDetector):

    name = "HTTPS"

    ports = {
        443,
        8443
    }

    def detect(
        self,
        target: str,
        port: int,
        timeout: float = 2.0
    ):

        try:
            context = ssl.create_default_context()

            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as raw_socket:

                with context.wrap_socket(
                    raw_socket,
                    server_hostname=target
                ) as sock:

                    request = (
                        f"HEAD / HTTP/1.0\r\n"
                        f"Host: {target}\r\n"
                        f"Connection: close\r\n"
                        f"\r\n"
                    ).encode()

                    sock.sendall(request)

                    response = sock.recv(
                        4096
                    ).decode(
                        errors="replace"
                    )

            lines = response.splitlines()

            server = None

            for line in lines:

                if line.lower().startswith("server:"):

                    server = line.strip()
                    break

            if server:

                return (
                    "HTTPS",
                    server
                )

            if response.startswith("HTTP/"):

                status = (
                    lines[0]
                    if lines
                    else "HTTPS response"
                )

                return (
                    "HTTPS",
                    status
                )

            return (
                "UNKNOWN",
                "TLS succeeded but HTTP was not confirmed"
            )

        except ssl.SSLError as error:

            return (
                "UNKNOWN",
                f"TLS error: {error}"
            )

        except Exception:

            return (
                "UNKNOWN",
                None
            )
