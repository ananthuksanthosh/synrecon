#!/usr/bin/env python3

import socket


class VNCDetector:

    name = "VNC"

    ports = {
        5900,
        5901,
        5902,
        5903,
        5904,
        5905,
        5906,
        5907,
        5908,
        5909,
    }

    def detect(self, target, port, timeout=2.0):

        if port not in self.ports:
            return None

        try:
            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.settimeout(timeout)

                banner = sock.recv(64)

                if not banner:
                    return None

                text = banner.decode(
                    "ascii",
                    errors="replace"
                ).strip()

                if text.startswith("RFB "):

                    version = text[4:].strip()

                    return (
                        "VNC",
                        f"RFB protocol version {version}",
                        "RFB_GREETING"
                    )

                return None

        except (
            socket.timeout,
            ConnectionRefusedError,
            OSError
        ):
            return None
