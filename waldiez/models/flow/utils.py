# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Helpers for the flow model."""

import uuid
from datetime import datetime, timezone
from typing import Iterator, List

from ..agents import (
    WaldiezAgent,
    WaldiezAgentNestedChat,
    WaldiezAgentNestedChatMessage,
    WaldiezSwarmAgent,
    WaldiezSwarmOnCondition,
)
from ..chat import WaldiezChat


def id_factory() -> str:
    """Generate a unique ID.

    Returns
    -------
    str
        The unique ID.
    """
    now_td = datetime.now(timezone.utc)
    now_str = now_td.strftime("%Y%m%d%H%M%S%f")
    return f"{now_str}-{uuid.uuid4().hex}"


def check_handoff_to_nested_chat(
    agent: WaldiezSwarmAgent,
    all_agents: Iterator[WaldiezAgent],
    all_chats: List[WaldiezChat],
) -> None:
    """Check the handoffs to a nested chat.

    If we have one and the agent does not have nested_chats,
    we should generate them with the `handoff.target.id`
    as the first (chat's) message.

    Parameters
    ----------
    agent : WaldiezSwarmAgent
        The swarm agent.
    all_agents : Iterator[WaldiezAgent]
        All agents.
    all_chats : List[WaldiezChat]
        All chats.

    Raises
    ------
    ValueError
        If the agent has a handoff to a nested chat,
        but no chat found with it as a source.
    """
    # pylint: disable=too-complex
    for handoff in agent.handoffs:
        if not isinstance(handoff, WaldiezSwarmOnCondition):
            continue
        is_nested_chat = handoff.target_type == "nested_chat"
        if is_nested_chat and (
            not agent.nested_chats or not agent.nested_chats[0].messages
        ):
            chats_with_agent_as_a_source = [
                chat for chat in all_chats if chat.data.source == agent.id
            ]
            first_chat = handoff.target.id
            if not chats_with_agent_as_a_source or first_chat not in (
                chat.id for chat in chats_with_agent_as_a_source
            ):
                print(first_chat, agent.id)
                # pylint: disable=line-too-long
                raise ValueError(
                    f"Agent {agent.id} has a handoff to a nested chat but no chat found with it as a source."  # noqa: E501
                )
            ids_added = [first_chat]
            nested_chat_messages: List[WaldiezAgentNestedChatMessage] = [
                WaldiezAgentNestedChatMessage(id=first_chat, is_reply=False)
            ]
            for chat in chats_with_agent_as_a_source:
                if chat.id in ids_added:
                    continue
                try:
                    target_agent = next(
                        agent
                        for agent in all_agents
                        if agent.id == chat.data.target
                    )
                except StopIteration:
                    continue
                if target_agent.agent_type == "swarm":
                    continue
                ids_added.append(chat.id)
                nested_chat_messages.append(
                    WaldiezAgentNestedChatMessage(id=chat.id, is_reply=True)
                )
            nested_chat = WaldiezAgentNestedChat(
                triggered_by=[], messages=nested_chat_messages
            )
            agent.data.nested_chats = [nested_chat]
            break
