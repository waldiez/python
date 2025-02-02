# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Test waldiez.models.agents.captain_agent.*."""

from waldiez.models.agents.captain_agent import WaldiezCaptainAgent


def test_waldiez_captain_agent() -> None:
    """Test `WaldiezCaptainAgent`."""
    agent = WaldiezCaptainAgent(id="wa-1", name="captain_agent")  # type: ignore
    assert agent.agent_type == "captain"
    assert agent.data.use_agent_lib is False
    assert agent.data.use_tool_lib is False
    assert agent.data.nested_config == {}
