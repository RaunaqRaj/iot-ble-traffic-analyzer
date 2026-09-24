from scapy.all import *


def extract_packet_info(packet):

    information = {
        "packet_type": "Unknown",
        "device_address": None,
        "packet_length": len(packet)
    }

    if packet.haslayer(BTLE_ADV_IND):
        information["packet_type"] = "BLE Advertising Indication"

        information["device_address"] = (
            packet[BTLE_ADV_IND].AdvA
        )

    return information


if __name__ == "__main__":

    packet = (
        BTLE()
        / BTLE_ADV()
        / BTLE_ADV_IND(
            AdvA="AA:BB:CC:DD:EE:FF"
        )
    )

    result = extract_packet_info(packet)

    print("\nExtracted Information:")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")