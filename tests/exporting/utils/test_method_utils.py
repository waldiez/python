"""Test waldiez.exporting.utils.method_utils.*."""

from waldiez.exporting.utils.method_utils import get_method_string
from waldiez.models import WaldiezMethodName


def test_get_method_string() -> None:
    """Test get_method_string."""
    # Given
    function_name: WaldiezMethodName = WaldiezMethodName.CALLABLE_MESSAGE
    renamed_function_name = "callable_message_agent1"
    # When
    result = get_method_string(
        function_name=function_name,
        renamed_function_name=renamed_function_name,
        method_body="    return 'callable_message'",
    )
    # Then
    assert result == (
        "def callable_message_agent1(\n"
        "    sender,\n"
        "    recipient,\n"
        "    context,\n"
        "):\n"
        "    return 'callable_message'"
    )
    # Given
    function_name = WaldiezMethodName.CUSTOM_EMBEDDING_FUNCTION
    renamed_function_name = "custom_embedding_function_agent1"
    # When
    result = get_method_string(
        function_name=function_name,
        renamed_function_name=renamed_function_name,
        method_body="    return lambda x: x",
    )
    # Then
    assert result == (
        "def custom_embedding_function_agent1():\n" "    return lambda x: x"
    )
