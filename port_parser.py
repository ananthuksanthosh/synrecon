def parse_ports(port_string):
    """
    Convert a port specification into a sorted list of unique ports.

    Examples:

        "80"            -> [80]

        "80,443"        -> [80, 443]

        "20-25"         -> [20, 21, 22, 23, 24, 25]

        "22,80,100-105" ->
        [22, 80, 100, 101, 102, 103, 104, 105]
    """

    ports = set()

    parts = port_string.split(",")

    for part in parts:

        part = part.strip()

        if not part:
            continue

        if "-" in part:

            start, end = part.split("-", 1)

            start = int(start)
            end = int(end)

            if start > end:
                raise ValueError(
                    f"Invalid port range: {part}"
                )

            for port in range(start, end + 1):
                ports.add(port)

        else:

            ports.add(int(part))

    for port in ports:

        if port < 1 or port > 65535:
            raise ValueError(
                f"Invalid port: {port}"
            )

    return sorted(ports)
