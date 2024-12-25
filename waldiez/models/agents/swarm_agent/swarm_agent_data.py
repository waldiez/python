"""Swarm agent data.

https://docs.ag2.ai/docs/reference/agentchat/contrib/swarm_agent
"""

from typing import List, Union

from pydantic import Field
from typing_extensions import Annotated

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
        A list of functions to register with the agent.

    update_agent_state_before_reply : List[str]
        A list of functions, including `UPDATE_SYSTEM_MESSAGE`,
        called to update the agent's state before it replies. Each function
        is called when the agent is selected and before it speaks.

    hand_offs : List[Union[WaldiezSwarmOnCondition, WaldiezSwarmAfterWork]]
        A list of hand offs to register.

    See Also
    --------
    waldiez.models.agents.swarm.on_condition.WaldiezSwarmOnCondition :
        A condition to handle handoff.
    waldiez.models.agents.swarm.after_work.WaldiezSwarmAfterWork :
        An after work to handle handoff.
    waldiez.models.agents.swarm.update_system_message.WaldiezSwarmUpdateSystemMessage :
        Update the agent's system message before they reply.

    Notes
    -----
    Each agent should have at most one `AfterWork` and (if any) it should be
    of the list of hand offs.
    """

    functions: Annotated[
        List[str],
        Field(
            title="Functions",
            description="A list of functions to register with the agent.",
            default_factory=list,
        ),
    ]
    update_agent_state_before_reply: Annotated[
        List[Union[str, WaldiezSwarmUpdateSystemMessage]],
        Field(
            title="Update Agent State Before Reply",
            description=(
                "A list of functions, including UPDATE_SYSTEM_MESSAGEs,"
                "called to update the agent's state before it replies. "
                " Each function is called when the agent is selected "
                "and before it speaks."
            ),
            default_factory=list,
        ),
    ]
    hand_offs: Annotated[
        List[Union[WaldiezSwarmOnCondition, WaldiezSwarmAfterWork]],
        Field(
            title="Hand Offs",
            description=(
                "A list of hand offs to register. "
                "There should only be at most one AfterWork per agent"
                "And (if any) it should be at the end of the list."
            ),
            default_factory=list,
        ),
    ]
