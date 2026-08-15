#!/usr/bin/env python3

import socket
import struct


class MySQLDetector:

    name = "MySQL"

    ports = {3306}

    def detect(self, target, port, timeout=2.0):

        if port != 3306:
            return None

        try:
            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.settimeout(timeout)

                packet = self._recv_packet(sock)

                if not packet:
                    return None

                # MySQL initial handshake:
                # first payload byte is normally protocol version 0x0a
                if len(packet) < 2:
                    return None

                protocol_version = packet[0]

                if protocol_version != 0x0A:
                    return None

                server_version = self._extract_server_version(packet)

                if server_version:
                    detail = (
                        f"MySQL {server_version}"
                    )
                else:
                    detail = (
                        "MySQL handshake received"
                    )

                return (
                    "MySQL",
                    detail,
                    "MYSQL_GREETING"
                )

        except (
            socket.timeout,
            ConnectionRefusedError,
            OSError
        ):
            return None

    def _recv_packet(self, sock):

        header = self._recv_exact(
            sock,
            4
        )

        if not header:
            return None

        payload_length = (
            header[0]
            | (header[1] << 8)
            | (header[2] << 16)
        )

        if payload_length <= 0:
            return None

        return self._recv_exact(
            sock,
            payload_length
        )

    def _recv_exact(self, sock, size):

        data = bytearray()

        while len(data) < size:

            chunk = sock.recv(
                size - len(data)
            )

            if not chunk:
                return None

            data.extend(chunk)

        return bytes(data)

    def _extract_server_version(self, packet):

        # Protocol version is byte 0.
        # Server version is a null-terminated string
        # immediately following it.

        try:

            end = packet.find(
                b"\x00",
                1
            )

            if end == -1:
                return None

            version = packet[
                1:end
            ].decode(
                "utf-8",
                errors="replace"
            )

            return version.strip()

        except Exception:
            return None
