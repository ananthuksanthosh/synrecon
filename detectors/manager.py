#!/usr/bin/env python3

from detectors.http import HTTPDetector
from detectors.https import HTTPSDetector
from detectors.ssh import SSHDetector
from detectors.ftp import FTPDetector
from detectors.mqtt import MQTTDetector
from detectors.smtp import SMTPDetector
from detectors.dns import DNSDetector
from detectors.mysql import MySQLDetector
from detectors.postgresql import PostgreSQLDetector
from detectors.vnc import VNCDetector
from detectors.telnet import TelnetDetector
from detectors.smb import SMBDetector
from detectors.tomcat import TomcatDetector
from detectors.generic import GenericTCPDetector


class DetectorManager:

    def __init__(self):

        self.detectors = [
            HTTPDetector(),
            HTTPSDetector(),
            SSHDetector(),
            FTPDetector(),
            MQTTDetector(),
            SMTPDetector(),
            DNSDetector(),
            MySQLDetector(),
            PostgreSQLDetector(),
            VNCDetector(),
            TelnetDetector(),
            SMBDetector(),
            TomcatDetector(),
        ]

        self.generic = GenericTCPDetector()

    def get_detector(self, port):

        for detector in self.detectors:

            if port in detector.ports:
                return detector

        return self.generic

    def detect(
        self,
        target,
        port,
        timeout=2.0
    ):

        detector = self.get_detector(port)

        if detector is None:
            return None

        return detector.detect(
            target,
            port,
            timeout
        )
