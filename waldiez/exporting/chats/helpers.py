"""Helper functions for exporting chat data to code.

Functions
---------
export_single_chat_string
    Get the chat string when there is only one chat in the flow.
export_multiple_chats_string
    Get the chats content, when there are more than one chats in the flow.
"""

# flake8: noqa E501
from typing import Any, Dict, Optional, Tuple

from waldiez.models import (
    WaldiezAgent,
    WaldiezChat,
    WaldiezChatMessage,
    WaldiezRagUser,
)

from ..utils import get_escaped_string, get_object_string


def escape_summary_args_quotes(chat_args: Dict[str, Any]) -> Dict[str, Any]:
    """Escape quotes in the summary args if they are strings.

    Parameters
    ----------
    chat_args : Dict[str, Any]
        The chat arguments.

    Returns
    -------
    Dict[str, Any]
        The chat arguments with the summary prompt escaped.
    """
    if "summary_args" in chat_args and isinstance(
        chat_args["summary_args"], dict
    ):
        for key, value in chat_args["summary_args"].items():
            if isinstance(value, str):
                chat_args["summary_args"][key] = get_escaped_string(value)
    return chat_args


def get_chat_message_string(
    chat: WaldiezChat,
    chat_names: Dict[str, str],
) -> Tuple[str, Optional[str]]:
    """Get the agent's message as a string.

    Parameters
    ----------
    chat : WaldiezChat
        The chat.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name with all the chats in the flow.

    Returns
    -------
    Tuple[str, Optional[str]]
        If the message is a string, the message content and None.
        If the message is a method, the method name and the method content.
        If the message is None, 'None' and None.
    """
    if (
        not chat.message
        or chat.message.type == "none"
        or chat.message.content is None
        or chat.message_content is None
    ):
        return "None", None
    if chat.message.type == "string":
        return get_escaped_string(chat.message.content), None
    chat_name = chat_names[chat.id]
    original_function_name = "callable_message"
    function_args = "sender, recipient, context"
    function_name = f"{original_function_name}_{chat_name}"
    function_def = f"def {function_name}({function_args}):"
    return function_name, function_def + "\n" + chat.message_content + "\n"


def get_chat_dict_string(
    chat: WaldiezChat,
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    chat_names: Dict[str, str],
    agent_names: Dict[str, str],
    tabs: int,
) -> Tuple[str, str]:
    """Get a chat dictionary string.

    If the chat message is a separate method and not a string or a lambda,
    we return the method string (definition and body) as well as the rest
    of the arguments.

    Parameters
    ----------
    chat : WaldiezChat
        The chat.
    sender : WaldiezAgent
        The sender.
    recipient : WaldiezAgent
        The recipient.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The chat dictionary string and additional methods string if any.
    """
    tab = "    " * tabs
    chat_args = chat.get_chat_args(sender=sender)
    chat_args = escape_summary_args_quotes(chat_args)
    chat_string = "{"
    chat_string += "\n" + f'{tab}    "sender": {agent_names[sender.id]},'
    chat_string += "\n" + f'{tab}    "recipient": {agent_names[recipient.id]},'
    additional_methods_string = ""
    for key, value in chat_args.items():
        if isinstance(value, str):
            chat_string += "\n" + f'{tab}    "{key}": "{value}",'
        elif isinstance(value, dict):
            chat_string += (
                "\n"
                f'{tab}    "{key}": {get_object_string(value, tabs=tabs + 1)},'
            )
        else:
            chat_string += "\n" + f'{tab}    "{key}": {value},'
    if (
        sender.agent_type == "rag_user"
        and isinstance(sender, WaldiezRagUser)
        and chat.message.type == "rag_message_generator"
    ):
        message = f"{agent_names[sender.id]}.message_generator"
        chat_string += "\n" + f'{tab}    "message": {message},'
        chat_string += "\n" + tab + "},"
        return chat_string, additional_methods_string
    message, method_content = get_chat_message_string(
        chat=chat,
        chat_names=chat_names,
    )
    if message and isinstance(chat.data.message, WaldiezChatMessage):
        message = get_escaped_string(message)
        if chat.data.message.type == "method":
            if method_content:
                additional_methods_string += "\n" + method_content
            chat_string += "\n" + f'{tab}    "message": {message},'
        elif chat.data.message.type == "string" and chat.data.message.content:
            chat_string += "\n" + f'{tab}    "message": "{message}",'
    chat_string += "\n" + tab + "},"
    return chat_string, additional_methods_string


def get_empty_simple_chat_string(
    tab: str,
    chat: WaldiezChat,
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    agent_names: Dict[str, str],
) -> Tuple[str, str]:
    """Get the chat string when there are no chat arguments.

    Parameters
    ----------
    tab : str
        The tab string.
    chat : WaldiezChat
        The chat.
    sender : WaldiezAgent
        The sender.
    recipient : WaldiezAgent
        The recipient.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.

    Returns
    -------
    Tuple[str, str]
        The chat string and additional methods string if any
    """
    content = tab
    sender_name = agent_names[sender.id]
    recipient_name = agent_names[recipient.id]
    content += f"{sender_name}.initiate_chat(\n"
    content += tab + f"    {recipient_name},\n"
    message_arg, _ = _get_chat_message(
        tab=tab,
        chat=chat,
        chat_names={},
        sender=sender,
        sender_name=sender_name,
    )
    content += message_arg
    content += tab + ")"
    return content, ""


def get_simple_chat_string(
    chat: WaldiezChat,
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    agent_names: Dict[str, str],
    chat_names: Dict[str, str],
    chat_args: Dict[str, Any],
    tabs: int,
) -> Tuple[str, str]:
    """Get the chat string when there are chat arguments.

    Parameters
    ----------
    chat : WaldiezChat
        The chat.
    sender : WaldiezAgent
        The sender.
    recipient : WaldiezAgent
        The recipient.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name.
    chat_args : Dict[str, Any]
        The chat arguments.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The chat string and additional methods string if any.
    """
    tab = "    " * tabs
    sender_name = agent_names[sender.id]
    recipient_name = agent_names[recipient.id]
    chat_string = f"{sender_name}.initiate_chat(\n"
    chat_string += f"{tab}    {recipient_name},"
    for key, value in chat_args.items():
        if isinstance(value, str):
            chat_string += f'\n{tab}    {key}="{value}",'
        elif isinstance(value, dict):
            chat_string += (
                f"\n{tab}    {key}={get_object_string(value, tabs + 1)},"
            )
        else:
            chat_string += f"\n{tab}    {key}={value},"
    message_arg, additional_methods_string = _get_chat_message(
        tab=tab,
        chat=chat,
        chat_names=chat_names,
        sender=sender,
        sender_name=sender_name,
    )
    chat_string += message_arg
    chat_string += f"\n{tab})"
    return chat_string, additional_methods_string


def _get_chat_message(
    tab: str,
    chat: WaldiezChat,
    chat_names: Dict[str, str],
    sender: WaldiezAgent,
    sender_name: str,
) -> Tuple[str, str]:
    additional_methods_string = ""
    method_content: Optional[str] = None
    if (
        sender.agent_type == "rag_user"
        and isinstance(sender, WaldiezRagUser)
        and chat.message.type == "rag_message_generator"
    ):
        message = f"{sender_name}.message_generator"
        return f"\n{tab}    message={message},", additional_methods_string
    message, method_content = get_chat_message_string(
        chat=chat,
        chat_names=chat_names,
    )
    if message and isinstance(chat.data.message, WaldiezChatMessage):
        message = get_escaped_string(message)
        if chat.data.message.type == "method":
            additional_methods_string += (
                method_content if method_content else ""
            )
            return f"\n{tab}    message={message},", additional_methods_string
        if chat.message.type == "string" and chat.data.message.content:
            return f'\n{tab}    message="{message}",', additional_methods_string
        return "", additional_methods_string
    return "", additional_methods_string  # pragma: no cover
