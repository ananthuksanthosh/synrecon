#!/usr/bin/env python3

import socket
import ssl


# ============================================================
# TCP SERVICE DATABASE
# ============================================================

TCP_SERVICES = {

    # File Transfer
    20: "FTP-DATA",
    21: "FTP",
    69: "TFTP",

    # Remote Access
    22: "SSH",
    23: "TELNET",
    3389: "RDP",
    5900: "VNC",
    5901: "VNC",
    5902: "VNC",
    5903: "VNC",
    5904: "VNC",
    5905: "VNC",
    5906: "VNC",
    5907: "VNC",
    5908: "VNC",
    5909: "VNC",

    # Mail
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    465: "SMTPS",
    587: "SMTP",
    993: "IMAPS",
    995: "POP3S",

    # DNS
    53: "DNS",

    # Web
    80: "HTTP",
    443: "HTTPS",
    8000: "HTTP-ALT",
    8008: "HTTP-ALT",
    8080: "HTTP-ALT",
    8081: "HTTP-ALT",
    8443: "HTTPS-ALT",
    8888: "HTTP-ALT",

    # RPC / Windows
    111: "RPC",
    135: "MSRPC",
    139: "NETBIOS-SSN",
    445: "SMB",
    593: "HTTP-RPC",

    # LDAP / Kerberos
    88: "KERBEROS",
    389: "LDAP",
    464: "KERBEROS-PASSWD",
    636: "LDAPS",

    # NFS
    2049: "NFS",

    # Databases
    1433: "MSSQL",
    1521: "ORACLE",
    3306: "MYSQL",
    5432: "POSTGRESQL",
    6379: "REDIS",
    11211: "MEMCACHED",
    27017: "MONGODB",

    # MQTT
    1883: "MQTT",
    8883: "MQTT-TLS",

    # RTSP
    554: "RTSP",

    # Docker
    2375: "DOCKER",
    2376: "DOCKER-TLS",

    # Kubernetes
    6443: "KUBERNETES-API",

    # Elasticsearch
    9200: "ELASTICSEARCH",
    9300: "ELASTICSEARCH-TRANSPORT",

    # Kibana
    5601: "KIBANA",

    # RabbitMQ
    5672: "RABBITMQ",
    15672: "RABBITMQ-MGMT",

    # ZooKeeper
    2181: "ZOOKEEPER",

    # Webmin
    10000: "WEBMIN",

    # IRC
    6667: "IRC",
    6697: "IRC-TLS",

    # Proxy
    1080: "SOCKS-PROXY",
    3128: "HTTP-PROXY",

    # IPP / CUPS
    631: "IPP/CUPS",

    # rsync
    873: "RSYNC",
}


# ============================================================
# UDP SERVICE DATABASE
# ============================================================

UDP_SERVICES = {

    # DHCP
    67: "DHCP-SERVER",
    68: "DHCP-CLIENT",

    # DNS
    53: "DNS",

    # SNMP
    161: "SNMP",
    162: "SNMP-TRAP",

    # CoAP
    5683: "COAP",
    5684: "COAPS",

    # VPN
    500: "ISAKMP/IKE",
    4500: "IPSEC-NAT-T",

    # TFTP
    69: "TFTP",

    # MQTT can be TCP only in this map;
    # MQTT-SN/other variants should be handled separately.
}


# ============================================================
# SERVICE LOOKUP
# ============================================================

def get_tcp_service_name(port):
    """
    Return the likely TCP service for a port.
    """

    return TCP_SERVICES.get(
        port,
        "UNKNOWN"
    )


def get_udp_service_name(port):
    """
    Return the likely UDP service for a port.
    """

    return UDP_SERVICES.get(
        port,
        "UNKNOWN"
    )


# ============================================================
# HTTP DETECTION
# ============================================================

def detect_http(target, port, timeout=2):
    """
    Perform a minimal HTTP HEAD request.

    Returns:
        HTTP response information or None.
    """

    try:

        with socket.create_connection(
            (target, port),
            timeout=timeout
        ) as sock:

            request = (
                "HEAD / HTTP/1.0\r\n"
                "Host: target\r\n"
                "Connection: close\r\n"
                "\r\n"
            )

            sock.sendall(
                request.encode()
            )

            response = sock.recv(4096)

            text = response.decode(
                errors="ignore"
            )

            lines = text.splitlines()

            for line in lines:

                if line.lower().startswith(
                    "server:"
                ):

                    return line.strip()

            if lines and lines[0].startswith(
                "HTTP/"
            ):

                return lines[0]

    except Exception:
        pass

    return None


# ============================================================
# HTTPS DETECTION
# ============================================================

def detect_https(target, port, timeout=2):
    """
    Perform a minimal TLS connection.

    Returns:
        TLS version or None.
    """

    try:

        context = ssl.create_default_context()

        context.check_hostname = False

        context.verify_mode = (
            ssl.CERT_NONE
        )

        with socket.create_connection(
            (target, port),
            timeout=timeout
        ) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=target
            ) as tls_sock:

                version = tls_sock.version()

                if version:
                    return f"TLS/{version}"

    except Exception:
        pass

    return None


# ============================================================
# SERVICE DETECTION
# ============================================================

def detect_service(
    target,
    port,
    timeout=2
):
    """
    Identify a likely TCP service.

    Returns:

        service
        detail
    """

    service = get_tcp_service_name(port)

    # --------------------------------------------------------
    # HTTP
    # --------------------------------------------------------

    if service in (
        "HTTP",
        "HTTP-ALT"
    ):

        detail = detect_http(
            target,
            port,
            timeout
        )

        if detail:
            return service, detail

        return (
            service,
            "HTTP suspected from port"
        )

    # --------------------------------------------------------
    # HTTPS
    # --------------------------------------------------------

    if service in (
        "HTTPS",
        "HTTPS-ALT"
    ):

        detail = detect_https(
            target,
            port,
            timeout
        )

        if detail:
            return service, detail

        return (
            service,
            "HTTPS suspected from port"
        )

    # --------------------------------------------------------
    # Known service without active probe
    # --------------------------------------------------------

    if service != "UNKNOWN":

        return (
            service,
            "Port-based identification"
        )

    # --------------------------------------------------------
    # Unknown
    # --------------------------------------------------------

    return (
        "UNKNOWN",
        "No service mapping"
    )
