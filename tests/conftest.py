"""Fixtures for the NDBC integration tests."""

from pathlib import Path

import pytest
from pytest_homeassistant_custom_component.test_util.aiohttp import (
    AiohttpClientMocker,
)

FIXTURES = Path(__file__).parent / "fixtures"

STATION_URL = "https://www.ndbc.noaa.gov/activestations.xml"
OBSERVATION_URL = "https://www.ndbc.noaa.gov/data/realtime2/46042.txt"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Let Home Assistant load the integration from custom_components."""


@pytest.fixture
def noaa(aioclient_mock: AiohttpClientMocker) -> AiohttpClientMocker:
    """Serve NOAA's station list and one buoy on Home Assistant's session.

    Only sessions made by Home Assistant's aiohttp helper are mocked. A session
    the integration opens on its own bypasses this and hits the blocked network.
    """
    aioclient_mock.get(
        STATION_URL, text=(FIXTURES / "activestations.xml").read_text()
    )
    aioclient_mock.get(OBSERVATION_URL, text=(FIXTURES / "46042.txt").read_text())
    return aioclient_mock
