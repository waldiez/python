# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# flake8: noqa E501
"""Utils to generate the content of a flow."""

from typing import Callable, Dict, List, Optional

from waldiez.models import Waldiez


def get_py_content_start(waldiez: Waldiez) -> str:
    """Get the first part of the python script.

    Parameters
    ----------
    waldiez : Waldiez
        The waldiez object.
    Returns
    -------
    str
        The first part of the python script.
    """
    content = "#!/usr/bin/env python\n"
    content += "# flake8: noqa E501\n"
    content += get_pylint_ignore_comment(False)
    content += "# cspell: disable\n"
    content += f'"""{waldiez.name}.' + "\n\n"
    content += f"{waldiez.description}" + "\n\n"
    tags = ", ".join(waldiez.tags)
    content += f"Tags: {tags}" + "\n\n"
    requirements = " ".join(waldiez.requirements)
    content += f"Requirements: {requirements}" + "\n\n"
    content += '"""\n\n'
    return content


def get_ipynb_content_start(
    waldiez: Waldiez, comment: Callable[[bool, int], str]
) -> str:
    """Get the first part of the ipynb file.

    Parameters
    ----------
    waldiez : Waldiez
        The waldiez object.
    comment : Callable[[bool, int], str]
        The function to create a comment.
    Returns
    -------
    str
        The first part of the ipynb file.
    """
    content = f"{comment(True, 1)}{waldiez.name}." + "\n\n"
    content += f"{comment(True, 2)}{waldiez.description}" + "\n\n"
    content += f"{comment(True, 2)}Dependencies" + "\n\n"
    content += "import sys\n"
    requirements = " ".join(waldiez.requirements)
    if requirements:
        # pylint: disable=line-too-long
        # fmt: off
        content += "# " + f"!{{sys.executable}} -m pip install -q {requirements}" + "\n"  # noqa: E501
        # fmt: on
    content += "# flake8: noqa E501"
    content += get_pylint_ignore_comment(True)
    content += "# cspell: disable\n"
    return content


PYLINT_RULES = [
    "line-too-long",
    "unknown-option-value",
    "unused-argument",
    "unused-import",
    "invalid-name",
    "import-error",
    "inconsistent-quotes",
    "missing-function-docstring",
    "missing-param-doc",
    "missing-return-doc",
]


def get_pylint_ignore_comment(
    notebook: bool, rules: Optional[List[str]] = None
) -> str:
    """Get the pylint ignore comment string.

    Parameters
    ----------
    notebook : bool
        Whether the comment is for a notebook.
    rules : Optional[List[str]], optional
        The pylint rules to ignore, by default None.

    Returns
    -------
    str
        The pylint ignore comment string.

    Example
    -------
    ```python
    >>> get_pylint_ignore_comment(True, ["invalid-name", "line-too-long"])

    # pylint: disable=invalid-name, line-too-long
    ```
    """
    if not rules:
        rules = PYLINT_RULES
    line = "# pylint: disable=" + ",".join(rules)
    if notebook is True:
        line = "\n" + line
    return line + "\n"


def get_after_run_content(
    waldiez: Waldiez,
    agent_names: Dict[str, str],
    tabs: int,
) -> str:
    """Get content to add after the flow is run.

    Parameters
    ----------
    waldiez : Waldiez
        The waldiez object.
    agent_names : Dict[str, str]
        The dictionary of agent names and their corresponding ids
    tabs : int
        The number of tabs to add before the content.
    Returns
    -------
    str
        The content to add after the flow is run.
    """
    # if th eflow has reasoning agents, we add
    # visualize_tree(agent._root) for each agent
    content = ""
    space = "    " * tabs
    for agent in waldiez.agents:
        if agent.agent_type == "reasoning":
            agent_name = agent_names[agent.id]
            content += f"""
{space}try:
{space}{space}visualize_tree({agent_name}._root)  # pylint: disable=protected-access
{space}except BaseException:  # pylint: disable=broad-except
{space}{space}pass
"""
    return content
