import argparse
from os import getenv

from SunCastPy.utils.utils import get_current_coordinates


def weather_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Weather data processing CLI")
    coords = get_current_coordinates()
    lat_default = getenv("LATITUDE", coords["latitude"])
    lon_default = getenv("LONGITUDE", coords["longitude"])
    parser.add_argument(
        "--latitude",
        type=float,
        required=lat_default is None,
        default=float(lat_default) if lat_default is not None else None,
        help=f"Latitude coordinate (float). Example: {lat_default}",
    )

    parser.add_argument(
        "--longitude",
        type=float,
        required=lon_default is None,
        default=float(lon_default) if lon_default is not None else None,
        help=f"Longitude coordinate (float). Example: {lon_default}",
    )

    parser.add_argument(
        "--flatten",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Flatten the output structure (flag, defaults to True)",
    )

    parser.add_argument(
        "--group-by",
        "-g",
        type=str,
        choices=["forecast", "date"],
        default=None,
        help="Optional grouping strategy: 'forecast' or 'date'",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        choices=range(1, 8),
        help="Limit the forecast days to show",
    )
    return parser


def parse_args():
    parser = weather_parser()
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(args)
