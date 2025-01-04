# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Swarm condition model for handoff."""

from typing import Any, Dict, Optional, Tuple, Union

from pydantic import Field, model_validator
from typing_extensions import Annotated, Literal, Self

from ...common import WaldiezBase, check_function, generate_function

WaldiezSwarmOnConditionTargetType = Literal["agent", "nested_chat"]
WaldiezSwarmOnConditionAvailableCheckType = Literal[
    "string", "callable", "none"
]

CUSTOM_ON_CONDITION_AVAILABLE = "custom_on_condition_available"
CUSTOM_ON_CONDITION_AVAILABLE_ARGS = ["agent", "message"]
CUSTOM_ON_CONDITION_AVAILABLE_TYPES = (
    ["Agent", "Dict[str, Any]"],
    "bool",
)

# In ag2 it used as:
#
# if on_condition.available is not None:
#     if isinstance(on_condition.available, Callable):
#         is_available = on_condition.available(
#           agent, next(iter(agent.chat_messages.values()))
#         )
#     elif isinstance(on_condition.available, str):
#         is_available = agent.get_context(on_condition.available) or False


class WaldiezSwarmOnCondition(WaldiezBase):
    """Swarm condition to handle handoff.

    Attributes
    ----------
    target : Union[Dict[str, Any], str]
        The agent to hand off to or the nested chat configuration
        If a Dict, it should follow the convention of the nested chat
        configuration, with the exception of a carryover configuration
        which is unique to Swarms.

    target_type: Literal["agent", "nested_chat"]
        The type of the target. Can be either 'agent' or 'nested_chat'.
        Default is 'agent'.

    condition : str
        The condition for transitioning to the target agent

    available: str, optional
        Optional condition to determine if this ON_CONDITION is available.
        Can be a Callable or a string.  If a string, it will look up the
        value of the context variable with that name, which should be a bool.

    available_check_type : Literal["string", "callable", "none"]
        The type of the `available` property to check. Default is "none".
    """

    target: Annotated[
        Union[Dict[str, Any], str],
        Field(
            ...,
            title="Target",
            description=(
                "The agent to hand off to or the nested chat configuration"
                "If a Dict, it should follow the convention of the nested "
                "chat configuration, with the exception of a carryover "
                "configuration which is unique to Swarms."
            ),
        ),
    ]
    target_type: Annotated[
        WaldiezSwarmOnConditionTargetType,
        Field(
            "agent",
            alias="targetType",
            title="Target Type",
            description=(
                "The type of the target. "
                "Can be either 'agent' or 'nested_chat'.Default is 'agent'."
            ),
        ),
    ] = "agent"
    condition: Annotated[
        str,
        Field(
            ...,
            title="Condition",
            description="The condition for transitioning to the target agent",
        ),
    ]
    available_check_type: Annotated[
        WaldiezSwarmOnConditionAvailableCheckType,
        Field(
            "none",
            alias="availableCheckType",
            title="Available Check Type",
            description=("The type of the `available` property to check. "),
        ),
    ] = "none"
    available: Annotated[
        Optional[str],
        Field(
            None,
            title="Available",
            description=(
                "Optional condition to determine if this ON_CONDITION "
                "is available. Can be a Callable or a string.  If a string, "
                " it will look up the value of the context variable with that "
                "name, which should be a bool."
            ),
        ),
    ]

    _available_string: str = ""

    @property
    def available_string(self) -> str:
        """Get the available string.

        Returns
        -------
        str
            The available string.
        """
        return self._available_string

    def get_available(
        self,
        name_prefix: Optional[str] = None,
        name_suffix: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Get the available string.

        Parameters
        ----------
        name_prefix : str, optional
            The prefix to add to the function name. Default is None.
        name_suffix : str, optional
            The suffix to add to the function name. Default is None.
        Returns
        -------
        Tuple[str, str]
            The available string or function name and code if available.
        """
        if self.available_check_type == "none" or not self.available:
            return "", ""
        if self.available_check_type == "string":
            return self.available_string, ""
        function_name = CUSTOM_ON_CONDITION_AVAILABLE
        if name_prefix:
            function_name = f"{name_prefix}_{function_name}"
        if name_suffix:
            function_name = f"{function_name}_{name_suffix}"
        return function_name, generate_function(
            function_name=function_name,
            function_args=CUSTOM_ON_CONDITION_AVAILABLE_ARGS,
            function_types=CUSTOM_ON_CONDITION_AVAILABLE_TYPES,
            function_body=self.available_string,
        )

    @model_validator(mode="after")
    def validate_available(self) -> Self:
        """Validate the available property.

        Returns
        -------
        Self
            The validated instance.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if self.available_check_type == "callable":
            if not self.available:
                raise ValueError("No callable provided.")
            is_valid, error_or_body = check_function(
                code_string=self.available,
                function_name=CUSTOM_ON_CONDITION_AVAILABLE,
                function_args=CUSTOM_ON_CONDITION_AVAILABLE_ARGS,
            )
            if not is_valid or not error_or_body:
                raise ValueError(f"Invalid callable: {error_or_body}")
            self._available_string = error_or_body
        elif self.available_check_type == "string":
            if not self.available:
                raise ValueError("No context variable name provided.")
            self._available_string = self.available
        else:
            self._available_string = ""
            self.available = None
        return self
