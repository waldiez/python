# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# flake8: noqa: E501
# pylint: disable=inconsistent-quotes, line-too-long
"""Get the main function."""


def get_def_main(flow_chats: str, after_run: str, is_async: bool) -> str:
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
    after_run : str
        The content after the run of the flow.
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
    content += "    # type: () -> Union[ChatResult, List[ChatResult], Dict[int, ChatResult]]\n"
    content += '    """Start chatting."""\n'
    content += f"{flow_chats}" + "\n"
    if is_async:
        content += "    await stop_logging()"
    else:
        content += "    stop_logging()"
    content += after_run
    content += "\n    return results\n\n\n"
    if is_async:
        content += "async def call_main():\n"
    else:
        content += "def call_main() -> None:\n"
    content += '    """Run the main function and print the results."""\n'
    content += "    results: Union[ChatResult, List[ChatResult], Dict[int, ChatResult]] = "
    if is_async:
        content += "await "
    content += "main()\n"
    content += "    if isinstance(results, dict):\n"
    content += "        # order by key\n"
    content += "        ordered_results = dict(sorted(results.items()))\n"
    content += "        for _, result in ordered_results.items():\n"
    content += "            pprint(asdict(result))\n"
    content += "    elif isinstance(results, list):\n"
    content += "        for result in results:\n"
    content += "            pprint(asdict(result))\n"
    content += "    else:\n"
    content += "        pprint(asdict(results))\n"
    content += 'if __name__ == "__main__":\n'
    if is_async:
        content += "    anyio.run(call_main)\n"
    else:
        content += "    call_main()\n"
    return content
