from pathlib import Path
from scapy.all import rdpcap


def read_capture(file_path):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Capture file not found: {path}"
        )

    return rdpcap(str(path))


def main():

    capture_path = "data/raw/ble_test_capture.pcap"

    packets = read_capture(capture_path)

    print("=" * 60)
    print("BLE CAPTURE READER")
    print("=" * 60)

    print(f"\nTotal packets read: {len(packets)}")

    print("\nFirst 10 packets:")

    for packet in packets[:10]:

        print(
            f"{packet.time} | "
            f"{packet.summary()}"
        )


if __name__ == "__main__":
    main()