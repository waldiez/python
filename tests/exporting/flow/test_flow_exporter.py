# SPDX-License-Identifier: MIT.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Test waldiez.exporting.flow.flow_exporter."""

import shutil
from pathlib import Path

from waldiez.exporting.flow.flow_exporter import FlowExporter
from waldiez.models import Waldiez

from .flow_helpers import get_flow

MY_DIR = Path(__file__).resolve().parent
ROOT_DIR = MY_DIR.parent.parent.parent
DOT_LOCAL = ROOT_DIR / ".local"
DOT_LOCAL.mkdir(exist_ok=True, parents=True)


def _export_flow(tmp_path: Path, is_async: bool) -> None:
    """Export flow to py.

    Parameters
    ----------
    tmp_path : Path
        Temporary directory.
    is_async : bool
        Whether the flow is async.
    """
    sync_mode = "async" if is_async else "sync"
    output_dir = tmp_path / f"test_export_flow_{sync_mode}"
    if output_dir.exists():
        shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(exist_ok=True)
    flow = get_flow(is_async=is_async)
    waldiez = Waldiez(flow=flow)
    exporter = FlowExporter(
        waldiez,
        for_notebook=False,
        output_dir=output_dir,
    )
    result = exporter.export()
    assert result["content"] is not None
    destination_dir = DOT_LOCAL / output_dir.name
    shutil.rmtree(destination_dir, ignore_errors=True)
    shutil.copytree(output_dir, destination_dir)
    destination_py = DOT_LOCAL / output_dir.name / "flow.py"
    destination_py.write_text(result["content"])
    shutil.rmtree(output_dir, ignore_errors=True)


def test_flow_exporter_to_py_sync(tmp_path: Path) -> None:
    """Test FlowExporter export to py.

    Parameters
    ----------
    tmp_path : Path
        Temporary directory.
    """
    _export_flow(tmp_path, is_async=False)


def test_flow_exporter_to_py_async(tmp_path: Path) -> None:
    """Test FlowExporter export to async py.

    Parameters
    ----------
    tmp_path : Path
        Temporary directory.
    """
    _export_flow(tmp_path, is_async=True)


def test_flow_export_to_ipynb(tmp_path: Path) -> None:
    """Test FlowExporter export to ipynb.

    Parameters
    ----------
    tmp_path : Path
        Temporary directory.
    """
    output_dir = tmp_path / "test_flow_export_to_ipynb"
    output_dir.mkdir(exist_ok=True)
    flow = get_flow(is_async=True)
    waldiez = Waldiez(flow=flow)
    exporter = FlowExporter(
        waldiez,
        for_notebook=True,
        output_dir=output_dir,
    )
    result = exporter.export()
    assert result["content"] is not None
    shutil.rmtree(output_dir)
