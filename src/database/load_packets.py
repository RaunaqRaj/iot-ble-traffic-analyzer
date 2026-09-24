import pandas as pd
from datetime import datetime

from database.db_connection import get_connection


INPUT_FILE = "data/processed/ble_packets.csv"


def load_csv():
    return pd.read_csv(INPUT_FILE)


def insert_packets(df):
    connection = get_connection()
    cursor = connection.cursor()

    # Clear previous packet data before loading a new capture
    cursor.execute("TRUNCATE TABLE ble_packets RESTART IDENTITY")

    query = """
    INSERT INTO ble_packets (
        packet_id,
        timestamp,
        device_address,
        packet_type,
        packet_length,
        payload_size
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():

        timestamp = datetime.fromtimestamp(
            row["timestamp"]
        )

        cursor.execute(
            query,
            (
                int(row["packet_id"]),
                timestamp,
                row["device_address"],
                row["packet_type"],
                int(row["packet_length"]),
                int(row["payload_size"])
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

def main():

    print("=" * 60)
    print("BLE CSV → POSTGRESQL LOADER")
    print("=" * 60)

    df = load_csv()

    print(f"\nRecords found in CSV: {len(df)}")

    insert_packets(df)

    print("Records inserted successfully!")


if __name__ == "__main__":
    main()