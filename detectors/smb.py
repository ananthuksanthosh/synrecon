#!/usr/bin/env python3

import socket

from .base import ServiceDetector


class SMBDetector(ServiceDetector):

    name = "SMB"

    ports = {139, 445}

    def detect(self, target, port, timeout=2.0):

        if port not in self.ports:
            return None

        try:
            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.settimeout(timeout)

                # SMB1 negotiate request
                smb_negotiate = bytes.fromhex(
                    "00000085ff534d42720000000000000000000000000000000000000000000000"
                    "0000000000000000000000000000000000000000000000000000000000000000"
                    "0000000000000000000000000000000000000000000000000000000000000000"
                    "0000000000000000000000000000000000000000000000000000000000000000"
                    "0000000000000000000000000000000000000000000000000000000000000000"
                )

                sock.sendall(smb_negotiate)

                response = sock.recv(1024)

                if response.startswith(b"\x00") and b"\xffSMB" in response:
                    return (
                        "SMB",
                        "SMB negotiation response received",
                        "SMB_NEGOTIATION"
                    )

                if b"\xfeSMB" in response or b"\xffSMB" in response:
                    return (
                        "SMB",
                        "SMB protocol response received",
                        "SMB_RESPONSE"
                    )

                return (
                    "SMB",
                    "SMB port responded; protocol negotiation inconclusive",
                    "SMB_PORT_RESPONSE"
                )

        except (
            socket.timeout,
            ConnectionRefusedError,
            OSError
        ):
            return None
