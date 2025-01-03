"""Waldiez Flow runner.

Run a waldiez flow.
The flow is first converted to an autogen flow with agents, chats and skills.
We then chown to temporary directory, call the flow's `main()` and
return the results. Before running the flow, any additional environment
variables specified in the waldiez file are set.
"""

# pylint: disable=import-outside-toplevel,reimported

import importlib.util
import sys
import tempfile
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, List, Optional, Type, Union

from asyncer import syncify

from .exporter import WaldiezExporter
from .models.waldiez import Waldiez
from .running import (
    a_chdir,
    a_install_requirements,
    after_run,
    before_run,
    chdir,
    get_printer,
    install_requirements,
    refresh_environment,
    reset_env_vars,
    set_env_vars,
)

if TYPE_CHECKING:
    from autogen import ChatResult  # type: ignore


class WaldiezRunner:
    """Waldiez runner class."""

    def __init__(
        self, waldiez: Waldiez, file_path: Optional[Union[str, Path]] = None
    ) -> None:
        """Initialize the Waldiez manager."""
        self._waldiez = waldiez
        self._running = False
        self._file_path = file_path
        self._exporter = WaldiezExporter(waldiez)
        self._called_install_requirements = False

    @classmethod
    def load(
        cls,
        waldiez_file: Union[str, Path],
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        requirements: Optional[List[str]] = None,
    ) -> "WaldiezRunner":
        """Create a WaldiezRunner instance from a file.

        Parameters
        ----------
        waldiez_file : Union[str, Path]
            The file path.
        name : Optional[str], optional
            The name of the Waldiez, by default None.
        description : Optional[str], optional
            The description of the Waldiez, by default None.
        tags : Optional[List[str]], optional
            The tags of the Waldiez, by default None.
        requirements : Optional[List[str]], optional
            The requirements of the Waldiez, by default None.

        Returns
        -------
        WaldiezRunner
            The Waldiez runner instance.

        Raises
        ------
        FileNotFoundError
            If the file is not found.
        RuntimeError
            If the file is not a valid Waldiez file.
        """
        waldiez = Waldiez.load(
            waldiez_file,
            name=name,
            description=description,
            tags=tags,
            requirements=requirements,
        )
        return cls(waldiez, file_path=waldiez_file)

    def __enter__(
        self,
    ) -> "WaldiezRunner":
        """Enter the context manager."""
        return self

    async def __aenter__(
        self,
    ) -> "WaldiezRunner":
        """Enter the context manager asynchronously."""
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        """Exit the context manager."""
        if self._running:
            self._running = False

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        """Exit the context manager asynchronously."""
        if self._running:
            self._running = False

    @property
    def waldiez(self) -> Waldiez:
        """Get the Waldiez instance."""
        return self._waldiez

    @property
    def running(self) -> bool:
        """Get the running status."""
        return self._running

    def install_requirements(self) -> None:
        """Install the requirements for the flow."""
        self._called_install_requirements = True
        printer = get_printer()
        extra_requirements = set(
            req for req in self.waldiez.requirements if req not in sys.modules
        )
        if extra_requirements:
            install_requirements(extra_requirements, printer)
            refresh_environment()

    async def a_install_requirements(self) -> None:
        """Install the requirements for the flow asynchronously."""
        self._called_install_requirements = True
        printer = get_printer()
        extra_requirements = set(
            req for req in self.waldiez.requirements if req not in sys.modules
        )
        if extra_requirements:
            await a_install_requirements(extra_requirements, printer)
            refresh_environment()

    def _run(
        self,
        output_path: Optional[Union[str, Path]],
        uploads_root: Optional[Union[str, Path]],
    ) -> Union["ChatResult", List["ChatResult"]]:
        """Run the Waldiez workflow.

        Parameters
        ----------
        output_path : Optional[Union[str, Path]]
            The output path.
        uploads_root : Optional[Union[str, Path]]
            The runtime uploads root.

        Returns
        -------
        Union[ChatResult, List[ChatResult]]
            The result(s) of the chat(s).
        """
        temp_dir = Path(tempfile.mkdtemp())
        file_name = before_run(output_path, uploads_root)
        module_name = file_name.replace(".py", "")
        if not self._called_install_requirements:
            self.install_requirements()
        else:
            refresh_environment()
        printer = get_printer()
        printer(
            "Requirements installed.\n"
            "NOTE: If new packages were added and you are using Jupyter, "
            "you might need to restart the kernel."
        )
        results: Union["ChatResult", List["ChatResult"]] = []
        with chdir(to=temp_dir):
            self._exporter.export(Path(file_name))
            spec = importlib.util.spec_from_file_location(
                module_name, temp_dir / file_name
            )
            if not spec or not spec.loader:
                raise ImportError("Could not import the flow")
            sys.path.insert(0, str(temp_dir))
            old_vars = set_env_vars(self.waldiez.get_flow_env_vars())
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            printer("<Waldiez> - Starting workflow...")
            results = module.main()
            sys.path.pop(0)
            reset_env_vars(old_vars)
        after_run(temp_dir, output_path, printer)
        return results

    async def _a_run(
        self,
        output_path: Optional[Union[str, Path]],
        uploads_root: Optional[Union[str, Path]],
    ) -> Union["ChatResult", List["ChatResult"]]:
        """Run the Waldiez workflow asynchronously."""
        temp_dir = Path(tempfile.mkdtemp())
        file_name = before_run(output_path, uploads_root)
        module_name = file_name.replace(".py", "")
        if not self._called_install_requirements:
            await self.a_install_requirements()
        else:
            refresh_environment()
        printer = get_printer()
        printer(
            "Requirements installed.\n"
            "NOTE: If new packages were added and you are using Jupyter, "
            "you might need to restart the kernel."
        )
        results: Union["ChatResult", List["ChatResult"]] = []
        async with a_chdir(to=temp_dir):
            self._exporter.export(Path(file_name))
            spec = importlib.util.spec_from_file_location(
                module_name, temp_dir / file_name
            )
            if not spec or not spec.loader:
                raise ImportError("Could not import the flow")
            sys.path.insert(0, str(temp_dir))
            old_vars = set_env_vars(self.waldiez.get_flow_env_vars())
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            printer("<Waldiez> - Starting workflow...")
            results = await module.main()
            sys.path.pop(0)
            reset_env_vars(old_vars)
        after_run(temp_dir, output_path, printer)
        return results

    def run(
        self,
        output_path: Optional[Union[str, Path]] = None,
        uploads_root: Optional[Union[str, Path]] = None,
    ) -> Union["ChatResult", List["ChatResult"]]:
        """Run the Waldiez workflow.

        Parameters
        ----------
        output_path : Optional[Union[str, Path]], optional
            The output path, by default None.
        uploads_root : Optional[Union[str, Path]], optional
            The uploads root, to get user-uploaded files, by default None.

        Returns
        -------
        Union[ChatResult, List[ChatResult]]
            The result(s) of the chat(s).

        Raises
        ------
        RuntimeError
            If the workflow is already running.
        """
        if self.waldiez.is_async:
            return syncify(self.a_run)(output_path, uploads_root)
        if self._running is True:
            raise RuntimeError("Workflow already running")
        self._running = True
        file_path = output_path or self._file_path
        try:
            return self._run(file_path, uploads_root)
        finally:
            self._running = False

    async def a_run(
        self,
        output_path: Optional[Union[str, Path]] = None,
        uploads_root: Optional[Union[str, Path]] = None,
    ) -> Union["ChatResult", List["ChatResult"]]:
        """Run the Waldiez workflow asynchronously.

        Parameters
        ----------
        output_path : Optional[Union[str, Path]], optional
            The output path, by default None.
        uploads_root : Optional[Union[str, Path]], optional
            The uploads root, to get user-uploaded files, by default None.

        Returns
        -------
        Union[ChatResult, List[ChatResult]]
            The result(s) of the chat(s).

        Raises
        ------
        RuntimeError
            If the workflow is already running.
        """
        if self._running is True:
            raise RuntimeError("Workflow already running")
        self._running = True
        file_path = output_path or self._file_path
        try:
            return await self._a_run(file_path, uploads_root)
        finally:
            self._running = False
