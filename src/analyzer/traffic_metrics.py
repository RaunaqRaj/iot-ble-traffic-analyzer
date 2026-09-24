import pandas as pd


INPUT_FILE = "data/processed/ble_packets.csv"


def load_data():

    df = pd.read_csv(INPUT_FILE)

    return df


def calculate_metrics(df):

    total_packets = len(df)

    unique_devices = df["device_address"].nunique()

    average_packet_size = df["packet_length"].mean()

    minimum_packet_size = df["packet_length"].min()

    maximum_packet_size = df["packet_length"].max()

    packets_per_device = (
        df["device_address"]
        .value_counts()
    )

    most_active_device = packets_per_device.index[0]

    most_active_device_packets = (
        packets_per_device.iloc[0]
    )

    # Calculate capture duration
    timestamps = pd.to_datetime(
        df["timestamp"],
        unit="s"
    )

    duration_seconds = (
        timestamps.max() - timestamps.min()
    ).total_seconds()

    if duration_seconds > 0:

        packets_per_second = (
            total_packets / duration_seconds
        )

    else:

        packets_per_second = 0

    metrics = {
        "total_packets": total_packets,
        "unique_devices": unique_devices,
        "average_packet_size": average_packet_size,
        "minimum_packet_size": minimum_packet_size,
        "maximum_packet_size": maximum_packet_size,
        "most_active_device": most_active_device,
        "most_active_device_packets": most_active_device_packets,
        "capture_duration_seconds": duration_seconds,
        "packets_per_second": packets_per_second
    }

    return metrics, packets_per_device


def display_metrics(metrics, packets_per_device):

    print("\n" + "=" * 60)
    print("BLE TRAFFIC ANALYTICS")
    print("=" * 60)

    print(
        f"\nTotal Packets          : "
        f"{metrics['total_packets']}"
    )

    print(
        f"Unique Devices         : "
        f"{metrics['unique_devices']}"
    )

    print(
        f"Average Packet Size    : "
        f"{metrics['average_packet_size']:.2f} bytes"
    )

    print(
        f"Minimum Packet Size    : "
        f"{metrics['minimum_packet_size']} bytes"
    )

    print(
        f"Maximum Packet Size    : "
        f"{metrics['maximum_packet_size']} bytes"
    )

    print(
        f"Capture Duration       : "
        f"{metrics['capture_duration_seconds']:.2f} seconds"
    )

    print(
        f"Packets Per Second     : "
        f"{metrics['packets_per_second']:.2f}"
    )

    print(
        f"\nMost Active Device     : "
        f"{metrics['most_active_device']}"
    )

    print(
        f"Packets From Device    : "
        f"{metrics['most_active_device_packets']}"
    )

    print("\nPackets Per Device:")
    print("-" * 60)

    for device, count in packets_per_device.items():

        print(
            f"{device} → {count} packets"
        )


def main():

    df = load_data()

    metrics, packets_per_device = (
        calculate_metrics(df)
    )

    display_metrics(
        metrics,
        packets_per_device
    )


if __name__ == "__main__":
    main()