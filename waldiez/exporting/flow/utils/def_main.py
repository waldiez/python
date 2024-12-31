"""Get the main function."""

from .logging_utils import (
    get_logging_stop_string,
    get_sqlite_to_csv_call_string,
)


def get_def_main(flow_chats: str, is_async: bool) -> str:
    """Get the main function.

    When exporting to python, waldiez_chats string will be the
    content of the main function. It contains either a
    `{sender.initiate_chat(recipient, ...)}` (if there is only one chat)
    or `initiate_chats([..])`, with the list of chats to initiate.
    If async: (sender.a_initiate_chat, a_initiate_chats)

    Parameters
    ----------
    flow_chats : str
        The content of the main function.
    is_async : bool
        Whether the main function is asynchronous.
    Returns
    -------
    str
        The main function.
    """
    content = ""
    if is_async:
        content += "async "
    content += "def main():\n"
    content += "    # type: () -> Union[ChatResult, List[ChatResult]]\n"
    content += '    """Start chatting."""\n'
    content += f"{flow_chats}" + "\n"
    content += get_logging_stop_string(1) + "\n"
    content += get_sqlite_to_csv_call_string(1) + "\n"
    content += "    return results\n\n\n"
    if is_async:
        content += "async def call_main():\n"
    else:
        content += "def call_main() -> None:\n"
    content += '    """Run the main function and print the results."""\n'
    if is_async:
        content += "    results = await main()\n"
    else:
        content += "    results = main()\n"
    content += "    if not isinstance(results, list):\n"
    content += "        results = [results]\n"
    content += "    for result in results:\n"
    content += "        pprint(asdict(result))\n\n\n"
    content += 'if __name__ == "__main__":\n'
    if is_async:
        content += "    anyio.run(call_main())\n"
    else:
        content += "    call_main()\n"
    return content
