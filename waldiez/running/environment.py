# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# pylint: disable=import-outside-toplevel,reimported
"""Environment related utilities."""

import importlib.util
import os
import site
import sys
import warnings
from typing import Dict, List, Tuple


def in_virtualenv() -> bool:
    """Check if we are inside a virtualenv.

    Returns
    -------
    bool
        True if inside a virtualenv, False otherwise.
    """
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


def refresh_environment() -> None:
    """Refresh the environment."""
    # backup the default IOStream
    from autogen.io import IOStream  # type: ignore

    default_io_stream = IOStream.get_default()
    site.main()
    # pylint: disable=import-outside-toplevel
    modules_to_reload = [mod for mod in sys.modules if "autogen" in mod]
    for mod in modules_to_reload:
        del sys.modules[mod]
    warnings.filterwarnings(
        "ignore", module="flaml", message="^.*flaml.automl is not available.*$"
    )
    import autogen  # type: ignore
    from autogen.io import IOStream

    importlib.reload(autogen)
    # restore the default IOStream
    IOStream.set_global_default(default_io_stream)


def set_env_vars(flow_env_vars: List[Tuple[str, str]]) -> Dict[str, str]:
    """Set environment variables and return the old ones (if any).

    Parameters
    ----------
    flow_env_vars : List[Tuple[str, str]]
        The environment variables to set.

    Returns
    -------
    Dict[str, str]
        The old environment variables.
    """
    old_vars: Dict[str, str] = {}
    for var_key, var_value in flow_env_vars:
        if var_key:
            current = os.environ.get(var_key, "")
            old_vars[var_key] = current
            os.environ[var_key] = var_value
    return old_vars


def reset_env_vars(old_vars: Dict[str, str]) -> None:
    """Reset the environment variables.

    Parameters
    ----------
    old_vars : Dict[str, str]
        The old environment variables.
    """
    for var_key, var_value in old_vars.items():
        if not var_value:
            os.environ.pop(var_key, "")
        else:
            os.environ[var_key] = var_value
