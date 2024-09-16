from pymodbus.client import ModbusTcpClient
from homeassistant.helpers.entity import Entity
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Modbus sensors."""
    modbus_client = hass.data["sprsun_modbus"]
    sensors = [
        SPRSUNModbusSensor(
            modbus_client,
            "Return Water Temperature",
            1,
            "°C",
            "sensor.return_water_temperature",
        ),
        SPRSUNModbusSensor(
            modbus_client, "Outlet Temperature", 2, "°C", "sensor.outlet_temperature"
        ),
        # Add more sensors as needed
    ]
    async_add_entities(sensors)


class SPRSUNModbusSensor(Entity):
    """Representation of a Modbus Sensor."""

    def __init__(self, client, name, register, unit_of_measurement, unique_id):
        """Initialize the sensor."""
        self._name = name
        self._register = register
        self._unit_of_measurement = unit_of_measurement
        self._unique_id = unique_id
        self._state = None
        self._client = client

    async def async_update(self):
        """Fetch new state data for the sensor."""
        if not self._client.is_socket_open():
            _LOGGER.warning(f"Reconnecting Modbus client for {self._name}")
            self._client.connect()

        try:
            # Read the Modbus register using the shared client
            result = self._client.read_holding_registers(self._register, 1, unit=1)

            if result.isError():
                _LOGGER.error(
                    f"Error reading Modbus register {self._register} for {self._name}"
                )
                self._state = None
            else:
                # Assume the first register holds the value, and assign it to the state
                self._state = result.registers[0]

        except Exception as e:
            _LOGGER.error(f"Error fetching Modbus data for {self._name}: {str(e)}")
            self._state = None
