# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# pylint: skip-file
# type: ignore
# isort: skip_file
"""Extra typer commands for CLI."""

from typing import Callable

import typer
from typer.models import CommandInfo
import subprocess  # nosemgrep # nosec

HAVE_STUDIO = False
HAVE_JUPYTER = False
try:
    from waldiez_studio.cli import run as studio_app

    HAVE_STUDIO = True
except BaseException:
    pass

try:
    import waldiez_jupyter  # noqa: F401

    HAVE_JUPYTER = True
except BaseException:
    pass


def add_cli_extras(app: typer.Typer) -> None:
    """Add extra CLI commands to the app.

    Parameters
    ----------
    app : typer.Typer
        The Typer app to add the extra commands to.

    Returns
    -------
    typer.Typer
        The app with the extra commands added
    """
    if HAVE_STUDIO:
        app.registered_commands.append(
            CommandInfo(name="studio", callback=studio_app)
        )
    if HAVE_JUPYTER:
        jupyter_app = get_jupyter_app()
        app.registered_commands.append(
            CommandInfo(name="lab", callback=jupyter_app)
        )


def get_jupyter_app() -> Callable[..., None]:
    """Get the Jupyter Typer app.

    Returns
    -------
    typer.Typer
        The Jupyter Typer app
    """
    jupyter_app = typer.Typer(
        add_completion=False,
        no_args_is_help=False,
        pretty_exceptions_enable=False,
    )

    @jupyter_app.callback(
        name="start",
        help="Start JupyterLab.",
        context_settings={
            "help_option_names": ["-h", "--help"],
            "allow_extra_args": True,
            "ignore_unknown_options": True,
        },
        no_args_is_help=False,
        invoke_without_command=True,
        add_help_option=True,
    )
    def start(
        port: int = typer.Option(
            8888,
            "--port",
            help="Port to run JupyterLab on.",
        ),
        host: str = typer.Option(
            "*",
            "--host",
            help="Host to run JupyterLab on.",
        ),
        browser: bool = typer.Option(
            False,
            help="Open the browser after starting JupyterLab.",
        ),
        password: str = typer.Option(
            None,
            "--password",
            help="Password to access JupyterLab.",
        ),
    ) -> None:
        """Start JupyterLab."""
        command = [
            "jupyter",
            "lab",
            f"--port={port}",
            f"--ip={host}",
            "--ServerApp.terminado_settings=\"shell_command=['/bin/bash']\"",
            "--ServerApp.allow_origin='*'",
            "--ServerApp.disable_check_xsrf=True",
        ]
        if not browser:
            command.append("--no-browser")
        if password:
            from jupyter_server.auth import passwd

            hashed_password = passwd(password)
            command.append(f"--ServerApp.password={hashed_password}")
        subprocess.run(command)

    return start
