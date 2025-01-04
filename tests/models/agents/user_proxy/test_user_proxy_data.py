# SPDX-License-Identifier: MIT.
# Copyright (c) 2024 - 2025 Waldiez and contributors.
"""Test waldiez.models.agents.user_proxy.user_proxy_data.*."""

from waldiez.models.agents.user_proxy.user_proxy_data import (
    WaldiezUserProxyData,
)


def test_waldiez_user_proxy_data() -> None:
    """Test WaldiezUserProxyData."""
    user_proxy_data = WaldiezUserProxyData()  # type: ignore
    assert user_proxy_data.human_input_mode == "ALWAYS"
