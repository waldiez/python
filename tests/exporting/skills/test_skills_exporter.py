# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Test waldiez.exporting.skills.SkillsExporter."""

import shutil
from pathlib import Path

from waldiez.exporting.base import AgentPosition, AgentPositions, ImportPosition
from waldiez.exporting.skills import SkillsExporter
from waldiez.models import WaldiezAgent, WaldiezSkill


# flake8: noqa E501
# pylint: disable=too-many-locals,unused-argument,line-too-long,inconsistent-quotes
def test_skills_exporter(tmp_path: Path) -> None:
    """Test SkillsExporter.

    Parameters
    ----------
    tmp_path : Path
        The temporary path.
    """
    flow_name = "flow1"
    agent1_name = "agent1"
    agent2_name = "agent2"
    skill1_name = "skill1"
    skill2_name = "skill2"
    # fmt: off
    skill1_content = (
        f"def {skill1_name}():" + "\n" + f'    return "skill body of {skill1_name}"'
    )
    skill2_content = (
        f"def {skill2_name}():" + "\n" + f'    return "skill body of {skill2_name}"'
    )
    # fmt: on
    skill1 = WaldiezSkill(  # type: ignore
        id="ws-1",
        name=skill1_name,
        description=f"{skill1_name} description",
        data={  # type: ignore
            "content": skill1_content,
            "secrets": {
                "SECRET_KEY_1": "SECRET_VALUE_1",
                "SECRET_KEY_2": "SECRET_VALUE_2",
            },
        },
    )
    skill2 = WaldiezSkill(  # type: ignore
        id="ws-2",
        name=skill2_name,
        description=f"{skill2_name} description",
        data={  # type: ignore
            "content": skill2_content,
            "secrets": {},
        },
    )
    agent1 = WaldiezAgent(  # type: ignore
        id="wa-1",
        name=agent1_name,
        agent_type="assistant",
        description="agent description",
        data={  # type: ignore
            "skills": [
                {
                    "id": "ws-1",
                    "executor_id": "wa-1",
                },
                {
                    "id": "ws-2",
                    "executor_id": "wa-2",
                },
            ],
        },
    )
    agent2 = WaldiezAgent(  # type: ignore
        id="wa-2",
        name=agent2_name,
        agent_type="assistant",
        description="agent description",
        data={"skills": []},  # type: ignore
    )
    agent_names = {"wa-1": "agent1", "wa-2": "agent2"}
    skill_names = {"ws-1": skill1_name, "ws-2": skill2_name}
    skills_exporter = SkillsExporter(
        flow_name=flow_name,
        agents=[agent1, agent2],
        agent_names=agent_names,
        skills=[skill1, skill2],
        skill_names=skill_names,
        output_dir=None,
    )
    first_import = (
        f"import {flow_name}_{skill1_name}_secrets  # type: ignore # noqa"
        "\n"
        f"from {flow_name}_{skill1_name} import {skill1_name}  # type: ignore # noqa"
    )
    second_import = f"from {flow_name}_{skill2_name} import {skill2_name}  # type: ignore # noqa"
    skill_imports = skills_exporter.get_imports()
    assert skill_imports[0][0] == first_import
    assert skill_imports[0][1] == ImportPosition.LOCAL
    assert skill_imports[1][0] == second_import
    assert skill_imports[1][1] == ImportPosition.LOCAL
    expected_environment_variables = [
        ("SECRET_KEY_1", "SECRET_VALUE_1"),
        ("SECRET_KEY_2", "SECRET_VALUE_2"),
    ]
    assert (
        skills_exporter.get_environment_variables()
        == expected_environment_variables
    )
    assert skills_exporter.get_before_export() is None
    expected_after_agent_position = AgentPosition(
        None, AgentPositions.AFTER_ALL, 1
    )
    expected_after_agent_string = (
        "\n"
        "register_function(\n"
        f"    {skill1_name},"
        "\n"
        f"    caller={agent1_name},"
        "\n"
        f"    executor={agent1_name},"
        "\n"
        f'    name="{skill1_name}",'
        "\n"
        f'    description="{skill1_name} description",'
        "\n"
        ")\n"
        "\n"
        "register_function(\n"
        f"    {skill2_name},"
        "\n"
        f"    caller={agent1_name},"
        "\n"
        f"    executor={agent2_name},"
        "\n"
        f'    name="{skill2_name}",'
        "\n"
        f'    description="{skill2_name} description",'
        "\n"
        ")\n"
        "\n"
    )
    after_agent = skills_exporter.get_after_export()
    assert after_agent is not None
    assert after_agent[0][0] == expected_after_agent_string
    assert after_agent[0][1] == expected_after_agent_position
    output_dir = tmp_path / "test_skills_exporter"
    output_dir.mkdir(exist_ok=True)
    skills_exporter = SkillsExporter(
        flow_name=flow_name,
        agents=[agent1, agent2],
        agent_names=agent_names,
        skills=[skill1, skill2],
        skill_names=skill_names,
        output_dir=str(output_dir),
    )
    expected_files = [
        f"{flow_name}_{skill1_name}_secrets.py",
        f"{flow_name}_{skill1_name}.py",
        f"{flow_name}_{skill2_name}.py",
    ]
    for file in expected_files:
        assert (output_dir / file).exists()
    shutil.rmtree(output_dir)

    # and one with no skills
    agent1.data.skills = []
    agent2.data.skills = []
    skills_exporter = SkillsExporter(
        flow_name=flow_name,
        agents=[agent1, agent2],
        agent_names=agent_names,
        skills=[],
        skill_names=skill_names,
        output_dir=str(output_dir),
    )
    imports = skills_exporter.get_imports()
    assert not imports
