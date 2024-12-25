"""Swarm after work model

Handles the next step in the conversation when an
agent doesn’t suggest a tool call or a handoff.

"""

# pylint: disable=line-too-long

from pydantic import Field, model_validator
from typing_extensions import Annotated, Literal, Self

from ...common import WaldiezBase, check_function

WaldiezSwarmAfterWorkRecipientType = Literal["agent", "option", "callable"]
WaldiezSwarmAfterWorkOption = Literal["TERMINATE", "REVERT_TO_USER", "STAY"]


# pylint: disable=line-too-long
CUSTOM_AFTER_WORK = "custom_after_work"
CUSTOM_AFTER_WORK_ARGS = ["last_speaker", "messages", "groupchat"]
CUSTOM_AFTER_WORK_HINTS = "# type: (SwarmAgent, List[dict], GroupChat) -> Union[AfterWorkOption, SwarmAgent, str]"  # noqa: E501


class WaldiezSwarmAfterWork(WaldiezBase):
    """Swarm after work.


    Attributes
    ----------
    recipient : str
        The agent to hand off to or the after work option.
        Can be a SwarmAgent, a string name of a SwarmAgent,
        an AfterWorkOption, or a Callable.

    recipient_type : WaldiezSwarmAfterWorkRecipientType
        The type of recipient.
        Can be 'agent', 'option', or 'callable'.
        If 'agent', the recipient is a SwarmAgent.
        If 'option', the recipient is an AfterWorkOption :
            ('TERMINATE', 'REVERT_TO_USER', 'STAY').
        If 'callable', it should have the signature:
        def custom_after_work(
            last_speaker: SwarmAgent,
            messages: List[dict],
            groupchat: GroupChat,
        ) -> Union[AfterWorkOption, SwarmAgent, str]:

    """

    recipient: Annotated[
        str,
        Field(
            ...,
            title="Agent",
            description=(
                "The agent to hand off to or the after work option. "
                "Can be a SwarmAgent, a string name of a SwarmAgent, "
                "an AfterWorkOption, or a Callable."
            ),
        ),
    ]
    recipient_type: Annotated[
        WaldiezSwarmAfterWorkRecipientType,
        Field(
            "agent",
            title="Recipient Type",
            description=(
                "The type of recipient. "
                "Can be 'agent', 'option', or 'callable'. "
                "If 'agent', the recipient is a SwarmAgent.  "
                "If 'option', the recipient is an AfterWorkOption :"
                "    ('TERMINATE', 'REVERT_TO_USER', 'STAY'). "
                "If 'callable', it should have the signature: "
                "def custom_after_work("
                "    last_speaker: SwarmAgent,"
                "    messages: List[dict],"
                "    groupchat: GroupChat,"
                ") -> Union[AfterWorkOption, SwarmAgent, str]:"
            ),
        ),
    ]

    _recipient_string: str = ""

    @property
    def recipient_string(self) -> str:
        """Return the recipient as a string.

        Returns
        -------
        str
            The recipient as a string.
        """
        return self._recipient_string

    @model_validator(mode="after")
    def validate_recipient(self) -> Self:
        """Validate the recipient.

        Returns
        -------
        WaldiezSwarmAfterWork
            The validated after work model.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        self._recipient_string = self.recipient
        if self.recipient_type == "callable":
            is_valid, error_or_body = check_function(
                code_string=self.recipient,
                function_name=CUSTOM_AFTER_WORK,
                function_args=CUSTOM_AFTER_WORK_ARGS,
                type_hints=CUSTOM_AFTER_WORK_HINTS,
            )
            if not is_valid or not error_or_body:
                # pylint: disable=inconsistent-quotes
                raise ValueError(
                    f"Invalid custom method: {error_or_body or 'no content'}"
                )
            self._recipient_string = error_or_body
        elif self.recipient_type == "option":
            if self.recipient not in ["TERMINATE", "REVERT_TO_USER", "STAY"]:
                raise ValueError("Invalid option.")
        return self
