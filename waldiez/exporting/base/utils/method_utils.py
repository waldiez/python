"""Method related string generation utilities."""

from typing import Union

from waldiez.models import WaldiezMethodArgs, WaldiezMethodName


def get_method_string(
    function_name: Union[str, WaldiezMethodName],
    renamed_function_name: str,
    method_body: str,
) -> str:
    """Get a function string.

    Parameters
    ----------
    function_name : WaldiezMethodName
        The method name.
    renamed_function_name : str
        The renamed method name.
    method_body : str
        The method body.

    Returns
    -------
    str
        The function string having the definition, type hints and body.
    """
    if isinstance(function_name, str):
        function_name = WaldiezMethodName(function_name.lower())

    function_args = WaldiezMethodArgs[function_name]
    content = f"def {renamed_function_name}("
    if len(function_args) == 0:
        content += "):"
    else:
        content += "\n"
        for arg in function_args:
            content += f"    {arg}," + "\n"
        content += "):"
    content += "\n" + f"{method_body}"
    return content
