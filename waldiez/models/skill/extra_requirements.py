# SPDX-License-Identifier: Apache-2.0.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Waldiez skill extra requirements."""

from typing import Iterator, Set

from .skill import WaldiezSkill


def get_skills_extra_requirements(
    skills: Iterator[WaldiezSkill],
) -> Set[str]:
    """Get the skills extra requirements.

    Parameters
    ----------
    skills : List[WaldiezSkill]
        The skills.
    Returns
    -------
    List[str]
        The skills extra requirements.
    """
    skill_requirements: Set[str] = set()
    for skill in skills:
        for requirement in skill.requirements:
            skill_requirements.add(requirement)
    return skill_requirements
