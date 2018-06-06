"""Otter Pilot command prune."""
import logging

import click

LOG = logging.getLogger(__name__)


@click.command()
@click.option(
    '-w', '--wheel-dir', type=click.Path(exists=True, file_okay=False), required=True, help='Location of Wheels.')
def main(wheel_dir):
    """Otter Pilot prune.

    Good for taking care of business.
    """
    print('Otter Pilot prune reporting for duty!')


if __name__ == '__main__':
    main()
