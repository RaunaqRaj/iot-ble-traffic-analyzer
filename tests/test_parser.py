from scapy.all import IP, TCP, Raw
from src.parser.ble_parser import inspect_ble_packet


def test_packet_creation():

    packet = (
        IP(src="192.168.1.10", dst="192.168.1.20")
        / TCP(sport=1234, dport=80)
        / Raw(load=b"test")
    )

    assert packet is not None
    assert packet.haslayer(IP)
    assert packet.haslayer(TCP)
    assert packet.haslayer(Raw)