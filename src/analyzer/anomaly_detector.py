import pandas as pd
from database.db_connection import get_connection


INPUT_FILE = "data/processed/ble_packets.csv"


def load_data():
    return pd.read_csv(INPUT_FILE)


def detect_anomalies(df):

    df["datetime"] = pd.to_datetime(
        df["timestamp"],
        unit="s"
    )

    # -------------------------------
    # Packet size anomaly
    # -------------------------------

    packet_length_mean = df["packet_length"].mean()
    packet_length_std = df["packet_length"].std()

    packet_length_threshold = (
        packet_length_mean +
        (2 * packet_length_std)
    )

    df["large_packet_anomaly"] = (
        df["packet_length"] >
        packet_length_threshold
    )

    # -------------------------------
    # Device frequency
    # -------------------------------

    device_stats = (
        df.groupby("device_address")
        .agg(
            packet_count=("packet_id", "count"),
            first_seen=("datetime", "min"),
            last_seen=("datetime", "max")
        )
        .reset_index()
    )

    device_stats["duration_seconds"] = (
        device_stats["last_seen"] -
        device_stats["first_seen"]
    ).dt.total_seconds()

    device_stats["duration_seconds"] = (
        device_stats["duration_seconds"]
        .replace(0, 1)
    )

    device_stats["packets_per_second"] = (
        device_stats["packet_count"] /
        device_stats["duration_seconds"]
    )

    df = df.merge(
        device_stats[
            [
                "device_address",
                "packets_per_second"
            ]
        ],
        on="device_address",
        how="left"
    )

    # -------------------------------
    # Frequency anomaly
    # -------------------------------

    frequency_median = (
        device_stats["packets_per_second"].median()
    )

    frequency_threshold = (
        frequency_median * 5
    )

    df["high_frequency_anomaly"] = (
        df["packets_per_second"] >
        frequency_threshold
    )

    # -------------------------------
    # Final anomaly
    # -------------------------------

    df["is_anomaly"] = (
        df["large_packet_anomaly"] |
        df["high_frequency_anomaly"]
    )

    return df


def save_to_database(df):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE ble_packets
        SET
            packets_per_second = %s,
            is_anomaly = %s,
            large_packet_anomaly = %s,
            high_frequency_anomaly = %s
        WHERE packet_id = %s
    """

    for _, row in df.iterrows():

        cursor.execute(
            query,
            (
                float(row["packets_per_second"]),
                bool(row["is_anomaly"]),
                bool(row["large_packet_anomaly"]),
                bool(row["high_frequency_anomaly"]),
                int(row["packet_id"])
            )
        )

    connection.commit()

    cursor.close()
    connection.close()


def main():

    print("=" * 60)
    print("BLE ANOMALY DETECTION + DATABASE UPDATE")
    print("=" * 60)

    df = load_data()

    df = detect_anomalies(df)

    total_packets = len(df)

    anomaly_count = int(
        df["is_anomaly"].sum()
    )

    print(f"\nTotal packets : {total_packets}")
    print(f"Anomalies     : {anomaly_count}")

    save_to_database(df)

    print("\nAnomaly results saved to PostgreSQL!")


if __name__ == "__main__":
    main()