import datetime
import hashlib
APP_ID = '3f373607-3ebb-413c-90fb-becfdd3bb2c5'
AUTH_TOKEN = 'YjcyZTcxNGUtYjRhZi00N2U4LWEwZjktNTZkOGVmNzM0ZWRh'
BASE_URL = 'http://onesignal.com/api/v1'


class Test_OneSignal_SDK(object):

    # def test_auth(self, one_signal_obj):
    #     # Tests the basic auth
    #     response = one_signal_obj.get_apps()
    #     assert response.status_code == 200
    #     app_data = response.json()[0]
    #     assert app_data['id'] and app_data['created_at'] and app_data['updated_at'] and \
    #         app_data['players']
    #
    #
    # def test_player_on_session(self, one_signal_obj, app):
    #     dt_now = datetime.datetime.now
    #     dt_format = "%d%m%Y%H%M%S%f"
    #     random_str = hashlib.sha256(dt_now().strftime(dt_format)).hexdigest()
    #     device_type = 0 # denotes iOS
    #     params = dict(
    #         identifier=random_str, language='en', device_os='7.0',
    #         device_model='iPhone'
    #     )
    #     response = one_signal_obj.create_player(app['id'], device_type, **params)
    #     print 'response create player', response.json()
    #     app_data = response.json()
    #     player_id = app_data['id']
    #     assert app_data['success'] and app_data['id']
    #     # Now test on_session code
    #     params = dict(
    #         language='en', device_os='7.0'
    #     )
    #     response = one_signal_obj.player_on_session(player_id, **params)
    #     data = response.json()
    #     assert data['success']
    #
    # def test_player_on_purchase(self, one_signal_obj, app):
    #     dt_now = datetime.datetime.now
    #     dt_format = "%d%m%Y%H%M%S%f"
    #     random_str = hashlib.sha256(dt_now().strftime(dt_format)).hexdigest()
    #     device_type = 0 # denotes iOS
    #     params = dict(
    #         identifier=random_str, language='en', device_os='7.0',
    #         device_model='iPhone'
    #     )
    #     response = one_signal_obj.create_player(app['id'], device_type, **params)
    #     print 'response create player', response.json()
    #     app_data = response.json()
    #     player_id = app_data['id']
    #     assert app_data['success'] and app_data['id']
    #     # Now test on_purchase code
    #     params = dict(
    #         purchases=[
    #             {
    #                 'sku': 'SKU123',
    #                 'iso': 'USD',
    #                 'amount': '0.99'
    #             }
    #         ]
    #     )
    #     response = one_signal_obj.player_on_purchase(player_id, **params)
    #     data = response.json()
    #     assert data['success']
    #
    # def test_player_on_focus(self, one_signal_obj, app):
    #     dt_now = datetime.datetime.now
    #     dt_format = "%d%m%Y%H%M%S%f"
    #     random_str = hashlib.sha256(dt_now().strftime(dt_format)).hexdigest()
    #     device_type = 0 # denotes iOS
    #     params = dict(
    #         identifier=random_str, language='en', device_os='7.0',
    #         device_model='iPhone'
    #     )
    #     response = one_signal_obj.create_player(app['id'], device_type, **params)
    #     print 'response create player', response.json()
    #     app_data = response.json()
    #     player_id = app_data['id']
    #     assert app_data['success'] and app_data['id']
    #     # Now test on_purchase code
    #     params = dict(
    #         state='ping',
    #         active_time=60
    #     )
    #     response = one_signal_obj.player_on_focus(player_id, **params)
    #     data = response.json()
    #     assert data['success']
    #
    # def test_all_players(self, one_signal_obj, app):
    #     response = one_signal_obj.get_players(app['id'], app['basic_auth_key'])
    #     players_data = response.json()
    #     assert all([players_data.has_key(item)
    #                 for item in ['total_count', 'offset', 'limit', 'players']])
    #
    # def test_player(self, one_signal_obj, app):
    #     dt_now = datetime.datetime.now
    #     dt_format = "%d%m%Y%H%M%S%f"
    #     random_str = hashlib.sha256(dt_now().strftime(dt_format)).hexdigest()
    #     device_type = 0 # denotes iOS
    #     params = dict(
    #         identifier=random_str, language='en', device_os='7.0',
    #         device_model='iPhone'
    #     )
    #     response = one_signal_obj.create_player(app['id'], device_type, **params)
    #     print 'response create player', response.json()
    #     app_data = response.json()
    #     player_id = app_data['id']
    #     assert app_data['success'] and app_data['id']
    #     # Let's edit the player
    #     params = dict(
    #         language='es', device_os='9.0'
    #     )
    #     response = one_signal_obj.edit_player(player_id, **params)
    #     print 'Response edit player', response.text
    #     player_data = response.json()
    #     assert player_data['success']
    #
    #     # Now let's get the player and see if the values actually changed
    #
    #     response = one_signal_obj.get_player(player_id)
    #     player_data = response.json()
    #     assert all([player_data.has_key(item) for item in
    #                 ['identifier', 'language', 'device_os', 'device_type', 'created_at']])
    #     assert player_data['language'] == 'es'
    #     assert player_data['device_os'] == '9.0'
    #
    def test_player_csv_export(self, one_signal_obj, app):
        response = one_signal_obj.export_players_to_csv(app['id'], app['basic_auth_key'])
        response = response.json()
        assert response['csv_file_url']
        assert '.csv' in response['csv_file_url']
    # def test_apps(self, one_signal_obj, app):
    #     # Create an app, get, update, get
    #
    #     assert isinstance(app, dict)
    #     assert app['id'] and app['name'] and app['updated_at'] and \
    #         app['created_at']
    #
    #     # now get this app
    #     app_id = app['id']
    #     response = one_signal_obj.get_app(app_id)
    #     app_data = response.json()
    #     assert app_data['id'] and app_data['name'] and app_data['updated_at'] and \
    #         app_data['created_at']
    #
    #     # now update the app
    #     params = dict(name='new app name')
    #     response = one_signal_obj.update_app(app_id, **params)
    #     app_data = response.json()
    #     assert app_data['name'] == params['name']


    # def test_notifications(self, one_signal_obj):
    #     """In order to test notifications we have to have an app configured
    #     to send notifications. We have preconfigured one such app. Here are credentials:
    #     one signal app id = 6f5f312f-7799-4aa8-a7de-8d00eabbb664
    #     one signal app name = 20012016104125275932
    #     Google credentials were created by following https://documentation.onesignal.com/docs/website-generating-a-gcm-push-notification
    #     Google API key = AIzaSyDL4jK9yBaIMVOAR-Bi40h-srDgVKeoSWA
    #     Google Project number = 703322744261
    #
    #     We also had to "Subscribe to the notifications". We did that by creating a small Flask app (also contained
    #     in this repository). We created a small template within that Flask app that allowed us to subscribe to
    #     notifications.
    #     """
    #
    #     app_id = '6f5f312f-7799-4aa8-a7de-8d00eabbb664'
    #     response = one_signal_obj.get_app(app_id)
    #     app = response.json()
    #     assert isinstance(app, dict)
    #     assert app['id'] and app['name'] and app['updated_at'] and \
    #         app['created_at']
    #     app_auth_key = app['basic_auth_key']
    #     assert response.status_code == 200
    #
    #     # Create a notification
    #     contents = dict(en="Lorel Ipsum Lorel Ipsum")
    #     params = dict(
    #         included_segments=['All'],
    #         headings={'en': 'Message Heading'},
    #         url='http://google.com',
    #         isChromeWeb=True
    #
    #     )
    #     response = one_signal_obj.create_notification(app_id, contents, app_auth_key, **params)
    #     notification_data = response.json()
    #     notification_id = notification_data['id']
    #     assert notification_data['id'] and notification_data['recipients']
    #
    #     # Get the notification
    #     response = one_signal_obj.get_notification(app_id, notification_id, app_auth_key)
    #     notification_data = response.json()
    #     assert notification_data['id'] == notification_id
    #     assert notification_data['contents']['en'] == contents['en']
    #
    #     # Won't be able to delete because notification has been sent
    #     response = one_signal_obj.delete_notification(app_id, notification_id, app_auth_key)
    #     notification_data = response.json()
    #     assert response.status_code == 400
    #     assert notification_data['errors'][0] == 'Notification has already been sent to all recipients'





