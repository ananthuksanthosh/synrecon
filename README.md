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
