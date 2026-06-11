import pandas as pd


def detect_dos(df):

    traffic_counts = (
        df.groupby("source_ip")
        .size()
        .reset_index(name="packet_count")
    )

    suspicious_ips = traffic_counts[
        traffic_counts["packet_count"] >= 100
    ]

    return suspicious_ips