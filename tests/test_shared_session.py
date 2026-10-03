"""Every NOAA request goes through Home Assistant's shared aiohttp session.

The integration used to open its own ClientSession for each fetch and never
close it, which Home Assistant logged as "Unclosed client session".
"""

from homeassistant.config_entries import SOURCE_USER, ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.test_util.aiohttp import (
    AiohttpClientMocker,
)

from custom_components.ndbcrealtime.const import DOMAIN


async def test_setup_fetches_through_shared_session(
    hass: HomeAssistant, noaa: AiohttpClientMocker
) -> None:
    """Setup and the first coordinator refresh both use the shared session."""
    entry = MockConfigEntry(domain=DOMAIN, data={"station_id": "46042"})
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED
    assert hass.states.get("sensor.weather_nbdc_46042_wave_height").state == "1.5"
    # Station list + observation, once for setup and once for the first refresh.
    assert noaa.call_count == 4


async def test_config_flow_fetches_through_shared_session(
    hass: HomeAssistant, noaa: AiohttpClientMocker
) -> None:
    """The station picker and the station check both use the shared session."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {"station_id": "46042"}
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "NDBC - MONTEREY - 27NM WNW of Monterey, CA"
    assert result["data"] == {"station_id": "46042"}
