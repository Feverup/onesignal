"""
Author: Zohaib Ijaz <mzohaib.qc@gmail.com> and Waqas Younas <waqas.younas@gmail.com>
"""
import datetime
import hashlib
from onesignalsdk import one_signal_sdk
import pytest


APP_ID = '3f373607-3ebb-413c-90fb-becfdd3bb2c5'
AUTH_TOKEN = 'YjcyZTcxNGUtYjRhZi00N2U4LWEwZjktNTZkOGVmNzM0ZWRh'
BASE_URL = 'http://onesignal.com/api/v1'


@pytest.fixture()
def one_signal_obj():
    return one_signal_sdk.OneSignalSdk(AUTH_TOKEN, APP_ID)


@pytest.fixture()
def app(one_signal_obj):
    """Creates an app as per https://documentation.onesignal.com/docs/apps-create-an-app.
    Also, the response would look like following:
    {
        "name" : "Your app 1",
        "apns_env": "sandbox",
        "apns_p12": "asdsadcvawe223cwef...",
        "apns_p12_password": "FooBar",
        "gcm_key": "a gcm push key"
    }
    """
    # dt_now = datetime.datetime.now
    # dt_format = "%d%m%Y%H%M%S%f"
    # params = dict(apns_env='sandbox')
    # app_name = dt_now().strftime(dt_format)
    # return one_signal_obj.create_app(app_name, **params).json()
    return one_signal_obj.get_app().json()


@pytest.fixture()
def player(one_signal_obj):
    dt_now = datetime.datetime.now
    dt_format = "%d%m%Y%H%M%S%f"
    random_str = hashlib.sha256(dt_now().strftime(dt_format)).hexdigest()
    device_type = 0 # denotes iOS
    params = dict(
        identifier=random_str, language='en', device_os='7.0',
        device_model='iPhone'
    )
    return one_signal_obj.create_player(device_type, **params).json()
