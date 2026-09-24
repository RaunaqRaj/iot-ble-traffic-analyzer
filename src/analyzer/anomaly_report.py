import pandas as pd
from database.db_connection import get_connection

OUTPUT_FILE = "data/processed/anomaly_report.csv"


def load_anomaly_data():
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
        WHERE is_anomaly = TRUE
        ORDER BY timestamp
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


def classify_anomaly(row):

    if (
        row["large_packet_anomaly"]
        and row["high_frequency_anomaly"]
    ):
        return "Large Packet + High Frequency"

    if row["large_packet_anomaly"]:
        return "Large Packet"

    if row["high_frequency_anomaly"]:
        return "High Frequency"

    return "Unknown"


def classify_severity(row):

    if (
        row["large_packet_anomaly"]
        and row["high_frequency_anomaly"]
    ):
        return "HIGH"

    if row["high_frequency_anomaly"]:
        return "HIGH"

    if row["large_packet_anomaly"]:
        return "MEDIUM"

    return "LOW"

def classify_severity(row):

    if (
        row["large_packet_anomaly"]
        and row["high_frequency_anomaly"]
    ):
        return "HIGH"

    if row["high_frequency_anomaly"]:
        return "HIGH"

    if row["large_packet_anomaly"]:
        return "MEDIUM"

    return "LOW"


def main():

    print("=" * 60)
    print("BLE ANOMALY REPORT GENERATOR")
    print("=" * 60)

    df = load_anomaly_data()

    if df.empty:
        print("\nNo anomalies detected.")
        return

    df["anomaly_type"] = df.apply(
        classify_anomaly,
        axis=1
    )

    df["severity"] = df.apply(
    classify_severity,
    axis=1
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nAnomalies found : {len(df)}")
    print(f"Report saved    : {OUTPUT_FILE}")

    print("\nAnomaly Breakdown:")

    print(
        df["anomaly_type"]
        .value_counts()
        .to_string()
    )

    print("\nSeverity Breakdown:")

    print(
        df["severity"]
        .value_counts()
        .to_string()
    )

if __name__ == "__main__":
    main()