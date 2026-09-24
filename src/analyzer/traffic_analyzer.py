from scapy.all import *
from collections import Counter


def create_test_packets():

    packets = []

    devices = [
        "AA:BB:CC:DD:EE:01",
        "AA:BB:CC:DD:EE:02",
        "AA:BB:CC:DD:EE:03"
    ]

    for device in devices:

        for _ in range(5):

            packet = (
                BTLE()
                / BTLE_ADV()
                / BTLE_ADV_IND(
                    AdvA=device
                )
            )

            packets.append(packet)

    return packets


def analyze_traffic(packets):

    total_packets = len(packets)

    devices = []

    packet_types = []

    packet_sizes = []

    for packet in packets:

        if packet.haslayer(BTLE_ADV_IND):

            device = packet[BTLE_ADV_IND].AdvA

            devices.append(device)

            packet_types.append("BLE Advertising Indication")

            packet_sizes.append(len(packet))

    unique_devices = set(devices)

    packet_type_counts = Counter(packet_types)

    print("\n" + "=" * 60)
    print("BLE TRAFFIC ANALYSIS")
    print("=" * 60)

    print(f"\nTotal Packets       : {total_packets}")

    print(f"Unique Devices      : {len(unique_devices)}")

    print(
        f"Average Packet Size : "
        f"{sum(packet_sizes) / len(packet_sizes):.2f} bytes"
    )

    print("\nPacket Types:")

    for packet_type, count in packet_type_counts.items():

        print(f"  {packet_type}: {count}")

    print("\nDevices:")

    device_counts = Counter(devices)

    for device, count in device_counts.items():

        print(f"  {device}: {count} packets")


def main():

    packets = create_test_packets()

    analyze_traffic(packets)


if __name__ == "__main__":

    main()