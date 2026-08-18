<div align="center">
⚡ SYN RECON
TCP SYN Reconnaissance & Service Enumeration Tool
A lightweight, modular reconnaissance tool built with Python and Scapy
<br>
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scapy](https://img.shields.io/badge/Scapy-Network%20Packets-00A8E8?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux-111111?style=for-the-badge&logo=linux&logoColor=white)
[![Category](https://img.shields.io/badge/Category-Red%20Team-E53935?style=for-the-badge)]()
![License](https://img.shields.io/badge/License-MIT-2EA043?style=for-the-badge)
[![Version](https://img.shields.io/badge/Version-1.0.1-00C853?style=for-the-badge)]()
<br>
SYN RECON watches the TCP layer — from SYN discovery to service enumeration.
</div>
---
🔎 What Is SYN RECON?
SYN RECON is a lightweight, modular TCP SYN reconnaissance and service enumeration tool built with Python and Scapy.
It is designed for:
Cybersecurity education
Authorized penetration testing
Network reconnaissance
Security research
Understanding TCP SYN scanning
Understanding service detection internally
SYN RECON performs reconnaissance in two primary stages:
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
```
---
⚡ Key Features
🔴 TCP Reconnaissance
TCP SYN reconnaissance
Open-port discovery
TCP response analysis
Configurable TCP port selection
🟢 Scanning
Common-port scanning
Specific-port scanning
Port-range scanning
Full TCP port scanning
Concurrent scanning
Configurable worker count
Configurable timeout
🔵 Service Enumeration
Modular service detection
Dedicated service detectors
Generic TCP fallback detection
Banner and protocol response analysis
Service confidence information
🟣 Output & Monitoring
Clean terminal output
Scan identifiers
Scan statistics
Response latency
Logging support
---
🧰 Supported Services
Service	Port(s)
FTP	21
SSH	22
Telnet	23
SMTP	25
DNS	53
HTTP	80
HTTPS	443
SMB	139, 445
MQTT	1883
MySQL	3306
PostgreSQL	5432
VNC	5900
Tomcat	8009, 8180
When a dedicated detector is not available, SYN RECON uses the Generic TCP Detector as a fallback.
---
🧠 How SYN RECON Works
Phase 1 — TCP Discovery
The scanner sends TCP SYN probes to the selected ports.
It analyzes the responses to determine the state of the port.
```text
SYN RECON
    │
    ▼
TCP SYN Probe
    │
    ▼
Target Port
    │
    ├───────────────┐
    │               │
 SYN/ACK          Other
    │               │
    ▼               ▼
 OPEN          CLOSED / NO RESPONSE
```
Open ports are then passed to the service enumeration stage.
---
Phase 2 — Service Enumeration
The discovered open ports are passed to the service detection layer.
```text
                Open Port
                    │
                    ▼
             DetectorManager
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   FTPDetector SSHDetector HTTPDetector
        │           │           │
        └───────────┼───────────┘
                    │
                    ▼
           GenericTCPDetector
                    │
                    ▼
                 Results
```
Dedicated detectors attempt to identify services and provide additional evidence such as:
Service banners
Protocol responses
Service-specific information
Confidence
Response latency
---
🏗️ Project Architecture
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
📦 Component Responsibilities
Component	Responsibility
`synrecon.py`	Main CLI and scan workflow
`scanner/tcp.py`	TCP SYN discovery and port-state analysis
`scanner/enumerator.py`	Coordinates service enumeration
`detectors/`	Modular service-specific detectors
`detectors/manager.py`	Selects the appropriate detector
`detectors/generic.py`	Generic TCP fallback detection
`core/port_modes.py`	Handles port-selection modes
`core/models.py`	Core scan data structures
`port_parser.py`	Parses port specifications
`validation.py`	Input validation
`logger.py`	Logging functionality
---
🚀 Installation
Requirements
SYN RECON requires:
Linux-based operating system
Python 3
Scapy
Network access to the authorized target
Appropriate privileges for TCP SYN packet scanning
---
1. Check Python
```bash
python3 --version
```
---
2. Clone the Repository
```bash
git clone https://github.com/ananthuksanthosh/synrecon.git
```
Enter the project directory:
```bash
cd synrecon
```
---
3. Install Dependencies
```bash
pip3 install -r requirements.txt
```
If Python and pip are not installed on a Debian-based Linux system:
```bash
sudo apt update
sudo apt install python3 python3-pip
```
---
▶️ How To Use
Basic Syntax
```bash
sudo python3 synrecon.py <TARGET> --ports <PORT_SPECIFICATION>
```
Where:
```text
<TARGET>
    Authorized IP address or hostname

<PORT_SPECIFICATION>
    Defines which TCP ports should be scanned
```
---
🎯 Port Selection
1. Common Ports
```bash
sudo python3 synrecon.py <TARGET> --ports common
```
---
2. Specific Ports
```bash
sudo python3 synrecon.py <TARGET> --ports 21,22,23,80,443
```
---
3. Port Range
```bash
sudo python3 synrecon.py <TARGET> --ports 1-100
```
Example:
```bash
sudo python3 synrecon.py <TARGET> --ports 1-1000
```
---
4. Multiple Ports and Ranges
```bash
sudo python3 synrecon.py <TARGET> --ports 20-25,80,443,3306
```
---
5. All TCP Ports
```bash
sudo python3 synrecon.py <TARGET> --ports all
```
This scans TCP ports:
```text
1 - 65535
```
Full TCP scanning can take considerably longer than a common-port scan.
---
⚙️ Scan Configuration
Workers
The `--workers` option controls concurrent scanning workers.
```bash
sudo python3 synrecon.py <TARGET> --ports common --workers 20
```
Examples:
```text
--workers 10
--workers 20
--workers 50
```
---
Timeout
The `--timeout` option controls the network operation timeout.
```bash
sudo python3 synrecon.py <TARGET> --ports common --timeout 2
```
Default:
```text
2 seconds
```
---
🔥 Combined Command
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
🧪 Laboratory Usage
For an authorized controlled laboratory target:
```bash
sudo python3 synrecon.py <TARGET> --ports common --workers 20
```
> Replace `<TARGET>` with an IP address or hostname you own or have explicit permission to test.
---
🖥️ Example Output
```text
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
```
---
📊 Understanding The Output
Scan Information
Field	Description
Target	Target IP address or hostname
Ports	Number of selected ports
Workers	Concurrent scanning workers
Timeout	Network operation timeout
Scan ID	Unique scan identifier
Started	Scan start time
Results
Field	Description
PORT	Discovered TCP port
SERVICE	Detected service
RESPONSE	TCP response
LATENCY	Approximate response time
---
🔍 Open Port Details
For detected services, SYN RECON can provide additional evidence.
Example:
```text
21/tcp
   Service     : FTP
   Confidence  : CONFIRMED
   Response    : SYN/ACK
   Latency     : 463.86 ms
   Detail      : FTP banner / protocol response
```
This provides more information than simply reporting:
```text
21/tcp OPEN
```
---
🧩 Service Detection Architecture
```text
                       DetectorManager
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        FTPDetector      SSHDetector      HTTPDetector
              │               │               │
              ▼               ▼               ▼
        FTP Evidence      SSH Evidence     HTTP Evidence
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
                    GenericTCPDetector
                              │
                              ▼
                           RESULTS
```
The modular design allows individual service detectors to be maintained independently.
---
🏗️ Internal Workflow
```text
             ┌───────────────────┐
             │     CLI INPUT     │
             │ Target + Ports    │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │  PORT VALIDATION  │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │  PORT SELECTION   │
             │ common/custom/all │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │   TCP SYN SCAN    │
             └─────────┬─────────┘
                       │
                       ▼
                  Open Ports
                       │
                       ▼
             ┌───────────────────┐
             │ ENUMERATION LAYER │
             └─────────┬─────────┘
                       │
                       ▼
             ┌───────────────────┐
             │ DETECTOR MANAGER  │
             └─────────┬─────────┘
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
       Dedicated Detector   Generic Detector
              │                 │
              └────────┬────────┘
                       │
                       ▼
             ┌───────────────────┐
             │      RESULTS      │
             └───────────────────┘
```
---
🧪 Verification
Main Application Import
```bash
python3 -c "import synrecon; print('SYN RECON import: OK')"
```
Expected:
```text
SYN RECON import: OK
```
---
Detector Manager
```bash
python3 -c "from detectors.manager import DetectorManager; print('DetectorManager: OK')"
```
Expected:
```text
DetectorManager: OK
```
---
Compile Main Application
```bash
python3 -m py_compile synrecon.py
```
---
Compile Scanner Modules
```bash
python3 -m py_compile scanner/tcp.py
python3 -m py_compile scanner/enumerator.py
```
---
Compile Detectors
```bash
python3 -m py_compile detectors/*.py
```
---
📁 Project Structure
```text
SYN RECON
│
├── synrecon.py
│
├── scanner/
│   ├── tcp.py
│   └── enumerator.py
│
├── detectors/
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
│   ├── models.py
│   └── port_modes.py
│
├── output/
│
├── logger.py
├── port_parser.py
├── service_detector.py
├── validation.py
└── requirements.txt
```
---
📈 Project Status
SYN RECON v1.0.1
Current Implementation
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
🔐 Ethical Use
SYN RECON is intended only for authorized security testing and controlled laboratory environments.
Use SYN RECON only against:
Systems you own
Personal laboratory systems
Authorized testing targets
Systems for which you have explicit permission to perform security testing
> **Do not scan systems or networks without authorization.**
The example target shown in this documentation represents a controlled laboratory environment.
The responsibility for using this tool legally and ethically belongs to the user.
---
👨‍💻 Author
Ananthu K Santhosh
Cybersecurity | Ethical Hacking | Network Security
GitHub:  
https://github.com/ananthuksanthosh
Project:  
https://github.com/ananthuksanthosh/synrecon
---
📄 License
SYN RECON is released under the MIT License.
Copyright © 2026 Ananthu K Santhosh.
See `LICENSE` for the complete license text.
---
<div align="center">
⚡ SYN RECON v1.0.1
Python • Scapy • TCP/IP • Linux
Built for cybersecurity education, authorized security testing,  
network reconnaissance, and security research.
<br>
Ananthu K Santhosh
</div>
