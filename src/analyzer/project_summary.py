import pandas as pd
from database.db_connection import get_connection

OUTPUT_FILE = "data/processed/project_summary.txt"


def load_data():
    connection = get_connection()

    query = """
        SELECT
            packet_id,
            timestamp,
            device_address,
            packet_length,
            payload_size,
            packets_per_second,
            is_anomaly,
            large_packet_anomaly,
            high_frequency_anomaly
        FROM ble_packets
        ORDER BY timestamp
    """

    df = pd.read_sql_query(query, connection)
    connection.close()

    return df


def generate_summary(df):

    total_packets = len(df)

    total_devices = df["device_address"].nunique()

    total_anomalies = int(df["is_anomaly"].sum())

    normal_packets = total_packets - total_anomalies

    anomaly_percentage = (
        total_anomalies / total_packets * 100
    )

    highest_traffic_device = (
        df.groupby("device_address")
        .size()
        .idxmax()
    )

    highest_traffic_count = (
        df.groupby("device_address")
        .size()
        .max()
    )

    high_frequency_count = int(
        df["high_frequency_anomaly"].sum()
    )

    large_packet_count = int(
        df["large_packet_anomaly"].sum()
    )

    summary = f"""
BLE NETWORK TRAFFIC ANALYTICS SUMMARY
=====================================

Traffic Overview
----------------
Total packets        : {total_packets}
Unique devices       : {total_devices}
Normal packets       : {normal_packets}
Anomalous packets    : {total_anomalies}
Anomaly percentage   : {anomaly_percentage:.2f}%

Anomaly Breakdown
-----------------
High-frequency      : {high_frequency_count}
Large-packet        : {large_packet_count}

Traffic Analysis
----------------
Most active device  : {highest_traffic_device}
Packet count        : {highest_traffic_count}

Device Packet Counts
--------------------
"""

    device_counts = (
        df.groupby("device_address")
        .size()
        .sort_values(ascending=False)
    )

    for device, count in device_counts.items():
        summary += f"{device} : {count} packets\n"

    return summary


def main():

    print("=" * 60)
    print("BLE PROJECT ANALYTICS SUMMARY")
    print("=" * 60)

    df = load_data()

    summary = generate_summary(df)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(summary)

    print("\n" + summary)

    print(f"\nSummary saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()