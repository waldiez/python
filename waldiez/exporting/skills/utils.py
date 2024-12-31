"""Skills/tools related string generation functions.

Functions
---------
get_agent_skill_registration
    Get an agent's skill registration string.
export_skills
    Get the skills content and secrets.
"""

from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union

from waldiez.models import WaldiezAgent, WaldiezSkill


def get_agent_skill_registration(
    caller_name: str,
    executor_name: str,
    skill_name: str,
    skill_description: str,
    string_escape: Callable[[str], str],
) -> str:
    """Get the agent skill string and secrets.

    Parameters
    ----------
    caller_name : str
        The name of the caller (agent).
    executor_name : str
        The name of the executor (agent).
    skill_name : str
        The name of the skill.
    skill_description : str
        The skill description.
    string_escape : Callable[[str], str]
        The string escape function.
    Returns
    -------
    str
        The agent skill string.

    Example
    -------
    ```python
    >>> get_agent_skill_registration(
    ...     caller_name="agent1",
    ...     executor_name="agent2",
    ...     skill_name="skill1",
    ...     skill_description="A skill that does something.",
    ...     string_escape=lambda x: x.replace('"', '\\"').replace("\\n", "\\n"),
    ... )
    register_function(
        skill1,
        caller=agent1,
        executor=agent2,
        name="skill1",
        description="A skill that does something.",
    )
    ```
    """
    skill_description = string_escape(skill_description)
    content = f"""register_function(
    {skill_name},
    caller={caller_name},
    executor={executor_name},
    name="{skill_name}",
    description="{skill_description}",
)
"""
    return content


def _write_skill_secrets(
    flow_name: str,
    skill: WaldiezSkill,
    skill_name: str,
    output_dir: Path,
) -> None:
    """Write the skill secrets to a file.

    Parameters
    ----------
    skill : WaldiezSkill
        The skill.
    skill_name : str
        The name of the skill.
    output_dir : Path
        The output directory to save the secrets to.
    """
    if not skill.secrets:
        return
    secrets_file = output_dir / f"{flow_name}_{skill_name}_secrets.py"
    first_line = f'"""Secrets for the skill: {skill_name}."""' + "\n"
    with secrets_file.open("w", encoding="utf-8", newline="\n") as f:
        f.write(first_line)
        f.write("import os\n\n")
        for key, value in skill.secrets.items():
            f.write(f'os.environ["{key}"] = "{value}"' + "\n")


def export_skills(
    flow_name: str,
    skills: List[WaldiezSkill],
    skill_names: Dict[str, str],
    output_dir: Optional[Union[str, Path]] = None,
) -> Tuple[List[str], List[Tuple[str, str]]]:
    """Get the skills' contents and secrets.

    If `output_dir` is provided, the contents are saved to that directory.

    Parameters
    ----------
    flow_name : str
        The name of the flow.
    skills : List[WaldiezSkill]
        The skills.
    skill_names : Dict[str, str]
        The skill names.
    output_dir : Optional[Union[str, Path]]
        The output directory to save the skills to.

    Returns
    -------
    Tuple[Set[str], Set[Tuple[str, str]]]
        - The skill imports to use in the main file.
        - The skill secrets to set as environment variables.

    Example
    -------
    ```python
    >>> from waldiez.models import WaldiezSkill, WaldiezSkillData
    >>> flow_name = "flow1"
    >>> skill1 = WaldiezSkill(
    ...     id="ws-1",
    ...     name="skill1",
    ...     description="A skill that does something.",
    ...     tags=["skill", "skill1"],
    ...     requirements=[],
    ...     data=WaldiezSkillData(
    ...         content="def skill1():\\n    pass",
    ...         secrets={"API_KEY": "1234567890"},
    ... )
    >>> skill_names = {"ws-1": "skill1"}
    >>> export_skills(flow_name, [skill1], skill_names, None)
    (
        [   "import flow1_skill1_secrets  # type: ignore # noqa",
            "from flow1_skill1 import skill1  # type: ignore # noqa",
        ],
        [('API_KEY', '1234567890')]
    )
    ```
    """
    skill_imports: List[str] = []
    skill_secrets: List[Tuple[str, str]] = []
    for skill in skills:
        skill_name = skill_names[skill.id]
        for key, value in skill.secrets.items():
            skill_secrets.append((key, value))
        if not output_dir:
            skill_imports.append(get_skill_imports(flow_name, skill))
            continue
        if not isinstance(output_dir, Path):
            output_dir = Path(output_dir)
        skill_imports.append(get_skill_imports(flow_name, skill))
        _write_skill_secrets(
            flow_name=flow_name,
            skill=skill,
            skill_name=skill_name,
            output_dir=output_dir,
        )
        skill_file = output_dir / f"{flow_name}_{skill_name}.py"
        with skill_file.open("w", encoding="utf-8", newline="\n") as f:
            f.write(skill.content)
    return skill_imports, skill_secrets


def get_skill_imports(flow_name: str, skill: WaldiezSkill) -> str:
    """Get the skill imports string.

    Parameters
    ----------
    flow_name : str
        The name of the flow.
    skill : WaldiezSkill
        The skill.
    Returns
    -------
    str
        The skill imports string.
    """
    ignore_noqa = "  # type: ignore # noqa"
    if not skill.secrets:
        # fmt: off
        return (
            f"from {flow_name}_{skill.name} import {skill.name}{ignore_noqa}"
        )
        # fmt: on
    # have the secrets before the skill
    return (
        f"import {flow_name}_{skill.name}_secrets{ignore_noqa}" + "\n"
        f"from {flow_name}_{skill.name} import {skill.name}{ignore_noqa}"
    )


def get_agent_skill_registrations(
    agent: WaldiezAgent,
    agent_names: Dict[str, str],
    all_skills: List[WaldiezSkill],
    skill_names: Dict[str, str],
    string_escape: Callable[[str], str],
) -> str:
    """Get the agent skill registrations.

    example output:

    ```python
    >>> string_escape = lambda x: x.replace('"', '\\"').replace("\\n", "\\n")
    >>> agent = WaldiezAgent(
    ...     id="wa-1",
    ...     name="agent1",
    ...     description="An agent that does something.",
    ...     ...,
    ...     skills=[
    ...         WaldiezSkillLink(id="ws-1", executor_id="wa-2", ...),
    ...         WaldiezSkillLink(id="ws-2", executor_id="wa-3", ...),
    ...     ],
    ... )
    >>> agent_names = {"wa-1": "agent1", "wa-2": "agent2", "wa-3": "agent3"}
    >>> all_skills = [
    ...     WaldiezSkill(id="ws-1", ...),
    ...     WaldiezSkill(id="ws-2", ...),
    ...     WaldiezSkill(id="ws-3", ...),
    ... ]
    >>> skill_names = {"ws-1": "skill1", "ws-2": "skill2", "ws-3": "skill3"}
    >>> get_agent_skill_registrations(
    ...     agent=agent,
    ...     agent_names=agent_names,
    ...     all_skills=all_skills,
    ...     skill_names=skill_names,
    ...     string_escape=string_escape,
    ... )

    register_function(
        skill1,
        caller=agent1,
        executor=agent2,
        name="skill1",
        description="A skill that does something.",
    )
    register_function(
        skill2,
        caller=agent1,
        executor=agent3,
        name="skill2",
        description="A skill that does something.",
    )
    ```

    Parameters
    ----------
    agent : WaldiezAgent
        The agent.
    agent_names : Dict[str, str]
        A mapping of agent id to agent name.
    all_skills : List[WaldiezSkill]
        All the skills in the flow.
    skill_names : Dict[str, str]
        A mapping of skill id to skill name.
    string_escape : Callable[[str], str]
        The string escape function.
    Returns
    -------
    str
        The agent skill registrations.
    """
    if not agent.data.skills or not all_skills:
        return ""
    content = "\n"
    for linked_skill in agent.data.skills:
        waldiez_skill = next(
            skill for skill in all_skills if skill.id == linked_skill.id
        )
        skill_name = skill_names[linked_skill.id]
        skill_description = (
            waldiez_skill.description or f"Description of {skill_name}"
        )
        caller_name = agent_names[agent.id]
        executor_name = agent_names[linked_skill.executor_id]
        content += (
            get_agent_skill_registration(
                caller_name=caller_name,
                executor_name=executor_name,
                skill_name=skill_name,
                skill_description=skill_description,
                string_escape=string_escape,
            )
            + "\n"
        )
    return content.replace("\n\n\n", "\n\n")
