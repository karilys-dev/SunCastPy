"""Module that defines the arguments for main"""

import argparse
from os import getenv
from pathlib import Path

from SunCastPy.data.zones_url import SJU_ZONES, SJU_ZONES_GROUPED
from SunCastPy.utils.utils import get_current_coordinates

GROUP_BY_OPTIONS = ["forecast", "date"]


def weather_parser() -> argparse.ArgumentParser:
    """Argument parser for main.py to create the weather report

    Returns:
        argparse.ArgumentParser: Arguments required in main.py
    """
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
        "--zone",
        type=str,
        choices=SJU_ZONES_GROUPED.keys(),
        default=None,
        help="(optional) Create a report for all cities in a zone",
    )
    parser.add_argument(
        "--city",
        type=str,
        choices=SJU_ZONES.keys(),
        default=None,
        help="(optional) Create a report for a single city without using coordinates",
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
        choices=GROUP_BY_OPTIONS,
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
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output file or directory path",
    )
    return parser


def parse_args(
    parser: argparse.ArgumentParser = weather_parser(),
) -> argparse.Namespace:  # pragma: no cover
    """Parse the arguments of the weather app

    Args:
        parser (argparse.Namespace, optional): Arguments without parsing.

    Returns:
        argparse.Namespace: arguments
    """

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(args)
