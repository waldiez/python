# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Get the agent class name."""

from waldiez.models import WaldiezAgent


# pylint: disable=too-many-return-statements
def get_agent_class_name(agent: WaldiezAgent) -> str:
    """Get the agent class name.

    Parameters
    ----------
    agent : WaldiezAgent
        The agent.

    Returns
    -------
    str
        The agent class name.
    """
    if agent.data.is_multimodal:
        return "MultimodalConversableAgent"
    if agent.agent_type == "assistant":
        return "AssistantAgent"
    if agent.agent_type == "user":
        return "UserProxyAgent"
    if agent.agent_type == "manager":
        return "GroupChatManager"
    if agent.agent_type == "rag_user":
        return "RetrieveUserProxyAgent"
    if agent.agent_type == "swarm":
        return "SwarmAgent"
    return "ConversableAgent"  # pragma: no cover
