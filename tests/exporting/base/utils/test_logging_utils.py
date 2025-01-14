# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# pylint: disable=inconsistent-quotes, line-too-long
"""Test waldiez.exporting.base.utils.logging_utils.*."""

from waldiez.exporting.flow.utils.logging_utils import (
    get_logging_start_string,
    get_logging_stop_string,
    get_sqlite_out,
    get_sqlite_out_call,
)


def test_get_logging_start_string() -> None:
    """Test get_logging_start_string."""
    # Given
    tabs = 0
    # When
    result = get_logging_start_string(tabs)
    # Then
    assert result == (
        "runtime_logging.start(\n"
        '    logger_type="sqlite",\n'
        '    config={"dbname": "flow.db"},\n'
        ")\n"
    )
    # Given
    tabs = 1
    # When
    result = get_logging_start_string(tabs)
    # Then
    assert result == (
        "    runtime_logging.start(\n"
        '        logger_type="sqlite",\n'
        '        config={"dbname": "flow.db"},\n'
        "    )\n"
    )


def test_get_logging_stop_string() -> None:
    """Test get_logging_stop_string."""
    # Given
    tabs = 0
    # When
    result = get_logging_stop_string(tabs)
    # Then
    assert result == "runtime_logging.stop()\n"
    # Given
    tabs = 1
    # When
    result = get_logging_stop_string(tabs)
    # Then
    assert result == "    runtime_logging.stop()\n"


def test_get_sqlite_out_call() -> None:
    """Test get_sqlite_out_call."""
    # Given
    tabs = 0
    # When
    result = get_sqlite_out_call(tabs)
    # Then
    assert result == (
        'if not os.path.exists("logs"):\n'
        '    os.makedirs("logs")\n'
        "for table in [\n"
        '    "chat_completions",\n'
        '    "agents",\n'
        '    "oai_wrappers",\n'
        '    "oai_clients",\n'
        '    "version",\n'
        '    "events",\n'
        '    "function_calls",\n'
        "]:\n"
        '    dest = os.path.join("logs", f"{table}.csv")\n'
        '    get_sqlite_out("flow.db", table, dest)\n'
    )


def test_get_sqlite_out() -> None:
    """Test test_get_sqlite_out."""
    # When
    result = get_sqlite_out()
    # Then
    assert result == (
        "\n\n"
        "def get_sqlite_out(dbname: str, table: str, csv_file: str) -> None:\n"
        '    """Convert a sqlite table to csv and json files.\n\n'
        "    Parameters\n"
        "    ----------\n"
        "    dbname : str\n"
        "        The sqlite database name.\n"
        "    table : str\n"
        "        The table name.\n"
        "    csv_file : str\n"
        "        The csv file name.\n"
        '    """\n'
        "    conn = sqlite3.connect(dbname)\n"
        '    query = f"SELECT * FROM {table}"  # nosec\n'
        "    try:\n"
        "        cursor = conn.execute(query)\n"
        "    except sqlite3.OperationalError:\n"
        "        conn.close()\n"
        "        return\n"
        "    rows = cursor.fetchall()\n"
        "    column_names = [description[0] for description "
        "in cursor.description]\n"
        "    data = [dict(zip(column_names, row)) for row in rows]\n"
        "    conn.close()\n"
        '    with open(csv_file, "w", newline="", encoding="utf-8") as file:\n'
        "        csv_writer = csv.DictWriter(file, fieldnames=column_names)\n"
        "        csv_writer.writeheader()\n"
        "        csv_writer.writerows(data)\n"
        '    json_file = csv_file.replace(".csv", ".json")\n'
        '    with open(json_file, "w", encoding="utf-8") as file:\n'
        "        json.dump(data, file, indent=4, ensure_ascii=False)\n"
        "\n\n"
    )
