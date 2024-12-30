"""Swarm after work model

Handles the next step in the conversation when an
agent doesn’t suggest a tool call or a handoff.

"""

# pylint: disable=line-too-long

from typing import Dict

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
        The agent_id to hand off to, an AfterWork option,
        or the custom after work method.
        If it is an AfterWork option, it can be one of
        ('TERMINATE', 'REVERT_TO_USER', 'STAY')

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
            "TERMINATE",
            title="Recipient",
            description=(
                "The agent_id to hand off to, an AfterWork option, "
                "or the custom after work method. "
                "If it is an AfterWork option, it can be one of "
                "('TERMINATE', 'REVERT_TO_USER', 'STAY')"
            ),
        ),
    ]
    recipient_type: Annotated[
        WaldiezSwarmAfterWorkRecipientType,
        Field(
            "option",
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

    def get_recipient_string(
        self,
        agent_names: Dict[str, str],
        function_name: str = "custom_after_work",
    ) -> str:
        """Get the recipient string.

        Parameters
        ----------
        agent_names : Dict[str, str]
            A mapping of agent id to agent name.
        function_name : str, optional
            The function name to use, by default "custom_after_work".

        Returns
        -------
        str
            The recipient string.
        """
        if self.recipient_type == "option":
            return f"AFTER_WORK(AfterWorkOption.{self.recipient})"
        if self.recipient_type == "agent":
            # the the recipient is passed as the agent name
            # (and not its id), care should be taken to ensure
            # the all the agents in the flow have unique names
            agent_instance = agent_names.get(self.recipient, self.recipient)
            return f"AFTER_WORK({agent_instance})"
        return (
            f"def {function_name}(last_speaker, messages, groupchat):"
            "\n"
            f"{self._recipient_string}"
        )

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
