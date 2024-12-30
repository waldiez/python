"""Test waldiez.exporting.agent.AgentExporter."""

# flake8: noqa E501
# pylint: disable=too-many-locals,too-many-statements,line-too-long

import shutil
from pathlib import Path
from typing import List, Tuple

from waldiez.models import WaldiezAgent, WaldiezModel, WaldiezSkill


def create_agent(
    counter: int,
) -> Tuple[WaldiezAgent, List[WaldiezSkill], List[WaldiezModel]]:
    """Create an agent.

    Parameters
    ----------
    counter : int
        The counter to use for the id and name.

    Returns
    -------
    WaldiezAgent
        The agent.
    """
    # fmt: off
    skill1 = WaldiezSkill(  # type: ignore
        id=f"ws-{counter}_1",
        name=f"skill{counter}_1",
        description=f"skill{counter}_1 description",
        data={  # type: ignore
            "content": f"def skill{counter}_1():" + "\n" + f'    return "skill body of skill{counter}_1"',
            "secrets": {
                "SECRET_KEY_1": "SECRET_VALUE_1",
                "SECRET_KEY_2": "SECRET_VALUE_2",
            },
        },
    )
    skill2 = WaldiezSkill(  # type: ignore
        id=f"ws-{counter}_2",
        name=f"skill{counter}_2",
        description=f"skill{counter}_2 description",
        data={  # type: ignore
            "content": f"def skill{counter}_2():" + "\n" + f'    return "skill body of skill{counter}_2"',
            "secrets": {},
        },
    )
    # fmt: on
    model1 = WaldiezModel(  # type: ignore
        id=f"wm-{counter}_1",
        name=f"model{counter}_1",
        description=f"model{counter}_1 description",
        data={"apiType": "anthropic"},  # type: ignore
    )
    model2 = WaldiezModel(  # type: ignore
        id=f"wm-{counter}_2",
        name=f"model{counter}_2",
        description=f"model{counter}_2 description",
        data={"apiType": "nim"},  # type: ignore
    )
    agent = WaldiezAgent(  # type: ignore
        id=f"wa-{counter}",
        name=f"agent{counter}",
        agent_type="assistant",
        description=f"agent{counter} description",
        data={  # type: ignore
            "skills": [
                {
                    "id": f"ws-{counter}_1",
                    "executor_id": f"wa-{counter}",
                },
                {
                    "id": f"ws-{counter}_2",
                    "executor_id": f"wa-{counter}",
                },
            ],
            "model_ids": [f"wm-{counter}_1", f"wm-{counter}_2"],
        },
    )
    return agent, [skill1, skill2], [model1, model2]


def test_agent_exporter(tmp_path: Path) -> None:
    """Test AgentExporter.

    Parameters
    ----------
    tmp_path : Path
        The temporary path.
    """
    output_dir = tmp_path / "test_agent_exporter"
    output_dir.mkdir(exist_ok=True)
    agent, _, __ = create_agent(1)
    print(agent.id)
    shutil.rmtree(output_dir)
