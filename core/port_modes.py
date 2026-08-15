#!/usr/bin/env python3

"""
Port selection modes for SYN RECON.

Supported modes:
    common  -> important/common TCP ports
    all     -> TCP ports 1-65535
    range   -> custom specification such as 1-1000
"""

# Important TCP ports commonly encountered during reconnaissance.
COMMON_PORTS = [
    20, 21,
    22,
    23,
    25,
    53,
    67, 68,
    69,
    80,
    88,
    110,
    111,
    135,
    137, 138, 139,
    143,
    161, 162,
    389,
    443,
    445,
    464,
    465,
    587,
    593,
    631,
    636,
    873,
    993,
    995,
    1080,
    11211,
    1194,
    1433, 1434,
    1521,
    1883,
    2049,
    2181,
    2375, 2376,
    27017,
    3128,
    3306,
    3389,
    500,
    5432,
    5601,
    5672,
    5900, 5901, 5902, 5903, 5904,
    5905, 5906, 5907, 5908, 5909,
    5985, 5986,
    6379,
    6443,
    6667,
    6697,
    8000,
    8008,
    8080,
    8180,
    8081,
    8443,
    8888,
    9000,
    9200,
    9300,
    10000,
]

COMMON_PORTS = sorted(set(COMMON_PORTS))


def get_common_ports():
    """Return the predefined common TCP ports."""
    return COMMON_PORTS.copy()


def get_all_ports():
    """Return every valid TCP port."""
    return list(range(1, 65536))


def parse_port_mode(value):
    """
    Convert a port-mode specification into a list of ports.

    Examples:
        common
        all
        1-100
        80,443,8080
    """

    if not value:
        raise ValueError("Port specification cannot be empty.")

    value = value.strip().lower()

    if value == "common":
        return get_common_ports()

    if value == "all":
        return get_all_ports()

    ports = set()

    for item in value.split(","):

        item = item.strip()

        if not item:
            continue

        if "-" in item:

            parts = item.split("-")

            if len(parts) != 2:
                raise ValueError(
                    f"Invalid port range: {item}"
                )

            try:
                start = int(parts[0])
                end = int(parts[1])
            except ValueError:
                raise ValueError(
                    f"Invalid port range: {item}"
                )

            if start < 1 or end > 65535:
                raise ValueError(
                    f"Port range out of bounds: {item}"
                )

            if start > end:
                raise ValueError(
                    f"Range start is greater than end: {item}"
                )

            ports.update(range(start, end + 1))

        else:

            try:
                port = int(item)
            except ValueError:
                raise ValueError(
                    f"Invalid port: {item}"
                )

            if port < 1 or port > 65535:
                raise ValueError(
                    f"Invalid port: {port}"
                )

            ports.add(port)

    if not ports:
        raise ValueError(
            "No valid ports specified."
        )

    return sorted(ports)
