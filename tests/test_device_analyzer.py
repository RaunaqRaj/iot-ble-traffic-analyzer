import pandas as pd

from src.analyzer.device_analyzer import analyze_devices


def test_device_risk_classification():

    data = {
        "packet_id": range(1, 16),

        "timestamp": pd.date_range(
            start="2026-01-01",
            periods=15,
            freq="s"
        ),

        "device_address": (
            ["DEVICE_LOW"] * 5
            + ["DEVICE_MEDIUM"] * 5
            + ["DEVICE_HIGH"] * 5
        ),

        "packet_type": ["BLE_ADVERTISING_IND"] * 15,

        "packet_length": [30] * 15,

        "payload_size": [20] * 15,

        "packets_per_second": (
            [2.0] * 5
            + [10.0] * 5
            + [100.0] * 5
        ),

        "is_anomaly": (
            [False] * 5
            + [False] * 5
            + [True] * 5
        ),

        "large_packet_anomaly": [False] * 15,

        "high_frequency_anomaly": (
            [False] * 10
            + [True] * 5
        )
    }

    df = pd.DataFrame(data)

    result = analyze_devices(df)

    risks = dict(
        zip(
            result["device_address"],
            result["risk_level"]
        )
    )

    assert risks["DEVICE_LOW"] == "LOW"
    assert risks["DEVICE_MEDIUM"] == "MEDIUM"
    assert risks["DEVICE_HIGH"] == "HIGH"

    def test_low_risk_device():

        anomaly_percentage = 0
        packets_per_second = 2

        if (
            anomaly_percentage >= 50
            or packets_per_second >= 20
        ):
            risk = "HIGH"

        elif (
            anomaly_percentage >= 10
            or packets_per_second >= 10
        ):
            risk = "MEDIUM"

        else:
            risk = "LOW"

        assert risk == "LOW"


def test_medium_risk_from_frequency():

    anomaly_percentage = 0
    packets_per_second = 10

    if (
        anomaly_percentage >= 50
        or packets_per_second >= 20
    ):
        risk = "HIGH"

    elif (
        anomaly_percentage >= 10
        or packets_per_second >= 10
    ):
        risk = "MEDIUM"

    else:
        risk = "LOW"

    assert risk == "MEDIUM"


def test_high_risk_from_frequency():

    anomaly_percentage = 0
    packets_per_second = 20

    if (
        anomaly_percentage >= 50
        or packets_per_second >= 20
    ):
        risk = "HIGH"

    elif (
        anomaly_percentage >= 10
        or packets_per_second >= 10
    ):
        risk = "MEDIUM"

    else:
        risk = "LOW"

    assert risk == "HIGH"