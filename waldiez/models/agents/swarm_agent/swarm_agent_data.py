# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
# https://docs.ag2.ai/docs/reference/agentchat/contrib/swarm_agent
"""Swarm agent data."""

from typing import List, Union

from pydantic import Field, model_validator
from typing_extensions import Annotated, Self

from ..agent import WaldiezAgentData
from .after_work import WaldiezSwarmAfterWork
from .on_condition import WaldiezSwarmOnCondition
from .update_system_message import WaldiezSwarmUpdateSystemMessage


# flake8: noqa: E501
# pylint: disable=line-too-long
class WaldiezSwarmAgentData(WaldiezAgentData):
    """Swarm agent data.

    Attributes
    ----------
    functions : List[str]
        A list of functions (skill ids) to register with the agent.

    update_agent_state_before_reply : List[str]
        A list of functions, including `UPDATE_SYSTEM_MESSAGE`,
        called to update the agent's state before it replies. Each function
        is called when the agent is selected and before it speaks.

    handoffs : List[Union[WaldiezSwarmOnCondition, WaldiezSwarmAfterWork]]
        A list of hand offs to register.

    Notes
    -----
    Each agent should have at most one `AfterWork` and (if any) it should be
    at the end the list of hand offs.
    """

    functions: Annotated[
        List[str],
        Field(
            title="Functions",
            description=(
                "A list of functions (skill ids) to register with the agent."
            ),
            default_factory=list,
        ),
    ]
    update_agent_state_before_reply: Annotated[
        List[Union[str, WaldiezSwarmUpdateSystemMessage]],
        Field(
            title="Update Agent State Before Reply",
            alias="updateAgentStateBeforeReply",
            description=(
                "A list of functions, including UPDATE_SYSTEM_MESSAGEs,"
                "called to update the agent's state before it replies. "
                " Each function is called when the agent is selected "
                "and before it speaks. If not an UPDATE_SYSTEM_MESSAGE, "
                "it should be a skill id."
            ),
            default_factory=list,
        ),
    ]
    handoffs: Annotated[
        List[Union[WaldiezSwarmOnCondition, WaldiezSwarmAfterWork]],
        Field(
            title="Handoffs",
            description=(
                "A list of hand offs to register. "
                "There should only be at most one `AfterWork` per agent"
                "And (if any) it should be at the end of the list."
            ),
            default_factory=list,
        ),
    ]

    @model_validator(mode="after")
    def validate_handoffs(self) -> Self:
        """Validate the hand offs.

        Returns
        -------
        Self
            The swarm agent data.

        Raises
        ------
        ValueError
            If there are more than one `AfterWork`s.
        """
        after_works = [
            hand_off
            for hand_off in self.handoffs
            if isinstance(hand_off, WaldiezSwarmAfterWork)
        ]
        if len(after_works) > 1:
            raise ValueError(
                "Each agent should have at most one `AfterWork` "
                "and (if any) it should be at the end of the list."
            )
        if after_works and after_works[0] != self.handoffs[-1]:
            self.handoffs.remove(after_works[0])
            self.handoffs.append(after_works[0])
        return self
