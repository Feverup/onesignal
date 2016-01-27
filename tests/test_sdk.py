"""
Contains tests for OneSignal's Python API
"""
APP_ID = '3f373607-3ebb-413c-90fb-becfdd3bb2c5'
AUTH_TOKEN = 'YjcyZTcxNGUtYjRhZi00N2U4LWEwZjktNTZkOGVmNzM0ZWRh'
BASE_URL = 'http://onesignal.com/api/v1'


class Test_OneSignal_SDK(object):

    def test_auth(self, one_signal_obj):
        """
        Tests the auth and we simulate that by trying to get all apps (that requires the auth)
        :param one_signal_obj: Contains the OneSignal API object
        :return:
        """
        # Tests the basic auth
        response = one_signal_obj.get_apps()
        assert response.status_code == 200
        app_data = response.json()[0]
        assert app_data['id'] and app_data['created_at'] and app_data['updated_at'] and \
            app_data['players']

    def test_player_on_session(self, one_signal_obj, app, player):
        """
        Tests the player on_session.
        :param one_signal_obj: OneSignal API object
        :param app: OneSignal's App
        :return:
        """

        player_id = player['id']
        assert player['success'] and player['id']
        # Now test on_session code
        params = dict(
            language='en', device_os='7.0'
        )
        response = one_signal_obj.player_on_session(player_id, **params)
        data = response.json()
        assert data['success']

    def test_player_on_purchase(self, one_signal_obj, player):
        """
        Tests the player on_purchase.
        :param one_signal_obj: OneSignal API object
        :param player: OneSignal's player object
        :return:
        """
        player_id = player['id']
        assert player['success'] and player['id']
        # Now test on_purchase code
        params = dict(
            purchases=[
                {
                    'sku': 'SKU123',
                    'iso': 'USD',
                    'amount': '0.99'
                }
            ]
        )
        response = one_signal_obj.player_on_purchase(player_id, **params)
        data = response.json()
        assert data['success']

    def test_player_on_focus(self, one_signal_obj, player):
        """
        Tests OneSignal's player on_focus.
        :param one_signal_obj: OneSignal object
        :param player: OneSignal player object
        :return:
        """
        player_id = player['id']
        assert player['success'] and player['id']
        # Now test on_purchase code
        params = dict(
            state='ping',
            active_time=60
        )
        response = one_signal_obj.player_on_focus(player_id, **params)
        data = response.json()
        assert data['success']

    def test_all_players(self, one_signal_obj, app):
        """
        Tests the endpoint that gets all players
        :param one_signal_obj: OneSignal object
        :param app: OneSignal App as created in conftest.py
        :return:
        """
        response = one_signal_obj.get_players(app['basic_auth_key'])
        players_data = response.json()
        assert all([players_data.has_key(item)
                    for item in ['total_count', 'offset', 'limit', 'players']])

    def test_player(self, one_signal_obj, player):
        """
        First we create a player and make sure it's created. Then we edit the player and finally
        we retrieve the player and make sure edits were correct.
        :param one_signal_obj: OneSignal API object
        :param player: OneSignal player as defined in the conftest.py
        :return:
        """

        player_id = player['id']
        assert player['success'] and player['id']
        # Let's edit the player
        params = dict(
            language='es', device_os='9.0'
        )
        response = one_signal_obj.edit_player(player_id, **params)
        player_data = response.json()
        assert player_data['success']
        # Now let's get the player and see if the values actually changed
        response = one_signal_obj.get_player(player_id)
        player_data = response.json()
        assert all([player_data.has_key(item) for item in
                    ['identifier', 'language', 'device_os', 'device_type', 'created_at']])
        assert player_data['language'] == 'es'
        assert player_data['device_os'] == '9.0'

    def test_player_csv_export(self, one_signal_obj, app):
        """
        Testing the endpoint that gives the URL of the CSV
        :param one_signal_obj: OneSignal API object
        :param app: OneSignal App as defined in the conftest.py
        :return:
        """
        response = one_signal_obj.export_players_to_csv(app['basic_auth_key'])
        response = response.json()
        assert response['csv_file_url']
        assert '.csv' in response['csv_file_url']

    def test_apps(self, one_signal_obj, app):
        """
        Test the endpoints of app. First an app is create, then it's retrieved and we make
        sure that edits are correct.
        :param one_signal_obj: OneSignal API object as defined in conftest.py
        :param app: OneSignal API object as defined in the conftest.py
        :return:
        """
        # Create an app, get, update, get
        assert isinstance(app, dict)
        assert app['id'] and app['name'] and app['updated_at'] and \
            app['created_at']
        response = one_signal_obj.get_app()
        app_data = response.json()
        assert app_data['id'] and app_data['name'] and app_data['updated_at'] and \
            app_data['created_at']
        # now update the app
        params = dict(name='new app name')
        response = one_signal_obj.update_app(**params)
        app_data = response.json()
        assert app_data['name'] == params['name']

    def test_notifications(self, one_signal_obj):
        """In order to test notifications we have to have an app configured
        to send notifications. We have preconfigured one such app. Here are credentials:
        one signal app id = 6f5f312f-7799-4aa8-a7de-8d00eabbb664
        one signal app name = 20012016104125275932
        Google credentials were created by following https://documentation.onesignal.com/docs/website-generating-a-gcm-push-notification
        Google API key = AIzaSyDL4jK9yBaIMVOAR-Bi40h-srDgVKeoSWA
        Google Project number = 703322744261
            We also had to "Subscribe to the notifications". We did that by creating a small Flask app (also contained
        in this repository). We created a small template within that Flask app that allowed us to subscribe to
        notifications.
        """
        app_id = '6f5f312f-7799-4aa8-a7de-8d00eabbb664'
        response = one_signal_obj.get_app(app_id)
        assert response.status_code == 200
        app = response.json()
        assert isinstance(app, dict)
        assert app['id'] and app['name'] and app['updated_at'] and \
            app['created_at']
        app_auth_key = app['basic_auth_key']
        one_signal_obj.user_auth_key = app_auth_key
        one_signal_obj.app_id = app_id
        # Create a notification
        contents = "Lorel Ipsum Lorel Ipsum"
        kwargs = dict(
            included_segments=['All'],
            isChromeWeb=True
            )
        url = 'http://google.com'
        heading = 'Message Heading'
        response = one_signal_obj.create_notification(contents, heading, url, **kwargs)
        assert response.status_code == 200
        notification_data = response.json()
        notification_id = notification_data['id']
        assert notification_data['id'] and notification_data['recipients']
        # Get the notification
        response = one_signal_obj.get_notification(app_id, notification_id, app_auth_key)
        notification_data = response.json()
        assert notification_data['id'] == notification_id
        assert notification_data['contents']['en'] == contents
        # Won't be able to delete because notification has been sent
        response = one_signal_obj.delete_notification(notification_id)
        assert response.status_code == 400
        notification_data = response.json()
        assert notification_data['errors'][0] == 'Notification has already been sent to all recipients'





