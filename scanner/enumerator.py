from typing import List

from core.models import PortResult
from detectors.manager import DetectorManager


def enumerate_services(
    target: str,
    results: List[PortResult],
    timeout: float = 2.0
) -> List[PortResult]:
    """
    Enumerate services on ports discovered as OPEN.

    Closed and non-responsive ports are returned unchanged.

    Detector results may contain:
        (service, detail)

    or:

        (service, detail, evidence)
    """

    manager = DetectorManager()

    updated_results = []

    for result in results:

        if result.state != "OPEN":
            updated_results.append(result)
            continue

        try:

            detection = manager.detect(
                target,
                result.port,
                timeout
            )

            if detection:

                result.service = detection[0]

                result.confidence = "CONFIRMED"

                result.detail = detection[1]

                if len(detection) >= 3:
                    result.evidence = detection[2]

            else:

                result.service = "UNKNOWN"
                result.confidence = "NONE"

                if not result.detail:
                    result.detail = (
                        "Open port; no service response detected"
                    )

        except Exception as error:

            result.service = "UNKNOWN"
            result.confidence = "NONE"

            result.detail = (
                f"Enumeration error: {error}"
            )

        updated_results.append(result)

    return updated_results
