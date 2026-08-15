from abc import ABC, abstractmethod
from typing import Optional, Tuple


class ServiceDetector(ABC):
    """
    Base interface for SYN RECON service detectors.
    """

    name = "GENERIC"
    ports = set()

    def supports(self, port: int) -> bool:
        """
        Return True if this detector is appropriate
        for the supplied TCP port.
        """
        return port in self.ports

    @abstractmethod
    def detect(
        self,
        target: str,
        port: int,
        timeout: float = 2.0
    ) -> Tuple[str, Optional[str]]:
        """
        Perform service detection.

        Returns:
            (service_name, detail)
        """
        raise NotImplementedError
