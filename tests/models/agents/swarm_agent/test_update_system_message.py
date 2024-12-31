"""Test waldiez.models.agents.swarm.WaldiezSwarmUpdateSystemMessage."""

import pytest

from waldiez.models.agents.swarm_agent.update_system_message import (
    WaldiezSwarmUpdateSystemMessage,
)


def test_waldiez_swarm_update_system_message() -> None:
    """Test WaldiezSwarmUpdateSystemMessage with string type."""
    update_system_message = WaldiezSwarmUpdateSystemMessage(
        update_function_type="string",
        update_function="Template to {use} variables in {context}",
    )
    assert update_system_message.update_function_type == "string"
    assert update_system_message.update_function == (
        "Template to {use} variables in {context}"
    )


def test_waldiez_swarm_update_system_message_callable() -> None:
    """Test WaldiezSwarmUpdateSystemMessage with callable type."""
    callable_body = """
def custom_update_system_message(agent, messages):
    return "custom message"
"""
    update_system_message = WaldiezSwarmUpdateSystemMessage(
        update_function_type="callable",
        update_function=callable_body,
    )
    # pylint: disable=inconsistent-quotes
    expected_update_function_string = '    return "custom message"'
    assert update_system_message.update_function_type == "callable"
    assert update_system_message.update_function_string == (
        expected_update_function_string
    )


def test_waldiez_swarm_update_system_message_callable_string() -> None:
    """Test WaldiezSwarmUpdateSystemMessage with string type."""
    callable_body = """
def custom_update_system_message(agent, messages):
    return "custom message"
"""
    update_system_message = WaldiezSwarmUpdateSystemMessage(
        update_function_type="string",
        update_function=callable_body,
    )
    assert update_system_message.update_function_type == "string"
    assert update_system_message.update_function == callable_body


def test_waldiez_swarm_update_system_message_invalid_callable() -> None:
    """Test WaldiezSwarmUpdateSystemMessage with invalid callable."""
    with pytest.raises(ValueError):
        WaldiezSwarmUpdateSystemMessage(
            update_function_type="callable",
            update_function="Template to {use} variables in {context}",
        )
