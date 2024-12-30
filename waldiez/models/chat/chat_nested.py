"""Nested chat model."""

from typing import Any, Optional

from pydantic import Field, ValidationInfo, field_validator, model_validator
from typing_extensions import Annotated, Self

from ..common import WaldiezBase
from .chat_message import WaldiezChatMessage, validate_message_dict

NESTED_CHAT_MESSAGE = "nested_chat_message"
NESTED_CHAT_REPLY = "nested_chat_reply"
NESTED_CHAT_ARGS = ["recipient", "messages", "sender", "config"]
# pylint: disable=line-too-long
NESTED_CHAT_HINTS = "# type: (ConversableAgent, list[dict], ConversableAgent, dict) -> Union[dict, str]"  # noqa: E501


class WaldiezChatNested(WaldiezBase):
    """Nested chat class.

    Attributes
    ----------
    message : WaldiezChatMessage
        The message in a nested chat (sender -> recipient).
    reply : WaldiezChatMessage
        The reply in a nested chat (recipient -> sender).
    """

    message: Annotated[
        Optional[WaldiezChatMessage],
        Field(
            None,
            title="Message",
            description="The message in a nested chat (sender -> recipient).",
        ),
    ]
    reply: Annotated[
        Optional[WaldiezChatMessage],
        Field(
            None,
            title="Reply",
            description="The reply in a nested chat (recipient -> sender).",
        ),
    ]

    _message_content: Optional[str] = None
    _reply_content: Optional[str] = None

    @property
    def message_content(self) -> Optional[str]:
        """Get the message content."""
        return self._message_content

    @property
    def reply_content(self) -> Optional[str]:
        """Get the reply content."""
        return self._reply_content

    @field_validator("message", "reply", mode="before")
    @classmethod
    def validate_message(
        cls, value: Any, info: ValidationInfo
    ) -> WaldiezChatMessage:
        """Validate the message.

        Parameters
        ----------
        value : Any
            The value.
        info : ValidationInfo
            The validation info.

        Returns
        -------
        WaldiezChatMessage
            The validated message.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        function_name = (
            NESTED_CHAT_MESSAGE
            if info.field_name == "message"
            else NESTED_CHAT_REPLY
        )
        if not value:
            return WaldiezChatMessage(
                type="none", use_carryover=False, content=None, context={}
            )
        if isinstance(value, str):
            return WaldiezChatMessage(
                type="string", use_carryover=False, content=value, context={}
            )
        if isinstance(value, dict):
            return validate_message_dict(
                value,
                function_name=function_name,
                function_args=NESTED_CHAT_ARGS,
                type_hints=NESTED_CHAT_HINTS,
            )
        if isinstance(value, WaldiezChatMessage):
            return validate_message_dict(
                {
                    "type": value.type,
                    "use_carryover": False,
                    "content": value.content,
                    "context": value.context,
                },
                function_name=function_name,
                function_args=NESTED_CHAT_ARGS,
                type_hints=NESTED_CHAT_HINTS,
            )
        raise ValueError(f"Invalid message type: {type(value)}")

    @model_validator(mode="after")
    def validate_nested_chat(self) -> Self:
        """Validate the nested chat.

        Returns
        -------
        WaldiezChatNested
            The validated nested chat.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if self.message is not None:
            if self.message.type == "none":
                self._message_content = ""
            elif self.message.type == "string":
                self._message_content = self.message.content
            else:
                self._message_content = validate_message_dict(
                    value={
                        "type": "method",
                        "content": self.message.content,
                    },
                    function_name=NESTED_CHAT_MESSAGE,
                    function_args=NESTED_CHAT_ARGS,
                    type_hints=NESTED_CHAT_HINTS,
                    skip_definition=True,
                ).content
        if self.reply is not None:
            if self.reply.type == "none":
                self._reply_content = ""
            elif self.reply.type == "string":
                self._reply_content = self.reply.content
            else:
                self._reply_content = validate_message_dict(
                    value={
                        "type": "method",
                        "content": self.reply.content,
                    },
                    function_name=NESTED_CHAT_REPLY,
                    function_args=NESTED_CHAT_ARGS,
                    type_hints=NESTED_CHAT_HINTS,
                    skip_definition=True,
                ).content
        return self
