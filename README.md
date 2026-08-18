⚡ SYN RECON
TCP SYN Reconnaissance & Service Enumeration Tool

A lightweight, modular reconnaissance tool built with Python and Scapy.

============================================================
WHAT IS SYN RECON?
============================================================

SYN RECON is a lightweight, modular TCP SYN reconnaissance
and service enumeration tool built with Python and Scapy.

It is designed for:

- Cybersecurity education
- Authorized penetration testing
- Network reconnaissance
- Security research
- Understanding TCP SYN scanning
- Understanding service detection internally

SYN RECON performs reconnaissance in two primary stages:

    SYN RECON
        |
        v
    TCP SYN DISCOVERY
        |
        v
    Open Ports
        |
        v
    SERVICE ENUMERATION
        |
        +-- Dedicated Detectors
        |
        +-- Generic TCP Fallback
        |
        v
    RESULTS

============================================================
KEY FEATURES
============================================================

TCP RECONNAISSANCE

- TCP SYN reconnaissance
- Open-port discovery
- TCP response analysis
- Configurable TCP port selection

SCANNING

- Common-port scanning
- Specific-port scanning
- Port-range scanning
- Full TCP port scanning
- Concurrent scanning
- Configurable worker count
- Configurable timeout

SERVICE ENUMERATION

- Modular service detection
- Dedicated service detectors
- Generic TCP fallback detection
- Banner and protocol response analysis
- Service confidence information

OUTPUT & MONITORING

- Clean terminal output
- Scan identifiers
- Scan statistics
- Response latency
- Logging support


============================================================
SUPPORTED SERVICES
============================================================

Service          Port(s)
------------------------------------------------------------
FTP              21
SSH              22
Telnet           23
SMTP             25
DNS              53
HTTP             80
HTTPS            443
SMB              139, 445
MQTT             1883
MySQL            3306
PostgreSQL       5432
VNC              5900
Tomcat            8009, 8180

When a dedicated detector is not available, SYN RECON uses
the Generic TCP Detector as a fallback.


============================================================
HOW SYN RECON WORKS
============================================================

PHASE 1 — TCP DISCOVERY

The scanner sends TCP SYN probes to the selected ports.

It analyzes the responses to determine the state of the port.

    SYN RECON
        |
        v
    TCP SYN Probe
        |
        v
    Target Port
        |
        +------ SYN/ACK ------> OPEN
        |
        +------ Other -------> CLOSED / NO RESPONSE

Open ports are then passed to the service enumeration stage.


PHASE 2 — SERVICE ENUMERATION

The discovered open ports are passed to the service
detection layer.

    Open Port
        |
        v
    DetectorManager
        |
        +-- FTPDetector
        |
        +-- SSHDetector
        |
        +-- HTTPDetector
        |
        +-- Other Detectors
        |
        v
    GenericTCPDetector
        |
        v
    Results

Dedicated detectors attempt to identify services and provide
additional evidence such as:

- Service banners
- Protocol responses
- Service-specific information
- Confidence
- Response latency


============================================================
PROJECT ARCHITECTURE
============================================================

synrecon/
|
├── synrecon.py
|
├── scanner/
│   ├── __init__.py
│   ├── tcp.py
│   └── enumerator.py
|
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
|
├── core/
│   ├── __init__.py
│   ├── models.py
│   └── port_modes.py
|
├── output/
│   └── __init__.py
|
├── logger.py
├── port_parser.py
├── service_detector.py
├── validation.py
└── requirements.txt


============================================================
COMPONENT RESPONSIBILITIES
============================================================

synrecon.py
    Main CLI and scan workflow.

scanner/tcp.py
    TCP SYN discovery and port-state analysis.

scanner/enumerator.py
    Coordinates service enumeration.

detectors/
    Modular service-specific detectors.

detectors/manager.py
    Selects the appropriate detector.

detectors/generic.py
    Generic TCP fallback detection.

core/port_modes.py
    Handles port-selection modes.

core/models.py
    Core scan data structures.

port_parser.py
    Parses port specifications.

validation.py
    Input validation.

logger.py
    Logging functionality.


============================================================
INSTALLATION
============================================================

REQUIREMENTS

- Linux-based operating system
- Python 3
- Scapy
- Network access to the authorized target
- Appropriate privileges for TCP SYN packet scanning


STEP 1 — CHECK PYTHON

    python3 --version


STEP 2 — CLONE THE REPOSITORY

    git clone https://github.com/ananthuksanthosh/synrecon.git

Enter the project directory:

    cd synrecon


STEP 3 — INSTALL DEPENDENCIES

    pip3 install -r requirements.txt

If Python and pip are not installed on a Debian-based
Linux system:

    sudo apt update
    sudo apt install python3 python3-pip


============================================================
HOW TO USE
============================================================

BASIC SYNTAX

    sudo python3 synrecon.py <TARGET> --ports <PORT_SPECIFICATION>


<TARGET>

Authorized IP address or hostname.


<PORT_SPECIFICATION>

Defines which TCP ports should be scanned.


============================================================
PORT SELECTION
============================================================

1. COMMON PORTS

    sudo python3 synrecon.py <TARGET> --ports common


2. SPECIFIC PORTS

    sudo python3 synrecon.py <TARGET> --ports 21,22,23,80,443


3. PORT RANGE

    sudo python3 synrecon.py <TARGET> --ports 1-100

Example:

    sudo python3 synrecon.py <TARGET> --ports 1-1000


4. MULTIPLE PORTS AND RANGES

    sudo python3 synrecon.py <TARGET> --ports 20-25,80,443,3306


5. ALL TCP PORTS

    sudo python3 synrecon.py <TARGET> --ports all

This scans TCP ports:

    1 - 65535

Full TCP scanning can take considerably longer than a
common-port scan.


============================================================
SCAN CONFIGURATION
============================================================

WORKERS

The --workers option controls concurrent scanning workers.

    sudo python3 synrecon.py <TARGET> --ports common --workers 20

Examples:

    --workers 10
    --workers 20
    --workers 50


TIMEOUT

The --timeout option controls the network operation timeout.

    sudo python3 synrecon.py <TARGET> --ports common --timeout 2

Default:

    2 seconds


============================================================
COMBINED COMMAND
============================================================

    sudo python3 synrecon.py <TARGET> \
        --ports common \
        --workers 20 \
        --timeout 2

Configuration:

    Port mode  -> common
    Workers    -> 20
    Timeout    -> 2 seconds


============================================================
LABORATORY USAGE
============================================================

For an authorized controlled laboratory target:

    sudo python3 synrecon.py <TARGET> --ports common --workers 20

Replace <TARGET> with an IP address or hostname you own or
have explicit permission to test.


============================================================
EXAMPLE OUTPUT
============================================================

SYN RECON
TCP SYN RECONNAISSANCE TOOL

SCAN INFORMATION
------------------------------------------------------------
 Target      : 192.168.56.9
 Ports       : 78
 Workers     : 20
 Timeout     : 2.0s
 Scan ID     : SR-20260815-102919

PHASE 1 — TCP DISCOVERY
------------------------------------------------------------
Scanning 78 TCP ports...
[+] Discovery complete: 16 open port(s) found

PHASE 2 — SERVICE ENUMERATION
------------------------------------------------------------
Enumerating 16 open port(s)...
[+] Enumeration complete

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
139     SMB               SYN/ACK       257.76 ms
445     SMB               SYN/ACK       136.27 ms
3306    MySQL             SYN/ACK       130.10 ms
5432    PostgreSQL        SYN/ACK       94.92 ms
5900    VNC               SYN/ACK       149.19 ms
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


============================================================
UNDERSTANDING THE OUTPUT
============================================================

SCAN INFORMATION

Target
    Target IP address or hostname.

Ports
    Number of selected ports.

Workers
    Concurrent scanning workers.

Timeout
    Network operation timeout.

Scan ID
    Unique scan identifier.

Started
    Scan start time.


RESULTS

PORT
    Discovered TCP port.

SERVICE
    Detected service.

RESPONSE
    TCP response.

LATENCY
    Approximate response time.


============================================================
OPEN PORT DETAILS
============================================================

For detected services, SYN RECON can provide additional
evidence.

Example:

21/tcp
    Service     : FTP
    Confidence  : CONFIRMED
    Response    : SYN/ACK
    Latency     : 463.86 ms
    Detail      : FTP banner / protocol response

This provides more information than simply reporting:

    21/tcp OPEN


============================================================
SERVICE DETECTION ARCHITECTURE
============================================================

                       DetectorManager
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
        FTPDetector      SSHDetector      HTTPDetector
              |               |               |
              v               v               v
        FTP Evidence      SSH Evidence     HTTP Evidence
              |               |               |
              +---------------+---------------+
                              |
                              v
                    GenericTCPDetector
                              |
                              v
                           RESULTS

The modular design allows individual service detectors to be
maintained independently.


============================================================
INTERNAL WORKFLOW
============================================================

    +-------------------+
    |     CLI INPUT     |
    | Target + Ports    |
    +---------+---------+
              |
              v
    +-------------------+
    |  PORT VALIDATION  |
    +---------+---------+
              |
              v
    +-------------------+
    |  PORT SELECTION   |
    | common/custom/all |
    +---------+---------+
              |
              v
    +-------------------+
    |   TCP SYN SCAN    |
    +---------+---------+
              |
              v
          Open Ports
              |
              v
    +-------------------+
    | ENUMERATION LAYER |
    +---------+---------+
              |
              v
    +-------------------+
    | DETECTOR MANAGER  |
    +---------+---------+
              |
       +------+------+
       |             |
       v             v
Dedicated Detector  Generic Detector
       |             |
       +------+------+
              |
              v
    +-------------------+
    |      RESULTS      |
    +-------------------+


============================================================
VERIFICATION
============================================================

MAIN APPLICATION IMPORT

    python3 -c "import synrecon; print('SYN RECON import: OK')"

Expected:

    SYN RECON import: OK


DETECTOR MANAGER

    python3 -c "from detectors.manager import DetectorManager; print('DetectorManager: OK')"

Expected:

    DetectorManager: OK


COMPILE MAIN APPLICATION

    python3 -m py_compile synrecon.py


COMPILE SCANNER MODULES

    python3 -m py_compile scanner/tcp.py
    python3 -m py_compile scanner/enumerator.py


COMPILE DETECTORS

    python3 -m py_compile detectors/*.py


============================================================
PROJECT STATUS
============================================================

SYN RECON v1.0.1

Current Implementation:

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


============================================================
ETHICAL USE
============================================================

SYN RECON is intended only for authorized security testing
and controlled laboratory environments.

Use SYN RECON only against:

- Systems you own
- Personal laboratory systems
- Authorized testing targets
- Systems for which you have explicit permission to perform
  security testing

DO NOT scan systems or networks without authorization.

The example target shown in this documentation represents a
controlled laboratory environment.

The responsibility for using this tool legally and ethically
belongs to the user.


============================================================
AUTHOR
============================================================

Ananthu K Santhosh

Cybersecurity | Ethical Hacking | Network Security

GitHub:
https://github.com/ananthuksanthosh

Project:
https://github.com/ananthuksanthosh/synrecon


============================================================
LICENSE
============================================================

SYN RECON is released under the MIT License.

Copyright © 2026 Ananthu K Santhosh.

See LICENSE for the complete license text.


============================================================
SYN RECON v1.0.1
============================================================

Python • Scapy • TCP/IP • Linux

Built for cybersecurity education, authorized security
testing, network reconnaissance, and security research.

Ananthu K Santhosh
