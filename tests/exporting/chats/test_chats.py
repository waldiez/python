"""Test waldiez.exporting.chats.chats.*."""

# flake8: noqa E501

from waldiez.exporting.chats.chats import export_chats
from waldiez.models import (
    Waldiez,
    WaldiezAgent,
    WaldiezAgents,
    WaldiezChat,
    WaldiezChatData,
    WaldiezChatMessage,
    WaldiezChatNested,
    WaldiezChatSummary,
    WaldiezFlow,
    WaldiezFlowData,
)


def test_export_chats() -> None:
    """Test export_chats()."""
    # Given
    agent1 = WaldiezAgent(  # type: ignore
        id="wa-1",
        name="agent1",
        agent_type="assistant",
    )
    agent2 = WaldiezAgent(  # type: ignore
        id="wa-2",
        name="agent2",
        agent_type="assistant",
    )
    agent3 = WaldiezAgent(  # type: ignore
        id="wa-3",
        name="agent3",
        agent_type="assistant",
    )
    agent4 = WaldiezAgent(  # type: ignore
        id="wa-4",
        name="agent4",
        agent_type="assistant",
    )
    chat1 = WaldiezChat(
        id="wc-1",
        data=WaldiezChatData(
            name="chat1",
            description="A chat.",
            source="wa-1",
            target="wa-2",
            position=1,
            order=1,
            clear_history=False,
            message=WaldiezChatMessage(
                type="string",
                use_carryover=False,
                content="Hello, world!",
                context={},
            ),
            summary=WaldiezChatSummary(
                method="reflection_with_llm",
                prompt=(
                    "Return the summary of the chat as a JSON object: "
                    '"{"summary": "Hello, world!"}"'
                ),
                args={
                    "problem": 'Solve this task: "{"task": "cleanup"}"',
                },
            ),
            max_turns=None,
            nested_chat=WaldiezChatNested(
                message=None,
                reply=None,
            ),
            silent=False,
            real_source="wa-3",
            real_target=None,
        ),
    )
    chat2 = WaldiezChat(
        id="wc-2",
        data=WaldiezChatData(
            name="chat2",
            description="Another chat.",
            source="wa-2",
            target="wa-1",
            position=2,
            order=2,
            clear_history=False,
            message=WaldiezChatMessage(
                type="string",
                use_carryover=False,
                content='{"Goodbye": "world!"}',
                context={},
            ),
            summary=WaldiezChatSummary(
                method=None,
                prompt="",
                args={},
            ),
            max_turns=None,
            nested_chat=WaldiezChatNested(
                message=None,
                reply=None,
            ),
            silent=False,
            real_source=None,
            real_target="wa-4",
        ),
    )
    chat3 = WaldiezChat(
        id="wc-3",
        data=WaldiezChatData(
            name="chat3",
            description="A third chat.",
            source="wa-1",
            target="wa-2",
            position=-1,
            order=-1,
            clear_history=False,
            message=WaldiezChatMessage(
                type="string",
                use_carryover=False,
                content="Hello, world!",
                context={},
            ),
            summary=WaldiezChatSummary(
                method="reflection_with_llm",
                prompt=(
                    "Return the summary of the chat as a JSON object: "
                    '"{"summary": "Hello, world!"}"'
                ),
                args={
                    "problem": 'Solve this task: "{"task": "cleanup"}"',
                },
            ),
            max_turns=None,
            nested_chat=WaldiezChatNested(
                message=None,
                reply=None,
            ),
            silent=False,
            real_source=None,
            real_target=None,
        ),
    )
    all_agents = [agent2, agent3]
    agent_names = {agent.id: agent.name for agent in all_agents}
    # When
    all_chats = [chat1]
    chat_names = {chat.id: chat.name for chat in all_chats}
    waldiez = Waldiez(
        flow=WaldiezFlow(
            id="wf-1",
            name="flow1",
            type="flow",
            description="A flow.",
            tags=[],
            requirements=[],
            storage_id="ws-1",
            created_at="2021-01-01T00:00:00Z",
            updated_at="2021-01-01T00:00:00Z",
            data=WaldiezFlowData(
                nodes=[],
                edges=[],
                viewport={},
                skills=[],
                models=[],
                agents=WaldiezAgents(
                    users=[],
                    managers=[],
                    assistants=[
                        agent.model_dump()  # type: ignore
                        for agent in all_agents
                    ],
                    rag_users=[],
                    swarm_agents=[],
                ),
                chats=all_chats,
            ),
        ),
    )
    # Then
    export_chats(
        agent_names=agent_names,
        chat_names=chat_names,
        waldiez=waldiez,
        # main_chats=[(chat1, agent1, agent2)],
        tabs=1,
    )
    # When
    all_agents = [agent1, agent2, agent3, agent4]
    all_chats = [chat1, chat2, chat3]
    chat_names = {chat.id: chat.name for chat in all_chats}
    agent_names = {agent.id: agent.name for agent in all_agents}
    waldiez = Waldiez(
        flow=WaldiezFlow(
            id="wf-1",
            name="flow1",
            type="flow",
            description="A flow.",
            tags=[],
            requirements=[],
            storage_id="ws-1",
            created_at="2021-01-01T00:00:00Z",
            updated_at="2021-01-01T00:00:00Z",
            data=WaldiezFlowData(
                nodes=[],
                edges=[],
                viewport={},
                skills=[],
                models=[],
                agents=WaldiezAgents(
                    users=[],
                    managers=[],
                    assistants=[
                        agent.model_dump()  # type: ignore
                        for agent in all_agents
                    ],
                    rag_users=[],
                    swarm_agents=[],
                ),
                chats=all_chats,
            ),
        ),
    )
    chats_string, _ = export_chats(
        agent_names=agent_names,
        chat_names=chat_names,
        waldiez=waldiez,
        tabs=1,
    )
    # Then
    expected = """initiate_chats([
        {
            "sender": agent3,
            "recipient": agent2,
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": "Return the summary of the chat as a JSON object: \\"{\\"summary\\": \\"Hello, world!\\"}\\"",
                "problem": "Solve this task: \\"{\\"task\\": \\"cleanup\\"}\\""
            },
            "clear_history": False,
            "silent": False,
            "message": "Hello, world!",
        },
        {
            "sender": agent2,
            "recipient": agent4,
            "clear_history": False,
            "silent": False,
            "message": "{\\\\"Goodbye\\\\": \\\\"world!\\\\"}",
        },
    ])"""
    assert chats_string == expected
