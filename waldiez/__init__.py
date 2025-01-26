# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Waldiez package."""

from ._version import __version__
from .exporter import WaldiezExporter
from .models import Waldiez
from .runner import WaldiezRunner
from .utils import check_conflicts, check_flaml_warnings

__WALDIEZ_INITIALIZED = False

if not __WALDIEZ_INITIALIZED:
    check_conflicts()
    check_flaml_warnings()
    # let's skip the one below
    # check_pysqlite3()
    # and use it only if needed:
    #   captain_agent dependency:
    #   before calling pip install pyautogen[captainagent]
    #   we should have pysqlite3 installed (at least on windows)
    # before running a flow
    __WALDIEZ_INITIALIZED = True

__all__ = [
    "Waldiez",
    "WaldiezExporter",
    "WaldiezRunner",
    "__version__",
]
