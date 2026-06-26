"""Wake button for Zidoo integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_DEVICE_ID, ATTR_ENTITY_ID
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import ZidooCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Zidoo wake button from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([ZidooWakeButton(coordinator, config_entry)])


class ZidooWakeButton(ButtonEntity):
    """Wake-on-LAN button for a Zidoo device."""

    _attr_has_entity_name = True
    _attr_name = "Wake"

    def __init__(
        self,
        coordinator: ZidooCoordinator,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the wake button."""
        self.coordinator = coordinator
        self._attr_unique_id = f"{config_entry.entry_id}_wake"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            manufacturer="Zidoo",
            name=config_entry.title,
        )

    @property
    def available(self) -> bool:
        """Return if the entity is available."""
        return True

    def _device_event_data(self) -> dict[str, Any]:
        """Return event data that identifies this entity and device."""
        data: dict[str, Any] = {ATTR_ENTITY_ID: self.entity_id}
        if self.device_entry is not None:
            data[ATTR_DEVICE_ID] = self.device_entry.id
        return data

    async def async_press(self) -> None:
        """Wake the Zidoo device."""
        await self.coordinator.async_wake(event_data=self._device_event_data())
