# Network Traffic & Signalling Protocol Analyzer (IoT/BLE)

A Python-based BLE traffic analysis and anomaly detection platform designed to monitor device behavior, identify unusual traffic patterns, store packet-level data in PostgreSQL, and visualize network activity through Power BI.

## Overview

IoT and BLE devices generate continuous network traffic that can be difficult to analyze manually. This project provides an automated pipeline for extracting BLE packet information, analyzing traffic behavior, detecting anomalies, classifying device risk, and generating analytical reports.

The project currently uses controlled synthetic BLE traffic generated with Scapy to provide reproducible testing and analysis.

> **Note:** The current implementation uses synthetic/test BLE traffic. It is not presented as a live over-the-air BLE capture system.

---

## Architecture

```text
BLE / IoT Traffic
       |
       v
Packet Capture / PCAP
       |
       v
Python Packet Parser
       |
       v
Traffic Analyzer
       |
       +-------------------+
       |                   |
       v                   v
 PostgreSQL          Anomaly Detection
       |                   |
       +---------+---------+
                 |
                 v
        Device Behavior Analysis
                 |
                 v
        Automated Reports
                 |
                 v
             Power BI