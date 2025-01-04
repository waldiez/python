# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# pylint: disable=unused-argument
"""Get the extras of a swarm agent."""

from typing import Callable, Dict, Tuple

from waldiez.models import (
    WaldiezAgent,
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
        arg_string += "\n"
    arg_string += f"{tab}],\n"
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
        arg_string = arg_string + "\n"
    arg_string += f"{tab}],\n"
    return arg_string, before_agent


def get_agent_handoff_registrations(
    agent: WaldiezSwarmAgent,
    agent_names: Dict[str, str],
    string_escape: Callable[[str], str],
) -> Tuple[str, str]:
    """Get the agent handoff registrations of a swarm agent.

    Parameters
    ----------
    agent : WaldiezSwarmAgent
        The swarm agent to get the agent handoff registrations for.
    agent_names : Dict[str, str]
        A mapping of agent IDs to agent names.
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
    for hand_off in agent.hand_offs:
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
                hand_off=hand_off,
                agent_names=agent_names,
                agent_name=agent_name,
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
        before_agent += f"\n{function_content}\n"
    return registration, before_agent


def get_agent_on_condition_handoff(
    hand_off: WaldiezSwarmOnCondition,
    agent_names: Dict[str, str],
    agent_name: str,
    string_escape: Callable[[str], str],
) -> Tuple[str, str]:
    """Get the agent's on condition hand off registration.

    Parameters
    ----------
    hand_off : WaldiezSwarmAfterWork
        The hand off to get the registration for.
    agent_names : Dict[str, str]
        A mapping of agent IDs to agent names.
    agent_name : str
        The name of the agent to register the hand off.
    string_escape : Callable[[str], str]
        The function to escape the string quotes and newlines.

    Returns
    -------
    Tuple[str, str]
        The registration and the content before the agent.
    """
    before_agent = ""
    registration = ""
    target_type = hand_off.target_type
    available, available_function = hand_off.get_available(
        name_suffix=agent_name,
    )
    if target_type == "agent" and isinstance(hand_off.target, str):
        recipient = agent_names[hand_off.target]
        condition_string = string_escape(hand_off.condition)
        on_condition = (
            "    ON_CONDITION(\n"
            f"        target={recipient}," + "\n"
            f'        condition="{condition_string}",' + "\n"
        )
        if available and available_function:
            on_condition += f"        available={available},\n"
            before_agent += f"\n{available_function}\n"
        on_condition += "    )"
        registration += (
            f"{agent_name}.register_hand_off(" "\n" f"{on_condition}" "\n)"
        )
    # else: TODO: handle nested chats.
    return registration, before_agent
