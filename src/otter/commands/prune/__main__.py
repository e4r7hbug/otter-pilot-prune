"""Otter Pilot command prune."""
import collections
import logging
import pathlib

import click

LOG = logging.getLogger(__name__)

Package = collections.namedtuple('Package', ['name', 'version', 'path'])


@click.command()
@click.option('--no-dry', is_flag=True, help='Enable deletion.')
@click.option(
    '-w', '--wheel-dir', type=click.Path(exists=True, file_okay=False), required=True, help='Location of Wheels.')
def main(no_dry, wheel_dir):
    """Otter Pilot prune.

    Good for taking care of business.
    """
    pruned_bytes = 0

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
                stat = previous.path.lstat()
                pruned_bytes += stat.st_size

                if no_dry:
                    previous.path.unlink()
                    LOG.info('Removed: %s', previous.path)
                else:
                    LOG.info('Should delete: %s', previous.path)
        else:
            LOG.debug('Different Packages: %s & %s', current.path.name, previous.path.name)

        previous = current

    LOG.info('Freed %s bytes.', pruned_bytes)


if __name__ == '__main__':
    main()
