#!/usr/bin/env python3

import socket
import struct


class DNSDetector:

    name = "DNS"

    ports = {53}

    def detect(self, target, port, timeout=2.0):

        if port != 53:
            return None

        return self._detect_dns(
            target,
            port,
            timeout
        )

    def _detect_dns(
        self,
        target,
        port,
        timeout
    ):

        # DNS transaction ID
        transaction_id = 0x5343

        # Standard recursive A-record query
        flags = 0x0100

        question_count = 1
        answer_count = 0
        authority_count = 0
        additional_count = 0

        header = struct.pack(
            "!HHHHHH",
            transaction_id,
            flags,
            question_count,
            answer_count,
            authority_count,
            additional_count
        )

        # Query: example.com
        query_name = b"\x07example\x03com\x00"

        # QTYPE = A
        # QCLASS = IN
        question = query_name + struct.pack(
            "!HH",
            1,
            1
        )

        packet = header + question

        try:

            with socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
            ) as sock:

                sock.settimeout(timeout)

                sock.sendto(
                    packet,
                    (target, port)
                )

                response, address = sock.recvfrom(4096)

                if len(response) < 12:
                    return None

                rx_transaction_id = struct.unpack(
                    "!H",
                    response[:2]
                )[0]

                if rx_transaction_id != transaction_id:
                    return None

                rx_flags = struct.unpack(
                    "!H",
                    response[2:4]
                )[0]

                # QR bit = response
                is_response = bool(
                    rx_flags & 0x8000
                )

                if not is_response:
                    return None

                response_code = rx_flags & 0x000F

                answer_count = struct.unpack(
                    "!H",
                    response[6:8]
                )[0]

                if response_code == 0:

                    return (
                        "DNS",
                        (
                            f"DNS response received; "
                            f"answers={answer_count}"
                        ),
                        "DNS_RESPONSE"
                    )

                return (
                    "DNS",
                    (
                        f"DNS response received; "
                        f"rcode={response_code}"
                    ),
                    "DNS_RESPONSE"
                )

        except (
            socket.timeout,
            OSError
        ):

            return None
