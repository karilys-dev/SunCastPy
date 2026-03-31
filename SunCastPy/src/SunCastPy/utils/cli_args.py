import argparse
from os import getenv


def weather_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Weather data processing CLI")
    lat_default = getenv("LATITUDE")
    lon_default = getenv("LONGITUDE")
    parser.add_argument(
        "--latitude",
        type=float,
        required=lat_default is None,
        default=float(lat_default) if lat_default is not None else None,
        help="Latitude coordinate (float). Example: 18.4655",
    )

    parser.add_argument(
        "--longitude",
        type=float,
        required=lon_default is None,
        default=float(lon_default) if lon_default is not None else None,
        help="Longitude coordinate (float). Example: -66.1057",
    )

    parser.add_argument(
        "--flatten",
        action="store_true",
        help="Flatten the output structure (flag, defaults to False)",
    )

    parser.add_argument(
        "--group-by",
        type=str,
        choices=["forecast", "date"],
        default=None,
        help="Optional grouping strategy: 'forecast' or 'date'",
    )

    return parser


def parse_args():
    parser = weather_parser()
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(args)
