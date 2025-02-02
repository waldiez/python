# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Agent models."""

from .agent import (
    IS_TERMINATION_MESSAGE,
    IS_TERMINATION_MESSAGE_ARGS,
    IS_TERMINATION_MESSAGE_TYPES,
    WaldiezAgent,
    WaldiezAgentCodeExecutionConfig,
    WaldiezAgentData,
    WaldiezAgentLinkedSkill,
    WaldiezAgentNestedChat,
    WaldiezAgentNestedChatMessage,
    WaldiezAgentTeachability,
    WaldiezAgentTerminationMessage,
    WaldiezAgentType,
)
from .agents import WaldiezAgents
from .assistant import WaldiezAssistant, WaldiezAssistantData
from .captain_agent import WaldiezCaptainAgent, WaldiezCaptainAgentData
from .extra_requirements import (
    get_captain_agent_extra_requirements,
    get_retrievechat_extra_requirements,
)
from .group_manager import (
    CUSTOM_SPEAKER_SELECTION,
    CUSTOM_SPEAKER_SELECTION_ARGS,
    CUSTOM_SPEAKER_SELECTION_TYPES,
    WaldiezGroupManager,
    WaldiezGroupManagerData,
    WaldiezGroupManagerSpeakers,
    WaldiezGroupManagerSpeakersSelectionMethod,
    WaldiezGroupManagerSpeakersSelectionMode,
    WaldiezGroupManagerSpeakersTransitionsType,
)
from .rag_user import (
    CUSTOM_EMBEDDING_FUNCTION,
    CUSTOM_EMBEDDING_FUNCTION_ARGS,
    CUSTOM_EMBEDDING_FUNCTION_TYPES,
    CUSTOM_TEXT_SPLIT_FUNCTION,
    CUSTOM_TEXT_SPLIT_FUNCTION_ARGS,
    CUSTOM_TEXT_SPLIT_FUNCTION_TYPES,
    CUSTOM_TOKEN_COUNT_FUNCTION,
    CUSTOM_TOKEN_COUNT_FUNCTION_ARGS,
    CUSTOM_TOKEN_COUNT_FUNCTION_TYPES,
    WaldiezRagUser,
    WaldiezRagUserChunkMode,
    WaldiezRagUserData,
    WaldiezRagUserModels,
    WaldiezRagUserRetrieveConfig,
    WaldiezRagUserTask,
    WaldiezRagUserVectorDb,
    WaldiezRagUserVectorDbConfig,
)
from .reasoning import (
    WaldiezReasoningAgent,
    WaldiezReasoningAgentData,
    WaldiezReasoningAgentReasonConfig,
)
from .swarm_agent import (
    CUSTOM_AFTER_WORK,
    CUSTOM_AFTER_WORK_ARGS,
    CUSTOM_AFTER_WORK_TYPES,
    CUSTOM_ON_CONDITION_AVAILABLE,
    CUSTOM_ON_CONDITION_AVAILABLE_ARGS,
    CUSTOM_ON_CONDITION_AVAILABLE_TYPES,
    CUSTOM_UPDATE_SYSTEM_MESSAGE,
    CUSTOM_UPDATE_SYSTEM_MESSAGE_ARGS,
    CUSTOM_UPDATE_SYSTEM_MESSAGE_TYPES,
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
)
from .user_proxy import WaldiezUserProxy, WaldiezUserProxyData

__all__ = [
    "get_retrievechat_extra_requirements",
    "get_captain_agent_extra_requirements",
    "IS_TERMINATION_MESSAGE",
    "IS_TERMINATION_MESSAGE_ARGS",
    "IS_TERMINATION_MESSAGE_TYPES",
    "CUSTOM_AFTER_WORK",
    "CUSTOM_AFTER_WORK_ARGS",
    "CUSTOM_AFTER_WORK_TYPES",
    "CUSTOM_EMBEDDING_FUNCTION",
    "CUSTOM_EMBEDDING_FUNCTION_ARGS",
    "CUSTOM_EMBEDDING_FUNCTION_TYPES",
    "CUSTOM_ON_CONDITION_AVAILABLE",
    "CUSTOM_ON_CONDITION_AVAILABLE_ARGS",
    "CUSTOM_ON_CONDITION_AVAILABLE_TYPES",
    "CUSTOM_SPEAKER_SELECTION",
    "CUSTOM_SPEAKER_SELECTION_ARGS",
    "CUSTOM_SPEAKER_SELECTION_TYPES",
    "CUSTOM_TEXT_SPLIT_FUNCTION",
    "CUSTOM_TEXT_SPLIT_FUNCTION_ARGS",
    "CUSTOM_TEXT_SPLIT_FUNCTION_TYPES",
    "CUSTOM_TOKEN_COUNT_FUNCTION",
    "CUSTOM_TOKEN_COUNT_FUNCTION_ARGS",
    "CUSTOM_TOKEN_COUNT_FUNCTION_TYPES",
    "CUSTOM_UPDATE_SYSTEM_MESSAGE",
    "CUSTOM_UPDATE_SYSTEM_MESSAGE_ARGS",
    "CUSTOM_UPDATE_SYSTEM_MESSAGE_TYPES",
    "WaldiezAgent",
    "WaldiezAgentType",
    "WaldiezAgents",
    "WaldiezAssistant",
    "WaldiezAssistantData",
    "WaldiezAgentCodeExecutionConfig",
    "WaldiezAgentData",
    "WaldiezAgentLinkedSkill",
    "WaldiezAgentNestedChat",
    "WaldiezAgentNestedChatMessage",
    "WaldiezAgentTeachability",
    "WaldiezAgentTerminationMessage",
    "WaldiezCaptainAgent",
    "WaldiezCaptainAgentData",
    "WaldiezGroupManager",
    "WaldiezGroupManagerData",
    "WaldiezGroupManagerSpeakers",
    "WaldiezGroupManagerSpeakersSelectionMethod",
    "WaldiezGroupManagerSpeakersSelectionMode",
    "WaldiezGroupManagerSpeakersTransitionsType",
    "WaldiezRagUser",
    "WaldiezRagUserData",
    "WaldiezRagUserModels",
    "WaldiezReasoningAgent",
    "WaldiezReasoningAgentData",
    "WaldiezReasoningAgentReasonConfig",
    "WaldiezUserProxy",
    "WaldiezUserProxyData",
    "WaldiezRagUserRetrieveConfig",
    "WaldiezRagUserTask",
    "WaldiezRagUserChunkMode",
    "WaldiezRagUserVectorDb",
    "WaldiezRagUserVectorDbConfig",
    "WaldiezSwarmAgent",
    "WaldiezSwarmAgentData",
    "WaldiezSwarmAfterWork",
    "WaldiezSwarmAfterWorkOption",
    "WaldiezSwarmAfterWorkRecipientType",
    "WaldiezSwarmHandoff",
    "WaldiezSwarmOnCondition",
    "WaldiezSwarmOnConditionTarget",
    "WaldiezSwarmOnConditionAvailable",
    "WaldiezSwarmUpdateSystemMessage",
]
