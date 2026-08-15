import time

from scapy.all import IP, TCP, sr1, send

from core.models import PortResult


def syn_probe(target, port, timeout=2):
    """
    Perform a TCP SYN probe against a single port.

    Returns:
        PortResult
    """

    start_time = time.perf_counter()

    packet = IP(dst=target) / TCP(
        dport=port,
        flags="S"
    )

    response = sr1(
        packet,
        timeout=timeout,
        verbose=0
    )

    latency_ms = (
        time.perf_counter() - start_time
    ) * 1000

    # --------------------------------------------------
    # No response
    # --------------------------------------------------

    if response is None:

        return PortResult(
            port=port,
            protocol="tcp",
            state="NO_RESPONSE",
            response="NONE",
            latency_ms=round(
                latency_ms,
                2
            ),
            service="UNKNOWN",
            confidence="NONE",
            detail="No TCP response"
        )

    # --------------------------------------------------
    # Unexpected non-TCP response
    # --------------------------------------------------

    if not response.haslayer(TCP):

        return PortResult(
            port=port,
            protocol="tcp",
            state="UNKNOWN",
            response="NON_TCP",
            latency_ms=round(
                latency_ms,
                2
            ),
            service="UNKNOWN",
            confidence="NONE",
            detail="Non-TCP response"
        )

    flags = response[TCP].flags

    # --------------------------------------------------
    # SYN + ACK = OPEN
    # --------------------------------------------------

    if flags & 0x12 == 0x12:

        # Terminate the half-open connection.
        rst = IP(dst=target) / TCP(
            dport=port,
            sport=response[TCP].dport,
            seq=response[TCP].ack,
            ack=response[TCP].seq + 1,
            flags="R"
        )

        send(
            rst,
            verbose=0
        )

        return PortResult(
            port=port,
            protocol="tcp",
            state="OPEN",
            response="SYN/ACK",
            latency_ms=round(
                latency_ms,
                2
            ),
            service="UNKNOWN",
            confidence="NONE",
            detail="SYN/ACK received"
        )

    # --------------------------------------------------
    # RST = CLOSED
    # --------------------------------------------------

    if flags & 0x04:

        return PortResult(
            port=port,
            protocol="tcp",
            state="CLOSED",
            response="RST",
            latency_ms=round(
                latency_ms,
                2
            ),
            service="UNKNOWN",
            confidence="NONE",
            detail="RST received"
        )

    # --------------------------------------------------
    # Unexpected TCP response
    # --------------------------------------------------

    return PortResult(
        port=port,
        protocol="tcp",
        state="UNKNOWN",
        response=str(flags),
        latency_ms=round(
            latency_ms,
            2
        ),
        service="UNKNOWN",
        confidence="NONE",
        detail="Unexpected TCP response"
    )
