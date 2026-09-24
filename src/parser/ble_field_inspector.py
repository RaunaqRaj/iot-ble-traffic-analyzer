from scapy.all import rdpcap, BTLE_ADV_IND

INPUT_FILE = "data/raw/ble_test_capture.pcap"


def main():
    packets = rdpcap(INPUT_FILE)

    for packet in packets:
        if packet.haslayer(BTLE_ADV_IND):
            print("=" * 60)
            print("BLE ADVERTISING PACKET FIELDS")
            print("=" * 60)

            packet[BTLE_ADV_IND].show()

            print("\nAvailable fields:")
            for field in packet[BTLE_ADV_IND].fields_desc:
                print(f"- {field.name}")

            break


if __name__ == "__main__":
    main()