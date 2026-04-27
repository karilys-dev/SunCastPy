"""Module that creates forecast report from command line"""

import logging

from SunCastPy.report.city import main as city_report
from SunCastPy.report.zone import main as zone_report
from SunCastPy.utils.cli_args import parse_args
from SunCastPy.utils.logging_config import setup_logging


def main(args=parse_args(), log_level=logging.INFO):
    """Get the weather forecast and print to command line

    Args:
        args (argument parser, optional): Argument parser values. Defaults to parse_args().
    """
    setup_logging(level=log_level)
    logger = logging.getLogger(__name__)

    for arg, val in args.__dict__.items():
        logger.debug(f"{arg}: {val}")
    if args.zone:
        if not args.output:
            raise ValueError("Output is required when creating a report for a zone")
        zone_report(zone=args.zone, output=args.output, flatten=args.flatten, limit=args.limit)
    else:
        # City or coordinates
        city_report(
            limit=args.limit,
            output=args.output,
            group_by=args.group_by,
            kwargs={
                "latitude": args.latitude,
                "longitude": args.longitude,
                "city": args.city,
                "flatten": args.flatten,
            },
        )


if __name__ == "__main__":
    main()
