"""Swarm agent."""

from pydantic import Field
from typing_extensions import Annotated, Literal

from ..agent import WaldiezAgent
from .swarm_agent_data import WaldiezSwarmAgentData


class WaldiezSwarmAgent(WaldiezAgent):
    """Swarm agent.

    It extends a user agent and has swarm related parameters.

    Attributes
    ----------
    agent_type : Literal["swarm"]
        The agent type: 'swarm' for a swarm agent.
    data : WaldiezSwarmAgentData
        The swarm agent's data.
        See `WaldiezSwarmAgentData` for more info.
    """

    agent_type: Annotated[
        Literal["swarm"],
        Field(
            "rag_user",
            title="Agent type",
            description="The agent type: 'rag_user' for a RAG user agent",
            alias="agentType",
        ),
    ]

    data: Annotated[
        WaldiezSwarmAgentData,
        Field(
            title="Data",
            description="The swarm agent's data",
            default_factory=WaldiezSwarmAgentData,
        ),
    ]
