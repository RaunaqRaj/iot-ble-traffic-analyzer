from pathlib import Path
import csv

from scapy.all import rdpcap, BTLE_ADV_IND, Raw


INPUT_FILE = "data/raw/ble_test_capture.pcap"
OUTPUT_FILE = "data/processed/ble_packets.csv"


def extract_packets(input_file):
    path = Path(input_file)

    if not path.exists():
        raise FileNotFoundError(
            f"Capture file not found: {input_file}"
        )

    packets = rdpcap(str(path))
    records = []

    for packet_id, packet in enumerate(packets, start=1):

        if packet.haslayer(BTLE_ADV_IND):

            ble_packet = packet[BTLE_ADV_IND]
            
            payload_size = 0

            if ble_packet.data:
                for item in ble_packet.data:
                    try:
                        payload_size += len(bytes(item))
                    except Exception:
                        pass

            record = {
                "packet_id": packet_id,
                "timestamp": float(packet.time),
                "device_address": ble_packet.AdvA,
                "packet_type": "BLE_ADVERTISING_IND",
                "packet_length": len(packet),
                "payload_size": payload_size
            }

            records.append(record)

    return records


def save_to_csv(records, output_file):

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "packet_id",
        "timestamp",
        "device_address",
        "packet_type",
        "packet_length",
        "payload_size"
    ]

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(records)


def main():

    print("=" * 60)
    print("BLE PCAP EXTRACTOR")
    print("=" * 60)

    records = extract_packets(INPUT_FILE)

    save_to_csv(
        records,
        OUTPUT_FILE
    )

    print(f"\nPackets extracted : {len(records)}")
    print(f"CSV file          : {OUTPUT_FILE}")

    print("\nFirst 5 records:")

    for record in records[:5]:
        print(record)


if __name__ == "__main__":
    main()