# Network Traffic & Signalling Protocol Analyzer (IoT/BLE)

A Python-based BLE traffic analysis and anomaly detection platform designed to analyze device behavior, identify unusual traffic patterns, store packet-level analytics in PostgreSQL, generate automated reports, and visualize network activity through Power BI.

> **Project status:** Core pipeline completed and tested.

---

## Overview

IoT and Bluetooth Low Energy (BLE) devices can generate large amounts of traffic that are difficult to inspect manually.

This project provides an automated analysis pipeline that:

- Generates controlled BLE test traffic
- Creates a PCAP capture
- Extracts BLE packet information
- Stores packet-level data in PostgreSQL
- Calculates traffic metrics
- Detects unusual traffic behavior
- Classifies device-level behavioral risk
- Generates automated reports
- Visualizes traffic through Power BI
- Provides automated testing with pytest
- Uses centralized logging for troubleshooting

The current implementation uses **controlled synthetic BLE traffic generated with Scapy**. This provides reproducible traffic patterns for development, testing, and anomaly-detection experiments.

> **Important:** The current implementation is not presented as a live over-the-air BLE capture system.

---

## Architecture

```text
BLE / IoT Test Traffic
          |
          v
   Scapy Packet Generator
          |
          v
       PCAP File
          |
          v
    Python Packet Parser
          |
          v
    Processed CSV Data
          |
          v
      PostgreSQL
          |
          +----------------------+
          |                      |
          v                      v
   Traffic Analysis       Anomaly Detection
          |                      |
          +----------+-----------+
                     |
                     v
          Device Behavior Analysis
                     |
                     v
             Automated Reports
                     |
                     v
                 Power BI