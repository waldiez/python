"""Swarm chat exporting functions."""

# flake8: noqa E501

from typing import Callable, Dict, List, Optional, Tuple

from waldiez.models import WaldiezAgent, WaldiezChat


# pylint: disable=too-many-locals,line-too-long
def export_swarm_chat(
    chat: WaldiezChat,
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    get_swarm_members: Callable[
        [WaldiezAgent], Tuple[List[WaldiezAgent], WaldiezAgent | None]
    ],
    serializer: Callable[..., str],
    string_escape: Callable[[str], str],
    tabs: int,
) -> Tuple[str, str]:
    """Get the swarm chat message string.

    Parameters
    ----------
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
    get_swarm_members: Callable[[WaldiezAgent], Tuple[List[WaldiezAgent], WaldiezAgent | None]],
        The function to get the swarm members.
    serializer : Callable[..., str]
        The function to generate the string representation of an object.
    string_escape : Callable[[str], str]
        The function to escape the string.
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
    """
    # either the sender or the recipient can be the swarm agent
    # one of them MUST be the swarm agent.
    if sender.agent_type != "swarm" and recipient.agent_type != "swarm":
        raise ValueError("One of the agents must be a swarm agent")
    initial_agent = sender if sender.agent_type == "swarm" else recipient
    tab = "    " * tabs if tabs > 0 else ""
    swarm_members = get_swarm_members(initial_agent)
    swarm_agents_string, user_agent_string = get_swarm_agents_strings(
        swarm_members=swarm_members,
        sender=sender,
        recipient=recipient,
        agent_names=agent_names,
        user_agent=None,
    )
    messages_string = get_swarm_messages_string(
        chat=chat, string_escape=string_escape
    )
    context_vars_string = (
        serializer(chat.context_variables, tabs=tabs + 1)
        if chat.context_variables
        else "{}"
    )
    after_work_string, additional_methods = get_swarm_after_work_string(
        chat=chat,
        chat_names=chat_names,
        agent_names=agent_names,
    )
    agent_name = agent_names[initial_agent.id]
    initiate_chat = "\n" + f"{tab}results, _, __ = initiate_swarm_chat(" + "\n"
    initiate_chat += f"{tab}    initial_agent={agent_name}," + "\n"
    initiate_chat += f"{tab}    agents=[{swarm_agents_string}]," + "\n"
    initiate_chat += f"{tab}    messages={messages_string}," + "\n"
    initiate_chat += f"{tab}    context_variables={context_vars_string}," + "\n"
    initiate_chat += f"{tab}    user_agent={user_agent_string}," + "\n"
    initiate_chat += f"{tab}    after_work={after_work_string}," + "\n"
    initiate_chat += f"{tab}    max_rounds={chat.max_rounds}," + "\n"
    initiate_chat += f"{tab})" + "\n"
    return initiate_chat, additional_methods


def get_swarm_agents_strings(
    swarm_members: Tuple[List[WaldiezAgent], WaldiezAgent | None],
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    agent_names: Dict[str, str],
    user_agent: Optional[WaldiezAgent],
) -> Tuple[str, str]:
    """Get the swarm agent strings to use in `initiate_swarm_chat`.

    Parameters
    ----------
    swarm_members : Tuple[List[WaldiezAgent], WaldiezAgent | None]
        The swarm agents and the user agent.
    sender : WaldiezAgent
        The chat initiator.
    recipient : WaldiezAgent
        The chat recipient.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    user_agent : Optional[WaldiezAgent]
        The user agent.
    Returns
    -------
    Tuple[str, str]
        The swarm agents string and the user agent string.
    """
    swarm_agents, user_member = swarm_members
    if user_agent is None and user_member is not None:
        user_agent = user_member
    if user_agent is None:  # pragma: no cover
        if sender.agent_type in ("user", "rag_user"):
            user_agent = sender
        elif recipient.agent_type in ("user", "rag_user"):
            user_agent = recipient
    agents_string = ", ".join(
        [f"{agent_names[agent.id]}" for agent in swarm_agents]
    )
    user_agent_string = "None"
    if user_agent:
        user_agent_string = agent_names[user_agent.id]
    return agents_string, user_agent_string


def get_swarm_messages_string(
    chat: WaldiezChat,
    string_escape: Callable[[str], str],
) -> str:
    """Get the swarm chat messages string to use in `initiate_swarm_chat`.

    Parameters
    ----------
    chat : WaldiezChat
        The chat.
    string_escape : Callable[[str], str]
        The string escape function.

    Returns
    -------
    str
        The swarm chat messages string.
    """
    chat_message = chat.message
    if chat.message.type == "string" and chat_message.content:
        messages_string = '[{"role": "user", "content": '
        escaped_message = string_escape(chat_message.content)
        messages_string += f'"{escaped_message}"'
        messages_string += "}]"
    else:
        messages_string = ""
    return messages_string


def get_swarm_after_work_string(
    chat: WaldiezChat,
    chat_names: Dict[str, str],
    agent_names: Dict[str, str],
) -> Tuple[str, str]:
    """Get the swarm after work string.

    Parameters
    ----------
    chat : WaldiezChat
        The chat.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    Returns
    -------
    Tuple[str, str]
        The after work string and the additional methods string.
    """
    if not chat.after_work:
        return "AFTER_WORK(AfterWorkOption.TERMINATE)", ""
    additional_methods = ""
    chat_name = chat_names[chat.id]
    function_name = f"custom_after_work_{chat_name}"
    after_work_string = chat.after_work.get_recipient_string(
        agent_names=agent_names, function_name=function_name
    )
    if chat.after_work.recipient_type == "callable":
        additional_methods = "\n" + f"{after_work_string}"
        after_work_string = f"{function_name}"
    return after_work_string, additional_methods
