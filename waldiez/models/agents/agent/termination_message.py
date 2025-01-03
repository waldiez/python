# SPDX-License-Identifier: MIT.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Waldiez Agent Termination Message Check."""

from typing import List, Optional, Tuple

from pydantic import Field, model_validator
from typing_extensions import Annotated, Literal, Self

from ...common import WaldiezBase, check_function, generate_function

IS_TERMINATION_MESSAGE = "is_termination_message"
IS_TERMINATION_MESSAGE_ARGS = ["message"]
IS_TERMINATION_MESSAGE_TYPES = (
    ["Dict[str, Any]"],
    "bool",
)


class WaldiezAgentTerminationMessage(WaldiezBase):
    """Waldiez Agent Termination Message Check.

    Attributes
    ----------
    type : Literal["none", "keyword", "method"]
        The type of the termination check to use: "none", "keyword", "method"
    keywords : List[str]
        If the type is "keyword", the keywords to search in the message.
    criterion : Optional[Literal["found", "ending", "exact"]] = None
        If the type is "keyword", the criterion to use (e.g.: in, endswith, ==)
    method_content: Optional[str]
        If the type is "method", the code of the method to use.
        The method must be called `is_termination_message`,
        have one argument (`message`) which is a dict, and
        return a bool (whether the message is a termination message or not.)
    string : str
        The value of the termination message.

    Functions
    ---------
    validate_termination_message() -> Self
        Validate the termination message configuration.
    """

    type: Annotated[
        Literal["none", "keyword", "method"],
        Field(
            "none",
            title="Type",
            description=(
                "The type of the termination check to use: "
                "none, keyword, method"
            ),
        ),
    ]
    keywords: Annotated[
        List[str],
        Field(
            default_factory=list,
            title="Keywords",
            description=(
                "If the type is `keyword`,"
                " the keywords to search in the message."
            ),
        ),
    ]
    criterion: Annotated[
        Optional[Literal["found", "ending", "exact"]],
        Field(
            "exact",
            title="Criterion",
            description=(
                "If the type is `keyword`, "
                "the criterion to use (e.g.: in, endswith, ==)"
            ),
        ),
    ]
    method_content: Annotated[
        Optional[str],
        Field(
            None,
            title="Method content",
            description=(
                "If the type is `method`, the code of the method to use."
                "The method must be called `is_termination_message`,"
                "have one argument (`message`) which is a dict, and return a"
                "bool (whether the message is a termination message or not.)"
            ),
        ),
    ]

    _string: str = "None"

    def get_termination_function(
        self,
        name_prefix: Optional[str] = None,
        name_suffix: Optional[str] = None,
    ) -> Tuple[str, str]:
        """Get the termination function.

        Parameters
        ----------
        name_prefix : str
            The function name prefix.
        name_suffix : str
            The function name suffix.

        Returns
        -------
        Tuple[str, str]
            The termination function and the function name.
        """
        function_name = "is_termination_message"
        if name_prefix:
            function_name = f"{name_prefix}_{function_name}"
        if name_suffix:
            function_name = f"{function_name}_{name_suffix}"
        return (
            generate_function(
                function_name=function_name,
                function_args=IS_TERMINATION_MESSAGE_ARGS,
                function_types=IS_TERMINATION_MESSAGE_TYPES,
                function_body=self.string,
            ),
            function_name,
        )

    @property
    def string(self) -> str:
        """Get the value of the termination message.

        - If the type is "none", the value is "None".
        - If the type is "keyword", the value is a lambda function that checks
            if any of the keywords comply with the criterion.
        - If the type is "method", the value is the method content.

        Returns
        -------
        str
            The value of the termination message.
        """
        return self._string

    def _validate_method_content(self) -> None:
        """Validate the method content."""
        if not self.method_content:
            raise ValueError(
                "Method content is required for method termination."
            )
        valid, error_or_content = check_function(
            self.method_content,
            function_name=IS_TERMINATION_MESSAGE,
            function_args=IS_TERMINATION_MESSAGE_ARGS,
        )
        if not valid:
            raise ValueError(error_or_content)
        self._string = error_or_content

    def _validate_keyword(self) -> None:
        """Validate the keyword termination configuration."""
        if not self.keywords:
            raise ValueError("Keywords are required for keyword termination.")
        if self.criterion not in ["found", "ending", "exact"]:
            raise ValueError(f"Invalid criterion: {self.criterion}")
        # pylint: disable=inconsistent-quotes
        keywords_str = ", ".join([f'"{keyword}"' for keyword in self.keywords])
        if self.criterion == "found":
            self._string = (
                'lambda x: any(x.get("content", "") and '
                'keyword in x.get("content", "") '
                f"for keyword in [{keywords_str}])"
            )
        if self.criterion == "ending":
            self._string = (
                'lambda x: any(x.get("content", "") and '
                'x.get("content", "").endswith(keyword) '
                f"for keyword in [{keywords_str}])"
            )
        if self.criterion == "exact":
            self._string = (
                'lambda x: any(x.get("content", "") == keyword '
                f"for keyword in [{keywords_str}])"
            )

    @model_validator(mode="after")
    def validate_termination_message(self) -> Self:
        """Validate the termination message configuration.

        Raises
        ------
        ValueError
            If the configuration is invalid.
        Returns
        -------
        WaldiezAgentTerminationMessage
            The validated termination message configuration.
        """
        if self.type == "method":
            self._validate_method_content()
        if self.type == "keyword":
            self._validate_keyword()
        if self.type == "none":
            self._string = "None"
        return self
