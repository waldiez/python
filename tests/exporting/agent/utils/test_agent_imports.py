# SPDX-License-Identifier: MIT.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# flake8: noqa E501
# pylint: disable=line-too-long
"""Test waldiez.exporting.agent.utils.agent_imports."""

from waldiez.exporting.agent.utils.agent_imports import get_agent_imports


def test_get_agent_imports() -> None:
    """Test get_agent_imports()."""
    user_proxy_imports = get_agent_imports("UserProxyAgent")
    assistant_imports = get_agent_imports("AssistantAgent")
    group_manager_imports = get_agent_imports("GroupChatManager")
    rag_user_imports = get_agent_imports("RetrieveUserProxyAgent")
    multimodal_agent_imports = get_agent_imports("MultimodalConversableAgent")
    conversable_agent_imports = get_agent_imports("ConversableAgent")
    swarm_agent_imports = get_agent_imports("SwarmAgent")

    assert user_proxy_imports == {
        "import autogen",
        "from autogen import UserProxyAgent",
    }
    assert assistant_imports == {
        "import autogen",
        "from autogen import AssistantAgent",
    }
    assert group_manager_imports == {
        "import autogen",
        "from autogen import GroupChatManager",
    }
    assert rag_user_imports == {
        "import autogen",
        "from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent",
    }
    assert multimodal_agent_imports == {
        "import autogen",
        "from autogen.agentchat.contrib.multimodal_conversable_agent import MultimodalConversableAgent",
    }
    assert conversable_agent_imports == {
        "import autogen",
        "from autogen import ConversableAgent",
    }
    assert swarm_agent_imports == {
        "import autogen",
        "from autogen import AFTER_WORK, ON_CONDITION, AfterWorkOption, SwarmAgent",
    }
