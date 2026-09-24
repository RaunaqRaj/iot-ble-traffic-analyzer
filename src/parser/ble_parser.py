from scapy.all import *


def inspect_ble_packet(packet):
    print("=" * 60)
    print("BLE PACKET ANALYZER")
    print("=" * 60)

    print("\nPacket Summary:")
    print(packet.summary())

    print("\nPacket Details:")
    packet.show()


def main():
    print("Creating test BLE packet...\n")

    # Create a basic BLE advertising packet
    packet = (
        BTLE()
        / BTLE_ADV()
        / BTLE_ADV_IND(
            AdvA="AA:BB:CC:DD:EE:FF"
        )
    )

    inspect_ble_packet(packet)


if __name__ == "__main__":
    main()