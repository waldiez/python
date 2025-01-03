"""Utilities for running code."""

import asyncio
import datetime
import io
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from typing import (
    AsyncIterator,
    Callable,
    Iterator,
    Optional,
    Set,
    Tuple,
    Union,
)

from .environment import in_virtualenv

# pylint: disable=import-outside-toplevel


@contextmanager
def chdir(to: Union[str, Path]) -> Iterator[None]:
    """Change the current working directory in a context.

    Parameters
    ----------
    to : Union[str, Path]
        The directory to change to.

    Yields
    ------
    Iterator[None]
        The context manager.
    """
    old_cwd = str(os.getcwd())
    os.chdir(to)
    try:
        yield
    finally:
        os.chdir(old_cwd)


@asynccontextmanager
async def a_chdir(to: Union[str, Path]) -> AsyncIterator[None]:
    """Asynchronously change the current working directory in a context.

    Parameters
    ----------
    to : Union[str, Path]
        The directory to change to.

    Yields
    ------
    AsyncIterator[None]
        The async context manager.
    """
    old_cwd = str(os.getcwd())
    os.chdir(to)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def before_run(
    output_path: Optional[Union[str, Path]],
    uploads_root: Optional[Union[str, Path]],
) -> str:
    """Actions to perform before running the flow.

    Parameters
    ----------
    output_path : Optional[Union[str, Path]]
        The output path.
    uploads_root : Optional[Union[str, Path]]
        The runtime uploads root.

    Returns
    -------
    str
        The file name.
    """
    printer = get_printer()
    printer(
        "Requirements installed.\n"
        "NOTE: If new packages were added and you are using Jupyter, "
        "you might need to restart the kernel."
    )
    if not uploads_root:
        uploads_root = Path(tempfile.mkdtemp())
    else:
        uploads_root = Path(uploads_root)
    if not uploads_root.exists():
        uploads_root.mkdir(parents=True)
    file_name = "flow.py" if not output_path else Path(output_path).name
    if file_name.endswith((".json", ".waldiez")):
        file_name = file_name.replace(".json", ".py").replace(".waldiez", ".py")
    if not file_name.endswith(".py"):
        file_name += ".py"
    return file_name


def install_requirements(
    extra_requirements: Set[str], printer: Callable[..., None]
) -> None:
    """Install the requirements.

    Parameters
    ----------
    extra_requirements : Set[str]
        The extra requirements.
    printer : Callable[..., None]
        The printer function.
    """
    requirements_string = ", ".join(extra_requirements)
    printer(f"Installing requirements: {requirements_string}")
    pip_install = [sys.executable, "-m", "pip", "install"]
    if not in_virtualenv():
        pip_install.append("--user")
    pip_install.extend(extra_requirements)
    with subprocess.Popen(
        pip_install,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as proc:
        if proc.stdout:
            for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
                printer(line.strip())
        if proc.stderr:
            for line in io.TextIOWrapper(proc.stderr, encoding="utf-8"):
                printer(line.strip())


async def a_install_requirements(
    extra_requirements: Set[str], printer: Callable[..., None]
) -> None:
    """Install the requirements asynchronously.

    Parameters
    ----------
    extra_requirements : Set[str]
        The extra requirements.
    printer : Callable[..., None]
        The printer function.
    """
    requirements_string = ", ".join(extra_requirements)
    printer(f"Installing requirements: {requirements_string}")
    pip_install = [sys.executable, "-m", "pip", "install"]
    if not in_virtualenv():
        pip_install.append("--user")
    pip_install.extend(extra_requirements)
    proc = await asyncio.create_subprocess_exec(
        *pip_install,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    if proc.stdout:
        async for line in proc.stdout:
            printer(line.decode().strip())
    if proc.stderr:
        async for line in proc.stderr:
            printer(line.decode().strip())


def after_run(
    temp_dir: Path,
    output_path: Optional[Union[str, Path]],
    printer: Callable[..., None],
) -> None:
    """Actions to perform after running the flow.

    Parameters
    ----------
    temp_dir : Path
        The temporary directory.
    output_path : Optional[Union[str, Path]]
        The output path.
    printer : Callable[..., None]
        The printer function.
    """
    if output_path:
        destination_dir = Path(output_path).parent
        destination_dir = (
            destination_dir
            / "waldiez_out"
            / datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        )
        destination_dir.mkdir(parents=True, exist_ok=True)
        # copy the contents of the temp dir to the destination dir
        printer(f"Copying the results to {destination_dir}")
        for item in temp_dir.iterdir():
            # skip cache files
            if (
                item.name.startswith("__pycache__")
                or item.name.endswith(".pyc")
                or item == ".cache"
            ):
                continue
            if item.is_file():
                shutil.copy(item, destination_dir)
            else:
                shutil.copytree(item, destination_dir / item.name)
    shutil.rmtree(temp_dir)


def get_printer() -> Callable[..., None]:
    """Get the printer function.

    Returns
    -------
    Callable[..., None]
        The printer function.
    """
    from autogen.io import IOStream  # type: ignore

    printer = IOStream.get_default().print

    def safe_printer(*args: object, **kwargs: object) -> None:
        try:
            printer(*args, **kwargs)
        except UnicodeEncodeError:
            # pylint: disable=too-many-try-statements
            try:
                msg, flush = get_what_to_print(*args, **kwargs)
                printer(msg, end="", flush=flush)
            except UnicodeEncodeError:
                sys.stdout = io.TextIOWrapper(
                    sys.stdout.buffer, encoding="utf-8"
                )
                sys.stderr = io.TextIOWrapper(
                    sys.stderr.buffer, encoding="utf-8"
                )
                try:
                    printer(*args, **kwargs)
                except UnicodeEncodeError:
                    sys.stderr.write(
                        "Could not print the message due to encoding issues.\n"
                    )

    return safe_printer


def get_what_to_print(*args: object, **kwargs: object) -> Tuple[str, bool]:
    """Get what to print.

    Parameters
    ----------
    args : object
        The arguments.
    kwargs : object
        The keyword arguments.

    Returns
    -------
    Tuple[str, bool]
        The message and whether to flush.
    """
    sep = kwargs.get("sep", " ")
    if not isinstance(sep, str):
        sep = " "
    end = kwargs.get("end", "\n")
    if not isinstance(end, str):
        end = "\n"
    flush = kwargs.get("flush", False)
    if not isinstance(flush, bool):
        flush = False
    msg = sep.join(str(arg) for arg in args) + end
    utf8_msg = msg.encode("utf-8", errors="replace").decode("utf-8")
    return utf8_msg, flush
