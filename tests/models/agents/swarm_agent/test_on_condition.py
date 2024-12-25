"""Test waldiez.models.agents.swarm.on_condition."""

import pytest

from waldiez.models.agents.swarm_agent.on_condition import (
    WaldiezSwarmOnCondition,
)


def test_waldiez_swarm_on_condition() -> None:
    """Test WaldiezSwarmOnCondition."""
    on_condition = WaldiezSwarmOnCondition(
        target="target", condition="condition", available="available"
    )
    assert on_condition.target == "target"
    assert on_condition.condition == "condition"
    assert on_condition.available is None
    assert on_condition.available_check_type == "none"


def test_waldiez_swarm_on_condition_available_string() -> None:
    """Test WaldiezSwarmOnCondition."""
    # this means, that in the context,
    # there should be a variable called "available" which is a boolean value
    on_condition = WaldiezSwarmOnCondition(
        target="target",
        condition="condition",
        available="available",
        available_check_type="string",
    )
    assert on_condition.target == "target"
    assert on_condition.condition == "condition"
    assert on_condition.available == "available"
    assert on_condition.available_check_type == "string"


def test_waldiez_swarm_on_condition_available_no_string() -> None:
    """Test WaldiezSwarmOnCondition."""
    with pytest.raises(ValueError):
        WaldiezSwarmOnCondition(
            target="target",
            condition="condition",
            available=None,
            available_check_type="string",
        )


def test_waldiez_swarm_on_condition_available_callable() -> None:
    """Test WaldiezSwarmOnCondition."""
    callable_body = """
def custom_on_condition_available(agent, message):
    return True
"""
    on_condition = WaldiezSwarmOnCondition(
        target="target",
        condition="condition",
        available=callable_body,
        available_check_type="callable",
    )
    expected_available_string = (
        "    # type: (ConversableAgent, dict) -> bool\n" "    return True"
    )
    assert on_condition.available_string == expected_available_string
    assert on_condition.available_check_type == "callable"


def test_waldiez_swarm_on_condition_invalid_callable_body() -> None:
    """Test WaldiezSwarmOnCondition."""
    with pytest.raises(ValueError):
        WaldiezSwarmOnCondition(
            target="target",
            condition="condition",
            available="INVALID",
            available_check_type="callable",
        )


def test_waldiez_swarm_on_condition_invalid_callable_no_body() -> None:
    """Test WaldiezSwarmOnCondition."""
    with pytest.raises(ValueError):
        WaldiezSwarmOnCondition(
            target="target",
            condition="condition",
            available=None,
            available_check_type="callable",
        )


def test_waldiez_swarm_on_condition_invalid_callable_signature() -> None:
    """Test WaldiezSwarmOnCondition."""
    callable_body = """
    def custom_on_condition_available():
        return True
"""

    with pytest.raises(ValueError):
        WaldiezSwarmOnCondition(
            target="target",
            condition="condition",
            available=callable_body,
            available_check_type="callable",
        )


def test_waldiez_swarm_on_condition_invalid_type() -> None:
    """Test WaldiezSwarmOnCondition."""
    with pytest.raises(ValueError):
        WaldiezSwarmOnCondition(
            target="target",
            condition="condition",
            available="INVALID",
            available_check_type="invalid",  # type: ignore
        )
