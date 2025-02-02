# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Waldiez captain agent data."""

from pydantic import Field

from ..agent import WaldiezAgentData


class WaldiezCaptainAgentData(WaldiezAgentData):
    """Captain agent data class.

    The data for a captain agent.
    Extends `WaldiezAgentData`.
    Extra attributes:
    - `use_agent_lib`: Whether to use the agent lib
    - `use_tool_lib`: Whether to use the tool lib
        if true, the relevant ag2 param would be : tool_lib="default"
    - `max_round`: The maximum number of rounds in a group chat
    - `max_turns`: The maximum number of turns for a chat
        we get this from the chat/edge pointing to this agent
    See the parent's docs (`WaldiezAgentData`) for the rest of the properties.
    """

    use_agent_lib: bool = Field(
        False,
        title="Use agent lib",
        description="Whether to use an agent lib",
        alias="useAgentLib",
    )
    use_tool_lib: bool = Field(
        False,
        title="Use tool lib",
        description="Whether to use a tool lib",
        alias="useToolLib",
    )
    max_round: int = Field(
        10,
        title="Max round",
        description="The maximum number of rounds in a group chat",
        alias="maxRound",
    )
