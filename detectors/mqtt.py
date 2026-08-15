#!/usr/bin/env python3

import socket
import ssl


class MQTTDetector:

    name = "MQTT"

    ports = {1883, 8883}

    def detect(self, target, port, timeout=2.0):

        if port not in self.ports:
            return None

        if port == 8883:
            return self._detect_tls(
                target,
                port,
                timeout
            )

        return self._detect_plain(
            target,
            port,
            timeout
        )

    def _detect_plain(
        self,
        target,
        port,
        timeout
    ):

        # MQTT 3.1.1 CONNECT
        packet = bytes([
            0x10,
            0x0C,
            0x00, 0x04,
            0x4D, 0x51, 0x54, 0x54,
            0x04,
            0x02,
            0x00, 0x3C,
            0x00, 0x00
        ])

        try:

            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.sendall(packet)

                response = sock.recv(128)

                if not response:
                    return (
                        "MQTT",
                        "MQTT endpoint responded without payload",
                        "TCP"
                    )

                # MQTT CONNACK packet
                if response[0] == 0x20:

                    return (
                        "MQTT",
                        "MQTT CONNACK received; MQTT 3.1.1 accepted",
                        "CONNACK"
                    )

                return (
                    "MQTT",
                    "MQTT endpoint responded",
                    "MQTT_RESPONSE"
                )

        except (
            socket.timeout,
            ConnectionRefusedError,
            OSError
        ):

            return None

    def _detect_tls(
        self,
        target,
        port,
        timeout
    ):

        context = ssl.create_default_context()

        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        try:

            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as raw_socket:

                with context.wrap_socket(
                    raw_socket,
                    server_hostname=target
                ):

                    return (
                        "MQTT-TLS",
                        "TLS connection established on MQTT port",
                        "TLS"
                    )

        except (
            socket.timeout,
            OSError,
            ssl.SSLError
        ):

            return None
