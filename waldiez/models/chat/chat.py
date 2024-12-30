"""Waldiez chat model."""

from typing import Any, Dict, Optional

from pydantic import Field
from typing_extensions import Annotated

from ..agents import WaldiezAgent, WaldiezRagUser, WaldiezSwarmAfterWork
from ..common import WaldiezBase
from .chat_data import WaldiezChatData
from .chat_message import WaldiezChatMessage
from .chat_nested import WaldiezChatNested


class WaldiezChat(WaldiezBase):
    """Chat class.

    Attributes
    ----------
    id : str
        The chat ID.
    data : WaldiezChatData
        The chat data.
        See `waldiez.models.chat.WaldiezChatData` for more information.
    name : str
        The chat name.
    source : str
        The chat source.
    target : str
        The chat target.
    nested_chat : WaldiezChatNested
        The nested chat message/reply if any.
    message : WaldiezChatMessage
        The chat message.
    message_content : Optional[str]
        The chat message content if any. If method, the method's body.

    Functions
    ---------
    get_chat_args()
        Get the chat arguments to use in autogen.
    """

    id: Annotated[
        str,
        Field(
            ...,
            title="ID",
            description="The chat ID.",
        ),
    ]
    data: Annotated[
        WaldiezChatData,
        Field(
            ...,
            title="Data",
            description="The chat data.",
        ),
    ]

    @property
    def name(self) -> str:
        """Get the name."""
        return self.data.name

    @property
    def description(self) -> str:
        """Get the description."""
        return self.data.description

    @property
    def source(self) -> str:
        """Get the source."""
        if self.data.real_source:
            return self.data.real_source
        return self.data.source

    @property
    def target(self) -> str:
        """Get the target."""
        if self.data.real_target:
            return self.data.real_target
        return self.data.target

    @property
    def nested_chat(self) -> WaldiezChatNested:
        """Get the nested chat."""
        return self.data.nested_chat

    @property
    def message(self) -> WaldiezChatMessage:
        """Get the message."""
        if isinstance(
            self.data.message, str
        ):  # pragma: no cover (just for the lint)
            return WaldiezChatMessage(
                type="string",
                use_carryover=False,
                content=self.data.message,
                context={},
            )
        return self.data.message

    @property
    def message_content(self) -> Optional[str]:
        """Get the message content."""
        return self.data.message_content

    @property
    def context_variables(self) -> Dict[str, Any]:
        """Get the context variables."""
        if isinstance(self.data.message, str):  # pragma: no cover
            # it can never be a string (just for the linter)
            # we manage this on the validation part in the model
            return {}
        return self.data.message.context

    @property
    def max_rounds(self) -> int:
        """Get the max rounds for swarm chat."""
        return self.data.max_rounds

    @property
    def after_work(self) -> Optional[WaldiezSwarmAfterWork]:
        """Get the after work."""
        return self.data.after_work

    def get_chat_args(
        self,
        sender: Optional[WaldiezAgent] = None,
    ) -> Dict[str, Any]:
        """Get the chat arguments to use in autogen.

        Parameters
        ----------
        sender : WaldiezAgent
            The sender agent, to check if it's a RAG user.
        Returns
        -------
        dict
            The chat arguments.
        """
        args_dict = self.data.get_chat_args()
        if (
            isinstance(sender, WaldiezRagUser)
            and sender.agent_type == "rag_user"
            and self.message.type == "rag_message_generator"
        ):
            # check for n_results in agent data, to add in context
            n_results = sender.data.retrieve_config.n_results
            if isinstance(n_results, int) and n_results > 0:
                args_dict["n_results"] = n_results
        return args_dict

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        """Dump the model to a dict including the chat attributes.

        Parameters
        ----------
        kwargs : Any
            The keyword arguments.
        Returns
        -------
        Dict[str, Any]
            The model dump with the chat attributes.
        """
        dump = super().model_dump(**kwargs)
        dump["name"] = self.name
        dump["description"] = self.description
        dump["source"] = self.source
        dump["target"] = self.target
        dump["nested_chat"] = self.nested_chat.model_dump()
        dump["message"] = self.message.model_dump()
        dump["message_content"] = self.message_content
        dump["context_variables"] = self.context_variables
        dump["max_rounds"] = self.max_rounds
        dump["after_work"] = (
            self.after_work.model_dump() if self.after_work else None
        )
        return dump
