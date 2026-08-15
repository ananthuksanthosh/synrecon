# SYN RECON

TCP SYN Reconnaissance & Service Enumeration Tool

SYN RECON is a lightweight, modular TCP SYN reconnaissance and service
enumeration tool built with Python and Scapy.

It is designed for cybersecurity education, authorized penetration testing,
network reconnaissance, and understanding how TCP SYN scanning and service
detection work internally.

---

## Overview

SYN RECON performs reconnaissance in two stages:

                    SYN RECON
                        |
                        v
              +-------------------+
              | TCP SYN DISCOVERY |
              |                   |
              | Open / Closed     |
              +---------+---------+
                        |
                   Open Ports
                        |
                        v
              +-------------------+
              | SERVICE ENUMERATION|
              |                   |
              | Dedicated Detectors|
              | + Generic Detector|
              +---------+---------+
                        |
                        v
              +-------------------+
              |      RESULTS      |
              |                   |
              | Port / Service    |
              | Response / Latency|
              +-------------------+

### Phase 1 - TCP Discovery

The scanner sends TCP SYN probes to the selected ports and analyzes the
responses to determine port state.

### Phase 2 - Service Enumeration

Open ports are passed to the service detection layer. Dedicated detectors
attempt to identify the service and provide additional evidence such as
banners, protocol responses, or service-specific information.

---

## Key Features

- TCP SYN reconnaissance
- Concurrent port scanning
- Common-port scanning
- Custom port selection
- Port-range scanning
- Full TCP port scanning
- Configurable worker count
- Configurable connection timeout
- Modular service detection architecture
- Dedicated service detectors
- Generic TCP fallback detection
- Scan identifiers and statistics
- Clean terminal output
- Logging support
- Python-based modular architecture

---

## Supported Services

| Service | Port(s) |
|---|---:|
| FTP | 21 |
| SSH | 22 |
| Telnet | 23 |
| SMTP | 25 |
| DNS | 53 |
| HTTP | 80 |
| HTTPS | 443 |
| SMB | 139, 445 |
| MQTT | 1883 |
| MySQL | 3306 |
| PostgreSQL | 5432 |
| VNC | 5900 |
| Tomcat | 8009, 8180 |

When a dedicated detector is not available, the generic TCP detector is used
as a fallback.

---

# Installation

## Requirements

- Linux
- Python 3
- Scapy
- Root/sudo privileges for SYN scanning

The project was developed and tested in a Kali Linux laboratory environment
using VirtualBox.

### Check Python

    python3 --version

### Clone the repository

    git clone https://github.com/ananthuksanthosh/synrecon.git
    cd synrecon

### Install dependencies

    pip3 install -r requirements.txt

If required on Kali Linux:

    sudo apt update
    sudo apt install python3 python3-pip

---

# Usage

## Basic Syntax

    sudo python3 synrecon.py <TARGET> --ports <PORT_SPECIFICATION>

Example:

    sudo python3 synrecon.py 192.168.56.9 --ports common

The example target is an intentionally vulnerable laboratory target.

---

# Port Selection

## Common Ports

Scan SYN RECON's predefined common TCP ports:

    sudo python3 synrecon.py 192.168.56.9 --ports common

This is the recommended starting point for a normal reconnaissance scan.

---

## Specific Ports

Scan selected ports:

    sudo python3 synrecon.py 192.168.56.9 --ports 21,22,23,80,443

---

## Port Range

Scan a continuous range:

    sudo python3 synrecon.py 192.168.56.9 --ports 1-100

---

## Multiple Ports and Ranges

    sudo python3 synrecon.py 192.168.56.9 --ports 20-25,80,443,3306

---

## All TCP Ports

Scan ports 1-65535:

    sudo python3 synrecon.py 192.168.56.9 --ports all

Full TCP scanning takes longer than a common-port scan.

---

# Scan Configuration

## Workers

The --workers option controls concurrent scanning workers.

    sudo python3 synrecon.py 192.168.56.9 --ports common --workers 20

Example values:

    --workers 10
    --workers 20
    --workers 50

Higher values can increase scan speed but should be selected appropriately
for the testing environment.

---

## Timeout

The --timeout option controls the timeout used for network operations.

    sudo python3 synrecon.py 192.168.56.9 --ports common --timeout 2

Default:

    2 seconds

---

# Recommended Laboratory Command

For a typical controlled laboratory environment:

    sudo python3 synrecon.py 192.168.56.9 --ports common --workers 20

This performs:

    Target       : 192.168.56.9
    Port mode    : common
    Workers      : 20
    Timeout      : 2 seconds

---

# Example Output

Example scan performed against a Metasploitable2 laboratory target:

    sudo python3 synrecon.py 192.168.56.9 --ports common --workers 20

Sample result:

    SYN RECON

    SCAN INFORMATION
    ------------------------------------------------------------
     Target      : 192.168.56.9
     Ports       : 78
     Workers     : 20
     Timeout     : 2.0s
     Scan ID     : SR-20260815-102919
     Started     : 2026-08-15T10:29:19

    PHASE 1 — TCP DISCOVERY
    ------------------------------------------------------------
    Scanning 78 TCP ports...
    [+] Discovery complete: 16 open port(s) found in 0.83s

    PHASE 2 — SERVICE ENUMERATION
    ------------------------------------------------------------
    Enumerating 16 open port(s)...
    [+] Enumeration complete in 6.72s

    RESULTS
    ------------------------------------------------------------
    PORT    SERVICE           RESPONSE      LATENCY
    ------------------------------------------------------------
    21      FTP               SYN/ACK       463.86 ms
    22      SSH               SYN/ACK       584.69 ms
    23      Telnet            SYN/ACK       348.92 ms
    25      SMTP              SYN/ACK       217.03 ms
    53      DNS               SYN/ACK       445.04 ms
    80      HTTP              SYN/ACK       429.15 ms
    111     TCP               SYN/ACK       479.09 ms
    139     SMB               SYN/ACK       257.76 ms
    445     SMB               SYN/ACK       136.27 ms
    2049    TCP               SYN/ACK       78.78 ms
    3306    MySQL             SYN/ACK       130.10 ms
    5432    PostgreSQL        SYN/ACK       94.92 ms
    5900    VNC               SYN/ACK       149.19 ms
    6667    TCP               SYN/ACK       86.53 ms
    6697    TCP               SYN/ACK       99.07 ms
    8180    Tomcat            SYN/ACK       86.13 ms

    SUMMARY
    ------------------------------------------------------------
     Open         : 16
     Closed       : 62
     No response  : 0
     Unknown      : 0
     Duration     : 7.56 seconds
    ------------------------------------------------------------
    [+] Scan completed successfully.

---

# Understanding the Output

### Scan Information

| Field | Description |
|---|---|
| Target | Target IP address |
| Ports | Number of selected ports |
| Workers | Concurrent scanning workers |
| Timeout | Network operation timeout |
| Scan ID | Unique scan identifier |
| Started | Scan start time |

### Results

| Field | Description |
|---|---|
| PORT | Discovered TCP port |
| SERVICE | Detected service |
| RESPONSE | TCP response |
| LATENCY | Approximate response time |

### Open Port Details

For detected services, SYN RECON can provide additional evidence.

Example:

    21/tcp
       Service     : FTP
       Confidence  : CONFIRMED
       Response    : SYN/ACK
       Latency     : 463.86 ms
       Detail      : 220 (vsFTPd 2.3.4)

---

# Architecture

    synrecon/
    |
    +-- core/
    |   +-- models.py
    |   +-- port_modes.py
    |
    +-- detectors/
    |   +-- base.py
    |   +-- manager.py
    |   +-- generic.py
    |   +-- ftp.py
    |   +-- ssh.py
    |   +-- telnet.py
    |   +-- smtp.py
    |   +-- dns.py
    |   +-- http.py
    |   +-- https.py
    |   +-- smb.py
    |   +-- mqtt.py
    |   +-- mysql.py
    |   +-- postgresql.py
    |   +-- vnc.py
    |   +-- tomcat.py
    |
    +-- scanner/
    |   +-- tcp.py
    |   +-- enumerator.py
    |
    +-- output/
    |
    +-- logger.py
    +-- port_parser.py
    +-- service_detector.py
    +-- validation.py
    +-- requirements.txt
    +-- synrecon.py

### Component Responsibilities

synrecon.py
    Main command-line interface and scan workflow.

scanner/tcp.py
    TCP SYN discovery and port-state analysis.

scanner/enumerator.py
    Coordinates service enumeration for discovered open ports.

detectors/
    Contains modular service-specific detectors.

detectors/manager.py
    Selects the appropriate detector for each port.

detectors/generic.py
    Fallback detector for unsupported TCP services.

core/port_modes.py
    Handles common, custom, range, and full TCP port selection.

core/models.py
    Defines core scan data structures.

---

# Service Detection Architecture

The detector system is designed to be modular.

                    DetectorManager
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
    FTPDetector      SSHDetector      HTTPDetector
          |                |                |
          +----------------+----------------+
                           |
                           v
                  GenericTCPDetector

A new service detector can be added without redesigning the main scanning
workflow.

---

# Verification

Check the main application:

    python3 -c "import synrecon; print('SYN RECON import: OK')"

Check the detector manager:

    python3 -c "from detectors.manager import DetectorManager; print('DetectorManager: OK')"

Compile the project:

    python3 -m py_compile synrecon.py
    python3 -m py_compile core/port_modes.py
    python3 -m py_compile scanner/tcp.py
    python3 -m py_compile scanner/enumerator.py
    python3 -m py_compile detectors/*.py

---

# Project Status

Version: 1.0.1

Current implementation includes:

- TCP SYN discovery
- Multi-port scanning
- Port-range support
- Full TCP port selection
- Concurrent scanning
- Service enumeration
- Modular service detectors
- Generic TCP detection
- Scan statistics
- Clean CLI output
- Configurable timeout
- Configurable workers

---

# Ethical Use

SYN RECON is intended only for authorized security testing and educational
laboratory environments.

Use this tool only against:

- Systems you own
- Personal virtual machines
- Authorized laboratory targets
- Systems for which you have explicit permission to perform security testing

The example target 192.168.56.9 represents a controlled laboratory environment.

Do not scan systems or networks without authorization.

The responsibility for using this tool legally and ethically belongs to the
user.

---

# Author

Ananthu K Santhosh

GitHub:
https://github.com/ananthuksanthosh

Project Repository:
https://github.com/ananthuksanthosh/synrecon

---

# License

SYN RECON is released under the MIT License.

Copyright (c) 2026 Ananthu K Santhosh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The complete license text is also provided in the repository's LICENSE file.
