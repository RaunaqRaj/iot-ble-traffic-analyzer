from scapy.all import BTLE, BTLE_ADV, BTLE_ADV_IND, Raw, wrpcap
from datetime import datetime, timedelta
import random

OUTPUT_FILE = "data/raw/ble_test_capture.pcap"

NORMAL_DEVICES = [
    "AA:BB:CC:DD:EE:01",
    "AA:BB:CC:DD:EE:02",
    "AA:BB:CC:DD:EE:03",
    "AA:BB:CC:DD:EE:04",
]

ANOMALOUS_DEVICE = "AA:BB:CC:DD:EE:99"


def create_packet(device, payload_size=20):

    return (
        BTLE()
        / BTLE_ADV()
        / BTLE_ADV_IND(
            AdvA=device
        )
        / Raw(
            load=bytes(
                random.randint(0, 255)
                for _ in range(payload_size)
            )
        )
    )


def generate_capture():

    packets = []
    start_time = datetime.now()

    packet_index = 0

    # Normal traffic
    for device in NORMAL_DEVICES:

        for _ in range(50):

            packet = create_packet(
                device,
                payload_size=random.randint(10, 20)
            )

            packet.time = (
                start_time
                + timedelta(
                    milliseconds=packet_index * 100
                )
            ).timestamp()

            packets.append(packet)

            packet_index += 1

    # High-frequency anomalous device
    for _ in range(80):

        packet = create_packet(
            ANOMALOUS_DEVICE,
            payload_size=random.randint(10, 20)
        )

        packet.time = (
            start_time
            + timedelta(
                milliseconds=packet_index * 10
            )
        ).timestamp()

        packets.append(packet)

        packet_index += 1

    # Large-payload anomalies
    for _ in range(20):

        device = random.choice(NORMAL_DEVICES)

        packet = create_packet(
            device,
            payload_size=80
        )

        packet.time = (
            start_time
            + timedelta(
                milliseconds=packet_index * 100
            )
        ).timestamp()

        packets.append(packet)

        packet_index += 1

    return packets


def main():

    print("=" * 60)
    print("BLE ANOMALOUS TEST CAPTURE GENERATOR")
    print("=" * 60)

    packets = generate_capture()

    wrpcap(
        OUTPUT_FILE,
        packets
    )

    print(f"\nGenerated packets : {len(packets)}")

    print("\nNormal devices:")

    for device in NORMAL_DEVICES:
        print(f"  - {device}")

    print("\nAnomalous device:")
    print(f"  - {ANOMALOUS_DEVICE}")

    print("\nLarge payload packets: 20")


if __name__ == "__main__":
    main()