from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from _pytest.config import Config
    from _pytest.nodes import Item


# TODO(ThomasHepworth): Update this to add an "all" marker that runs all tests.
def pytest_collection_modifyitems(config: Config, items: list[Item]) -> None:
    """
    Modify collected tests:
    - If '-m all' is specified, do not filter or skip any tests.
    - If '-m slow' is specified, run slow tests.
    - By default, skip tests marked as 'slow'.
    """

    markers = config.option.markexpr

    # If you pass in '-m all', run all tests.
    if "all" in markers:
        items = [item.add_marker("all") for item in items]
        return

    skip_slow = pytest.mark.skip(
        reason="Skipped slow test. Use '-m slow' or '-m all' to run."
    )
    for item in items:
        if "slow" in item.keywords and "slow" not in markers:
            item.add_marker(skip_slow)
