from dataclasses import dataclass
from typing import Optional


@dataclass
class SelfAssertedResponse:
    status: str
    errorCode: Optional[str]
    message: Optional[str]


@dataclass
class Locale:
    lang: str


@dataclass
class XhrSettings:
    retryEnabled: bool
    retryMaxAttempts: int
    retryDelay: int
    retryExponent: int
    retryOn: list[str]


@dataclass
class SignInConfig:
    remoteResource: str
    retryLimit: int
    trimSpacesInPassword: bool
    api: str
    csrf: str
    transId: str
    pageViewId: str
    suppressElementCss: bool
    isPageViewIdSentWithHeader: bool
    allowAutoFocusOnPasswordField: bool
    pageMode: int
    config: dict[str, str]
    hosts: dict[str, str]
    locale: Locale
    xhrSettings: XhrSettings


@dataclass
class ApparatusProperty:
    name: str
    value: str
    type: str


@dataclass
class ApparatusAttribute:
    name: str
    value: str
    type: int


@dataclass
class ApparatusInfo:
    apparatusId: int
    apparatusName: str
    productType: str
    description: str
    properties: list[ApparatusProperty]
    attributes: list[ApparatusAttribute]


@dataclass
class Weather:
    @dataclass
    class Temperature:
        value: float
        unit: str
        unitType: int

    temperature: Temperature
    iconCode: int


@dataclass()
class Apparatus:
    apparatusId: int
    serialNumber: str
    name: str
    type: int
    localizedAddress: str
    materialDescription: Optional[str]
    heroImageUrl: str
    apparatusStatus: int
    isConnected: bool
    isConnecting: bool
    showWarning: bool
    weather: Weather
    preferredDealerName: Optional[str]
    preferredDealerPhone: Optional[str]
    preferredDealerEmail: Optional[str]
    isDealerManaged: bool
    isDealerUnmonitored: bool
    modelNumber: str
    panelId: str

    @dataclass
    class Property:
        name: str

        @dataclass
        class Value:
            type: Optional[int]
            status: int | str
            isLegacy: Optional[bool]
            isRunning: Optional[bool]
            deviceId: Optional[str]
            deviceType: Optional[str]
            signalStrength: Optional[str]
            batteryLevel: Optional[str]
        value: Value
        type: int
    properties: list[Property]


@dataclass
class Address:
    """ generated source for class Address """
    line1: str
    line2: Optional[str]
    city: str
    region: str
    country: str
    postalCode: str


@dataclass
class Subscription:
    """ generated source for class Subscription """
    type: int
    status: int
    isLegacy: bool
    isDunning: bool


@dataclass
class ApparatusDetail:
    @dataclass
    class Property:
        name: Optional[str]
        value: str | int | float
        type: int

    @dataclass
    class ProductInfo:
        name: str
        value: str
        type: int
    apparatusId: int
    name: str
    serialNumber: str
    apparatusClassification: int
    panelId: str
    activationDate: str
    deviceType: str
    deviceSsid: str
    shortDeviceId: Optional[str]
    apparatusStatus: int
    heroImageUrl: str
    statusLabel: str
    statusText: str
    eCodeLabel: Optional[str]
    weather: Weather
    isConnected: bool
    isConnecting: bool
    showWarning: bool
    hasMaintenanceAlert: bool
    lastSeen: str
    connectionTimestamp: str
    address: Address
    properties: list[Property]
    subscription: Subscription
    enrolledInVpp: bool
    hasActiveVppEvent: bool
    productInfo: list[Property]
    hasDisconnectedNotificationsOn: bool


@dataclass
class Item:
    apparatus: Apparatus
    apparatusDetail: ApparatusDetail
