"""Otter Pilot command prune."""
import collections
import logging
import pathlib

import click

import bitmath

LOG = logging.getLogger(__name__)

Wheel = collections.namedtuple('Wheel', ['name', 'version', 'path'])


def old_wheels(wheel_dir):
    """Iterate through Wheels that should be deleted.

    Yields:
        Wheel: Old Wheel that is safe to delete.

    """
    location = pathlib.Path(wheel_dir)

    previous = Wheel('', '', pathlib.Path())
    for wheel in sorted(location.iterdir()):
        LOG.debug('Checking for pruning: %s', wheel)

        name, version, *_ = wheel.name.split('-')
        current = Wheel(name=name, version=version, path=wheel)

        if current.name == previous.name:
            if current.version == previous.version:
                LOG.debug('Most likely compiled for different Python versions: %s & %s', current.path.name,
                          previous.path.name)
            else:
                LOG.debug('Should delete: %s', previous)
                yield previous
        else:
            LOG.debug('Different Packages: %s & %s', current.path.name, previous.path.name)

        previous = current


@click.command()
@click.option('--no-dry', is_flag=True, help='Enable deletion.')
@click.option(
    '-w', '--wheel-dir', type=click.Path(exists=True, file_okay=False), required=True, help='Location of Wheels.')
def main(no_dry, wheel_dir):
    """Remove old Python Wheels from local directory."""
    pruned_bytes = bitmath.MiB()

    for old_wheel in old_wheels(wheel_dir):
        pruned_bytes += bitmath.getsize(old_wheel.path)

        if no_dry:
            old_wheel.path.unlink()
            LOG.info('Removed: %s', old_wheel.path)
        else:
            LOG.info('Would delete: %s', old_wheel.path)

    LOG.info('Freed: %s', pruned_bytes)


if __name__ == '__main__':
    main()
