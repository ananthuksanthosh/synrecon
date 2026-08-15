#!/usr/bin/env python3

import socket


class TelnetDetector:

    name = "TELNET"

    ports = {23}

    def detect(self, target, port, timeout=2.0):

        if port != 23:
            return None

        try:
            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.settimeout(timeout)

                data = sock.recv(256)

                if not data:
                    return None

                is_negotiation = (
                    b"\xff" in data
                    or b"\xfb" in data
                    or b"\xfd" in data
                    or b"\xfc" in data
                    or b"\xfe" in data
                )

                text = data.decode(
                    "ascii",
                    errors="ignore"
                ).strip()

                if is_negotiation:

                    return (
                        "Telnet",
                        "Telnet negotiation detected",
                        "TELNET_NEGOTIATION"
                    )

                if "telnet" in text.lower():

                    return (
                        "Telnet",
                        "Telnet banner detected",
                        "TELNET_RESPONSE"
                    )

                return (
                    "Telnet",
                    "Telnet connection established",
                    "TELNET_RESPONSE"
                )

        except (
            socket.timeout,
            ConnectionRefusedError,
            OSError
        ):
            return None
