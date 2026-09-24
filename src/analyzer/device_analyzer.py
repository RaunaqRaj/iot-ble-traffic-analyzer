import pandas as pd
from database.db_connection import get_connection

OUTPUT_FILE = "data/processed/device_behavior_report.csv"
SUMMARY_FILE = "data/processed/device_behavior_summary.txt"

def load_data():
    connection = get_connection()

    query = """
        SELECT
            packet_id,
            timestamp,
            device_address,
            packet_type,
            packet_length,
            payload_size,
            packets_per_second,
            is_anomaly,
            large_packet_anomaly,
            high_frequency_anomaly
        FROM ble_packets
        ORDER BY packet_id
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


def analyze_devices(df):

    df["datetime"] = pd.to_datetime(df["timestamp"])

    device_report = (
        df.groupby("device_address")
        .agg(
            packet_count=("packet_id", "count"),

            avg_packet_length=(
                "packet_length",
                "mean"
            ),

            min_packet_length=(
                "packet_length",
                "min"
            ),

            max_packet_length=(
                "packet_length",
                "max"
            ),

            avg_payload_size=(
                "payload_size",
                "mean"
            ),

            packets_per_second=(
                "packets_per_second",
                "max"
            ),

            anomaly_count=(
                "is_anomaly",
                "sum"
            ),

            large_packet_anomaly_count=(
                "large_packet_anomaly",
                "sum"
            ),

            high_frequency_anomaly_count=(
                "high_frequency_anomaly",
                "sum"
            ),

            first_seen=(
                "datetime",
                "min"
            ),

            last_seen=(
                "datetime",
                "max"
            )
        )
        .reset_index()
    )

    # Calculate anomaly percentage
    device_report["anomaly_percentage"] = (
        device_report["anomaly_count"]
        / device_report["packet_count"]
        * 100
    )

    # Default risk
    device_report["risk_level"] = "LOW"

    # Medium risk
    medium_condition = (
        (device_report["anomaly_percentage"] >= 10)
        |
        (device_report["packets_per_second"] >= 10)
    )

    device_report.loc[
        medium_condition,
        "risk_level"
    ] = "MEDIUM"

    # High risk
    high_condition = (
        (device_report["anomaly_percentage"] >= 50)
        |
        (device_report["packets_per_second"] >= 20)
    )

    device_report.loc[
        high_condition,
        "risk_level"
    ] = "HIGH"

    return device_report


def main():

    print("=" * 60)
    print("BLE DEVICE BEHAVIOR ANALYZER")
    print("=" * 60)

    # Load packet data from PostgreSQL
    df = load_data()

    print(f"\nPackets loaded : {len(df)}")

    # Analyze devices
    device_report = analyze_devices(df)

    # Round numerical values
    device_report["avg_packet_length"] = (
        device_report["avg_packet_length"].round(2)
    )

    device_report["avg_payload_size"] = (
        device_report["avg_payload_size"].round(2)
    )

    device_report["packets_per_second"] = (
        device_report["packets_per_second"].round(2)
    )

    device_report["anomaly_percentage"] = (
        device_report["anomaly_percentage"].round(2)
    )

    # Save report
    device_report.to_csv(
        OUTPUT_FILE,
        index=False
    )

        # Generate human-readable summary
    total_devices = len(device_report)

    high_risk_count = (
        device_report["risk_level"] == "HIGH"
    ).sum()

    medium_risk_count = (
        device_report["risk_level"] == "MEDIUM"
    ).sum()

    low_risk_count = (
        device_report["risk_level"] == "LOW"
    ).sum()

    total_anomalies = int(
        device_report["anomaly_count"].sum()
    )

    highest_risk_device = device_report.loc[
        device_report["packets_per_second"].idxmax()
    ]

    summary = f"""
        BLE DEVICE BEHAVIOR ANALYSIS REPORT
        ====================================

        Total Devices Analyzed : {total_devices}
        Total Packets Analyzed : {len(df)}
        Total Anomalies        : {total_anomalies}

        Risk Distribution
        -----------------
        HIGH   : {high_risk_count}
        MEDIUM : {medium_risk_count}
        LOW    : {low_risk_count}

        Highest Traffic Device
        ----------------------
        Device              : {highest_risk_device["device_address"]}
        Packets/sec         : {highest_risk_device["packets_per_second"]}
        Anomaly Count       : {highest_risk_device["anomaly_count"]}
        Anomaly Percentage  : {highest_risk_device["anomaly_percentage"]}%
        Risk Level          : {highest_risk_device["risk_level"]}

        ====================================
        """

    with open(SUMMARY_FILE, "w") as file:
        file.write(summary)

    print(f"Summary saved    : {SUMMARY_FILE}")

    print(f"Devices analyzed : {len(device_report)}")
    print(f"Report saved     : {OUTPUT_FILE}")

    print("\nDevice Risk Summary:")
    print(
        device_report[
            [
                "device_address",
                "packet_count",
                "packets_per_second",
                "anomaly_count",
                "anomaly_percentage",
                "risk_level"
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()