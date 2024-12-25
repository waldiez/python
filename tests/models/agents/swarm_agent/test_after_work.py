"""Test waldiez.models.agents.swarm.after_work.*."""

# pylint: disable=line-too-long
# flake8: noqa E501
import pytest

from waldiez.models.agents.swarm_agent.after_work import WaldiezSwarmAfterWork


def test_waldiez_swarm_after_work_terminate() -> None:
    """Test WaldiezSwarmAfterWork."""
    after_work = WaldiezSwarmAfterWork(
        recipient="TERMINATE", recipient_type="option"
    )
    assert after_work.recipient == "TERMINATE"
    assert after_work.recipient_type == "option"


def test_waldiez_swarm_after_work_revert_to_user() -> None:
    """Test WaldiezSwarmAfterWork."""
    after_work = WaldiezSwarmAfterWork(
        recipient="REVERT_TO_USER", recipient_type="option"
    )
    assert after_work.recipient == "REVERT_TO_USER"
    assert after_work.recipient_type == "option"


def test_waldiez_swarm_after_work_stay() -> None:
    """Test WaldiezSwarmAfterWork."""
    after_work = WaldiezSwarmAfterWork(
        recipient="STAY", recipient_type="option"
    )
    assert after_work.recipient == "STAY"
    assert after_work.recipient_type == "option"


def test_waldiez_swarm_after_work_invalid_option() -> None:
    """Test WaldiezSwarmAfterWork."""
    with pytest.raises(ValueError):
        WaldiezSwarmAfterWork(recipient="INVALID", recipient_type="option")


def test_waldiez_swarm_after_work_callable() -> None:
    """Test WaldiezSwarmAfterWork."""
    callable_body = """
def custom_after_work(last_speaker, messages, groupchat):
    return "TERMINATE"
"""
    after_work = WaldiezSwarmAfterWork(
        recipient=callable_body, recipient_type="callable"
    )
    expected_recipient_string = (
        "    # type: (SwarmAgent, List[dict], GroupChat) -> Union[AfterWorkOption, SwarmAgent, str]\n"
        '    return "TERMINATE"'
    )
    assert after_work.recipient_string == expected_recipient_string
    assert after_work.recipient_type == "callable"


def test_waldiez_swarm_after_work_invalid_callable_body() -> None:
    """Test WaldiezSwarmAfterWork."""
    with pytest.raises(ValueError):
        WaldiezSwarmAfterWork(recipient="INVALID", recipient_type="callable")


def test_waldiez_swarm_after_work_invalid_callable_signature() -> None:
    """Test WaldiezSwarmAfterWork."""
    callable_body = """
    def custom_after_work():
        return "TERMINATE"
"""

    with pytest.raises(ValueError):
        WaldiezSwarmAfterWork(
            recipient=callable_body, recipient_type="callable"
        )


def test_waldiez_swarm_after_work_invalid_type() -> None:
    """Test WaldiezSwarmAfterWork."""
    with pytest.raises(ValueError):
        WaldiezSwarmAfterWork(
            recipient="INVALID",
            recipient_type="invalid",  # type: ignore
        )
