from pydantic import BaseModel


class DeviceInfo(BaseModel):
    """Модель статуса устройства - xsl"""

    deviceName: str
    deviceID: str
    deviceDescription: str
    deviceLocation: str
    systemContact: str
    model: str
    serialNumber: str
    macAddress: str
    firmwareVersion: str
    firmwareReleasedDate: str
    bootVersion: str
    bootReleasedDate: str
    hardwareVersion: str
    encoderVersion: str
    encoderReleasedDate: str
    deviceType: str
    subDeviceType: str
    telecontrolID: int
    supportBeep: bool
    supportVideoLoss: bool
    alarmOutNum: int
    alarmInNum: int
    RS485Num: int
    customizedInfo: str


class Status(BaseModel):
    """Статус вызова - json"""

    status: str


class CallStatus(BaseModel):
    """Статус домофона - json"""

    call_status: Status
