#!/usr/bin/env python3

import socket

from .base import ServiceDetector


class TomcatDetector(ServiceDetector):

    name = "Tomcat"

    ports = {8180, 8009}

    def detect(self, target, port, timeout=2.0):

        if port not in self.ports:
            return None

        try:
            with socket.create_connection(
                (target, port),
                timeout=timeout
            ) as sock:

                sock.settimeout(timeout)

                if port == 8180:
                    request = (
                        b"GET / HTTP/1.1\r\n"
                        b"Host: " + target.encode() + b"\r\n"
                        b"Connection: close\r\n\r\n"
                    )

                    sock.sendall(request)

                    response = sock.recv(4096)

                    text = response.decode(
                        "ascii",
                        errors="replace"
                    )

                    lower = text.lower()

                    if (
                        "tomcat" in lower
                        or "apache-coyote" in lower
                        or "catalina" in lower
                    ):
                        return (
                            "Tomcat",
                            "Apache Tomcat HTTP response detected",
                            "TOMCAT_HTTP"
                        )

                    return (
                        "HTTP",
                        "HTTP response received; Tomcat not confirmed",
                        "HTTP_RESPONSE"
                    )

                return (
                    "Tomcat",
                    "Tomcat AJP port responded",
                    "TOMCAT_AJP"
                )

        except (
            socket.timeout,
            ConnectionRefusedError,
            OSError
        ):
            return None
