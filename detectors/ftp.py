import socket

from .base import ServiceDetector


class FTPDetector(ServiceDetector):

    name = "FTP"

    ports = {
        20,
        21,
        989,
        990
    }

    def detect(
        self,
        target: str,
        port: int,
        timeout: float = 2.0
    ):

        try:

            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.settimeout(timeout)

                banner = sock.recv(
                    4096
                ).decode(
                    errors="replace"
                ).strip()

            if (
                banner.startswith("220")
                or "FTP" in banner.upper()
            ):

                return (
                    "FTP",
                    banner
                )

            return (
                "UNKNOWN",
                "TCP connection succeeded but FTP banner was not confirmed"
            )

        except Exception:

            return (
                "UNKNOWN",
                None
            )
