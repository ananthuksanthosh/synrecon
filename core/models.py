from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class PortResult:
    """Structured result for a single scanned port."""

    port: int
    protocol: str = "tcp"
    state: str = "UNKNOWN"
    response: str = "NONE"
    latency_ms: float = 0.0

    service: str = "UNKNOWN"
    confidence: str = "NONE"

    product: Optional[str] = None
    version: Optional[str] = None
    banner: Optional[str] = None
    evidence: Optional[str] = None
    detail: Optional[str] = None

    def to_dict(self):
        """Convert the result to a dictionary."""
        return asdict(self)
