# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.

"""Handle the version of the package."""
# > - `scripts/version.py`: the script to update the version
# >    The script should expect the arguments `--set` or `--get`
# >    and it should either return `x.y.z` or set the version to `x.y.z`.

import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def read_version_from_file() -> str:
    """Read the version from the _version.py file.

    Returns
    -------
    str
        The version string in the format x.y.z

    Raises
    ------
    ValueError
        If the version string was not found in the _version.py file
    FileNotFoundError
        If the _version.py file was not found
    """
    version_py_path = ROOT_DIR / "waldiez" / "_version.py"
    if not version_py_path.exists():
        raise FileNotFoundError("The _version.py file was not found")
    with open(version_py_path, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("__version__"):
                return line.split(" = ")[1].strip().strip('"')
    raise ValueError("The version string was not found in the _version.py file")


def set_version(version_string: str) -> None:
    """Set the version to the given value.

    Parameters
    ----------
    version_string : str
        The version string in the format x.y.z

    Raises
    ------
    ValueError
        If the version string is not in the format x.y.z
        If the version string was not found in the _version.py file
    FileNotFoundError
        If the _version.py file was not found
    """
    try:
        major_str, minor_str, patch_str = version_string.split(".")
        major, minor, patch = int(major_str), int(minor_str), int(patch_str)
    except BaseException as error:
        raise ValueError(
            "The version string must be in the format x.y.z"
        ) from error
    new_version = f"{major}.{minor}.{patch}"
    version_py_path = ROOT_DIR / "waldiez" / "_version.py"
    if not version_py_path.exists():
        raise FileNotFoundError("The _version.py file was not found")
    with open(version_py_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    found_version = False
    for index, line in enumerate(lines):
        if line.startswith("__version__"):
            lines[index] = f'__version__ = "{new_version}"' + "\n"
            found_version = True
            break
    if not found_version:
        raise ValueError(
            "The version string was not found in the _version.py file"
        )
    with open(version_py_path, "w", encoding="utf-8", newline="\n") as file:
        file.writelines(lines)


def update_extras(version_string: str) -> None:
    """Update the related extras in pyproject.toml.

    [project.optional-dependencies]
    studio = [
        "waldiez_studio==x.y.z",  <- this one
    ]
    jupyter = [
        "waldiez_jupyter==x.y.z",  <- and this one
        "jupyterlab>=4.3.0",
    ]

    Parameters
    ----------
    version_string : str
        The version string in the format x.y.z

    Raises
    ------
    FileNotFoundError
        If the pyproject.toml file was not found
    """
    pyproject_toml_path = ROOT_DIR / "pyproject.toml"
    if not pyproject_toml_path.exists():
        raise FileNotFoundError("The pyproject.toml file was not found")
    with open(pyproject_toml_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    for index, line in enumerate(lines):
        if "waldiez_studio" in line:
            lines[index] = f'    "waldiez_studio=={version_string}",' + "\n"
        elif "waldiez_jupyter" in line:
            lines[index] = f'    "waldiez_jupyter=={version_string}",' + "\n"
    with open(pyproject_toml_path, "w", encoding="utf-8", newline="\n") as file:
        file.writelines(lines)


def check_versions_match() -> str:
    """Check if the versions of the core and the extras match.

    Returns
    -------
    str
        The version string in the format x.y.z

    Raises
    ------
    ValueError
        If the version strings do not match
    FileNotFoundError
        If the pyproject.toml file was not found
    """
    core_version = read_version_from_file()
    studio_version = jupyter_version = ""
    pyproject_toml_path = ROOT_DIR / "pyproject.toml"
    if not pyproject_toml_path.exists():
        raise FileNotFoundError("The pyproject.toml file was not found")
    with open(pyproject_toml_path, "r", encoding="utf-8") as file:
        for line in file:
            if "waldiez_studio" in line:
                studio_version = line.split("==")[1].strip().strip('",')
            elif "waldiez_jupyter" in line:
                jupyter_version = line.split("==")[1].strip().strip('",')
    if (
        core_version != studio_version
        or core_version != jupyter_version
        or not studio_version
        or not jupyter_version
    ):
        raise ValueError("The version strings do not match")
    return f"The core and the extras match with version {core_version}"


def main() -> None:
    """Handle the command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--set", help="Set the version to the given value in the format x.y.z"
    )
    parser.add_argument(
        "--get", action="store_true", help="Get the current version"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if the versions of the core and the extras match",
    )
    args, _ = parser.parse_known_args()

    if args.set:
        set_version(args.set)
        update_extras(args.set)
    elif args.get:
        print(read_version_from_file())
    elif args.check:
        print(check_versions_match())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
