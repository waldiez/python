"""Common helper functions for chat exporting."""

from typing import Any, Callable, Dict, Optional, Tuple

from waldiez.models import (
    WaldiezAgent,
    WaldiezChat,
    WaldiezChatMessage,
    WaldiezRagUser,
)
from waldiez.models.chat import (
    CALLABLE_MESSAGE_HINTS,
    CALLABLE_MESSAGE_RAG_WITH_CARRYOVER_HINTS,
)


def update_summary_chat_args(
    chat_args: Dict[str, Any],
    string_escape: Callable[[str], str],
) -> Dict[str, Any]:
    """Escape quotes in the summary args if they are strings.

    Parameters
    ----------
    chat_args : Dict[str, Any]
        The chat arguments.
    string_escape : Callable[[str], str]
        The function to escape the string

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
                chat_args["summary_args"][key] = string_escape(value)
    return chat_args


def get_chat_message_string(
    sender: WaldiezAgent,
    chat: WaldiezChat,
    chat_names: Dict[str, str],
    string_escape: Callable[[str], str],
) -> Tuple[str, Optional[str]]:
    """Get the agent's message as a string.

    Parameters
    ----------
    sender : WaldiezAgent
        The sender.
    chat : WaldiezChat
        The chat.
    chat_names : Dict[str, str]
        A mapping of chat id to chat name with all the chats in the flow.
    string_escape : Callable[[str], str]
        The function to escape the string.

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
        return string_escape(chat.message.content), None

    is_rag_with_carryover = (
        sender.agent_type == "rag_user" and chat.message.use_carryover
    )
    chat_name = chat_names[chat.id]
    original_function_name = "callable_message"
    function_args = "sender, recipient, context"
    function_name = f"{original_function_name}_{chat_name}"
    function_def = f"def {function_name}({function_args}):"
    message_content = chat.message_content
    if is_rag_with_carryover:
        message_content = chat.message_content.replace(
            CALLABLE_MESSAGE_HINTS,
            CALLABLE_MESSAGE_RAG_WITH_CARRYOVER_HINTS,
            1,
        )
    return function_name, function_def + "\n" + message_content + "\n"


# pylint: disable=too-many-locals
def get_chat_dict_string(
    chat: WaldiezChat,
    sender: WaldiezAgent,
    recipient: WaldiezAgent,
    chat_names: Dict[str, str],
    agent_names: Dict[str, str],
    serializer: Callable[..., str],
    string_escape: Callable[[str], str],
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
    serializer : Callable[[str], str]
        The function to serialize the dictionaries or lists.
    string_escape : Callable[[str], str]
        The function to escape the string.
    tabs : int
        The number of tabs to use for indentation.

    Returns
    -------
    Tuple[str, str]
        The chat dictionary string and additional methods string if any.
    """
    tab = "    " * tabs
    chat_args = chat.get_chat_args(sender=sender)
    chat_args = update_summary_chat_args(chat_args, string_escape)
    chat_string = "{"
    chat_string += "\n" + f'{tab}    "sender": {agent_names[sender.id]},'
    chat_string += "\n" + f'{tab}    "recipient": {agent_names[recipient.id]},'
    additional_methods_string = ""
    for key, value in chat_args.items():
        if isinstance(value, str):
            chat_string += "\n" + f'{tab}    "{key}": "{value}",'
        elif isinstance(value, dict):
            chat_string += (
                "\n" f'{tab}    "{key}": {serializer(value, tabs=tabs + 1)},'
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
        sender=sender,
        chat=chat,
        chat_names=chat_names,
        string_escape=string_escape,
    )
    if message and isinstance(chat.data.message, WaldiezChatMessage):
        message = string_escape(message)
        if chat.data.message.type == "method":
            if method_content:
                additional_methods_string += "\n" + method_content
            chat_string += "\n" + f'{tab}    "message": {message},'
        elif chat.data.message.type == "string" and chat.data.message.content:
            chat_string += "\n" + f'{tab}    "message": "{message}",'
    chat_string += "\n" + tab + "},"
    return chat_string, additional_methods_string
