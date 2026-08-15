#!/usr/bin/env python3

import socket
import ssl


class SMTPDetector:

    name = "SMTP"

    ports = {25, 465, 587}

    def detect(self, target, port, timeout=2.0):

        if port not in self.ports:
            return None

        if port == 465:
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

        try:

            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.settimeout(timeout)

                response = sock.recv(512)

                if not response:
                    return None

                text = response.decode(
                    "utf-8",
                    errors="replace"
                ).strip()

                if (
                    text.startswith("220")
                    or "ESMTP" in text.upper()
                    or "SMTP" in text.upper()
                ):

                    return (
                        "SMTP",
                        f"SMTP greeting: {text}",
                        "SMTP_GREETING"
                    )

                return (
                    "SMTP",
                    f"Response received: {text}",
                    "SMTP_RESPONSE"
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
                ) as tls_socket:

                    tls_socket.settimeout(timeout)

                    response = tls_socket.recv(512)

                    if not response:
                        return (
                            "SMTPS",
                            "TLS connection established; no SMTP greeting",
                            "TLS"
                        )

                    text = response.decode(
                        "utf-8",
                        errors="replace"
                    ).strip()

                    if (
                        text.startswith("220")
                        or "ESMTP" in text.upper()
                        or "SMTP" in text.upper()
                    ):

                        return (
                            "SMTPS",
                            f"SMTP over TLS greeting: {text}",
                            "SMTP_TLS_GREETING"
                        )

                    return (
                        "SMTPS",
                        "TLS connection established; SMTP response received",
                        "TLS_SMTP"
                    )

        except (
            socket.timeout,
            ConnectionRefusedError,
            OSError,
            ssl.SSLError
        ):

            return None
