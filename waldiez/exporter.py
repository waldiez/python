# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""
The role of the exporter is to export the model's data
to an autogen's flow with one or more chats.

The resulting file(s): a `flow.py` file with one `main()` function
to trigger the chat(s).
If additional tools/skills are used,
they are exported as their `skill_name` in the same directory with
the `flow.py` file. So the `flow.py` could have entries like:
`form {flow_name}_{skill1_name} import {skill1_name}`
`form {flow_name}_{skill2_name} import {skill2_name}`
"""

# pylint: disable=inconsistent-quotes

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Union

from .exporting import FlowExporter
from .models import Waldiez


class WaldiezExporter:
    """Waldiez exporter.

    Attributes:
        waldiez (Waldiez): The Waldiez instance.
    """

    def __init__(self, waldiez: Waldiez) -> None:
        """Initialize the Waldiez exporter.

        Parameters:
            waldiez (Waldiez): The Waldiez instance.
        """
        self.waldiez = waldiez
        # self._initialize()

    @classmethod
    def load(cls, file_path: Path) -> "WaldiezExporter":
        """Load the Waldiez instance from a file.

        Parameters
        ----------
        file_path : Path
            The file path.

        Returns
        -------
        WaldiezExporter
            The Waldiez exporter.
        """
        waldiez = Waldiez.load(file_path)
        return cls(waldiez)

    def export(self, path: Union[str, Path], force: bool = False) -> None:
        """Export the Waldiez instance.

        Parameters
        ----------
        path : Union[str, Path]
            The path to export to.
        force : bool, optional
            Override the output file if it already exists, by default False.

        Raises
        ------
        FileExistsError
            If the file already exists and force is False.
        IsADirectoryError
            If the output is a directory.
        ValueError
            If the file extension is invalid.
        """
        if not isinstance(path, Path):
            path = Path(path)
        path = path.resolve()
        if path.is_dir():
            raise IsADirectoryError(f"Output is a directory: {path}")
        if path.exists():
            if force is False:
                raise FileExistsError(f"File already exists: {path}")
            path.unlink(missing_ok=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        extension = path.suffix
        if extension == ".waldiez":
            self.to_waldiez(path)
        elif extension == ".py":
            self.to_py(path)
        elif extension == ".ipynb":
            self.to_ipynb(path)
        else:
            raise ValueError(f"Invalid extension: {extension}")

    def to_ipynb(self, path: Path) -> None:
        """Export flow to jupyter notebook.

        Parameters
        ----------
        path : Path
            The path to export to.

        Raises
        ------
        RuntimeError
            If the notebook could not be generated.
        """
        # we first create a .py file with the content
        # and then convert it to a notebook using jupytext
        exporter = FlowExporter(
            waldiez=self.waldiez,
            output_dir=path.parent,
            for_notebook=True,
        )
        output = exporter.export()
        content = output["content"]
        if not content:
            raise RuntimeError("Could not generate notebook")
        py_path = path.with_suffix(".tmp.py")
        with open(py_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        if not shutil.which("jupytext"):  # pragma: no cover
            run_command(
                [sys.executable, "-m", "pip", "install", "jupytext"],
                allow_error=False,
            )
        run_command(
            [
                sys.executable,
                "-m",
                "jupytext",
                "--to",
                "notebook",
                str(py_path),
            ],
            allow_error=False,
        )
        ipynb_path = str(py_path).replace(".tmp.py", ".tmp.ipynb")
        if not os.path.exists(ipynb_path):  # pragma: no cover
            raise RuntimeError("Could not generate notebook")
        Path(ipynb_path).rename(ipynb_path.replace(".tmp.ipynb", ".ipynb"))
        py_path.unlink(missing_ok=True)

    def to_py(self, path: Path) -> None:
        """Export waldiez flow to python script.

        Parameters
        ----------
        path : Path
            The path to export to.

        Raises
        ------
        RuntimeError
            If the python script could not be generated.
        """
        exporter = FlowExporter(
            waldiez=self.waldiez,
            output_dir=path.parent,
            for_notebook=False,
        )
        output = exporter.export()
        content = output["content"]
        if not content:
            raise RuntimeError("Could not generate python script")
        with open(path, "w", encoding="utf-8", newline="\n") as file:
            file.write(content)

    def to_waldiez(self, file_path: Path) -> None:
        """Export the Waldiez instance.

        Parameters
        ----------
        file_path : Path
            The file path.
        """
        with open(file_path, "w", encoding="utf-8", newline="\n") as file:
            file.write(self.waldiez.model_dump_json())


def run_command(
    cmd: List[str],
    cwd: Optional[Path] = None,
    allow_error: bool = True,
) -> None:
    """Run a command.

    Parameters
    ----------
    cmd : List[str]
        The command to run.
    cwd : Path, optional
        The working directory, by default None (current working directory).
    allow_error : bool, optional
        Whether to allow errors, by default True.

    Raises
    ------
    RuntimeError
        If the command fails and allow_error is False.
    """
    if not cwd:
        cwd = Path.cwd()
    # pylint: disable=broad-except
    try:
        subprocess.run(
            cmd,
            check=True,
            cwd=cwd,
            env=os.environ,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )  # nosemgrep # nosec
    except BaseException as error:  # pragma: no cover
        if allow_error:
            return
        raise RuntimeError(f"Error running command: {error}") from error
