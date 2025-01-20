# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Get the imports needed for the agent."""

from typing import Set


def get_agent_imports(agent_class: str) -> Set[str]:
    """Get the imports needed for the agent.

    Parameters
    ----------
    agent_class : str
        The agent class name.

    Returns
    -------
    Set[str]
        The imports needed for the agent.
    """
    imports = set(["import autogen"])
    if agent_class == "AssistantAgent":
        imports.add("from autogen import AssistantAgent")
    elif agent_class == "UserProxyAgent":
        imports.add("from autogen import UserProxyAgent")
    elif agent_class == "GroupChatManager":
        imports.add("from autogen import GroupChatManager")
    elif agent_class == "RetrieveUserProxyAgent":
        imports.add(
            "from autogen.agentchat.contrib.retrieve_user_proxy_agent "
            "import RetrieveUserProxyAgent"
        )
    elif agent_class == "MultimodalConversableAgent":
        imports.add(
            "from autogen.agentchat.contrib.multimodal_conversable_agent "
            "import MultimodalConversableAgent"
        )
    elif agent_class == "SwarmAgent":
        imports.add(
            "from autogen import "
            "AFTER_WORK, "
            "ON_CONDITION, "
            "UPDATE_SYSTEM_MESSAGE, "
            "AfterWorkOption, "
            "SwarmAgent, "
            "SwarmResult"
        )
    else:
        imports.add("from autogen import ConversableAgent")
    return imports
