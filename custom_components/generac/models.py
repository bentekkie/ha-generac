from dataclasses import dataclass
from typing import Optional


@dataclass
class SelfAssertedResponse:
    status: Optional[str]
    errorCode: Optional[str]
    message: Optional[str]


@dataclass
class Locale:
    lang: Optional[str]


@dataclass
class XhrSettings:
    retryEnabled: Optional[bool]
    retryMaxAttempts: Optional[int]
    retryDelay: Optional[int]
    retryExponent: Optional[int]
    retryOn: Optional[list[str]]


@dataclass
class SignInConfig:
    remoteResource: Optional[str]
    retryLimit: Optional[int]
    trimSpacesInPassword: Optional[bool]
    api: Optional[str]
    csrf: Optional[str]
    transId: Optional[str]
    pageViewId: Optional[str]
    suppressElementCss: Optional[bool]
    isPageViewIdSentWithHeader: Optional[bool]
    allowAutoFocusOnPasswordField: Optional[bool]
    pageMode: Optional[int]
    config: dict[str, Optional[str]]
    hosts: dict[str, Optional[str]]
    locale: Optional[Locale]
    xhrSettings: Optional[XhrSettings]


@dataclass
class ApparatusProperty:
    name: Optional[str]
    value: Optional[str]
    type: Optional[str]


@dataclass
class ApparatusAttribute:
    name: Optional[str]
    value: Optional[str]
    type: Optional[int]


@dataclass
class ApparatusInfo:
    apparatusId: Optional[int]
    apparatusName: Optional[str]
    productType: Optional[str]
    description: Optional[str]
    properties: Optional[list[ApparatusProperty]]
    attributes: Optional[list[ApparatusAttribute]]


@dataclass
class Weather:
    @dataclass
    class Temperature:
        value: Optional[float]
        unit: Optional[str]
        unitType: Optional[int]

    temperature: Optional[Temperature]
    iconCode: Optional[int]


@dataclass()
class Apparatus:
    apparatusId: Optional[int]
    serialNumber: Optional[str]
    name: Optional[str]
    type: Optional[int]
    localizedAddress: Optional[str]
    materialDescription: Optional[str]
    heroImageUrl: Optional[str]
    apparatusStatus: Optional[int]
    isConnected: Optional[bool]
    isConnecting: Optional[bool]
    showWarning: Optional[bool]
    weather: Optional[Weather]
    preferredDealerName: Optional[str]
    preferredDealerPhone: Optional[str]
    preferredDealerEmail: Optional[str]
    isDealerManaged: Optional[bool]
    isDealerUnmonitored: Optional[bool]
    modelNumber: Optional[str]
    panelId: Optional[str]

    @dataclass
    class Property:
        name: Optional[str]

        @dataclass
        class Value:
            type: Optional[int]
            status: Optional[int] | Optional[str]
            isLegacy: Optional[bool]
            isRunning: Optional[bool]
            deviceId: Optional[str]
            deviceType: Optional[str]
            signalStrength: Optional[str]
            batteryLevel: Optional[str]

        value: Optional[Value | list]
        type: Optional[int]

    properties: Optional[list[Property]]


@dataclass
class Address:
    """generated source for class Address"""

    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    region: Optional[str]
    country: Optional[str]
    postalCode: Optional[str]


@dataclass
class Subscription:
    """generated source for class Subscription"""

    type: Optional[int]
    status: Optional[int]
    isLegacy: Optional[bool]
    isDunning: Optional[bool]


@dataclass
class ApparatusDetail:
    @dataclass
    class Property:
        name: Optional[str]
        value: Optional[str] | Optional[int] | float
        type: Optional[int]

    @dataclass
    class ProductInfo:
        name: Optional[str]
        value: Optional[str]
        type: Optional[int]

    apparatusId: Optional[int]
    name: Optional[str]
    serialNumber: Optional[str]
    apparatusClassification: Optional[int]
    panelId: Optional[str]
    activationDate: Optional[str]
    deviceType: Optional[str]
    deviceSsid: Optional[str]
    shortDeviceId: Optional[str]
    apparatusStatus: Optional[int]
    heroImageUrl: Optional[str]
    statusLabel: Optional[str]
    statusText: Optional[str]
    eCodeLabel: Optional[str]
    weather: Optional[Weather]
    isConnected: Optional[bool]
    isConnecting: Optional[bool]
    showWarning: Optional[bool]
    hasMaintenanceAlert: Optional[bool]
    lastSeen: Optional[str]
    connectionTimestamp: Optional[str]
    address: Optional[Address]
    properties: Optional[list[Property]]
    subscription: Optional[Subscription]
    enrolledInVpp: Optional[bool]
    hasActiveVppEvent: Optional[bool]
    productInfo: Optional[list[Property]]
    hasDisconnectedNotificationsOn: Optional[bool]


@dataclass
class Item:
    apparatus: Apparatus
    apparatusDetail: ApparatusDetail
