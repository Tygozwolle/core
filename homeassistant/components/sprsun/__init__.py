"""The sprsun modbus integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
import pymodbus.client as ModbusClient
from pymodbus.client import ModbusTcpClient
from pymodbus import (
    ExceptionResponse,
    Framer,
    ModbusException,
    pymodbus_apply_logging_config,
)
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SENSOR]

# TODO Create ConfigEntry type alias with API object
# TODO Rename type alias and update all entry annotations
from homeassistant.components.sprsun.sensor import SPRSUNModbusSensor

type New_NameConfigEntry = ConfigEntry[SPRSUNModbusSensor]  # noqa: F821


# TODO Update entry annotation
async def async_setup_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
    """Set up sprsun modbus from a config entry."""
    modbus_client = ModbusClient.ModbusTcpClient(
        host=entry.data[CONF_HOST],
        port=entry.data[CONF_PORT],
        framer=Framer.RTU,
    )
    modbus_client.connect()
    hass.data["sprsun_modbus"] = modbus_client
    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    # entry.runtime_data = MyAPI(...)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: New_NameConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
