"""Test waldiez.exporting.chats.ChatsExporter with a single chat.

With the agents also having nested chats.
"""

from waldiez.exporting.chats import ChatsExporter
from waldiez.models import (
    WaldiezAgent,
    WaldiezChat,
    WaldiezChatData,
    WaldiezChatMessage,
    WaldiezChatNested,
)


# pylint: disable=too-many-locals
def test_single_chat_with_nested() -> None:
    """Test ChatsExporter with a single chat."""
    agent1_name = "agent1"
    agent2_name = "agent2"
    agent3_name = "agent3"
    agent4_name = "agent4"
    chat_name = "chat1"
    agent1 = WaldiezAgent(  # type: ignore
        id="wa-1",
        name=agent1_name,
        agent_type="assistant",
        description="agent description",
        data={},  # type: ignore
    )
    agent2 = WaldiezAgent(  # type: ignore
        id="wa-2",
        name=agent2_name,
        agent_type="assistant",
        description="agent description",
        data={},  # type: ignore
    )
    agent3 = WaldiezAgent(  # type: ignore
        id="wa-3",
        name=agent3_name,
        agent_type="assistant",
        description="agent description",
        data={  # type: ignore
            "nestedChats": [
                {
                    "triggeredBy": ["wa-1"],
                    "messages": [{"id": "wc-2", "isReply": True}],
                }
            ]
        },
    )
    agent4 = WaldiezAgent(  # type: ignore
        id="wa-4",
        name=agent4_name,
        agent_type="assistant",
        description="agent description",
        data={  # type: ignore
            "nestedChats": [
                {
                    "triggeredBy": ["wa-2"],
                    "messages": [{"id": "wc-2", "isReply": False}],
                }
            ]
        },
    )
    chat1 = WaldiezChat(  # type: ignore
        id="wc-1",
        name=chat_name,
        description="A chat between two agents.",
        tags=["chat", chat_name],
        requirements=[],
        data=WaldiezChatData(  # type: ignore
            name="chat1",
            description="A chat between two agents.",
            source="wa-1",
            target="wa-2",
            order=1,
            message=WaldiezChatMessage(
                type="string",
                content="Hello wa-2 from wa-1",
                use_carryover=False,
                context={
                    "variable1": "value1",
                },
            ),
        ),
    )
    chat2 = WaldiezChat(  # type: ignore
        id="wc-2",
        name=chat_name,
        description="A chat between two agents.",
        tags=["chat", chat_name],
        requirements=[],
        data=WaldiezChatData(  # type: ignore
            name="chat1",
            description="A chat between two agents.",
            source="wa-1",
            target="wa-3",
            order=-1,
            message=WaldiezChatMessage(
                type="none",
                content=None,
                use_carryover=False,
                context={},
            ),
            nested_chat=WaldiezChatNested(
                message=WaldiezChatMessage(
                    type="string",
                    content="Hello wa-3 from wa-1",
                    use_carryover=False,
                    context={},
                ),
                reply=WaldiezChatMessage(
                    type="string",
                    content="Hello wa-1 from wa-3",
                    use_carryover=False,
                    context={},
                ),
            ),
        ),
    )
    method_content = """
def nested_chat_message(recipient, messages, sender, config):
    return f"Hello to {recipient.name} from {sender.name}"
"""
    chat3 = WaldiezChat(  # type: ignore
        id="wc-3",
        name=chat_name,
        description="A chat between two agents.",
        tags=["chat", chat_name],
        requirements=[],
        data=WaldiezChatData(  # type: ignore
            name="chat1",
            description="A chat between two agents.",
            source="wa-2",
            target="wa-4",
            order=-1,
            message=WaldiezChatMessage(
                type="none",
                content=None,
                use_carryover=False,
                context={},
            ),
            nested_chat=WaldiezChatNested(
                message=WaldiezChatMessage(
                    type="method",
                    content=method_content,
                    use_carryover=False,
                    context={
                        "variable1": "value1",
                    },
                ),
                reply=WaldiezChatMessage(
                    type="string",
                    content="Hello wa-2 from wa-4",
                    use_carryover=False,
                    context={},
                ),
            ),
        ),
    )
    agent_names = {
        "wa-1": agent1_name,
        "wa-2": agent2_name,
        "wa-3": agent3_name,
        "wa-4": agent4_name,
    }
    chat_names = {"wc-1": chat_name, "wc-2": chat_name, "wc-3": chat_name}
    exporter = ChatsExporter(
        get_swarm_members=lambda _: ([], None),
        all_agents=[agent1, agent2, agent3, agent4],
        agent_names=agent_names,
        all_chats=[chat1, chat2, chat3],
        chat_names=chat_names,
        main_chats=[
            (chat1, agent1, agent2),
        ],
        for_notebook=False,
    )
    generated = exporter.generate()
    expected = """
    results = agent1.initiate_chat(
        agent2,
        summary_method="last_msg",
        variable1="value1",
        message="Hello wa-2 from wa-1",
    )
"""
    assert generated == expected
    after_export = exporter.get_after_export()
    assert after_export is not None
    after_export_str, _ = after_export[0]
    excepted_after_string = """
agent3_chat_queue = [
    {
        "summary_method": "last_msg",
        "recipient": agent1,
        "message": "Hello wa-1 from wa-3"
    },
]

agent3.register_nested_chats(
    trigger=["agent1"],
    chat_queue=agent3_chat_queue,
)

agent4_chat_queue = [
    {
        "summary_method": "last_msg",
        "recipient": agent3,
        "sender": agent1,
        "message": "Hello wa-3 from wa-1"
    },
]

agent4.register_nested_chats(
    trigger=["agent2"],
    chat_queue=agent4_chat_queue,
)
"""
    assert after_export_str == excepted_after_string