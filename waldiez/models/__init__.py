# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Waldiez models.
- Agents (Users, Assistants, Group Managers, etc.).
- Chat (Messages, Summaries, etc.).
- Model (LLM config, API type, etc.).
- Skill (Skills/Tools to be registered).
- Flow (Flow of the conversation).
- Methods (Method names, arguments, hints, etc.).
- Waldiez (Main class to hold the flow).
"""

from .agents import (
    WaldiezAgent,
    WaldiezAgentCodeExecutionConfig,
    WaldiezAgentData,
    WaldiezAgentLinkedSkill,
    WaldiezAgentNestedChat,
    WaldiezAgentNestedChatMessage,
    WaldiezAgents,
    WaldiezAgentTeachability,
    WaldiezAgentTerminationMessage,
    WaldiezAgentType,
    WaldiezAssistant,
    WaldiezAssistantData,
    WaldiezCaptainAgent,
    WaldiezCaptainAgentData,
    WaldiezGroupManager,
    WaldiezGroupManagerData,
    WaldiezGroupManagerSpeakers,
    WaldiezGroupManagerSpeakersSelectionMethod,
    WaldiezGroupManagerSpeakersSelectionMode,
    WaldiezGroupManagerSpeakersTransitionsType,
    WaldiezRagUser,
    WaldiezRagUserChunkMode,
    WaldiezRagUserData,
    WaldiezRagUserModels,
    WaldiezRagUserRetrieveConfig,
    WaldiezRagUserTask,
    WaldiezRagUserVectorDb,
    WaldiezRagUserVectorDbConfig,
    WaldiezReasoningAgent,
    WaldiezReasoningAgentData,
    WaldiezReasoningAgentReasonConfig,
    WaldiezSwarmAfterWork,
    WaldiezSwarmAfterWorkOption,
    WaldiezSwarmAfterWorkRecipientType,
    WaldiezSwarmAgent,
    WaldiezSwarmAgentData,
    WaldiezSwarmHandoff,
    WaldiezSwarmOnCondition,
    WaldiezSwarmOnConditionAvailable,
    WaldiezSwarmOnConditionTarget,
    WaldiezSwarmUpdateSystemMessage,
    WaldiezUserProxy,
    WaldiezUserProxyData,
)
from .chat import (
    WaldiezChat,
    WaldiezChatData,
    WaldiezChatMessage,
    WaldiezChatNested,
    WaldiezChatSummary,
    WaldiezChatSummaryMethod,
)
from .flow import WaldiezFlow, WaldiezFlowData
from .model import (
    WaldiezModel,
    WaldiezModelAPIType,
    WaldiezModelData,
    WaldiezModelPrice,
)
from .skill import SHARED_SKILL_NAME, WaldiezSkill, WaldiezSkillData
from .waldiez import Waldiez

# pylint: disable=duplicate-code
__all__ = [
    "SHARED_SKILL_NAME",
    "Waldiez",
    "WaldiezAgent",
    "WaldiezAgentCodeExecutionConfig",
    "WaldiezAgentData",
    "WaldiezAgentLinkedSkill",
    "WaldiezAgentNestedChat",
    "WaldiezAgentNestedChatMessage",
    "WaldiezAgents",
    "WaldiezAgentTeachability",
    "WaldiezAgentTerminationMessage",
    "WaldiezAgentType",
    "WaldiezAssistant",
    "WaldiezAssistantData",
    "WaldiezCaptainAgent",
    "WaldiezCaptainAgentData",
    "WaldiezChat",
    "WaldiezChatData",
    "WaldiezChatSummary",
    "WaldiezChatNested",
    "WaldiezChatSummaryMethod",
    "WaldiezFlow",
    "WaldiezFlowData",
    "WaldiezGroupManager",
    "WaldiezGroupManagerData",
    "WaldiezGroupManagerSpeakers",
    "WaldiezGroupManagerSpeakersSelectionMethod",
    "WaldiezGroupManagerSpeakersSelectionMode",
    "WaldiezGroupManagerSpeakersTransitionsType",
    "WaldiezChatMessage",
    "WaldiezModel",
    "WaldiezModelAPIType",
    "WaldiezModelData",
    "WaldiezModelPrice",
    "WaldiezRagUser",
    "WaldiezRagUserData",
    "WaldiezReasoningAgent",
    "WaldiezReasoningAgentData",
    "WaldiezReasoningAgentReasonConfig",
    "WaldiezSkill",
    "WaldiezSkillData",
    "WaldiezUserProxy",
    "WaldiezUserProxyData",
    "WaldiezRagUserRetrieveConfig",
    "WaldiezRagUserTask",
    "WaldiezRagUserChunkMode",
    "WaldiezRagUserVectorDb",
    "WaldiezRagUserVectorDbConfig",
    "WaldiezRagUserModels",
    "WaldiezSwarmAgent",
    "WaldiezSwarmAfterWork",
    "WaldiezSwarmAfterWorkOption",
    "WaldiezSwarmAfterWorkRecipientType",
    "WaldiezSwarmAgentData",
    "WaldiezSwarmHandoff",
    "WaldiezSwarmOnCondition",
    "WaldiezSwarmOnConditionTarget",
    "WaldiezSwarmOnConditionAvailable",
    "WaldiezSwarmUpdateSystemMessage",
]
