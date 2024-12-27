from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    TextSelector,
    NumberSelector,
    TextSelectorConfig,
    NumberSelectorConfig,
)
import voluptuous as vol

DOMAIN = "ts3_sensor"

class TS3ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for TeamSpeak 3 Sensor."""

    VERSION = 1

    def __init__(self):
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Validate user input
            errors = await self._validate_input(user_input)
            if not errors:
                return self.async_create_entry(title="TeamSpeak 3 Sensor", data=user_input)

            self._errors = errors

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("host", default="192.168.1.33"): str,
                    vol.Required("port", default=10011): int,
                    vol.Required("username", default="serveradmin"): str,
                    vol.Required("password"): str,
                }
            ),
            errors=self._errors,
        )

    async def _validate_input(self, user_input):
        """Validate the user input."""
        errors = {}
        try:
            # Test connection
            import ts3

            with ts3.query.TS3ServerConnection(
                f"telnet://{user_input['username']}:{user_input['password']}@{user_input['host']}:{user_input['port']}"
            ) as ts3conn:
                ts3conn.exec_("use", sid=1)
        except Exception:
            errors["base"] = "cannot_connect"

        return errors

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return TS3OptionsFlow(config_entry)


class TS3OptionsFlow(config_entries.OptionsFlow):
    """Handle options for the integration."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional("scan_interval", default=self.config_entry.options.get("scan_interval", 60)): int,
                }
            ),
        )
