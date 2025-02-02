# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Test waldiez.models.agents.captain_agent.captain_agent_data.*."""

from waldiez.models.agents.captain_agent.captain_agent_data import (
    WaldiezCaptainAgentData,
)


def test_waldiez_captain_agent_data() -> None:
    """Test `WaldiezCaptainAgentData`."""
    data = WaldiezCaptainAgentData(  # type: ignore
        use_agent_lib=True,
        use_tool_lib=True,
        max_round=20,
    )
    assert data.use_agent_lib is True
    assert data.use_tool_lib is True
    assert data.max_round == 20
