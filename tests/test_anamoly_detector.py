import pandas as pd

from src.analyzer.anomaly_detector import detect_anomalies


def test_high_frequency_anomaly_detection():

    data = {
        "packet_id": range(1, 21),

        "timestamp": [
            1000, 1001, 1002, 1003, 1004,
            1010, 1011, 1012, 1013, 1014,
            1020, 1021, 1022, 1023, 1024,
            1030.00, 1030.01, 1030.02, 1030.03, 1030.04
        ],

        "device_address": (
            ["AA:AA:AA:AA:AA:01"] * 5
            + ["AA:AA:AA:AA:AA:02"] * 5
            + ["AA:AA:AA:AA:AA:03"] * 5
            + ["AA:AA:AA:AA:AA:99"] * 5
        ),

        "packet_length": [30] * 20
    }

    df = pd.DataFrame(data)

    result = detect_anomalies(df)

    anomalous_device = result[
        result["device_address"] == "AA:AA:AA:AA:AA:99"
    ]

    assert anomalous_device["high_frequency_anomaly"].all()


def test_large_packet_anomaly_detection():

    data = {
        "packet_id": range(1, 11),

        "timestamp": [
            1000,
            1001,
            1002,
            1003,
            1004,
            1005,
            1006,
            1007,
            1008,
            1009
        ],

        "device_address": [
            "AA:AA:AA:AA:AA:01",
            "AA:AA:AA:AA:AA:01",
            "AA:AA:AA:AA:AA:01",
            "AA:AA:AA:AA:AA:01",
            "AA:AA:AA:AA:AA:01",
            "AA:AA:AA:AA:AA:02",
            "AA:AA:AA:AA:AA:02",
            "AA:AA:AA:AA:AA:02",
            "AA:AA:AA:AA:AA:02",
            "AA:AA:AA:AA:AA:02"
        ],

        "packet_length": [
            30,
            30,
            30,
            30,
            30,
            30,
            30,
            30,
            30,
            100
        ]
    }

    df = pd.DataFrame(data)

    result = detect_anomalies(df)

    large_packet = result[
        result["packet_length"] == 100
    ]

    assert large_packet["large_packet_anomaly"].all()

def test_empty_dataframe():

        df = pd.DataFrame(
        columns=[
            "packet_id",
            "timestamp",
            "device_address",
            "packet_length"
        ]
    )

        result = detect_anomalies(df)

        assert result.empty


def test_single_packet_device():

    df = pd.DataFrame([
        {
            "packet_id": 1,
            "timestamp": 1000,
            "device_address": "AA:BB:CC:DD:EE:01",
            "packet_length": 20
        }
    ])

    result = detect_anomalies(df)

    assert len(result) == 1
    assert "is_anomaly" in result.columns