# SPDX-License-Identifier: MIT.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Test waldiez.exporting.agents.agent.get_agent_class_name."""

from waldiez.exporting.agent.utils.agent_class_name import get_agent_class_name
from waldiez.models import (
    WaldiezAssistant,
    WaldiezAssistantData,
    WaldiezGroupManager,
    WaldiezRagUser,
    WaldiezSwarmAgent,
    WaldiezUserProxy,
)


def test_get_agent_class_name() -> None:
    """Test get_agent_class_name()."""
    # Given
    user_proxy = WaldiezUserProxy(  # type: ignore
        id="wa-1",
        name="user_proxy",
    )
    assistant = WaldiezAssistant(  # type: ignore
        id="wa-2",
        name="assistant",
    )
    group_manager = WaldiezGroupManager(  # type: ignore
        id="wa-3",
        name="group_manager",
    )
    rag_user = WaldiezRagUser(  # type: ignore
        id="wa-4",
        name="rag_user",
    )
    multimodal_agent = WaldiezAssistant(  # type: ignore
        id="wa-5",
        name="multimodal_agent",
        data=WaldiezAssistantData(  # type: ignore
            is_multimodal=True,
        ),
    )
    swarm_agent = WaldiezSwarmAgent(  # type: ignore
        id="wa-6",
        name="swarm_agent",
    )
    # When
    user_proxy_class_name = get_agent_class_name(user_proxy)
    assistant_class_name = get_agent_class_name(assistant)
    group_manager_class_name = get_agent_class_name(group_manager)
    rag_user_class_name = get_agent_class_name(rag_user)
    multimodal_agent_class_name = get_agent_class_name(multimodal_agent)
    swarm_agent_class_name = get_agent_class_name(swarm_agent)
    # Then
    assert user_proxy_class_name == "UserProxyAgent"
    assert assistant_class_name == "AssistantAgent"
    assert group_manager_class_name == "GroupChatManager"
    assert rag_user_class_name == "RetrieveUserProxyAgent"
    assert multimodal_agent_class_name == "MultimodalConversableAgent"
    assert swarm_agent_class_name == "SwarmAgent"
