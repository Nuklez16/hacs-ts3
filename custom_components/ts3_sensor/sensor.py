from homeassistant.helpers.entity import Entity
import ts3

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([TS3Sensor()])

class TS3Sensor(Entity):
    def __init__(self):
        self._state = None
        self._attributes = {}

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
            with ts3.query.TS3ServerConnection("telnet://serveradmin:PASSWORDHERE@192.168.1.33:10011") as ts3conn:
                ts3conn.exec_("use", sid=1)
                clients = ts3conn.exec_("clientlist").parsed
                channels = ts3conn.exec_("channellist").parsed

                self._state = len(clients)
                self._attributes = {"clients": clients, "channels": channels}
        except Exception as e:
            self._state = "Error"
            self._attributes = {"error": str(e)}
