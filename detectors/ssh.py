import socket

from .base import ServiceDetector


class SSHDetector(ServiceDetector):

    name = "SSH"

    ports = {
        22
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
                    1024
                ).decode(
                    errors="replace"
                ).strip()

            if banner.startswith("SSH-"):

                return (
                    "SSH",
                    banner
                )

            return (
                "UNKNOWN",
                "TCP connection succeeded but SSH banner was not confirmed"
            )

        except Exception:

            return (
                "UNKNOWN",
                None
            )
