import pandas as pd

from src.analyzer.anomaly_report import classify_anomaly


def test_high_frequency_classification():

    row = pd.Series({
        "large_packet_anomaly": False,
        "high_frequency_anomaly": True
    })

    assert classify_anomaly(row) == "High Frequency"


def test_large_packet_classification():

    row = pd.Series({
        "large_packet_anomaly": True,
        "high_frequency_anomaly": False
    })

    assert classify_anomaly(row) == "Large Packet"


def test_combined_classification():

    row = pd.Series({
        "large_packet_anomaly": True,
        "high_frequency_anomaly": True
    })

    assert (
        classify_anomaly(row)
        == "Large Packet + High Frequency"
    )

    def test_combined_anomaly_classification():

        large_packet = True
        high_frequency = True

        if large_packet and high_frequency:
            classification = "Large Packet + High Frequency"

        elif large_packet:
            classification = "Large Packet"

        elif high_frequency:
            classification = "High Frequency"

        else:
            classification = "Normal"

        assert classification == "Large Packet + High Frequency"