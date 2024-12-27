from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import ts3

DOMAIN = "ts3_sensor"

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the sensor."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([TS3Sensor(config)])


class TS3Sensor(Entity):
    def __init__(self, config):
        self._state = None
        self._attributes = {}
        self._config = config

    @property
    def name(self):
        return "TeamSpeak 3 Sensor"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        try:
            with ts3.query.TS3ServerConnection(
                f"telnet://{self._config['username']}:{self._config['password']}@{self._config['host']}:{self._config['port']}"
            ) as ts3conn:
                ts3conn.exec_("use", sid=1)
                clients = ts3conn.exec_("clientlist").parsed
                channels = ts3conn.exec_("channellist").parsed
                server_info = ts3conn.exec_("serverinfo").parsed[0]
                max_clients = int(server_info["virtualserver_maxclients"])

                self._state = len(clients)
                self._attributes = {
                    "clients": clients,
                    "channels": channels,
                    "max_clients": max_clients,
                }
        except Exception as e:
            self._state = "Error"
            self._attributes = {"error": str(e)}
