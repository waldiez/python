"""Test waldiez.models.common.method_utils.*."""

import ast

from waldiez.models.common.method_utils import check_function, parse_code_string
from waldiez.models.methods import (
    WaldiezMethodArgs,
    WaldiezMethodHints,
    WaldiezMethodName,
)


def test_parse_code_string() -> None:
    """Test parse_code_string."""
    # Given
    code_string = "def test():\n    return 42"
    # When
    error, tree = parse_code_string(code_string)
    # Then
    assert error is None
    assert tree is not None
    assert isinstance(tree, ast.Module)

    # Given
    code_string = "def test():\n   4x = 2\n"
    # When
    error, tree = parse_code_string(code_string)
    assert error is not None
    assert tree is None
    assert "SyntaxError" in error


def test_check_function() -> None:
    """Test check_function."""
    # Given
    code_string = """
def callable_message(sender, recipient, context):
    return "Hello"
    """
    function_name: WaldiezMethodName = WaldiezMethodName.CALLABLE_MESSAGE
    # When
    valid, body = check_function(
        code_string=code_string,
        function_name=function_name,
        function_args=WaldiezMethodArgs[function_name],
        type_hints=WaldiezMethodHints[function_name],
    )
    # Then
    assert valid
    assert body == (
        "    # type: (ConversableAgent, ConversableAgent, dict) -> "
        'Union[dict, str]\n    return "Hello"'
    )

    # Given
    code_string = """
def callable_message(sender, recipient, context):
    return "Hello"
    """
    function_name = "invalid_function"  # type: ignore[assignment]
    # When
    valid, body = check_function(
        code_string=code_string,
        function_name=function_name,
        function_args=[],
        type_hints="",
    )
    # Then
    assert not valid
    assert "No method with name" in body

    # Given
    code_string = """
def callable_message(other, context):
    return "Hello"
    """
    function_name = WaldiezMethodName.CALLABLE_MESSAGE
    # When
    valid, body = check_function(
        code_string=code_string,
        function_name=function_name,
        function_args=WaldiezMethodArgs[function_name],
        type_hints=WaldiezMethodHints[function_name],
    )
    # Then
    assert not valid
    assert "Invalid number of arguments" in body
    # Given
    code_string = """
def is_termination_message(x):
    return True
    """
    function_name = WaldiezMethodName.IS_TERMINATION_MESSAGE
    # When
    valid, body = check_function(
        code_string=code_string,
        function_name=function_name,
        function_args=WaldiezMethodArgs[function_name],
        type_hints=WaldiezMethodHints[function_name],
    )
    # Then
    assert not valid
    assert "Invalid argument name" in body

    # Given
    code_string = """
def is_termination_message(4):
    return True
    """
    function_name = WaldiezMethodName.IS_TERMINATION_MESSAGE
    # When
    valid, body = check_function(
        code_string=code_string,
        function_name=function_name,
        function_args=WaldiezMethodArgs[function_name],
        type_hints=WaldiezMethodHints[function_name],
    )
    # Then
    assert not valid
    assert "SyntaxError" in body

    # Given
    code_string = """
def some_other_function(sender, recipient, context):
    return "Hello"

def nested_chat_reply(recipient, messages, sender, config):
    return "Hello"
    """
    function_name = WaldiezMethodName.NESTED_CHAT_REPLY
    # When
    valid, body = check_function(
        code_string=code_string,
        function_name=function_name,
        function_args=WaldiezMethodArgs[function_name],
        type_hints=WaldiezMethodHints[function_name],
    )
    # Then
    assert valid
    # pylint: disable=line-too-long
    # fmt: off
    assert body == (
        '    # type: (ConversableAgent, list[dict], ConversableAgent, dict) -> Union[dict, str]\n    return "Hello"'  # noqa: E501
    )
    # fmt: on

    # Given
    code_string = """
def nested_chat_reply_(recipient, messages, sender, config):
    return "Hello"
    """
    function_name = WaldiezMethodName.NESTED_CHAT_REPLY
    # When
    valid, body = check_function(
        code_string=code_string,
        function_name=function_name,
        function_args=WaldiezMethodArgs[function_name],
        type_hints=WaldiezMethodHints[function_name],
    )
    # Then
    assert not valid
    assert "No method with name" in body
