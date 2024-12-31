"""Utility functions for exporting sequential chats."""

from typing import Callable, Dict, List, Tuple

from waldiez.models import WaldiezAgent, WaldiezChat

from .helpers import get_chat_dict_string


def export_sequential_chat(
    main_chats: List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]],
    chat_names: Dict[str, str],
    agent_names: Dict[str, str],
    serializer: Callable[..., str],
    string_escape: Callable[[str], str],
    tabs: int,
    is_async: bool,
) -> Tuple[str, str]:
    """Get the chats content, when there are more than one chats in the flow.

    Parameters
    ----------
    main_chats : List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]]
        The main chats.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    serializer : Callable[..., str]
        The serializer function to escape quotes in a string.
    string_escape : Callable[[str], str]
        The string escape function.
    tabs : int
        The number of tabs to use for indentation.
    is_async : bool
        Whether the chat is asynchronous.

    Returns
    -------
    Tuple[str, str]
        The main chats content and additional methods string if any.

    Example
    -------
    ```python
    >>> from waldiez.models import (
    ...     WaldiezAgent,
    ...     WaldiezChat,
    ...     WaldiezChatData,
    ...     WaldiezChatMessage,
    ... )
    >>> chat1 = WaldiezChat(
    ...     id="wc-1",
    ...     name="chat1",
    ...     description="A chat between two agents.",
    ...     tags=["chat", "chat1"],
    ...     requirements=[],
    ...     data=WaldiezChatData(
    ...         sender="wa-1",
    ...         recipient="wa-2",
    ...         position=0,
    ...         message=WaldiezChatMessage(
    ...             type="string",
    ...             content="Hello, how are you?",
    ...         ),
    ...     ),
    ... )
    >>> chat2 = WaldiezChat(
    ...     id="wc-2",
    ...     name="chat2",
    ...     description="A chat between two agents.",
    ...     tags=["chat", "chat2"],
    ...     requirements=[],
    ...     data=WaldiezChatData(
    ...         sender="wa-2",
    ...         recipient="wa-1",
    ...         position=1,
    ...         message=WaldiezChatMessage(
    ...             type="string",
    ...             content="I am good, thank you. How about you?",
    ...         ),
    ...     ),
    ... )
    >>> agent_names = {"wa-1": "agent1", "wa-2": "agent2"}
    >>> chat_names = {"wc-1": "chat1", "wc-2": "chat2"}
    >>> serializer = lambda x: x.replace('"', "\"").replace("\n", "\\n")
    >>>  export_sequential_chat(
    ...     main_chats=[(chat1, agent1, agent2), (chat2, agent2, agent1)],
    ...     chat_names=chat_names,
    ...     agent_names=agent_names,
    ...     serializer=serializer,
    ...     tabs=0,
    ...     is_async=False,
    ... )
    results = initiate_chats([
        {
            "sender": agent1,
            "recipient": agent2,
            "message": "Hello, how are you?",
        },
        {
            "sender": agent2,
            "recipient": agent1,
            "message": "I am good, thank you. How about you?",
        },
    ])
    ```
    """
    tab = "    " * tabs if tabs > 0 else ""
    content = "\n"
    additional_methods_string = ""
    content += _get_initiate_chats_line(tab, is_async)
    for chat, sender, recipient in main_chats:
        chat_string, additional_methods = get_chat_dict_string(
            chat=chat,
            chat_names=chat_names,
            sender=sender,
            recipient=recipient,
            agent_names=agent_names,
            serializer=serializer,
            string_escape=string_escape,
            tabs=tabs + 1,
        )
        additional_methods_string += additional_methods
        content += "\n" + f"{tab}    {chat_string}"
    content += "\n" + "    " * tabs + "])\n"
    return content, additional_methods_string


def _get_initiate_chats_line(
    tab: str,
    is_async: bool,
) -> str:
    """Get the initiate chats line.

    Parameters
    ----------
    tab : str
        The tab string.
    is_async : bool
        Whether the chat is asynchronous.

    Returns
    -------
    str
        The initiate chats line.
    """
    results_is = f"{tab}results = "
    initiate = "initiate_chats"
    if is_async:
        results_is += "await "
        initiate = "a_initiate_chats"
    return results_is + initiate + "(["
