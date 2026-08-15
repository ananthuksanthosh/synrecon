# SYN RECON

A lightweight Python-based TCP SYN reconnaissance and service detection tool designed for authorized security testing, cybersecurity education, and controlled laboratory environments.

SYN RECON performs TCP SYN-based port discovery and then uses modular service detectors to identify commonly encountered network services.

---

## Project Status

**Version:** 1.0.0  
**Status:** Core Development Complete

---

## Overview

SYN RECON was developed to provide a clear and understandable implementation of TCP SYN reconnaissance.

The project focuses on the complete basic reconnaissance workflow:

1. Target validation
2. Port selection
3. TCP SYN discovery
4. Port-state classification
5. Open-port filtering
6. Service enumeration
7. Service-specific detection
8. Evidence collection
9. Scan statistics
10. Clean terminal reporting

The project is intentionally lightweight and does not attempt to replace mature reconnaissance frameworks such as Nmap.

---

## Features

- TCP SYN port scanning
- Common-port scanning
- Custom port scanning
- Port-range scanning
- Full TCP port scanning
- Configurable scan timeout
- Configurable worker threads
- Concurrent port scanning
- TCP response analysis
- Open/closed/unknown state classification
- Open-port-only results table
- Modular service detection
- Service detection confidence
- Service detection evidence
- Generic TCP fallback detection
- Scan ID generation
- Scan timing
- Logging support
- Clean CLI output
- Development history and archived versions

---

## Supported Service Detection

SYN RECON currently includes dedicated detectors for:

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

When a dedicated detector is not available, SYN RECON uses a generic TCP detector.

---

## Architecture

```text
SYN RECON
│
├── synrecon.py
│   └── Main CLI and scan workflow
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
├── validation.py
├── service_detector.py
│
├── requirements.txt
├── README.md
└── development-history.log
```

---

## Scanning Workflow

### Phase 1 — TCP Discovery

SYN RECON sends TCP SYN probes to the selected ports.

The response is analyzed to determine the port state.

Typical results include:

```text
OPEN
CLOSED
UNKNOWN
```

An open TCP port is identified when a SYN/ACK response is received.

### Phase 2 — Service Enumeration

Only ports identified as `OPEN` are passed to the service enumeration layer.

The `DetectorManager` selects the appropriate service detector based on the port.

For example:

```text
21    → FTPDetector
22    → SSHDetector
23    → TelnetDetector
25    → SMTPDetector
53    → DNSDetector
80    → HTTPDetector
139   → SMBDetector
445   → SMBDetector
1883  → MQTTDetector
3306  → MySQLDetector
5432  → PostgreSQLDetector
5900  → VNCDetector
8180  → TomcatDetector
```

If no dedicated detector matches the port, the generic TCP detector is used.

---

## Port Selection Modes

SYN RECON supports multiple ways to specify ports.

### Common Ports

```bash
sudo python3 synrecon.py 192.168.56.9 --ports common --workers 20
```

The `common` mode scans the predefined list of commonly encountered TCP ports.

### Specific Ports

```bash
sudo python3 synrecon.py 192.168.56.9 --ports 21,22,80,8180
```

### Port Range

```bash
sudo python3 synrecon.py 192.168.56.9 --ports 20-25
```

### Multiple Ports and Ranges

```bash
sudo python3 synrecon.py 192.168.56.9 --ports 20-25,80,443,3306
```

### All TCP Ports

```bash
sudo python3 synrecon.py 192.168.56.9 --ports all --workers 50
```

---

## Command-Line Options

A typical scan uses:

```bash
sudo python3 synrecon.py <target> --ports <ports> --workers <number>
```

Example:

```bash
sudo python3 synrecon.py 192.168.56.9 --ports common --workers 20
```

The scanner also supports configurable timeout values where provided by the CLI.

---

## Example Scan

The following example was produced while testing SYN RECON against a controlled Metasploitable2 laboratory target.

```text
S Y N   R E C O N
TCP SYN RECONNAISSANCE TOOL

SCAN INFORMATION
────────────────────────────────────────────────────────────
 Target      : 192.168.56.9
 Ports       : 78
 Workers     : 20
 Timeout     : 2.0s

PHASE 1 — TCP DISCOVERY
────────────────────────────────────────────────────────────
Scanning 78 TCP ports...
[+] Discovery complete: 16 open port(s) found

PHASE 2 — SERVICE ENUMERATION
────────────────────────────────────────────────────────────
Enumerating 16 open port(s)...

RESULTS
────────────────────────────────────────────────────────────
PORT    SERVICE           RESPONSE      LATENCY
────────────────────────────────────────────────────────────
21      FTP               SYN/ACK       ...
22      SSH               SYN/ACK       ...
23      Telnet            SYN/ACK       ...
25      SMTP              SYN/ACK       ...
53      DNS               SYN/ACK       ...
80      HTTP              SYN/ACK       ...
111     TCP               SYN/ACK       ...
139     SMB               SYN/ACK       ...
445     SMB               SYN/ACK       ...
2049    TCP               SYN/ACK       ...
3306    MySQL             SYN/ACK       ...
5432    PostgreSQL        SYN/ACK       ...
5900    VNC               SYN/ACK       ...
6667    TCP               SYN/ACK       ...
6697    TCP               SYN/ACK       ...
8180    Tomcat            SYN/ACK       ...

SUMMARY
────────────────────────────────────────────────────────────
 Open         : 16
 Closed       : 62
 No response  : 0
 Unknown      : 0
```

The main `RESULTS` table intentionally displays only open ports.

The summary retains the complete scan statistics.

---

## Service Detection Evidence

Service detectors can provide evidence supporting their identification.

### FTP

```text
Service     : FTP
Confidence  : CONFIRMED
Detail      : 220 (vsFTPd 2.3.4)
```

### SSH

```text
Service     : SSH
Confidence  : CONFIRMED
Detail      : SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1
```

### Telnet

Telnet negotiation data can contain binary protocol bytes. SYN RECON therefore avoids displaying the raw binary data.

Instead, it reports:

```text
Service     : Telnet
Confidence  : CONFIRMED
Evidence    : TELNET_NEGOTIATION
Detail      : Telnet negotiation detected
```

### SMB

```text
Service     : SMB
Confidence  : CONFIRMED
Evidence    : SMB_NEGOTIATION
Detail      : SMB negotiation response received
```

### MySQL

```text
Service     : MySQL
Confidence  : CONFIRMED
Evidence    : MYSQL_GREETING
Detail      : MySQL 5.0.51a-3ubuntu5
```

### PostgreSQL

```text
Service     : PostgreSQL
Confidence  : CONFIRMED
Evidence    : POSTGRES_SSL_RESPONSE
Detail      : PostgreSQL service supports SSL negotiation
```

### VNC

```text
Service     : VNC
Confidence  : CONFIRMED
Evidence    : RFB_GREETING
Detail      : RFB protocol version 003.003
```

### Tomcat

```text
Service     : Tomcat
Confidence  : CONFIRMED
Evidence    : TOMCAT_HTTP
Detail      : Apache Tomcat HTTP response detected
```

---

## Generic TCP Detection

SYN RECON does not attempt to identify every possible network service.

For unsupported ports, the generic detector can establish a TCP connection and optionally collect an initial banner.

For example:

```text
Service     : TCP
Confidence  : CONFIRMED
Detail      : TCP connection established; no banner received
```

This keeps the project lightweight instead of attempting to reproduce the complete service fingerprinting capabilities of Nmap.

---

## Testing Environment

SYN RECON was developed and tested in a controlled cybersecurity laboratory environment.

### Primary Environment

- Kali Linux
- Python 3
- VirtualBox
- Scapy

### Testing Tools

- Metasploitable2
- Nmap
- Wireshark

Metasploitable2 was used as an intentionally vulnerable laboratory target to provide multiple open network services for testing.

Example target:

```text
192.168.56.9
```

---

## Validation

The project's Python modules were validated using Python's bytecode compiler.

```bash
python3 -m py_compile synrecon.py
python3 -m py_compile core/port_modes.py
python3 -m py_compile scanner/tcp.py
python3 -m py_compile scanner/enumerator.py
python3 -m py_compile detectors/*.py
```

Successful compilation produces no output.

The project was also tested through:

- Common-port scans
- Specific-port scans
- Port-range scans
- Service detector tests
- Detector manager tests
- Metasploitable2 scans
- TCP discovery tests

---

## Project Testing Examples

### Test Service Detector

```bash
sudo python3 -c "from detectors.manager import DetectorManager; m=DetectorManager(); print(m.detect('192.168.56.9',23))"
```

Example:

```text
('Telnet', 'Telnet negotiation detected', 'TELNET_NEGOTIATION')
```

### Test SMB Detector

```bash
sudo python3 -c "from detectors.manager import DetectorManager; m=DetectorManager(); print(m.detect('192.168.56.9',139)); print(m.detect('192.168.56.9',445))"
```

Example:

```text
('SMB', 'SMB negotiation response received', 'SMB_NEGOTIATION')
```

### Test Tomcat Detector

```bash
sudo python3 -c "from detectors.manager import DetectorManager; m=DetectorManager(); print(m.detect('192.168.56.9',8180))"
```

Example:

```text
('Tomcat', 'Apache Tomcat HTTP response detected', 'TOMCAT_HTTP')
```

---

## Technology Stack

- Python 3
- Scapy
- Linux
- TCP/IP
- VirtualBox

---

## Development Environment

- Kali Linux
- VirtualBox
- Metasploitable2
- Wireshark
- Nmap
- Python 3

---

## Design Principles

SYN RECON follows several simple design principles.

### Modular

Service detection is separated into individual detector modules.

### Lightweight

The project focuses on fundamental reconnaissance instead of attempting to implement every feature of a mature security scanner.

### Evidence-Based

Service identification is based on protocol responses, greetings, negotiation messages, and other observable evidence.

### Extensible

New service detectors can be added without rewriting the complete scanning engine.

### Educational

The code is structured to make TCP SYN scanning and service enumeration easier to understand.

---

## Limitations

SYN RECON is intentionally a lightweight reconnaissance tool and is not intended to replace mature tools such as Nmap.

Current limitations include:

- Limited number of dedicated service detectors
- Generic TCP fallback for unsupported services
- No vulnerability scanning
- No exploit functionality
- No automated OS fingerprinting
- No complete service fingerprint database
- Limited protocol-specific enumeration
- No attempt to reproduce the complete feature set of Nmap

The project focuses on implementing and understanding the fundamental reconnaissance workflow.

---

## Ethical Use

SYN RECON is intended only for:

- Authorized security testing
- Cybersecurity education
- Personal cybersecurity laboratories
- Controlled penetration-testing labs
- Systems for which explicit permission has been obtained

Only scan systems that you own or systems for which you have authorization to perform security testing.

Do not use SYN RECON to scan unauthorized systems or networks.

---

## Project Goal

The primary goal of SYN RECON is to demonstrate a modular implementation of TCP SYN reconnaissance while developing practical understanding of:

- TCP/IP networking
- TCP three-way handshake
- TCP SYN scanning
- Packet crafting
- TCP response analysis
- Port-state classification
- Service detection
- Protocol evidence
- Concurrent scanning
- Modular Python architecture
- Security reconnaissance methodology

---

## License

This project is intended for educational and authorized security-testing purposes.

Use responsibly and only against systems for which you have permission.
