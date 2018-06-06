"""Otter Pilot command prune."""
import collections
import logging
import pathlib

import click

import bitmath

LOG = logging.getLogger(__name__)

Package = collections.namedtuple('Package', ['name', 'version', 'path'])


@click.command()
@click.option('--no-dry', is_flag=True, help='Enable deletion.')
@click.option(
    '-w', '--wheel-dir', type=click.Path(exists=True, file_okay=False), required=True, help='Location of Wheels.')
def main(no_dry, wheel_dir):
    """Remove old Python Wheels from local directory."""
    pruned_bytes = bitmath.MiB()

    location = pathlib.Path(wheel_dir)

    previous = Package('', '', pathlib.Path())
    for wheel in sorted(location.iterdir()):
        LOG.debug('Checking for pruning: %s', wheel)

        name, version, *_ = wheel.name.split('-')
        current = Package(name=name, version=version, path=wheel)

        if current.name == previous.name:
            if current.version == previous.version:
                LOG.debug('Most likely compiled for different Python versions: %s & %s', current.path.name,
                          previous.path.name)
            else:
                pruned_bytes += bitmath.getsize(previous.path)

                if no_dry:
                    previous.path.unlink()
                    LOG.info('Removed: %s', previous.path)
                else:
                    LOG.info('Should delete: %s', previous.path)
        else:
            LOG.debug('Different Packages: %s & %s', current.path.name, previous.path.name)

        previous = current

    LOG.info('Freed: %s', pruned_bytes)


if __name__ == '__main__':
    main()
