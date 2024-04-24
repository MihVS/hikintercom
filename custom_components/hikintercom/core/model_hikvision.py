from pydantic import BaseModel, Field


class DeviceInfo(BaseModel):
    """Модель статуса устройства - xsl"""

    name: str = Field(alias="deviceName")
    id: str = Field(alias="deviceID")
    description: str = Field(alias="deviceDescription")
    location: str = Field(alias="deviceLocation")
    system_contact: str = Field(alias="systemContact")
    model: str = Field(alias="model")
    serial: str = Field(alias="serialNumber")
    mac_address: str = Field(alias="macAddress")
    firmware_version: str = Field(alias="firmwareVersion")
    firmware_released: str = Field(alias="firmwareReleasedDate")
    boot_version: str = Field(alias="bootVersion")
    boot_released: str = Field(alias="bootReleasedDate")
    hardware_version: str = Field(alias="hardwareVersion")
    encoder_version: str = Field(alias="encoderVersion")
    encoder_released: str = Field(alias="encoderReleasedDate")
    type: str = Field(alias="deviceType")
    sub_type: str = Field(alias="subDeviceType", default=None)
    telecontrol_id: int = Field(alias="telecontrolID")
    support_beep: bool = Field(alias="supportBeep")
    support_video_loss: bool = Field(alias="supportVideoLoss")
    alarm_out: int = Field(alias="alarmOutNum")
    alarm_in: int = Field(alias="alarmInNum")
    rs485: int = Field(alias="RS485Num")
    customized_info: str = Field(alias="customizedInfo")


class BaseDeviseInfo(BaseModel):
    """Базовая модель инфы устройства"""

    device_info: DeviceInfo = Field(alias="DeviceInfo")


class Status(BaseModel):
    """Статус вызова - json"""

    status: str


class CallStatus(BaseModel):
    """Статус домофона - json"""

    call_status: Status = Field(alias='CallStatus')
