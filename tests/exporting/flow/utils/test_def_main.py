"""Test waldiez.exporting.flow.utils.def_main."""

from waldiez.exporting.flow.utils.def_main import get_def_main


def test_get_def_main() -> None:
    """Test get_def_main."""
    flow_chats = "flow chats content"
    is_async = True
    result = get_def_main(flow_chats, is_async)
    assert isinstance(result, str)
    assert "async def run():" in result
    assert "def main():" in result
    assert 'if __name__ == "__main__":' in result
    assert "return asyncio.run(run())" in result
    assert "return run()" not in result
    assert "return results" in result
    assert "flow chats content" in result
    assert "runtime_logging.stop()" in result
    assert "sqlite_to_csv" in result

    is_async = False
    result = get_def_main(flow_chats, is_async)
    assert isinstance(result, str)
    assert "async def run():" not in result
    assert "def main():" in result
    assert 'if __name__ == "__main__":' in result
    assert "return asyncio.run(run())" not in result
    assert "return run()" in result
