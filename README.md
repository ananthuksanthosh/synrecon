<div align="center">

# ⚡ SYN RECON

### TCP SYN Reconnaissance & Service Enumeration Tool

**A lightweight, modular reconnaissance tool built with Python and Scapy**

<br>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scapy](https://img.shields.io/badge/Scapy-Network%20Packets-00A8E8?style=for-the-badge)](https://scapy.net/)
[![Platform](https://img.shields.io/badge/Platform-Linux-111111?style=for-the-badge&logo=linux&logoColor=white)](https://www.kernel.org/)
[![Category](https://img.shields.io/badge/Category-Red%20Team-E53935?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-2EA043?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.1-00C853?style=for-the-badge)]()

<br>

**SYN RECON watches the TCP layer — from SYN discovery to service enumeration.**

</div>

---

# 🔎 What Is SYN RECON?

**SYN RECON** is a lightweight, modular **TCP SYN reconnaissance and service enumeration tool** built with **Python and Scapy**.

It is designed for:

- Cybersecurity education
- Authorized penetration testing
- Network reconnaissance
- Security research
- Understanding TCP SYN scanning
- Understanding service detection internally

SYN RECON performs reconnaissance in **two primary stages**:

```text
                         SYN RECON
                             │
                             ▼
                  ┌─────────────────────┐
                  │  TCP SYN DISCOVERY  │
                  │                     │
                  │  Open / Closed      │
                  └──────────┬──────────┘
                             │
                       Open Ports
                             │
                             ▼
                  ┌─────────────────────┐
                  │ SERVICE ENUMERATION │
                  │                     │
                  │ Dedicated Detectors │
                  │          +          │
                  │ Generic TCP Fallback│
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │       RESULTS       │
                  │                     │
                  │ Port / Service      │
                  │ Response / Latency  │
                  └─────────────────────┘
````

---

# ⚡ Key Features

## 🔴 TCP Reconnaissance

* TCP SYN reconnaissance
* Open-port discovery
* TCP response analysis
* TCP port-state identification
* Configurable TCP port selection

## 🟢 Port Scanning

* Common-port scanning
* Specific-port scanning
* Port-range scanning
* Full TCP port scanning
* Concurrent scanning
* Configurable worker count
* Configurable timeout

## 🔵 Service Enumeration

* Modular service detection
* Dedicated service detectors
* Generic TCP fallback detection
* Protocol-specific response analysis
* Banner detection where supported
* Service confidence reporting
* Response latency measurement

## 🟣 Output & Monitoring

* Clean terminal interface
* Scan identifiers
* Scan statistics
* Open-port summary
* Service information
* Response latency
* Logging support

---

# 🧰 Supported Services

| Service    |    Port(s) | Detection            |
| ---------- | ---------: | -------------------- |
| FTP        |         21 | FTP banner           |
| SSH        |         22 | SSH banner           |
| Telnet     |         23 | Telnet negotiation   |
| SMTP       |         25 | SMTP greeting        |
| DNS        |         53 | DNS response         |
| HTTP       |         80 | HTTP response        |
| HTTPS      |        443 | HTTPS response       |
| SMB        |   139, 445 | SMB negotiation      |
| MQTT       |       1883 | MQTT response        |
| MySQL      |       3306 | MySQL greeting       |
| PostgreSQL |       5432 | PostgreSQL response  |
| VNC        |       5900 | RFB greeting         |
| Tomcat     | 8009, 8180 | HTTP/Tomcat response |

When a dedicated detector is not available for an open TCP service, SYN RECON uses the **Generic TCP Detector** as a fallback.

---

# 🧠 How SYN RECON Works

## Phase 1 — TCP Discovery

SYN RECON first performs TCP SYN discovery against the selected ports.

```text
                  TCP SYN PROBE
                        │
                        ▼
                  Target Port
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
           SYN/ACK             Other
              │                   │
              ▼                   ▼
            OPEN          CLOSED / NO RESPONSE
              │
              ▼
        Open Port List
```

The discovery phase determines which ports are reachable and appear open.

---

# 🔎 Phase 2 — Service Enumeration

Only discovered open ports are passed to the enumeration stage.

```text
                         Open Port
                             │
                             ▼
                    ┌─────────────────┐
                    │ DetectorManager │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        FTP Detector    SSH Detector   HTTP Detector
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                    Generic TCP Detector
                             │
                             ▼
                         Detection
                             │
                             ▼
                          Results
```

Service detectors can inspect protocol-specific responses and provide additional evidence.

---

# 🔬 Detection Evidence

Depending on the detected service, SYN RECON can use evidence such as:

```text
SYN/ACK
    │
    ▼
Port appears open
    │
    ▼
Protocol-specific probe
    │
    ▼
Service response
    │
    ▼
Service identification
```

Examples include:

* FTP banners
* SSH banners
* Telnet negotiation
* SMTP greetings
* DNS responses
* HTTP responses
* SMB negotiation responses
* MySQL greetings
* PostgreSQL responses
* VNC/RFB greetings
* Tomcat HTTP responses

---

# 🏗️ Project Architecture

```text
synrecon/
│
├── synrecon.py
│
├── scanner/
│   ├── __init__.py
│   ├── tcp.py
│   └── enumerator.py
│
├── detectors/
│   ├── __init__.py
│   ├── base.py
│   ├── manager.py
│   ├── generic.py
│   ├── ftp.py
│   ├── ssh.py
│   ├── telnet.py
│   ├── smtp.py
│   ├── dns.py
│   ├── http.py
│   ├── https.py
│   ├── smb.py
│   ├── mqtt.py
│   ├── mysql.py
│   ├── postgresql.py
│   ├── vnc.py
│   └── tomcat.py
│
├── core/
│   ├── __init__.py
│   ├── models.py
│   └── port_modes.py
│
├── output/
│   └── __init__.py
│
├── logger.py
├── port_parser.py
├── service_detector.py
├── validation.py
└── requirements.txt
```

---

# 📦 Component Responsibilities

| Component               | Responsibility                            |
| ----------------------- | ----------------------------------------- |
| `synrecon.py`           | Main CLI and scan workflow                |
| `scanner/tcp.py`        | TCP SYN discovery and port-state analysis |
| `scanner/enumerator.py` | Coordinates service enumeration           |
| `detectors/base.py`     | Base detector structure                   |
| `detectors/manager.py`  | Detector selection and coordination       |
| `detectors/generic.py`  | Generic TCP fallback detection            |
| `detectors/*.py`        | Individual service detectors              |
| `core/models.py`        | Core scan data structures                 |
| `core/port_modes.py`    | Port selection modes                      |
| `port_parser.py`        | Port specification parsing                |
| `validation.py`         | Input validation                          |
| `logger.py`             | Logging functionality                     |

---

# 🧩 Modular Detector System

One of the main design principles of SYN RECON is modular service detection.

```text
                       DetectorManager
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   FTP Detector          SSH Detector         HTTP Detector
        │                     │                     │
        ▼                     ▼                     ▼
   FTP Evidence          SSH Evidence          HTTP Evidence
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    Generic TCP Detector
                              │
                              ▼
                           Results
```

This structure allows service detectors to be developed and maintained independently.

---

# 🔄 Internal Workflow

```text
                 ┌──────────────────────┐
                 │      CLI INPUT       │
                 │ Target + Port Mode   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   INPUT VALIDATION   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    PORT SELECTION    │
                 │ common/custom/range  │
                 │        /all          │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    TCP SYN SCAN      │
                 └──────────┬───────────┘
                            │
                            ▼
                       Open Ports
                            │
                            ▼
                 ┌──────────────────────┐
                 │  SERVICE ENUMERATION │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   DETECTOR MANAGER   │
                 └──────────┬───────────┘
                            │
                   ┌────────┴────────┐
                   │                 │
                   ▼                 ▼
            Dedicated Detector  Generic Detector
                   │                 │
                   └────────┬────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │       RESULTS        │
                 └──────────────────────┘
```

---

# 🚀 Installation

## Requirements

* Linux-based operating system
* Python 3
* Scapy
* Network access to an authorized target
* Appropriate privileges for TCP SYN packet scanning

---

## 1. Check Python

```bash
python3 --version
```

Example:

```text
Python 3.x.x
```

---

## 2. Clone the Repository

```bash
git clone https://github.com/ananthuksanthosh/synrecon.git
```

Enter the project directory:

```bash
cd synrecon
```

---

## 3. Install Dependencies

```bash
pip3 install -r requirements.txt
```

If Python and pip are not installed on a Debian-based Linux system:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

# ▶️ Usage

## Basic Syntax

```bash
sudo python3 synrecon.py <TARGET> --ports <PORT_SPECIFICATION>
```

### Parameters

| Parameter   | Description                       |
| ----------- | --------------------------------- |
| `<TARGET>`  | Authorized IP address or hostname |
| `--ports`   | Port selection mode/specification |
| `--workers` | Number of concurrent workers      |
| `--timeout` | Network timeout in seconds        |

---

# 🎯 Port Selection

## Common Ports

Scan the predefined common TCP ports:

```bash
sudo python3 synrecon.py <TARGET> --ports common
```

---

## Specific Ports

Scan selected TCP ports:

```bash
sudo python3 synrecon.py <TARGET> --ports 21,22,23,80,443
```

---

## Port Range

Scan a continuous range:

```bash
sudo python3 synrecon.py <TARGET> --ports 1-100
```

Example:

```bash
sudo python3 synrecon.py <TARGET> --ports 1-1000
```

---

## Multiple Ports and Ranges

Combine individual ports and ranges:

```bash
sudo python3 synrecon.py <TARGET> --ports 20-25,80,443,3306
```

---

## All TCP Ports

Scan the full TCP port range:

```bash
sudo python3 synrecon.py <TARGET> --ports all
```

This scans:

```text
1 - 65535
```

Full TCP scanning can take considerably longer than a common-port scan.

---

# ⚙️ Scan Configuration

## Workers

The `--workers` option controls the number of concurrent scanning workers.

```bash
sudo python3 synrecon.py <TARGET> --ports common --workers 20
```

Examples:

```text
--workers 10
--workers 20
--workers 50
```

Higher worker counts can increase scanning speed but may also increase network load.

---

## Timeout

The `--timeout` option controls the network operation timeout.

```bash
sudo python3 synrecon.py <TARGET> --ports common --timeout 2
```

Default:

```text
2 seconds
```

---

# 🔥 Combined Command

Multiple options can be used together:

```bash
sudo python3 synrecon.py <TARGET> \
    --ports common \
    --workers 20 \
    --timeout 2
```

Configuration:

```text
Port mode  → common
Workers    → 20
Timeout    → 2 seconds
```

---

# 🧪 Laboratory Command

For an authorized controlled laboratory environment:

```bash
sudo python3 synrecon.py <TARGET> --ports common --workers 20
```

Replace:

```text
<TARGET>
```

with an IP address or hostname you own or have explicit permission to test.

---

# 🖥️ Sample Output

The following is an example from a controlled laboratory scan:

```text
   ███████╗██╗   ██╗███╗   ██╗
   ██╔════╝╚██╗ ██╔╝████╗  ██║
   ███████╗ ╚████╔╝ ██╔██╗ ██║
   ╚════██║  ╚██╔╝  ██║╚██╗██║
   ███████║   ██║   ██║ ╚████║
   ╚══════╝   ╚═╝   ╚═╝  ╚═══╝

              S Y N   R E C O N
        TCP SYN RECONNAISSANCE TOOL


SCAN INFORMATION
────────────────────────────────────────────────────────────
 Target      : 192.168.56.9
 Ports       : 78
 Workers     : 20
 Timeout     : 2.0s
 Scan ID     : SR-20260815-102919
 Started     : 2026-08-15T10:29:19

PHASE 1 — TCP DISCOVERY
────────────────────────────────────────────────────────────
Scanning 78 TCP ports...
[+] Discovery complete: 16 open port(s) found in 0.83s

PHASE 2 — SERVICE ENUMERATION
────────────────────────────────────────────────────────────
Enumerating 16 open port(s)...
[+] Enumeration complete in 6.72s

RESULTS
────────────────────────────────────────────────────────────
PORT    SERVICE           RESPONSE      LATENCY
────────────────────────────────────────────────────────────
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

OPEN PORT DETAILS
────────────────────────────────────────────────────────────
21/tcp
   Service     : FTP
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 463.86 ms
   Detail      : 220 (vsFTPd 2.3.4)

22/tcp
   Service     : SSH
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 584.69 ms
   Detail      : SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1

23/tcp
   Service     : Telnet
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 348.92 ms
   Evidence    : TELNET_NEGOTIATION
   Detail      : Telnet negotiation detected

25/tcp
   Service     : SMTP
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 217.03 ms
   Evidence    : SMTP_GREETING
   Detail      : SMTP greeting: 220 metasploitable.localdomain ESMTP Postfix

53/tcp
   Service     : DNS
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 445.04 ms
   Evidence    : DNS_RESPONSE
   Detail      : DNS response received; rcode=2

80/tcp
   Service     : HTTP
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 429.15 ms
   Detail      : Server: Apache/2.2.8 (Ubuntu) DAV/2

111/tcp
   Service     : TCP
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 479.09 ms
   Detail      : TCP connection established; no banner received

139/tcp
   Service     : SMB
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 257.76 ms
   Evidence    : SMB_NEGOTIATION
   Detail      : SMB negotiation response received

445/tcp
   Service     : SMB
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 136.27 ms
   Evidence    : SMB_NEGOTIATION
   Detail      : SMB negotiation response received

2049/tcp
   Service     : TCP
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 78.78 ms
   Detail      : TCP connection established; no banner received

3306/tcp
   Service     : MySQL
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 130.10 ms
   Evidence    : MYSQL_GREETING
   Detail      : MySQL 5.0.51a-3ubuntu5

5432/tcp
   Service     : PostgreSQL
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 94.92 ms
   Evidence    : POSTGRES_SSL_RESPONSE
   Detail      : PostgreSQL service supports SSL negotiation

5900/tcp
   Service     : VNC
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 149.19 ms
   Evidence    : RFB_GREETING
   Detail      : RFB protocol version 003.003

6667/tcp
   Service     : TCP
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 86.53 ms
   Detail      : IRC banner received

6697/tcp
   Service     : TCP
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 99.07 ms
   Detail      : IRC banner received

8180/tcp
   Service     : Tomcat
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 86.13 ms
   Evidence    : TOMCAT_HTTP
   Detail      : Apache Tomcat HTTP response detected

SUMMARY
────────────────────────────────────────────────────────────
 Open         : 16
 Closed       : 62
 No response  : 0
 Unknown      : 0
 Duration     : 7.56 seconds
────────────────────────────────────────────────────────────
[+] Scan completed successfully.
```

---

# 📊 Understanding the Output

## Scan Information

| Field     | Meaning                       |
| --------- | ----------------------------- |
| `Target`  | Target IP address or hostname |
| `Ports`   | Number of selected ports      |
| `Workers` | Number of concurrent workers  |
| `Timeout` | Network operation timeout     |
| `Scan ID` | Unique scan identifier        |
| `Started` | Scan start timestamp          |

---

## Results Table

| Field      | Meaning                   |
| ---------- | ------------------------- |
| `PORT`     | Discovered TCP port       |
| `SERVICE`  | Detected service          |
| `RESPONSE` | TCP response              |
| `LATENCY`  | Approximate response time |

---

## Open Port Details

For detected services, SYN RECON can provide additional information.

Example:

```text
21/tcp
   Service     : FTP
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 463.86 ms
   Detail      : 220 (vsFTPd 2.3.4)
```

This provides more information than simply reporting:

```text
21/tcp OPEN
```

---

# 📈 Scan Summary

At the end of a scan, SYN RECON provides a summary:

```text
SUMMARY
────────────────────────────────────────────────────────────
 Open         : 16
 Closed       : 62
 No response  : 0
 Unknown      : 0
 Duration     : 7.56 seconds
────────────────────────────────────────────────────────────
```

This provides a quick overview of the scan result and execution time.

---

# 🧪 Verification

## Main Application Import

```bash
python3 -c "import synrecon; print('SYN RECON import: OK')"
```

Expected:

```text
SYN RECON import: OK
```

---

## Detector Manager

```bash
python3 -c "from detectors.manager import DetectorManager; print('DetectorManager: OK')"
```

Expected:

```text
DetectorManager: OK
```

---

## Compile Main Application

```bash
python3 -m py_compile synrecon.py
```

---

## Compile Scanner Modules

```bash
python3 -m py_compile scanner/tcp.py
python3 -m py_compile scanner/enumerator.py
```

---

## Compile Detectors

```bash
python3 -m py_compile detectors/*.py
```

---

# 📁 Project Structure

```text
SYN RECON
│
├── synrecon.py
│
├── scanner/
│   ├── __init__.py
│   ├── tcp.py
│   └── enumerator.py
│
├── detectors/
│   ├── __init__.py
│   ├── base.py
│   ├── manager.py
│   ├── generic.py
│   ├── ftp.py
│   ├── ssh.py
│   ├── telnet.py
│   ├── smtp.py
│   ├── dns.py
│   ├── http.py
│   ├── https.py
│   ├── smb.py
│   ├── mqtt.py
│   ├── mysql.py
│   ├── postgresql.py
│   ├── vnc.py
│   └── tomcat.py
│
├── core/
│   ├── __init__.py
│   ├── models.py
│   └── port_modes.py
│
├── output/
│   └── __init__.py
│
├── logger.py
├── port_parser.py
├── service_detector.py
├── validation.py
└── requirements.txt
```

---

# 📌 Project Design

SYN RECON separates its functionality into independent components.

```text
                 SYN RECON
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
    Scanner        Core        Detectors
       │             │             │
       │             │             ├── FTP
       │             │             ├── SSH
       │             │             ├── HTTP
       │             │             ├── SMB
       │             │             ├── MySQL
       │             │             └── Generic
       │             │
       └─────────────┼─────────────┘
                     │
                     ▼
                  Results
```

This modular structure makes it easier to:

* Maintain individual components
* Add new service detectors
* Extend port-selection functionality
* Separate scanning from enumeration
* Improve individual modules independently

---

# 📊 Project Status

## SYN RECON v1.0.1

### Current Implementation

```text
✓ TCP SYN discovery
✓ Open-port discovery
✓ Common-port scanning
✓ Custom port selection
✓ Port-range scanning
✓ Full TCP port selection
✓ Concurrent scanning
✓ Configurable workers
✓ Configurable timeout
✓ Service enumeration
✓ Modular service detectors
✓ Generic TCP detection
✓ Scan identifiers
✓ Scan statistics
✓ Response latency
✓ Clean CLI output
✓ Logging support
```

---

# 🛠️ Technology Stack

| Technology                  | Purpose                                 |
| --------------------------- | --------------------------------------- |
| Python 3                    | Core programming language               |
| Scapy                       | Packet crafting and network interaction |
| TCP/IP                      | Network reconnaissance                  |
| Linux                       | Primary execution environment           |
| Python Concurrency          | Parallel scanning                       |
| Modular Python Architecture | Service detection system                |

---

# 🔐 Ethical Use

SYN RECON is intended **only for authorized security testing and controlled laboratory environments**.

Use SYN RECON only against:

* Systems you own
* Personal laboratory systems
* Authorized testing targets
* Systems for which you have explicit permission to perform security testing

> **Do not scan systems or networks without authorization.**

The example target shown in this documentation represents a controlled laboratory environment.

The responsibility for using this tool legally and ethically belongs to the user.

---

# 👨‍💻 Author

## Ananthu K Santhosh

**Cybersecurity | Ethical Hacking | Network Security**

**GitHub:**
[https://github.com/ananthuksanthosh](https://github.com/ananthuksanthosh)

**Project Repository:**
[https://github.com/ananthuksanthosh/synrecon](https://github.com/ananthuksanthosh/synrecon)

---

# 📄 License

SYN RECON is released under the **MIT License**.

Copyright © 2026 **Ananthu K Santhosh**.

See [`LICENSE`](LICENSE) for the complete license text.

---

<div align="center">

# ⚡ SYN RECON v1.0.1

**Python • Scapy • TCP/IP • Linux**

Built for cybersecurity education, authorized security testing,
network reconnaissance, and security research.

<br>

**Ananthu K Santhosh**

</div>
```
