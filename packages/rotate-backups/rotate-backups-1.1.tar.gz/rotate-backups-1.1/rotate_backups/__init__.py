# rotate-backups: Simple command line interface for backup rotation.
#
# Author: Peter Odding <peter@peterodding.com>
# Last Change: July 19, 2015
# URL: https://github.com/xolox/python-rotate-backups

# Semi-standard module versioning.
__version__ = '1.1'

# Standard library modules.
import collections
import datetime
import fnmatch
import functools
import logging
import os
import re

# External dependencies.
from dateutil.relativedelta import relativedelta
from executor import execute
from humanfriendly import concatenate, Timer
from natsort import natsort

# Initialize a logger.
logger = logging.getLogger(__name__)

# Ordered mapping of frequency names to the amount of time in each frequency.
ordered_frequencies = (('hourly', relativedelta(hours=1)),
                       ('daily', relativedelta(days=1)),
                       ('weekly', relativedelta(weeks=1)),
                       ('monthly', relativedelta(months=1)),
                       ('yearly', relativedelta(years=1)))
supported_frequencies = dict(ordered_frequencies)

# Regular expression that matches timestamps encoded in filenames.
timestamp_pattern = re.compile(r'''
    # Required components.
    (?P<year>\d{4} ) \D?
    (?P<month>\d{2}) \D?
    (?P<day>\d{2}  ) \D?
    (?:
        # Optional components.
        (?P<hour>\d{2}  ) \D?
        (?P<minute>\d{2}) \D?
        (?P<second>\d{2})?
    )?
''', re.VERBOSE)


def rotate_backups(directory, rotation_scheme, include_list=[], exclude_list=[],
                   dry_run=False, io_scheduling_class=None):
    """
    Rotate the backups in a directory according to a flexible rotation scheme.

    :param directory: The directory containing the backups (a string).
    :param rotation_scheme: A dictionary with one or more of the keys 'hourly',
                            'daily', 'weekly', 'monthly', 'yearly'. Each key is
                            expected to have one of the following values:

                            - An integer gives the number of backups in the
                              corresponding category to preserve, starting from
                              the most recent backup and counting back in
                              time.
                            - The string 'always' means all backups in the
                              corresponding category are preserved (useful for
                              the biggest time unit in the rotation scheme).

                            By default no backups are preserved for categories
                            (keys) not present in the dictionary.
    :param include_list: A list of strings with :mod:`fnmatch` patterns. If a
                         nonempty include list is specified each backup must
                         match a pattern in the include list, otherwise it
                         will be ignored.
    :param exclude_list: A list of strings with :mod:`fnmatch` patterns. If a
                         backup matches the exclude list it will be ignored,
                         *even if it also matched the include list* (it's the
                         only logical way to combine both lists).
    :param dry_run: If this is ``True`` then no changes will be made, which
                    provides a 'preview' of the effect of the rotation scheme
                    (the default is ``False``). Right now this is only useful
                    in the command line interface because there's no return
                    value.
    :param io_scheduling_class: Use ``ionice`` to set the I/O scheduling class
                                (expected to be one of the strings 'idle',
                                'best-effort' or 'realtime').
    """
    # Find the backups and their dates.
    backups = set()
    directory = os.path.abspath(directory)
    logger.info("Scanning directory for timestamped backups: %s", directory)
    for entry in natsort(os.listdir(directory)):
        # Check for a time stamp in the directory entry's name.
        match = timestamp_pattern.search(entry)
        if match:
            # Make sure the entry matches the given include/exclude patterns.
            if exclude_list and any(fnmatch.fnmatch(entry, p) for p in exclude_list):
                logger.debug("Excluded %r (it matched the exclude list).", entry)
            elif include_list and not any(fnmatch.fnmatch(entry, p) for p in include_list):
                logger.debug("Excluded %r (it didn't match the include list).", entry)
            else:
                backups.add(Backup(
                    pathname=os.path.join(directory, entry),
                    datetime=datetime.datetime(*(int(group, 10) for group in match.groups('0'))),
                ))
        else:
            logger.debug("Failed to match time stamp in filename: %s", entry)
    if not backups:
        logger.info("No backups found in %s.", directory)
        return
    logger.info("Found %i timestamped backups in %s.", len(backups), directory)
    # Sort the backups by date and find the date/time of the most recent backup.
    sorted_backups = sorted(backups)
    most_recent_backup = sorted_backups[-1].datetime
    # Group the backups by rotation frequencies.
    grouped_backups = dict((frequency, collections.defaultdict(list)) for frequency in supported_frequencies)
    for backup in backups:
        grouped_backups['hourly'][(backup.year, backup.month, backup.day, backup.hour)].append(backup)
        grouped_backups['daily'][(backup.year, backup.month, backup.day)].append(backup)
        grouped_backups['weekly'][(backup.year, backup.week)].append(backup)
        grouped_backups['monthly'][(backup.year, backup.month)].append(backup)
        grouped_backups['yearly'][backup.year].append(backup)
    # Apply the user defined rotation scheme.
    # FIXME Guard against an empty rotation scheme?!
    for frequency, backups_by_frequency in grouped_backups.items():
        # Ignore frequencies not specified by the user.
        if frequency not in rotation_scheme:
            grouped_backups[frequency].clear()
        else:
            retention_period = rotation_scheme[frequency]
            # Reduce the number of backups in each period to a single backup
            # (the first one within the period).
            for period, backups_in_period in backups_by_frequency.items():
                backups_by_frequency[period] = sorted(backups_in_period)[0]
            if retention_period != 'always':
                # Remove backups older than the minimum date.
                minimum_date = most_recent_backup - supported_frequencies[frequency] * retention_period
                for period, backup in backups_by_frequency.items():
                    if backup.datetime < minimum_date:
                        backups_by_frequency.pop(period)
                # If more than the configured number of backups remain at this
                # point then we remove the oldest backups.
                grouped_backups[frequency] = dict(sorted(backups_by_frequency.items())[-retention_period:])
    # Find out which backups should be purged.
    backups_to_preserve = collections.defaultdict(list)
    for frequency, delta in ordered_frequencies:
        for backup in grouped_backups[frequency].values():
            backups_to_preserve[backup].append(frequency)
    for backup in sorted(backups):
        if backup in backups_to_preserve:
            matching_periods = backups_to_preserve[backup]
            logger.info("Preserving %s (matches %s retention %s) ..", backup.pathname,
                        concatenate(map(repr, matching_periods)),
                        "period" if len(matching_periods) == 1 else "periods")
        else:
            logger.info("Deleting %s %s ..", backup.type, backup.pathname)
            if not dry_run:
                command = ['rm', '-Rf', backup.pathname]
                if io_scheduling_class:
                    command = ['ionice', '--class', io_scheduling_class] + command
                timer = Timer()
                execute(*command, logger=logger)
                logger.debug("Deleted %s in %s.", backup.pathname, timer)
    if len(backups_to_preserve) == len(backups):
        logger.info("Nothing to do!")


@functools.total_ordering
class Backup(object):

    """
    :py:class:`Backup` objects represent a rotation subject.

    In addition to the :attr:`type` and :attr:`week` properties :class:`Backup`
    objects support all of the attributes of :py:class:`~datetime.datetime`
    objects by deferring attribute access for unknown attributes to the
    :py:class:`~datetime.datetime` object given to the constructor.
    """

    def __init__(self, pathname, datetime):
        """
        Initialize a :py:class:`Backup` object.

        :param pathname: The filename of the backup (a string).
        :param datetime: The date/time when the backup was created (a
                         :py:class:`~datetime.datetime` object).
        """
        self.pathname = pathname
        self.datetime = datetime

    @property
    def type(self):
        """Get a string describing the type of backup (e.g. file, directory)."""
        if os.path.islink(self.pathname):
            return 'symbolic link'
        elif os.path.isdir(self.pathname):
            return 'directory'
        else:
            return 'file'

    @property
    def week(self):
        """Get the ISO week number."""
        return self.datetime.isocalendar()[1]

    def __getattr__(self, name):
        """Defer attribute access to the datetime object."""
        return getattr(self.datetime, name)

    def __repr__(self):
        """Enable pretty printing of :py:class:`Backup` objects."""
        return "Backup(pathname=%r, datetime=%r)" % (self.pathname, self.datetime)

    def __hash__(self):
        """Make it possible to use :py:class:`Backup` objects in sets and as dictionary keys."""
        return hash(self.pathname)

    def __eq__(self, other):
        """Make it possible to use :py:class:`Backup` objects in sets and as dictionary keys."""
        return type(self) == type(other) and self.datetime == other.datetime

    def __lt__(self, other):
        """Enable proper sorting of backups."""
        return self.datetime < other.datetime
