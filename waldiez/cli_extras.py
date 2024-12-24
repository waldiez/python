# type: ignore
# flake8: noqa
# pylint: skip-file
# isort: skip_file
"""Extra typer commands for CLI."""

import typer
import subprocess  # nosemgrep # nosec

HAVE_STUDIO = False
HAVE_JUPYTER = False
try:
    from waldiez_studio.cli import app as studio_app

    HAVE_STUDIO = True
except BaseException:
    pass

try:
    import waldiez_jupyter

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
        app.add_typer(
            studio_app,
            name="studio",
            help="Start Waldiez Studio.",
            no_args_is_help=False,
        )
    if HAVE_JUPYTER:
        jupyter_app = get_jupyter_app()
        app.add_typer(jupyter_app, name="lab")


def get_jupyter_app() -> typer.Typer:
    """Get the Jupyter Typer app.

    Returns
    -------
    typer.Typer
        The Jupyter Typer app
    """
    jupyter_app = typer.Typer(
        name="lab",
        help="Start jupyter lab with the waldiez extension.",
        context_settings={
            "help_option_names": ["-h", "--help"],
            "allow_extra_args": True,
            "ignore_unknown_options": True,
        },
        add_completion=False,
        no_args_is_help=False,
        invoke_without_command=True,
        add_help_option=True,
        pretty_exceptions_enable=False,
        epilog=(
            "Use `waldiez lab [COMMAND] --help` for command-specific help. "
        ),
    )

    @jupyter_app.command(
        name="start",
        help="Start JupyterLab.",
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
            "--no-browser",
            help="Don't open the browser.",
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
        if browser:
            command.append("--no-browser")
        if password:
            from jupyter_server.auth import passwd

            hashed_password = passwd(password)
            command.append(f"--ServerApp.password={hashed_password}")
        subprocess.run(command)

    return jupyter_app
