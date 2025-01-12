# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# pylint: disable=unused-argument
"""Get the extras for a swarm agent."""

from typing import Any, Callable, Dict, List, Tuple

from waldiez.exporting.chats.utils.nested import get_nested_chat_queue
from waldiez.models import (
    WaldiezAgent,
    WaldiezAgentNestedChat,
    WaldiezChat,
    WaldiezSwarmAfterWork,
    WaldiezSwarmAgent,
    WaldiezSwarmOnCondition,
    WaldiezSwarmUpdateSystemMessage,
)

# SwarmAgent is a subclass of ConversableAgent.

# Additional args:
# functions (List[Callable]):
#   -A list of functions to register with the agent.
# update_agent_state_before_reply (List[Callable]):
# - A list of functions, including UPDATE_SYSTEM_MESSAGEs,
#   called to update the agent before it replies.


def get_swarm_extras(
    agent: WaldiezAgent,
    agent_names: Dict[str, str],
    skill_names: Dict[str, str],
    chats: Tuple[List[WaldiezChat], Dict[str, str]],
    is_async: bool,
    serializer: Callable[..., str],
    string_escape: Callable[[str], str],
) -> Tuple[str, str, str]:
    """Get the extras of a swarm agent.

    Parameters
    ----------
    agent : WaldiezAgent
        The agent to get the extras for.
    agent_names : Dict[str, str]
        A mapping of agent IDs to agent names.
    skill_names : Dict[str, str]
        A mapping of skill IDs to skill names.
    chats : Tuple[List[WaldiezChat], Dict[str, str]]
        The list of all chats and the mapping of chat IDs to chat names.
    is_async : bool
        Whether the chat is asynchronous.
    serializer : Callable[..., str]
        The serializer to get the string representation of an object.
    string_escape : Callable[[str], str]
        The function to escape the string quotes and newlines.
    Returns
    -------
    Tuple[str, str, str]
        The extras of the swarm agent:
        the content before the agent,
        the extra argument(s) for the agent initialization,
        and the content after the agent.
    """
    args_string = ""
    before_agent = ""
    after_agent = ""
    if agent.agent_type != "swarm" or not isinstance(agent, WaldiezSwarmAgent):
        return args_string, before_agent, after_agent
    args_string = get_function_arg(agent, skill_names)
    before_reply = get_update_agent_state_before_reply_arg(
        agent=agent,
        agent_names=agent_names,
        skill_names=skill_names,
        string_escape=string_escape,
    )
    args_string += before_reply[0]
    before_agent += before_reply[1]
    before_registration, after_agent = get_agent_handoff_registrations(
        agent=agent,
        agent_names=agent_names,
        all_chats=chats[0],
        chat_names=chats[1],
        is_async=is_async,
        serializer=serializer,
        string_escape=string_escape,
    )
    before_agent += before_registration
    return before_agent, args_string, after_agent


def get_function_arg(
    agent: WaldiezSwarmAgent,
    skill_names: Dict[str, str],
) -> str:
    """Get the function argument of a swarm agent.

    Parameters
    ----------
    agent : WaldiezSwarmAgent
        The swarm agent to get the function argument for.
    skill_names : Dict[str, str]
        A mapping of skill IDs to skill names.

    Returns
    -------
    str
        The function argument of the swarm agent.
    """
    tab = "    "
    arg_string = f"{tab}functions=["
    added_skills = False
    for function in agent.data.functions:
        skill_name = skill_names.get(function, "")
        if skill_name:
            arg_string += "\n" + f"{tab}{tab}{skill_name},"
            added_skills = True
    if added_skills:
        arg_string += "\n" + tab
    arg_string += "],\n"
    return arg_string


def get_update_agent_state_before_reply_arg(
    agent: WaldiezSwarmAgent,
    agent_names: Dict[str, str],
    skill_names: Dict[str, str],
    string_escape: Callable[[str], str],
) -> Tuple[str, str]:
    """Get the update_agent_state_before_reply argument of a swarm agent.

    Parameters
    ----------
    agent : WaldiezSwarmAgent
        The swarm agent to get the argument for.
    agent_names : Dict[str, str]
        A mapping of agent IDs to agent names.
    skill_names : Dict[str, str]
        A mapping of skill IDs to skill names.
    string_escape : Callable[[str], str]
        The function to escape the string quotes and newlines.

    Returns
    -------
    Tuple[str, str]
        The update_agent_state_before_reply argument of the swarm agent
        and the content before the agent if any.
    """
    #     update_function_type : Literal["string", "callable"]
    #     The type of the update function. Can be either a string or a callable.
    # update_function : str
    #     "The string template or function definition to update "
    #          "the agent's system message. Can be a string or a Callable. "
    #           "If the function_type is 'string' it will be used as a "
    #            "template and substitute the context variables. "
    #         ag2 checks for: vars = re.findall(r"\{(\w+)\}", function)
    #     "If function_type is 'callable', it should have signature:
    #  "def custom_update_system_message("
    #     " agent: ConversableAgent, "
    #     " messages: List[Dict[str, Any]]
    #   ) -> str"
    tab = "    "
    before_agent = ""
    arg_string = f"{tab}update_agent_state_before_reply=["
    added_functions = False
    for function in agent.data.update_agent_state_before_reply:
        if isinstance(function, WaldiezSwarmUpdateSystemMessage):
            added_functions = True
            if function.update_function_type == "callable":
                function_content, function_name = function.get_update_function(
                    name_suffix=agent_names[agent.id],
                )
                arg_string += "\n" + f"{tab}{tab}{function_name},"
                before_agent += "\n" + function_content + "\n"
            else:
                escaped_function = string_escape(function.update_function)
                arg_string += "\n" + f'{tab}{tab}"{escaped_function}",'
        else:
            skill_name = skill_names.get(function, "")
            if skill_name:
                added_functions = True
                arg_string += "\n" + f"{tab}{tab}{skill_name},"
    if added_functions:
        arg_string = arg_string + "\n" + tab
    arg_string += "],\n"
    return arg_string, before_agent


def get_agent_handoff_registrations(
    agent: WaldiezSwarmAgent,
    agent_names: Dict[str, str],
    all_chats: List[WaldiezChat],
    chat_names: Dict[str, str],
    is_async: bool,
    serializer: Callable[..., str],
    string_escape: Callable[[str], str],
) -> Tuple[str, str]:
    """Get the agent handoff registrations of a swarm agent.

    Parameters
    ----------
    agent : WaldiezSwarmAgent
        The swarm agent to get the agent handoff registrations for.
    agent_names : Dict[str, str]
        A mapping of agent IDs to agent names.
    all_chats : List[WaldiezChat]
        The list of all chats.
    chat_names : Dict[str, str]
        A mapping of chat IDs to chat names.
    is_async : bool
        Whether the chat is asynchronous.
    serializer : Callable[..., str]
        The serializer to get the string representation of an object.
    string_escape : Callable[[str], str]
        The function to escape the string quotes and newlines.

    Returns
    -------
    Tuple[str, str]
        the contents before and after the agent.
    """
    # examples:
    # agent_3.register_hand_off(ON_CONDITION(agent_4, "Transfer to Agent 4"))
    # agent_4.register_hand_off([AFTER_WORK(agent_5)])
    # agent_5.register_hand_off(AFTER_WORK(AfterWorkOption.TERMINATE))
    # agent_6.register_hand_off(AFTER_WORK(custom_after_work_6)) # custom
    agent_name = agent_names[agent.id]
    registrations = []
    before_agent = ""
    for hand_off in agent.handoffs:
        if isinstance(hand_off, WaldiezSwarmAfterWork):
            # AFTER_WORK
            registration, before_handoff = get_agent_after_work_handoff(
                hand_off=hand_off,
                agent_names=agent_names,
                agent_name=agent_name,
            )
            registrations.append(registration)
            before_agent += before_handoff
        else:
            # ON_CONDITION
            registration, before_handoff = get_agent_on_condition_handoff(
                agent=agent,
                hand_off=hand_off,
                agent_names=agent_names,
                agent_name=agent_name,
                all_chats=all_chats,
                chat_names=chat_names,
                is_async=is_async,
                serializer=serializer,
                string_escape=string_escape,
            )
            if registration:
                registrations.append(registration)
            before_agent += before_handoff
    after_agent = "\n".join(registrations) + "\n" if registrations else ""
    return before_agent, after_agent


def get_agent_after_work_handoff(
    hand_off: WaldiezSwarmAfterWork,
    agent_names: Dict[str, str],
    agent_name: str,
) -> Tuple[str, str]:
    """Get the agent's after work hand off registration.

    Parameters
    ----------
    hand_off : WaldiezSwarmAfterWork
        The hand off to get the registration for.
    agent_names : Dict[str, str]
        A mapping of agent IDs to agent names.
    agent_name : str
        The name of the agent to register the hand off.

    Returns
    -------
    Tuple[str, str]
        The registration and the content before the agent.
    """
    before_agent = ""
    recipient_type = hand_off.recipient_type
    recipient, function_content = hand_off.get_recipient(
        agent_names=agent_names,
        name_suffix=agent_name,
    )
    registration = f"{agent_name}.register_hand_off({recipient})"
    if recipient_type == "callable" and function_content:
        before_agent += "\n" + function_content + "\n"
    return registration, before_agent


def get_agent_on_condition_handoff(
    agent: WaldiezSwarmAgent,
    hand_off: WaldiezSwarmOnCondition,
    agent_names: Dict[str, str],
    agent_name: str,
    all_chats: List[WaldiezChat],
    chat_names: Dict[str, str],
    is_async: bool,
    serializer: Callable[..., str],
    string_escape: Callable[[str], str],
) -> Tuple[str, str]:
    """Get the agent's on condition hand off registration.

    Parameters
    ----------
    agent : WaldiezSwarmAgent
        The agent to get the registration for.
    hand_off : WaldiezSwarmAfterWork
        The hand off to get the registration for.
    agent_names : Dict[str, str]
        A mapping of agent IDs to agent names.
    agent_name : str
        The name of the agent to register the hand off.
    all_chats : List[WaldiezChat]
        The list of all chats.
    chat_names : Dict[str, str]
        A mapping of chat IDs to chat names.
    is_async : bool
        Whether the chat is asynchronous.
    serializer : Callable[..., str]
        The serializer to get the string representation of an object.
    string_escape : Callable[[str], str]
        The function to escape the string quotes and newlines.

    Returns
    -------
    Tuple[str, str]
        The registration and the content before the agent.
    """
    before_agent = ""
    registration = ""
    available, available_function = hand_off.get_available(
        name_suffix=agent_name,
    )
    if hand_off.target_type == "agent" and isinstance(hand_off.target, str):
        recipient = agent_names[hand_off.target]
        results = _get_agent_on_condition_handoff_to_agent(
            recipient=recipient,
            agent_name=agent_name,
            available=available,
            available_function=available_function,
        )
        before_agent += results[0]
        registration = results[1]
    # else: # target_type == "nested_chat"
    if hand_off.target_type == "nested_chat" and isinstance(
        hand_off.target, dict
    ):
        results = _get_agent_on_condition_handoff_to_nested_chat(
            agent=agent,
            target=hand_off.target,
            agent_names=agent_names,
            available=available,
            available_function=available_function,
            all_chats=all_chats,
            chat_names=chat_names,
            is_async=is_async,
            serializer=serializer,
            string_escape=string_escape,
        )
        registration = results[0]
        before_agent += results[1]
    return registration, before_agent


def _get_agent_on_condition_handoff_to_agent(
    recipient: str,
    agent_name: str,
    available: str,
    available_function: str,
) -> Tuple[str, str]:
    before_agent = ""
    registration = ""
    condition_string = f"Transfer to {recipient}"
    on_condition = (
        "    ON_CONDITION(\n"
        f"        target={recipient}," + "\n"
        f'        condition="{condition_string}",' + "\n"
    )
    if available and available_function:
        on_condition += f"        available={available}," + "\n"
        before_agent += "\n" + available_function + "\n"
    on_condition += "    )"
    registration += (
        f"{agent_name}.register_hand_off(" + "\n" + f"{on_condition}\n)"
    )
    return before_agent, registration


# pylint: disable=too-many-locals
def _get_agent_on_condition_handoff_to_nested_chat(
    target: Dict[str, Any],
    agent: WaldiezAgent,
    agent_names: Dict[str, str],
    available: str,
    available_function: str,
    all_chats: List[WaldiezChat],
    chat_names: Dict[str, str],
    is_async: bool,
    serializer: Callable[..., str],
    string_escape: Callable[[str], str],
) -> Tuple[str, str]:
    try:
        nested_chat = WaldiezAgentNestedChat.model_validate(target)
    except BaseException:  # pylint: disable=broad-except
        return "", ""
    chat_queue, extra_methods = get_nested_chat_queue(
        nested_chat=nested_chat,
        agent=agent,
        agent_names=agent_names,
        chat_names=chat_names,
        all_chats=all_chats,
        serializer=serializer,
        string_escape=string_escape,
    )
    if not chat_queue:
        return "", ""
    before_agent = ""
    registration = ""
    condition_string = "Transfer to nested chat"
    chat_queue_var_name = f"{agent_names[agent.id]}_handoff_nested_chat_queue"
    if extra_methods:
        before_agent += "\n".join(extra_methods) + "\n"
    before_agent += f"{chat_queue_var_name} = {chat_queue}\n"
    on_condition = (
        "    ON_CONDITION(\n"
        f"        target={{\n"
        f"            'chat_queue': {chat_queue_var_name},\n"
        f"            'config': None,\n"
        f"            'reply_func_from_nested_chats': None,\n"
        f"            'use_async': {is_async},\n"
        f"        }}," + "\n"
        f'        condition="{condition_string}",' + "\n"
    )
    if available and available_function:
        on_condition += f"        available={available}," + "\n"
        before_agent += "\n" + available_function + "\n"
    on_condition += "    )"
    registration += (
        f"{agent_names[agent.id]}.register_hand_off(" + "\n" + f"{on_condition}"
        "\n)"
    )
    return before_agent, registration
