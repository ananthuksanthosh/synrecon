#!/usr/bin/env python3

import socket
import struct


class PostgreSQLDetector:

    name = "PostgreSQL"

    ports = {5432}

    def detect(self, target, port, timeout=2.0):

        if port != 5432:
            return None

        try:
            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.settimeout(timeout)

                # PostgreSQL SSLRequest.
                # This is a harmless protocol capability check.
                packet = struct.pack(
                    "!II",
                    8,
                    80877103
                )

                sock.sendall(packet)

                response = sock.recv(1)

                if response == b"S":
                    return (
                        "PostgreSQL",
                        "PostgreSQL service supports SSL negotiation",
                        "POSTGRES_SSL_RESPONSE"
                    )

                if response == b"N":
                    return (
                        "PostgreSQL",
                        "PostgreSQL service detected; SSL not supported",
                        "POSTGRES_SSL_RESPONSE"
                    )

                # Some PostgreSQL configurations may not respond
                # to the SSL request in the expected way.
                if response:
                    return (
                        "PostgreSQL",
                        "PostgreSQL protocol response received",
                        "POSTGRES_RESPONSE"
                    )

                return None

        except (
            socket.timeout,
            ConnectionRefusedError,
            OSError
        ):
            return None
