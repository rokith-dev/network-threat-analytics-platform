import pandas as pd


def detect_port_scans(df):

    suspicious_ips = []

    grouped = df.groupby("source_ip")

    for ip, group in grouped:

        unique_ports = group["destination_port"].nunique()

        if unique_ports >= 10:

            suspicious_ips.append(
                {
                    "source_ip": ip,
                    "ports_scanned": unique_ports
                }
            )

    return pd.DataFrame(suspicious_ips)