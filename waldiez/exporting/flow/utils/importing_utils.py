"""Get the standard imports for the flow exporter."""

from typing import List, Optional, Tuple

from waldiez.exporting.base import ImportPosition

BUILTIN_IMPORTS = [
    "import csv",
    "import os",
    "import sqlite3",
]
TYPING_IMPORTS = [
    "Any",
    "Callable",
    "Dict",
    "List",
    "Optional",
    "Tuple",
    "Union",
]
COMMON_AUTOGEN_IMPORTS = [
    "from autogen import Agent",
    "from autogen import ConversableAgent",
    "from autogen import ChatResult",
    "from autogen import runtime_logging",
]


def get_standard_imports(is_async: bool) -> str:
    """Get the standard imports.

    Parameters
    ----------
    is_async : bool
        If the flow is async.

    Returns
    -------
    str
        The standard imports.
    """
    builtin_imports = BUILTIN_IMPORTS.copy()
    if is_async:
        builtin_imports.insert(0, "import asyncio")
    imports_string = "\n".join(builtin_imports) + "\n"
    typing_imports = "from typing import " + ", ".join(TYPING_IMPORTS)
    imports_string += typing_imports
    return imports_string


def sort_imports(
    all_imports: List[Tuple[str, ImportPosition]],
) -> Tuple[List[str], List[str], List[str], List[str], bool]:
    """Sort the imports.

    Parameters
    ----------
    all_imports : List[Tuple[str, ImportPosition]]
        All the imports.

    Returns
    -------
    Tuple[List[str], List[str], List[str], List[str], bool]
        The sorted imports and a flag if we got `import autogen`.
    """
    builtin_imports = []
    third_party_imports = []
    local_imports = []
    autogen_imports = COMMON_AUTOGEN_IMPORTS.copy()
    got_import_autogen = False
    for import_string, position in all_imports:
        if "import autogen" in import_string:
            got_import_autogen = True
            continue
        if import_string.startswith("from autogen"):
            autogen_imports.append(import_string)
            continue
        if position == ImportPosition.BUILTINS:
            builtin_imports.append(import_string)
        elif position == ImportPosition.THIRD_PARTY:
            third_party_imports.append(import_string)
        elif position == ImportPosition.LOCAL:
            local_imports.append(import_string)
    autogen_imports = list(set(autogen_imports))
    return (
        sorted(builtin_imports),
        sorted(autogen_imports),
        sorted(third_party_imports),
        sorted(local_imports),
        got_import_autogen,
    )


def get_the_imports_string(
    all_imports: List[Tuple[str, ImportPosition]],
) -> str:
    """Get the final imports string.

    Parameters
    ----------
    all_imports : List[Tuple[str, ImportPosition]]
        All the imports.
    Returns
    -------
    str
        The final imports string.
    """
    (
        builtin_imports,
        autogen_imports,
        third_party_imports,
        local_imports,
        got_import_autogen,
    ) = sort_imports(all_imports)
    # Get the final imports string.
    # making sure, there are two lines after each import section
    # (builtin, third party, local)
    final_string = "\n".join(builtin_imports) + "\n"
    while not final_string.endswith("\n\n"):
        final_string += "\n"
    if got_import_autogen:
        final_string += "\nimport autogen\n"
    if autogen_imports:
        final_string += "\n".join(autogen_imports) + "\n"
    if third_party_imports:
        final_string += "\n".join(third_party_imports) + "\n"
    while not final_string.endswith("\n\n"):
        final_string += "\n"
    if local_imports:
        final_string += "\n".join(local_imports) + "\n"
    while not final_string.endswith("\n\n"):
        final_string += "\n"
    return final_string.replace("\n\n\n", "\n\n")  # avoid too many newlines


def gather_imports(
    is_async: bool,
    model_imports: Optional[List[Tuple[str, ImportPosition]]],
    skill_imports: Optional[List[Tuple[str, ImportPosition]]],
    chat_imports: Optional[List[Tuple[str, ImportPosition]]],
    agent_imports: Optional[List[Tuple[str, ImportPosition]]],
) -> List[Tuple[str, ImportPosition]]:
    """Gather all the imports.

    Parameters
    ----------
    is_async : bool
        If the flow is async.
    model_imports : Tuple[str, ImportPosition]
        The model imports.
    skill_imports : Tuple[str, ImportPosition]
        The skill imports.
    chat_imports : Tuple[str, ImportPosition]
        The chat imports.
    agent_imports : Tuple[str, ImportPosition]
        The agent imports.

    Returns
    -------
    Tuple[str, ImportPosition]
        The gathered imports.
    """
    imports_string = get_standard_imports(is_async)
    all_imports: List[Tuple[str, ImportPosition]] = [
        (
            imports_string,
            ImportPosition.BUILTINS,
        )
    ]
    if model_imports:
        all_imports.extend(model_imports)
    if skill_imports:
        all_imports.extend(skill_imports)
    if chat_imports:
        all_imports.extend(chat_imports)
    if agent_imports:
        all_imports.extend(agent_imports)
    return list(set(all_imports))
