"""Diagnostics support for Generac."""
from __future__ import annotations

import ipaddress
from dataclasses import asdict
from email.utils import parseaddr
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import GeneracDataUpdateCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator: GeneracDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    diagnostics_data = {
        "data": redact(
            {gen_id: asdict(item) for gen_id, item in coordinator.data.items()}, False
        ),
    }

    return diagnostics_data


DataDict = dict[str, "str | DataDict"]


def redact(data: Any, redact_all: bool):
    if isinstance(data, dict):
        return redact_dict(data, redact_all)
    if isinstance(data, list):
        return redact_array(data, redact_all)
    if isinstance(data, str):
        if parseaddr(data) == ("", ""):
            return "REDACTED_VALID_EMAIL"
        if is_ipv4(data):
            return "REDACTED_IPV4"
        if is_ipv6(data):
            return "REDACTED_IPV6"
    if redact_all:
        return "REDACTED"
    return data


def is_ipv4(s: str):
    try:
        ipaddress.IPv4Network(s)
        return True
    except ValueError:
        return False


def is_ipv6(s: str):
    try:
        ipaddress.IPv6Network(s)
        return True
    except ValueError:
        return False


_REDACTED_KEYS = {
    "deviceSsid",
    "serialNumber",
    "apparatusId",
    "address",
    "localizedAddress",
}


def redact_dict(data: dict, redact_all: bool) -> dict:
    return {
        k: redact(v, True) if k in _REDACTED_KEYS else redact(v, redact_all)
        for k, v in data.items()
    }


def redact_array(data: list, redact_all: bool) -> list:
    return [redact(it, redact_all) for it in data]
