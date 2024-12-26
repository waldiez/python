"""Export the chats content."""

# flake8: noqa E501
# pylint: disable=line-too-long
from typing import Dict, List, Tuple

from waldiez.models import Waldiez, WaldiezAgent, WaldiezChat, WaldiezFlow

from ..utils import get_object_string
from .helpers import (
    escape_summary_args_quotes,
    get_chat_dict_string,
    get_empty_simple_chat_string,
    get_simple_chat_string,
    get_swarm_after_work_string,
    get_swarm_agents_strings,
    get_swarm_messages_string,
)


def export_chats(
    waldiez: Waldiez,
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    tabs: int,
) -> Tuple[str, str]:
    """Get the chats content.

    Parameters
    ----------
    waldiez : Waldiez
        The Waldiez instance.
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
    main_chats = waldiez.chats
    if len(main_chats) == 1:
        main_chat = main_chats[0]
        chat, sender, recipient = main_chat
        if sender.agent_type == "swarm" or recipient.agent_type == "swarm":
            return export_swarm_message_string(
                flow=waldiez.flow,
                chat=chat,
                agent_names=agent_names,
                chat_names=chat_names,
                sender=sender,
                recipient=recipient,
                tabs=tabs,
            )
        return export_single_chat_string(
            sender=sender,
            recipient=recipient,
            chat=chat,
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
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    chat: WaldiezChat,
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    tabs: int,
) -> Tuple[str, str]:
    """Get the chat string when there is only one chat in the flow.

    Parameters
    ----------
    sender : WaldiezAgent
        The sender.
    recipient : WaldiezAgent
        The recipient.
    chat : WaldiezChat
        The chat.
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
    >>> export_single_chat_string(
    ...     sender=agent1,
    ...     recipient=agent2,
    ...     chat=chat,
    ...     agent_names=agent_names,
    ...     chat_names=chat_names,
    ...     tabs=0,
    ... )
    agent1.initiate_chat(
        agent2,
        message="Hello, how are you?",
    )
    ```
    """
    tab = "    " * tabs if tabs > 0 else ""
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
    tab = "    " * tabs if tabs > 0 else ""
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


# pylint: disable=too-many-locals
def export_swarm_message_string(
    flow: WaldiezFlow,
    chat: WaldiezChat,
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    tabs: int,
) -> Tuple[str, str]:
    """Get the swarm chat message string.

    Parameters
    ----------
    flow : WaldiezFlow
        The flow.
    chat : WaldiezChat
        The chat.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    sender : WaldiezAgent
        The sender.
    recipient : WaldiezAgent
        The recipient.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The `initiate_swarm_chat` message string and additional methods string.

    Raises
    ------
    ValueError
        If neither the sender nor the recipient is a swarm agent.

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezAgent, WaldiezChat, WaldiezChatData, WaldiezChatMessage, WaldiezSwarmAfterWork
    >>> chat = WaldiezChat(
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
    ...         max_rounds=10,
    ...         context_variables={"variable1": "value1"},
    ...         after_work=WaldiezSwarmAfterWork(
    ...             recipient="wa-1",
    ...             recipient_type="agent",
    ...         ),
    ...     ),
    ... )
    >>> agent1 = WaldiezAgent(
    ...     id="wa-1",
    ...     name="agent1",
    ...     agent_type="swarm",
    ...     description="A swarm agent.",
    ...     ...,
    ... )
    >>> agent2 = WaldiezAgent(
    ...     id="wa-2",
    ...     name="agent2",
    ...     agent_type="swarm",
    ...     description="A swarm agent.",
    ...     ...,
    ... )
    >>> agent3 = WaldiezAgent(
    ...     id="wa-3",
    ...     name="agent3",
    ...     agent_type="user",
    ...     description="A user agent.",
    ...     ...,
    ... )
    >>> flow = WaldiezFlow(
    ...     ...
    ... )
    >>> agent_names = {"wa-1": "agent1", "wa-2": "agent2", "wa-3": "agent3"}
    >>> chat_names = {"wc-1": "chat1"}
    >>> export_swarm_message_string(flow, chat, agent_names, chat_names, agent1, agent2, 0)
    initiate_swarm_chat(
        initial_agent=agent1,
        agents=[agent1, agent2],
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        context_variables={"variable1": "value1"},
        user_agent=agent3,
        after_work=AFTER_WORK(agent1)",
        max_rounds=10,
    )
    ```
    """
    # either the sender or the recipient can be the swarm agent
    # one of them MUST be the swarm agent.
    if sender.agent_type != "swarm" and recipient.agent_type != "swarm":
        raise ValueError("One of the agents must be a swarm agent")
    initial_agent = sender if sender.agent_type == "swarm" else recipient
    tab = "    " * tabs if tabs > 0 else ""
    swarm_agents_string, user_agent_string = get_swarm_agents_strings(
        flow=flow,
        initial_agent=initial_agent,
        sender=sender,
        recipient=recipient,
        agent_names=agent_names,
        user_agent=None,
    )
    messages_string = get_swarm_messages_string(chat)
    context_variables_string = (
        get_object_string(chat.context_variables, tabs=tabs + 1)
        if chat.context_variables
        else "{}"
    )
    after_work_string, additional_methods = get_swarm_after_work_string(
        chat=chat,
        chat_names=chat_names,
        agent_names=agent_names,
    )
    # fmt: off
    initiate_chat = "initiate_swarm_chat(\n"
    initiate_chat += f"{tab}    initial_agent={agent_names[initial_agent.id]},\n"
    initiate_chat += f"{tab}    agents=[{swarm_agents_string}],\n"
    initiate_chat += f"{tab}    messages={messages_string},\n"
    initiate_chat += f"{tab}    context_variables={context_variables_string},\n"
    initiate_chat += f"{tab}    user_agent={user_agent_string},\n"
    initiate_chat += f"{tab}    after_work={after_work_string},\n"
    initiate_chat += f"{tab}    max_rounds={chat.max_rounds},\n"
    initiate_chat += f"{tab})"
    # fmt: on
    return initiate_chat, additional_methods
