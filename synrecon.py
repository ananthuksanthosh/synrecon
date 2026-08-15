#!/usr/bin/env python3

import argparse
import csv
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from core.models import PortResult
from core.port_modes import parse_port_mode
from scanner.tcp import syn_probe
from scanner.enumerator import enumerate_services
from validation import validate_target
from logger import create_scan_id, setup_logger


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="SYN RECON - TCP SYN reconnaissance scanner"
    )

    parser.add_argument(
        "target",
        help="Target IP address or hostname"
    )

    parser.add_argument(
        "-p",
        "--port",
        help="Explicit ports: 80,443,8080 or 1-1000"
    )

    parser.add_argument(
        "--ports",
        help="Port mode: common, all, range, or explicit ports"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=2.0,
        help="Response timeout in seconds (default: 2)"
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=10,
        help="Number of concurrent workers (default: 10)"
    )

    parser.add_argument(
        "--json",
        metavar="FILE",
        help="Save results as JSON"
    )

    parser.add_argument(
        "--csv",
        metavar="FILE",
        help="Save results as CSV"
    )

    parser.add_argument(
        "--log",
        metavar="FILE",
        help="Save scan log to a file"
    )

    return parser.parse_args()


def select_ports(args):
    if args.port and args.ports:
        raise ValueError(
            "Use either -p/--port OR --ports, not both."
        )

    specification = args.port or args.ports

    if not specification:
        raise ValueError(
            "Port selection required. Use -p 80,443 or --ports common/all."
        )

    return parse_port_mode(specification)


def save_json(
    filename,
    scan_id,
    target,
    started_at,
    timeout,
    workers,
    results,
    elapsed
):
    data = {
        "scan_id": scan_id,
        "target": target,
        "started_at": started_at,
        "timeout_seconds": timeout,
        "workers": workers,
        "scan_time_seconds": round(elapsed, 4),
        "results": [
            result.to_dict()
            for result in results
        ]
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def save_csv(filename, scan_id, target, results):
    fieldnames = [
        "scan_id",
        "target",
        "port",
        "protocol",
        "state",
        "response",
        "latency_ms",
        "service",
        "confidence",
        "product",
        "version",
        "banner",
        "evidence",
        "detail"
    ]

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for result in results:
            row = result.to_dict()

            writer.writerow({
                "scan_id": scan_id,
                "target": target,
                **row
            })


def print_header():
    print()
    print("   ███████╗██╗   ██╗███╗   ██╗")
    print("   ██╔════╝╚██╗ ██╔╝████╗  ██║")
    print("   ███████╗ ╚████╔╝ ██╔██╗ ██║")
    print("   ╚════██║  ╚██╔╝  ██║╚██╗██║")
    print("   ███████║   ██║   ██║ ╚████║")
    print("   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝")
    print()
    print("              S Y N   R E C O N")
    print("        TCP SYN RECONNAISSANCE TOOL")
    print()



def print_section(title):
    print()
    print(title)
    print("─" * 60)


def print_scan_information(
    target,
    ports,
    workers,
    timeout,
    scan_id,
    started_at
):
    print_section("SCAN INFORMATION")

    print(f" Target      : {target}")
    print(f" Ports       : {len(ports)}")
    print(f" Workers     : {workers}")
    print(f" Timeout     : {timeout:.1f}s")
    print(f" Scan ID     : {scan_id}")
    print(f" Started     : {started_at}")


def print_results(results):
    print_section("RESULTS")

    open_ports = [
        result
        for result in results
        if result.state == "OPEN"
    ]

    if not open_ports:
        print("No open ports found.")
        return

    print(
        f"{'PORT':<8}"
        f"{'SERVICE':<18}"
        f"{'RESPONSE':<14}"
        f"LATENCY"
    )

    print("─" * 60)

    for result in open_ports:

        print(
            f"{result.port:<8}"
            f"{result.service:<18}"
            f"{result.response:<14}"
            f"{result.latency_ms:.2f} ms"
        )


def print_open_port_details(results):
    open_ports = [
        result
        for result in results
        if result.state == "OPEN"
    ]

    if not open_ports:
        return

    print_section("OPEN PORT DETAILS")

    for index, result in enumerate(open_ports):

        print(
            f"{result.port}/{result.protocol}"
        )

        print(
            f"   Service     : {result.service}"
        )

        print(
            f"   Confidence  : {result.confidence}"
        )

        print(
            f"   Response    : {result.response}"
        )

        print(
            f"   Latency     : "
            f"{result.latency_ms:.2f} ms"
        )

        if result.product:
            print(
                f"   Product     : {result.product}"
            )

        if result.version:
            print(
                f"   Version     : {result.version}"
            )

        if result.banner:
            print(
                f"   Banner      : {result.banner}"
            )

        if result.evidence:
            print(
                f"   Evidence    : {result.evidence}"
            )

        if result.detail:
            print(
                f"   Detail      : {result.detail}"
            )

        if index != len(open_ports) - 1:
            print()


def print_summary(statistics, elapsed):
    print_section("SUMMARY")

    print(f" Open         : {statistics['OPEN']}")
    print(f" Closed       : {statistics['CLOSED']}")
    print(f" No response  : {statistics['NO_RESPONSE']}")
    print(f" Unknown      : {statistics['UNKNOWN']}")
    print(f" Duration     : {elapsed:.2f} seconds")

    print("─" * 60)
    print("[+] Scan completed successfully.")
    print()


def main():
    args = parse_arguments()

    if not validate_target(args.target):
        print(f"[!] Invalid target: {args.target}")
        return 1

    if args.timeout <= 0:
        print("[!] Timeout must be greater than 0.")
        return 1

    if args.workers < 1:
        print("[!] Workers must be at least 1.")
        return 1

    try:
        ports = select_ports(args)

    except ValueError as error:
        print(f"[!] {error}")
        return 1

    if not ports:
        print("[!] No valid ports specified.")
        return 1

    scan_id = create_scan_id()

    started_at = datetime.now().isoformat(
        timespec="seconds"
    )

    logger = setup_logger(args.log)

    logger.info(
        f"Scan started | "
        f"ID={scan_id} | "
        f"Target={args.target} | "
        f"Ports={len(ports)} | "
        f"Timeout={args.timeout}s | "
        f"Workers={args.workers}"
    )

    print_header()

    print_scan_information(
        args.target,
        ports,
        args.workers,
        args.timeout,
        scan_id,
        started_at
    )

    # ========================================================
    # PHASE 1 — TCP DISCOVERY
    # ========================================================

    print_section("PHASE 1 — TCP DISCOVERY")

    print(
        f"Scanning {len(ports)} TCP ports..."
    )

    discovery_start = time.perf_counter()

    discovery_results = []

    with ThreadPoolExecutor(
        max_workers=args.workers
    ) as executor:

        future_map = {
            executor.submit(
                syn_probe,
                args.target,
                port,
                args.timeout
            ): port
            for port in ports
        }

        for future in as_completed(future_map):

            port = future_map[future]

            try:
                result = future.result()

            except Exception as error:

                logger.error(
                    f"Port={port} | "
                    f"Discovery error={error}"
                )

                result = PortResult(
                    port=port,
                    protocol="tcp",
                    state="UNKNOWN",
                    response="ERROR",
                    service="UNKNOWN",
                    confidence="NONE",
                    detail=str(error)
                )

            discovery_results.append(result)

    discovery_results.sort(
        key=lambda item: item.port
    )

    discovery_elapsed = (
        time.perf_counter()
        - discovery_start
    )

    open_count = sum(
        1
        for result in discovery_results
        if result.state == "OPEN"
    )

    print(
        f"[+] Discovery complete: "
        f"{open_count} open port(s) found "
        f"in {discovery_elapsed:.2f}s"
    )

    # ========================================================
    # PHASE 2 — SERVICE ENUMERATION
    # ========================================================

    print_section("PHASE 2 — SERVICE ENUMERATION")

    open_results = [
        result
        for result in discovery_results
        if result.state == "OPEN"
    ]

    if open_results:

        print(
            f"Enumerating {len(open_results)} "
            f"open port(s)..."
        )

        enumeration_start = time.perf_counter()

        final_results = enumerate_services(
            args.target,
            discovery_results,
            args.timeout
        )

        enumeration_elapsed = (
            time.perf_counter()
            - enumeration_start
        )

        print(
            f"[+] Enumeration complete "
            f"in {enumeration_elapsed:.2f}s"
        )

    else:

        final_results = discovery_results

        enumeration_elapsed = 0.0

        print(
            "[*] No open ports to enumerate."
        )

    final_results.sort(
        key=lambda item: item.port
    )

    # ========================================================
    # STATISTICS
    # ========================================================

    statistics = {
        "OPEN": 0,
        "CLOSED": 0,
        "NO_RESPONSE": 0,
        "UNKNOWN": 0
    }

    for result in final_results:

        if result.state not in statistics:
            result.state = "UNKNOWN"

        statistics[result.state] += 1

        logger.info(
            f"Port={result.port} | "
            f"State={result.state} | "
            f"Service={result.service} | "
            f"Confidence={result.confidence} | "
            f"Response={result.response} | "
            f"Latency={result.latency_ms}ms | "
            f"Detail={result.detail}"
        )

    total_elapsed = (
        discovery_elapsed
        + enumeration_elapsed
    )

    # ========================================================
    # OUTPUT
    # ========================================================

    print_results(final_results)

    print_open_port_details(final_results)

    print_summary(
        statistics,
        total_elapsed
    )

    # ========================================================
    # JSON
    # ========================================================

    if args.json:

        save_json(
            args.json,
            scan_id,
            args.target,
            started_at,
            args.timeout,
            args.workers,
            final_results,
            total_elapsed
        )

        print(
            f"[+] JSON saved: {args.json}"
        )

    # ========================================================
    # CSV
    # ========================================================

    if args.csv:

        save_csv(
            args.csv,
            scan_id,
            args.target,
            final_results
        )

        print(
            f"[+] CSV saved: {args.csv}"
        )

    # ========================================================
    # LOG
    # ========================================================

    logger.info(
        f"Scan completed | "
        f"ID={scan_id} | "
        f"Elapsed={total_elapsed:.2f}s | "
        f"Open={statistics['OPEN']} | "
        f"Closed={statistics['CLOSED']} | "
        f"NoResponse={statistics['NO_RESPONSE']} | "
        f"Unknown={statistics['UNKNOWN']}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
