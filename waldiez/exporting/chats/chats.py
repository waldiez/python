"""Export the chats content."""

# flake8: noqa E501
# pylint: disable=line-too-long
from typing import Dict, List, Tuple

from waldiez.models import WaldiezAgent, WaldiezChat

from .helpers import (
    escape_summary_args_quotes,
    get_chat_dict_string,
    get_empty_simple_chat_string,
    get_simple_chat_string,
)


def export_chats(
    main_chats: List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]],
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    tabs: int,
) -> Tuple[str, str]:
    """Get the chats content.

    Parameters
    ----------
    main_chats : List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]]
        The main flow chats.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The chats content and additional methods string if any.
    """
    if len(main_chats) == 1:
        return export_single_chat_string(
            flow=main_chats[0],
            agent_names=agent_names,
            chat_names=chat_names,
            tabs=tabs,
        )
    return export_multiple_chats_string(
        main_chats=main_chats,
        chat_names=chat_names,
        agent_names=agent_names,
        tabs=tabs,
    )


# pylint: disable=line-too-long
def export_single_chat_string(
    flow: Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent],
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    tabs: int,
) -> Tuple[str, str]:
    """Get the chat string when there is only one chat in the flow.

    Parameters
    ----------
    flow : Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]
        The chat flow.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The chat string and additional methods string if any

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezAgent, WaldiezChat, WaldiezChatData, WaldiezChatMessage
    >>> chat = WaldiezChat(
    ...     id="wc-1",
    ...     name="chat1",
    ...     description="A chat between two agents.",
    ...     tags=["chat", "chat1"],
    ...     requirements=[],
    ...     data=WaldiezChatData(
    ...         sender="wa-1",
    ...         recipient="wa-2",
    ...         message=WaldiezChatMessage(
    ...             type="string",
    ...             content="Hello, how are you?",
    ...         ),
    ...     ),
    ... )
    >>> agent_names = {"wa-1": "agent1", "wa-2": "agent2"}
    >>> chat_names = {"wc-1": "chat1"}
    >>> export_single_chat_string((chat, agent1, agent2), agent_names, chat_names, 0)
    agent1.initiate_chat(
        agent2,
        message="Hello, how are you?",
    )
    ```
    """
    tab = "    " * tabs
    chat, sender, recipient = flow
    chat_args = chat.get_chat_args(sender=sender)
    chat_args = escape_summary_args_quotes(chat_args)
    if not chat_args:
        return get_empty_simple_chat_string(
            tab,
            chat=chat,
            sender=sender,
            recipient=recipient,
            agent_names=agent_names,
        )
    return get_simple_chat_string(
        chat=chat,
        chat_args=chat_args,
        sender=sender,
        recipient=recipient,
        agent_names=agent_names,
        chat_names=chat_names,
        tabs=tabs,
    )


def export_multiple_chats_string(
    main_chats: List[Tuple[WaldiezChat, WaldiezAgent, WaldiezAgent]],
    chat_names: Dict[str, str],
    agent_names: Dict[str, str],
    tabs: int,
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
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The main chats content and additional methods string if any.

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezAgent, WaldiezChat, WaldiezChatData, WaldiezChatMessage
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
    >>> export_multiple_chats_string([(chat1, agent1, agent2), (chat2, agent2, agent1)], chat_names, agent_names, 0)
    initiate_chats([
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
    tab = "    " * tabs
    content = "\n"
    additional_methods_string = ""
    content = "initiate_chats(["
    for chat, sender, recipient in main_chats:
        chat_string, additional_methods = get_chat_dict_string(
            chat=chat,
            chat_names=chat_names,
            sender=sender,
            recipient=recipient,
            agent_names=agent_names,
            tabs=tabs + 1,
        )
        additional_methods_string += additional_methods
        content += f"\n{tab}    {chat_string}"
    content += "\n" + "    " * tabs + "])"
    return content, additional_methods_string
