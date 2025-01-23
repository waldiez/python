# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Test waldiez.models.skill.*."""

import pytest

from waldiez.models.skill import (
    SHARED_SKILL_NAME,
    WaldiezSkill,
    WaldiezSkillData,
)


def test_waldiez_skill() -> None:
    """Test WaldiezSkill."""
    # Given
    skill_id = "ws-1"
    name = "skill_name"
    description = "description"
    data = {"content": "def skill_name():\n    pass"}
    # When
    skill = WaldiezSkill(  # type: ignore
        id=skill_id,
        name=name,
        description=description,
        data=data,  # type: ignore
    )
    # Then
    assert skill.id == skill_id
    assert skill.name == name
    assert skill.description == description
    assert skill.content == data["content"]
    assert not skill.secrets
    assert not skill.tags
    assert not skill.requirements


def test_invalid_skill() -> None:
    """Test invalid WaldiezSkill."""
    with pytest.raises(ValueError):
        WaldiezSkill()  # type: ignore

    # Given
    skill_id = "ws-1"
    name = "skill_name"
    description = "description"
    data = {"content": "def skill_name(4):"}
    # Then
    with pytest.raises(ValueError):
        WaldiezSkill(  # type: ignore
            id=skill_id,
            name=name,
            description=description,
            data=data,  # type: ignore
        )

    # Given
    skill_id = "ws-1"
    name = "skill_name"
    description = "description"
    data = {"content": "def not_skill_name():\n    pass"}
    # Then
    with pytest.raises(ValueError):
        WaldiezSkill(  # type: ignore
            id=skill_id,
            name=name,
            description=description,
            data=data,  # type: ignore
        )


def test_shared_skill() -> None:
    """Test shared skill."""
    # When
    skill = WaldiezSkill(
        id="ws-1",
        type="skill",
        tags=[],
        requirements=[],
        name=SHARED_SKILL_NAME,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        description="shared skill",
        data=WaldiezSkillData(content="GLOBAL_VARIABLE = 5", secrets={}),
    )
    # Then
    assert skill.id == "ws-1"
    assert skill.name == SHARED_SKILL_NAME
    assert skill.description == "shared skill"
    assert skill.content == "GLOBAL_VARIABLE = 5"
    assert not skill.secrets
    assert not skill.tags
    assert not skill.requirements
    assert skill.get_content() == "GLOBAL_VARIABLE = 5"
