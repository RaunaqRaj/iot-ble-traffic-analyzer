from src.config import (
    PACKET_SIZE_STD_MULTIPLIER,
    FREQUENCY_THRESHOLD_MULTIPLIER
)


def test_packet_size_multiplier():
    assert PACKET_SIZE_STD_MULTIPLIER == 2


def test_frequency_multiplier():
    assert FREQUENCY_THRESHOLD_MULTIPLIER == 5