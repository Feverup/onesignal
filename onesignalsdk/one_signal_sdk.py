"""
This module contains code that implements API calls for OneSignal Restful API. Some important concepts:

App: Represents a single App across all platforms.
Players (aka devices or users): Each OneSignal app represent many users.
Notification: A notification can be sent to individuals, segments and users.

Two type of API keys are used and it's important to distinguish them. As per their docs available at
https://documentation.onesignal.com/docs/server-api-overview:

---------------------------------------------------------------------------------------------------
Some API methods require User or App authentication REST API Keys. They are:

1. OneSignal App creation or modification - Requires your OneSignal 'User REST API Key'.

2. Notification Creation - Requires your OneSignal 'App REST API Key' when specifying
targets using "tags" or "included_segments". Otherwise no token is required.

Also note:

The 'User REST API Key' is visible on the "Account Management" page under the "API Keys" tab.

The 'App REST API Key' is under the "Application Settings" page under the "API Keys" tab.

---------------------------------------------------------------------------------------------------

"""
import json
import requests


BASE_URL = 'https://onesignal.com/api/v1'

def send_request(url, method='GET', data=None, headers=None):
    """
    Sends a request using `requests` module.
    :param url: URL to send requrest to
    :param method: HTTP method to use e.g. GET, PUT, DELETE, POST
    :param data: Data to send in case of PUT and POST
    :param headers: HTTP headers to use
    :return: Returns a HTTP Response object
    """
    assert url and method
    assert method in ['GET', 'PUT', 'DELETE', 'POST']
    method = getattr(requests, method.lower())
    response = method(url=url, data=data, headers=headers)
    return response


class OneSignalSdk(object):

    def __init__(self, app_id, user_auth_key):
        """
        Initilizates the OneSignalSDK object.
        :param app_id: You get an app_id once you are done creating an app using OneSignal's API
        :param user_auth_key: This can be found by logging-in to http://onesignal.com and then clicking "API Keys"
        from the top right menu.
        :return:
        """
        self.app_id = app_id
        self.user_auth_key = user_auth_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic %s" % self.user_auth_key
        }

    def get_players(self, app_id, app_auth_key, limit=300, offset=0):
        """
        Represents this endpoint; https://onesignal.com/api/v1/players?app_id=:app_id&limit=:limit&offset=:offset
        :param app_id: app_id represnts an 'App' in OneSignal's universe. This is the app_id you want to view devices
        from
        :param app_auth_key: Each OneSignal App has a 'basic_auth_key'
        :param limit:
        :param offset:
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {
            "total_count": 3,
            "offset": 2,
            "limit": 2,
            "players": [{
                "identifier": "ce777617da7f548fe7a9ab6febb56cf39fba6d382000c0395666288d961ee566",
                "session_count": 1,
                "language": "en",
                "timezone": -28800,
                "game_version": "1.0",
                "device_os": "7.0.4",
                "device_type": 0,
                "device_model": "iPhone",
                "ad_id": null,
                "tags": {
                    "a": "1",
                    "foo": "bar"
                },
                "last_active": 1395096859,
                "amount_spent": "0",
                "created_at": 1395096859,
                "invalid_identifier": false,
                "badge_count": 0
            }]
        }
        """
        url = BASE_URL + ("/players?app_id=%s&limit=%s&offset=%s" % (app_id, limit, offset))
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' % app_auth_key
        }
        return send_request(url, method='GET', headers=headers)

    def get_player(self, player_id):
        """
        It takes data from this endpoint: https://onesignal.com/api/v1/players/:id
        :param player_id:
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {
              "identifier":"ce777617da7f548fe7a9ab6febb56cf39fba6d382000c0395666288d961ee566",
              "session_count":1,
              "language":"en",
              "timezone":-28800,
              "game_version":"1.0",
              "device_os":"7.0.4",
              "device_type":0,
              "device_model":"iPhone",
              "ad_id":null,
              "tags":{"a":"1","foo":"bar"},
              "last_active":1395096859,
              "amount_spent":"0",
              "created_at":1395096859,
              "invalid_identifier":false,
              "badge_count": 0
        }
        """
        assert player_id
        url = BASE_URL + "/players/" + player_id
        return send_request(url, method='GETA'
                                        '')
    def create_player(self, app_id, device_type, **kwargs):
        """
        Sends a POST request to https://onesignal.com/api/v1/players to create a player.
        :param app_id: OneSignal's app_id
        :param device_type: Required parameter to create a device. 0 = iOS, 1 = Android, 2 = Amazon,
        3 = WindowsPhone(MPNS), 4 = ChromeApp, 5 = ChromeWebsite, 6 = WindowsPhone(WNS), 7 = Safari, 8 = Firefox
        :param kwargs: May add other parameters as given on https://documentation.onesignal.com/docs/players-add-a-device
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {"success": true, "id": "ffffb794-ba37-11e3-8077-031d62f86ebf" }
        """
        assert app_id
        assert device_type in range(0, 9)
        url = BASE_URL + "/players"
        kwargs['app_id'] = app_id
        kwargs['device_type'] = device_type
        data = json.dumps(kwargs)
        return send_request(url, method='POST', headers={
            'Content-Type': 'application/json'
        }, data=data)

    def edit_player(self, player_id, **kwargs):
        """
        Edits a player by sending a PUT request to https://onesignal.com/api/v1/players/:id
        :param player_id: Player's ID.
        :param kwargs: Represents other arguments this call can receiver per
        https://documentation.onesignal.com/docs/playersid-1
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {"success": true }
        """
        assert player_id
        url = BASE_URL + "/players/" + player_id
        data = json.dumps(kwargs)
        return send_request(url, method='PUT', headers={
            'Content-Type': 'application/json'
        }, data=data)

    def player_on_session(self, player_id, **kwargs):
        """
        Call on new device session in your app
        :param player_id: Player's ID.
        :param kwargs: Other arguments as given here https://documentation.onesignal.com/docs/playersidon_session
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {"success": true }
        """
        assert player_id
        url = BASE_URL + "/players/" + player_id + "/on_session"
        data = json.dumps(kwargs)
        return send_request(url, method='POST', headers={
            'Content-Type': 'application/json'
        }, data=data)

    def player_on_purchase(self, player_id, **kwargs):
        """
        Track a new purchase
        :param player_id: Player's ID
        :param kwargs: Take other arguments as given on https://documentation.onesignal.com/docs/on_purchase
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {"success": true }
        """
        assert player_id
        url = BASE_URL + "/players/" + player_id + "/on_purchase"
        data = json.dumps(kwargs)
        return send_request(url, method='POST', headers={
            'Content-Type': 'application/json'
        }, data=data)

    def player_on_focus(self, player_id, **kwargs):
        """
        Increment the device's total session length.
        :param player_id: Player's ID
        :param kwargs: Take other arguments as given on https://documentation.onesignal.com/docs/playersidon_focus
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {"success": true }
        """
        assert player_id
        url = BASE_URL + "/players/" + player_id + "/on_focus"
        data = json.dumps(kwargs)
        return send_request(url, method='POST', headers={
            'Content-Type': 'application/json'
        }, data=data)

    def create_app(self, app_name, **kwargs):
        """
        Creates a OneSignal app by sending a POST to https://onesignal.com/api/v1/apps
        :param app_name: App's name
        :param kwargs: Other arguments as given on https://documentation.onesignal.com/docs/apps-create-an-app
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {
                id: "e4e87830-b954-11e3-811d-f3b376925f15",
                name: "Your app 1",
                players: 0,
                messagable_players: 0,
                updated_at: "2014-04-01T04:20:02.003Z",
                created_at: "2014-04-01T04:20:02.003Z",
                gcm_key: "a gcm push key",
                chrome_key: "A Chrome Web Push GCM key",
                chrome_web_origin: "Chrome Web Push Site URL",
                chrome_web_gcm_sender_id: "Chrome Web Push GCM Sender ID",
                chrome_web_default_notification_icon: "http://yoursite.com/chrome_notification_icon",
                chrome_web_sub_domain: "your_site_name",
                apns_env: "sandbox",
                apns_certificates: "Your apns certificate",
                safari_apns_cetificate: "Your Safari APNS certificate",
                safari_site_origin: "The homename for your website for Safari Push, including http or https",
                safari_push_id: "The certificate bundle ID for Safari Web Push",
                safari_icon_16_16: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/16x16.png",
                safari_icon_32_32: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/16x16@2.png",
                safari_icon_64_64: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/32x32@2x.png",
                safari_icon_128_128: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/128x128.png",
                safari_icon_256_256: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/128x128@2x.png",
                site_name: "The URL to your website for Web Push",
                basic_auth_key: "NGEwMGZmMjItY2NkNy0xMWUzLTk5ZDUtMDAwYzI5NDBlNjJj"
        }
        """
        url = BASE_URL + "/apps?limit=300&offset=0"
        kwargs['name'] = app_name
        data = json.dumps(kwargs)
        return send_request(url, method='POST', headers=self.headers, data=data)

    def update_app(self, app_id, **kwargs):
        """
        Updates an app by sending a PUT to https://onesignal.com/api/v1/apps/:id
        :param app_id: App's ID
        :param kwargs: Other arguments as given on https://documentation.onesignal.com/docs/appsid-update-an-app
        :return: Returns HTTP response object which contains a response that, per docs, looks like
        {
                id: "e4e87830-b954-11e3-811d-f3b376925f15",
                name: "Your app 1",
                players: 0,
                messagable_players: 0,
                updated_at: "2014-04-01T04:20:02.003Z",
                created_at: "2014-04-01T04:20:02.003Z",
                gcm_key: "a gcm push key",
                chrome_key: "A Chrome Web Push GCM key",
                chrome_web_origin: "Chrome Web Push Site URL",
                chrome_web_gcm_sender_id: "Chrome Web Push GCM Sender ID",
                chrome_web_default_notification_icon: "http://yoursite.com/chrome_notification_icon",
                chrome_web_sub_domain: "your_site_name",
                apns_env: "sandbox",
                apns_certificates: "Your apns certificate",
                safari_apns_cetificate: "Your Safari APNS certificate",
                safari_site_origin: "The homename for your website for Safari Push, including http or https",
                safari_push_id: "The certificate bundle ID for Safari Web Push",
                safari_icon_16_16: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/16x16.png",
                safari_icon_32_32: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/16x16@2.png",
                safari_icon_64_64: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/32x32@2x.png",
                safari_icon_128_128: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/128x128.png",
                safari_icon_256_256: "http://onesignal.com/safari_packages/e4e87830-b954-11e3-811d-f3b376925f15/128x128@2x.png",
                site_name: "The URL to your website for Web Push",
                basic_auth_key: "NGEwMGZmMjItY2NkNy0xMWUzLTk5ZDUtMDAwYzI5NDBlNjJj"
        }
        """
        url = BASE_URL + "/apps/" + app_id
        data = json.dumps(kwargs)
        return send_request(url, method='PUT', headers=self.headers, data=data)

    def get_apps(self):
        """
        GET Apps by sending a GET to https://onesignal.com/api/v1/apps
        :return: Returns HTTP response object which contains a response that, per docs, looks like
        [{
                {
                    id: "92911750-242d-4260-9e00-9d9034f139ce",
                    name: "Your app 1",
                    players: 150,
                    messagable_players: 143,
                    updated_at: "2014-04-01T04:20:02.003Z",
                    created_at: "2014-04-01T04:20:02.003Z",
                    gcm_key: "a gcm push key",
                    chrome_key: "A Chrome Web Push GCM key",
                    chrome_web_origin: "Chrome Web Push Site URL",
                    chrome_web_gcm_sender_id: "Chrome Web Push GCM Sender ID",
                    chrome_web_default_notification_icon: "http://yoursite.com/chrome_notification_icon",
                    chrome_web_sub_domain: "your_site_name",
                    apns_env: "sandbox",
                    apns_certificates: "Your apns certificate",
                    safari_apns_cetificate: "Your Safari APNS certificate",
                    safari_site_origin: "The homename for your website for Safari Push, including http or https",
                    safari_push_id: "The certificate bundle ID for Safari Web Push",
                    safari_icon_16_16: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16.png",
                    safari_icon_32_32: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16@2.png",
                    safari_icon_64_64: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/32x32@2x.png",
                    safari_icon_128_128: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128.png",
                    safari_icon_256_256: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128@2x.png",
                    site_name: "The URL to your website for Web Push",
                    basic_auth_key: "NGEwMGZmMjItY2NkNy0xMWUzLTk5ZDUtMDAwYzI5NDBlNjJj"
                }
        }]
        """
        url = BASE_URL + "/apps"
        return send_request(url, method='GET', headers=self.headers)

    def get_app(self, app_id):
        """
        Gets an app by sending a GET to https://onesignal.com/api/v1/apps/:id
        :param app_id: App's ID
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {
              id: "92911750-242d-4260-9e00-9d9034f139ce",
              name: "Your app 1",
              players: 150,
              messagable_players: 143,
              updated_at: "2014-04-01T04:20:02.003Z",
              created_at: "2014-04-01T04:20:02.003Z",
              gcm_key: "a gcm push key",
              chrome_key: "A Chrome Web Push GCM key",
              chrome_web_origin: "Chrome Web Push Site URL",
              chrome_web_gcm_sender_id: "Chrome Web Push GCM Sender ID",
              chrome_web_default_notification_icon: "http://yoursite.com/chrome_notification_icon",
              chrome_web_sub_domain:"your_site_name",
              apns_env: "sandbox",
              apns_certificates: "Your apns certificate",
              safari_apns_cetificate: "Your Safari APNS certificate",
              safari_site_origin: "The homename for your website for Safari Push, including http or https",
              safari_push_id: "The certificate bundle ID for Safari Web Push",
              safari_icon_16_16: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16.png",
              safari_icon_32_32: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/16x16@2.png",
              safari_icon_64_64: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/32x32@2x.png",
              safari_icon_128_128: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128.png",
              safari_icon_256_256: "http://onesignal.com/safari_packages/92911750-242d-4260-9e00-9d9034f139ce/128x128@2x.png",
              site_name: "The URL to your website for Web Push",
              basic_auth_key: "NGEwMGZmMjItY2NkNy0xMWUzLTk5ZDUtMDAwYzI5NDBlNjJj"
        }
        """
        url = BASE_URL + "/apps/" + app_id
        return send_request(url, method='GET', headers=self.headers)

    def get_player(self, player_id):
        """
        Gets a player by sending a GET to https://onesignal.com/api/v1/players/:id
        :param _id: Player's id
        :return: Returns HTTP response object which contains a response that, per docs, looks like:
        {
            "identifier": "ce777617da7f548fe7a9ab6febb56cf39fba6d382000c0395666288d961ee566",
            "session_count": 1,
            "language": "en",
            "timezone": -28800,
            "game_version": "1.0",
            "device_os": "7.0.4",
            "device_type": 0,
            "device_model": "iPhone",
            "ad_id": null,
            "tags": {
                "a": "1",
                "foo": "bar"
            },
            "last_active": 1395096859,
            "amount_spent": "0",
            "created_at": 1395096859,
            "invalid_identifier": false,
            "badge_count": 0
    }
        """
        url = BASE_URL + "/players/" + player_id
        return send_request(url, method='GET')

    def export_players_to_csv(self, app_id, app_auth_key):
        """
        Sends a GET to https://onesignal.com/api/v1/players/csv_export?app_id=:app_id and in return it send a URL
        through which CSV file can be downloaded.
        :param app_id: App's ID.
        :param app_auth_key: App's auth key
        :return: Returns HTTP response object which contains a response,per their docs, that looks like:
        {
            "csv_file_url":
            "https://onesignal.com/csv_exports/b2f7f966-d8cc-11e4-bed1-df8f05be55ba/users_184948440ec0e334728e87228011ff41_2015-11-10.csv"
        }
        """
        assert app_id and app_auth_key
        url = BASE_URL + "/players/csv_export?app_id=" + app_id
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' % app_auth_key
        }
        return send_request(url, headers=headers, method='GET')

    def create_notification(self, app_id, contents, app_auth_key,  **kwargs):
        """
        Creates a notification by sending a notification to https://onesignal.com/api/v1/notifications
        :param app_id: App's ID
        :param contents: Contents of the message
        :param app_auth_key: App's auth key
        :param kwargs: There can be more arguments as given on https://documentation.onesignal.com/docs/notifications-create-notification
        :return: Returns a HTTP response object which, per docs, will contain response like:
        {
              "id": "458dcec4-cf53-11e3-add2-000c2940e62c",
              "recipients": 5
        }
        """
        assert app_id and contents and app_auth_key
        assert isinstance(contents, dict), "'contents' should be a dict"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' % app_auth_key
        }
        url = BASE_URL + "/notifications"
        kwargs['app_id'] = app_id
        kwargs['contents'] = contents
        data = json.dumps(kwargs)
        return send_request(url, method='POST', headers=headers, data=data)

    def get_notification(self, app_id, notification_id, app_auth_key):
        """
        Gets a notification by sending a GET to https://onesignal.com/api/v1/notifications/:id?app_id=:app_id
        :param app_id: App's ID
        :param notification_id: Notification ID that you want to get.
        :param app_auth_key: App's auth key
        :return: Returns a HTTP response object which, per docs, will contain response like:
        {
            "id": "481a2734-6b7d-11e4-a6ea-4b53294fa671",
            "successful": 15,
            "failed": 1,
            "converted": 3,
            "remaining": 0,
            "queued_at": 1415914655,
            "send_after": 1415914655,
            "data": {
                "foo": "bar",
                "your": "custom metadata"
            },
            "canceled": false,
            "headings": {
                "en": "English and default langauge heading",
                "es": "Spanish language heading"
            },
            "contents": {
                "en": "English language content",
                "es": "Hola"
            }
        }
        """

        assert app_id and notification_id and app_auth_key
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' % app_auth_key
        }
        url = BASE_URL + ('/notifications/%s?app_id=%s' % (notification_id, app_id))
        return send_request(url, method='GET', headers=headers)

    def delete_notification(self, app_id, notification_id, app_auth_key):
        """
        Deletes a notification by sending a DELETE to https://onesignal.com/api/v1/notifications/:id?app_id=:app_id
        :param app_id: App's ID
        :param notification_id:  Notification ID that you want to delete
        :param app_auth_key: App's auth key
        :return: Returns a HTTP response object which, per docs, will contain response like:
        {'success': "true"}
        """
        assert app_id and notification_id and app_auth_key
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic %s' % app_auth_key
        }
        url = BASE_URL + ('/notifications/%s?app_id=%s' % (notification_id, app_id))
        return send_request(url, method='DELETE', headers=headers)





