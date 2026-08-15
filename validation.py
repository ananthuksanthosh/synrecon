import ipaddress
import socket


def validate_target(target):
    """
    Validate an IPv4 address or resolve a hostname.

    Returns:
        True if valid
        False if invalid
    """

    try:
        ipaddress.ip_address(target)
        return True

    except ValueError:
        pass

    try:
        socket.gethostbyname(target)
        return True

    except socket.gaierror:
        return False
