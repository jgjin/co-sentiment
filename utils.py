"""Utility functions."""

from itertools import chain, islice


def chunks(
        iterator,
        size=10,
):
    """Get chunks of certain size from iterator."""
    # https://stackoverflow.com/questions/24527006/split-a-generator-into-chunks-without-pre-walking-it
    for first in iterator:
        yield chain([first], islice(iterator, size - 1))
