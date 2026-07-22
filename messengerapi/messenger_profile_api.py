"""Wrapper for the Profile API"""

from ._base_api import BaseApiClient
from .constants import API_VERSION


class ProfileApi(BaseApiClient):
    def __init__(self, page_access_token: str, *, timeout: float = 30.0):
        super().__init__(page_access_token, timeout=timeout)
        self.__graph_version = API_VERSION
        self.__api_url = f"https://graph.facebook.com/v{self.__graph_version}/me"
        self.__global_level_endpoint = "/messenger_profile"
        self.__user_level_endpoint = "/custom_user_settings"

    def get_api_url(self):
        return self.__api_url

    def get_access_token(self):
        return super().get_access_token()

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

        if not isinstance(greetings, list) or not greetings or not isinstance(greetings[0], dict):
            raise TypeError("greetings must be a non-empty list of dictionaries")
        if greetings[0].get("locale") != "default":
            raise ValueError("the first greetings item must use locale='default'")

        request_body = {
            "get_started":
                {
                    "payload": get_started_button_payload
                },
            "greeting": greetings
        }

        return self._post_json(
            self.get_api_url() + self.__global_level_endpoint,
            request_body,
        )

    def set_user_persistent_menu(self, user_id: str, persistent_menu: list):
        """Set the persistent menu for any user of the page.

        Args:
			user_id (str) : The user id.
			persistent_menu (PersistentMenu object) : The content of the PersistentMenu object , obtained via the PersistentMenu().get_content() method.
        """

        return self._post_json(
            self.get_api_url() + self.__user_level_endpoint,
            {
                "psid": user_id,
                "persistent_menu": persistent_menu
            },
        )

    def set_persistent_menu(self, persistent_menu: list):
        """Set the persistent menu for the page.

        Args:
                persistent_menu (PersistentMenu object) : The content of the PersistentMenu object , obtained via the PersistentMenu().get_content() method.
        """

        return self._post_json(
            self.get_api_url() + self.__global_level_endpoint,
            {"persistent_menu": persistent_menu},
        )
