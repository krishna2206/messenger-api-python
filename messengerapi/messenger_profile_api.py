"""Wrapper for the Profile API , version 16.0"""

import requests

from .constants import API_VERSION


class ProfileApi:
    def __init__(self, page_access_token: str):
        self.__graph_version = API_VERSION
        self.__api_url = f"https://graph.facebook.com/v{self.__graph_version}/me"
        self.__page_access_token = page_access_token
        self.__global_level_endpoint = "/messenger_profile"
        self.__user_level_endpoint = "/custom_user_settings"

    def get_api_url(self):
        return self.__api_url

    def get_access_token(self):
        return self.__page_access_token

    def get_graph_version(self):
        return self.__graph_version

    def set_welcome_screen(self, get_started_button_payload: str, greetings: list = None):
        """
        Set the welcome screen of the page. (https://developers.facebook.com/docs/messenger-platform/discovery/welcome-screen/)
        A welcome screen is the first screen a person sees when he clicks on the "Send message" button in the page.

        Args:
			get_started_payload (str) : The payload to be sent by the API when the user clicks on "Get started" button.
			greetings (list , optional) : The welcome message.
					Supports multiples locales by specifying the local and the corresponding message.
					Defaults to [{"locale":"default","text":"Welcome , {{user_full_name}} !"}]
        """
        greetings = (
            [{"locale": "default", "text": "Welcome , {{user_full_name}} !"}] if greetings is None
            else greetings)

        assert isinstance(greetings, list) and isinstance(
            greetings[0], dict), "param greetings must be a list of dicts"
        assert greetings[0]["locale"] == "default", "first element of param greetings must be the default locale used"

        request_body = {
            "get_started":
                {
                    "payload": get_started_button_payload
                },
            "greeting": greetings
        }

        return requests.post(
            self.get_api_url() + self.__global_level_endpoint,
            params={"access_token": self.get_access_token()},
            json=request_body).json()

    def set_user_persistent_menu(self, user_id: str, persistent_menu: list):
        """Set the persistent menu for any user of the page.

        Args:
			user_id (str) : The user id.
			persistent_menu (PersistentMenu object) : The content of the PersistentMenu object , obtained via the PersistentMenu().get_content() method.
        """

        return requests.post(
            self.get_api_url() + self.__user_level_endpoint,
            params={"access_token": self.get_access_token()},
            json={
                "psid": user_id,
                "persistent_menu": persistent_menu
            }).json()

    def set_persistent_menu(self, persistent_menu: list):
        """Set the persistent menu for the page.

        Args:
                persistent_menu (PersistentMenu object) : The content of the PersistentMenu object , obtained via the PersistentMenu().get_content() method.
        """

        return requests.post(
            self.get_api_url() + self.__global_level_endpoint,
            params={"access_token": self.get_access_token()},
            json={"persistent_menu": persistent_menu}).json()
