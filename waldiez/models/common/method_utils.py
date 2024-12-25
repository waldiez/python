"""Function related utilities."""

import ast
from typing import List, Optional, Tuple


def parse_code_string(
    code_string: str,
) -> Tuple[Optional[str], Optional[ast.Module]]:
    """Parse the code string.

    Parameters
    ----------
    code_string : str
        The code string.

    Returns
    -------
    Tuple[Optional[str], Optional[ast.Module]]
        If valid, None and the ast module.
        If invalid, the error message and None.
    """
    # pylint: disable=broad-except
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return f"SyntaxError: {e}, in \n{code_string}", None
    except BaseException as e:  # pragma: no cover
        return f"Invalid code: {e}, in \n{code_string}", None
    return None, tree


def check_function(
    code_string: str,
    function_name: str,
    function_args: List[str],
    type_hints: Optional[str] = None,
) -> Tuple[bool, str]:
    """Check the function.

    Parameters
    ----------
    code_string : str
        The code string.
    function_name : str
        The expected method name.
    function_args : List[str]
        The expected method arguments.
    type_hints : Optional[str], optional
        The type hints to include, by default None

    Returns
    -------
    Tuple[bool, str]
        If valid, True and the function body (only), no extra lines.
        If invalid, False and the error message.
    """
    error, tree = parse_code_string(code_string)
    if error is not None or tree is None:
        return False, error or "Invalid code"
    return _get_function_body(
        tree,
        code_string,
        function_name,
        function_args,
        type_hints=type_hints,
    )


def _get_function_body(
    tree: ast.Module,
    code_string: str,
    function_name: str,
    function_args: List[str],
    type_hints: Optional[str] = None,
) -> Tuple[bool, str]:
    """Get the function body.

    Parameters
    ----------
    tree : ast.Module
        The ast module.
    code_string : str
        The code string.
    function_name : str
        The expected method name.
    function_args : List[str]
        The expected method arguments.
    type_hints : Optional[str], optional
        The type hints to include, by default None

    Returns
    -------
    Tuple[bool, str]
        If valid, True and the function body (only), no extra lines.
        If invalid, False and the error message.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if node.name != function_name:
                continue
            if len(node.args.args) != len(function_args):
                return (
                    False,
                    f"Invalid number of arguments in function {node.name}",
                )
            for arg, expected_arg in zip(node.args.args, function_args):
                if arg.arg != expected_arg:
                    return (
                        False,
                        f"Invalid argument name in function {node.name}",
                    )
            function_body_lines = code_string.splitlines()[
                node.lineno - 1 : node.end_lineno
            ]
            function_body = "\n".join(function_body_lines[1:])
            if type_hints:
                # add type hints after the function definition
                function_body = f"    {type_hints}\n{function_body}"
            return True, function_body
    error_msg = (
        f"No method with name `{function_name}`"
        f" and arguments `{function_args}` found"
    )
    return False, error_msg
