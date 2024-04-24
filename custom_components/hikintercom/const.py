DOMAIN = 'hikintercom'
MANUFACTURER = 'Hikvision'
HTTP_URL = 'http://'

URL_GET_INFO = '/ISAPI/System/deviceInfo'
URL_GET_STATE = '/ISAPI/VideoIntercom/callStatus?format=json'
URL_OPEN_DOOR = '/ISAPI/AccessControl/RemoteControl/door/'

CONFIGURATION_URL = 'https://www.hikvision.com'

BOODY_OPEN_DOOR = '''
    <RemoteOpenDoor>
        <cmd>open</cmd>
    </RemoteOpenDoor>
'''

TIME_OUT_UPDATE_DATA = 10
TIME_UPDATE = 2

PLATFORMS = [
    'sensor',
    'button'
]
