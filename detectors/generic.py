import socket

from .base import ServiceDetector


class GenericTCPDetector(ServiceDetector):

    name = "TCP"

    ports = set()

    def supports(self, port: int) -> bool:
        """
        Generic detector is the fallback for any TCP port.
        """
        return True

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

                try:
                    banner = sock.recv(1024)
                except socket.timeout:
                    banner = b""

            if banner:

                text = banner.decode(
                    errors="replace"
                ).strip()

                return (
                    "TCP",
                    f"Banner: {text[:200]}"
                )

            return (
                "TCP",
                "TCP connection established; no banner received"
            )

        except Exception as error:

            return (
                "UNKNOWN",
                f"Generic TCP detection failed: {error}"
            )
