"""Test waldiez.exporting.flow.flow_exporter."""

import shutil
from pathlib import Path

from waldiez.exporting.flow.flow_exporter import FlowExporter
from waldiez.models import Waldiez

from .flow_helpers import get_flow


def test_flow_exporter_to_py(tmp_path: Path) -> None:
    """Test FlowExporter export to py.

    Parameters
    ----------
    tmp_path : Path
        Temporary directory.
    """
    output_dir = tmp_path / "test_flow_exporter_to_py"
    output_dir.mkdir(exist_ok=True)
    flow = get_flow(is_async=True)
    waldiez = Waldiez(flow=flow)
    exporter = FlowExporter(
        waldiez,
        for_notebook=False,
        output_dir=str(output_dir),
    )
    result = exporter.export()
    assert result["content"] is not None
    shutil.rmtree(output_dir)


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
