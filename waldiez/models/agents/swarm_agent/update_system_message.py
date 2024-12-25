"""Update the agent's system message before they reply."""

from pydantic import Field, model_validator
from typing_extensions import Annotated, Literal, Self

from ...common import WaldiezBase, check_function

CUSTOM_UPDATE_SYSTEM_MESSAGE = "custom_update_system_message"
CUSTOM_UPDATE_SYSTEM_MESSAGE_ARGS = ["agent", "messages"]
CUSTOM_UPDATE_SYSTEM_MESSAGE_HINTS = (
    "# type: (ConversableAgent, List[Dict[str, Any]]) -> str"
)


class WaldiezSwarmUpdateSystemMessage(WaldiezBase):
    """Update the agent's system message before they reply.

    Attributes
    ----------
    update_function_type : Literal["string", "callable"]
        The type of the update function. Can be either a string or a callable.
    update_function : str
        "The string template or function definition to update "
        "the agent's system message. Can be a string or a Callable.  "
        "If the `function_type` is 'string' it will be used as a "
        "template and substitute the context variables.  "
        "If `function_type` is 'callable', it should have signature: "
        "def custom_update_system_message("
        "   agent: ConversableAgent, "
        "   messages: List[Dict[str, Any]] "
        ") -> str"
    """

    update_function_type: Annotated[
        Literal["string", "callable"],
        Field(
            "string",
            title="Function Type",
            description=(
                "The type of the update function. "
                "Can be either 'string' or 'callable'."
            ),
        ),
    ]

    update_function: Annotated[
        str,
        Field(
            ...,
            title="Update Function",
            description=(
                "The string template or function definition to update "
                "the agent's system message. Can be a string or a Callable.  "
                "If the `update_function_type` is 'string', "
                " it will be used as a template and substitute "
                "the context variables. If `update_function_type` "
                "is 'callable', it should have signature: "
                "def custom_update_system_message("
                "   agent: ConversableAgent, "
                "   messages: List[Dict[str, Any]] "
                ") -> str"
            ),
        ),
    ]

    _update_function_string: str = ""

    @property
    def update_function_string(self) -> str:
        """Return the update function as a string.

        Returns
        -------
        str
            The update function as a string.
        """
        return self._update_function_string

    @model_validator(mode="after")
    def validate_update_system_message(self) -> Self:
        """Validate the update system message function.

        Returns
        -------
        UpdateSystemMessage
            The validated update system message.

        Raises
        ------
        ValueError
            If the type is callable and the function is invalid.
            or if the function type is not 'string' or 'callable'.

        """
        self._update_function_string = self.update_function
        if self.update_function_type == "callable":
            valid, error_or_body = check_function(
                code_string=self.update_function,
                function_name=CUSTOM_UPDATE_SYSTEM_MESSAGE,
                function_args=CUSTOM_UPDATE_SYSTEM_MESSAGE_ARGS,
                type_hints=CUSTOM_UPDATE_SYSTEM_MESSAGE_HINTS,
            )
            if not valid or not error_or_body:
                # pylint: disable=inconsistent-quotes
                raise ValueError(
                    f"Invalid custom method: {error_or_body or 'no content'}"
                )
            self._update_function_string = error_or_body
        return self
