import subprocess
import sys


STEPS = [
    ("Generate BLE test capture", [
        sys.executable,
        "-m",
        "src.capture.generate_capture"
    ]),
    ("Extract packets from PCAP", [
        sys.executable,
        "-m",
        "src.parser.pcap_extractor"
    ]),
    ("Load packets into PostgreSQL", [
        sys.executable,
        "-m",
        "src.database.load_packets"
    ]),
    ("Detect anomalies", [
        sys.executable,
        "-m",
        "src.analyzer.anomaly_detector"
    ]),
    ("Analyze device behavior", [
        sys.executable,
        "-m",
        "src.analyzer.device_analyzer"
    ]),
    ("Generate anomaly report", [
        sys.executable,
        "-m",
        "src.analyzer.anomaly_report"
    ]),
    ("Generate project summary", [
        sys.executable,
        "-m",
        "src.analyzer.project_summary"
    ])
]


def run_step(name, command):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"\nFAILED: {name}")
        return False

    print(f"\nCOMPLETED: {name}")
    return True


def main():
    print("=" * 70)
    print("IOT/BLE TRAFFIC ANALYSIS PIPELINE")
    print("=" * 70)

    for name, command in STEPS:
        success = run_step(name, command)

        if not success:
            print("\nPipeline stopped because a step failed.")
            sys.exit(1)

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()