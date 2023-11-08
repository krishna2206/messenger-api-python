"""A module containing various elements used when sending message in Messenger API."""

from messengerapi import ButtonType


class Elements:
    """A list of Element objects.

    Attributes:
        elements (str , private) : A list containing the content of each Element object.

    Notes:
        Use the add_element() method to add an Element object's content.
        Use the get_content() method to get the content of the Elements object before using it in an generic message.

        The maximum of elements is 10 , sending generic message with more than 10 elements will return an error message from Facebook API's server.
    """

    def __init__(self):
        self.__elements = []

    def add_element(self, element):
        self.__elements.append(element)

    def get_content(self):
        return self.__elements


class Element:
    def __init__(self, title="An element of a generic message.", subtitle=None, image_url=None, buttons=None):
        """Represent one element (block , card) of a generic message

        Args:
            title (str, optional): The title of the element , use set_title() method to change its default value. Defaults to "An element of a generic message.".
            subtitle (str, optional): The subtitle of the element , use set_subtitle() method to change its default value. Defaults to None.
            image_url (str, optional): The url of the image to show in the element , use set_image_url() method to change its default value. Defaults to None.
            buttons (list, optional): List of the buttons in the element , max supported is 3(?). Defaults to an empty list.

        Notes:
            param image_url and buttons must be non-empty.
            Use the get_content() method to get the content of the Element object before using it in an generic message or an Elements object.
        """
        assert isinstance(
            title, str), f"type of param title must be str , not {type(title)}"
        assert title != "", "param title must be non empty"

        self.__title = title
        self.__subtitle = subtitle
        self.__image_url = image_url
        self.__buttons = [] if buttons is None else buttons

        if self.__image_url == None or len(self.__buttons) == 0:
            print("WARNING : param image_url and buttons must be non-empty.")

    def set_title(self, title):
        assert isinstance(
            title, str), f"type of param title must be str , not {type(title)}"
        assert title != "", "param title must be non empty"

        self.__title = title

    def set_subtitle(self, subtitle):
        assert isinstance(
            subtitle, str), f"type of param subtitle must be str , not {type(subtitle)}"
        self.__subtitle = subtitle

    def set_image_url(self, image_url):
        assert isinstance(
            image_url, str), f"type of param image_url must be str , not {type(image_url)}"

        self.__image_url = image_url

    def add_button(self, button):
        assert isinstance(
            button, dict), f"type of param button must be list , not {type(button)}"

        self.__buttons.append(button)

    def get_content(self):
        """Return the content of the Element object.

        Returns:
            dict: The content of the Element object.
        """
        if self.__subtitle == None:
            return {
                "title": self.__title,
                "image_url": self.__image_url,
                "buttons": self.__buttons
            }
        return {
            "title": self.__title,
            "subtitle": self.__subtitle,
            "image_url": self.__image_url,
            "buttons": self.__buttons
        }


class Buttons:
    """A list of Button objects.

    Attributes:
        buttons (str , private) : A list containing the content of each Button object.

    Notes:
        Use the add_button() method to add an Button object's content.
        Use the get_content() method to get the content of the Buttons object before using it in an generic message.

        The maximum of buttons is 3 (in a element), sending generic message with more than 3 buttons will return an error message from Facebook API's server.
    """

    def __init__(self):
        self.__buttons = []

    def add_button(self, element):
        self.__buttons.append(element)

    def get_content(self):
        return self.__buttons


class Button:
    def __init__(self, button_type=ButtonType.POSTBACK, title="Button"):
        """Represent a button , used for generic message , persistent menu , ...

        Args:
            button_type (str, optional): The type of the button. Supported values are POSTBACK and WEB_URL. Defaults to POSTBACK.
            title (str, optional): The title of the button. Defaults to "Button".

        Notes:
            param title must be non-empty.
            If the button is a postback button , use set_payload() method to change the default value.
            If the button is a web_url button , use set_url() method to change the default value.
            Use the get_content() method to get the content of the Button object before using it.
        """
        assert button_type in (
            ButtonType.POSTBACK, ButtonType.WEB_URL), "param type must be POSTBACK or WEB_URL"
        assert isinstance(
            title, str), f"type of param title must be str , not {type(title)}"
        assert title != "", "param title must be non empty"

        self.__type = button_type
        self.__title = title

        if self.__type == ButtonType.POSTBACK:
            self.__payload = "<DEVELOPER_DEFINED_PAYLOAD>"
        elif self.__type == ButtonType.WEB_URL:
            self.__url = "<DEVELOPER_DEFINED_URL>"

    def set_title(self, title):
        assert isinstance(
            title, str), f"type of param title must be str , not {type(title)}"
        assert title != "", "param title must be non empty"

        self.__title = title

    def set_payload(self, payload):
        assert self.__type == ButtonType.POSTBACK, "param payload is only supported on postback buttons"
        assert isinstance(
            payload, str), f"type of param payload must be str , not {type(payload)}"

        self.__payload = payload

    def set_url(self, url):
        assert self.__type == ButtonType.WEB_URL, "param url is only supported on web_url buttons"
        assert isinstance(
            url, str), f"type of param url must be str , not {type(url)}"

        self.__url = url

    def get_content(self):
        """Return the content of the Button object.

        Returns:
            dict: The content of the Button object.
        """
        if self.__type == ButtonType.POSTBACK:
            return {
                "type": self.__type,
                "title": self.__title,
                "payload": self.__payload
            }
        return {
            "type": self.__type,
            "title": self.__title,
            "url": self.__url
        }


class QuickReplies:
    """A list of QuickReply objects.

    Attributes:
        quick_replies (str , private) : A list containing the content of each QuickReply object.

    Notes:
        Use the add_quick_reply() method to add an QuickReply object's content.
        Use the get_content() method to get the content of the QuickReplies object before using it.

        The maximum of quick replies is 13 , sending more than 13 quick replies will return an error message from Facebook API's server.
    """

    def __init__(self):
        self.__quick_replies = []

    def add_quick_reply(self, quick_reply):
        self.__quick_replies.append(quick_reply)

    def get_content(self):
        return self.__quick_replies


class QuickReply:
    def __init__(self, title="Quick reply", payload="<DEVELOPER_DEFINED_PAYLOAD>", image_url=None,content_type="text"):
        """Represent a quick reply , used for a quick reply message.

        Args:
            title (str, optional): The title of the quick reply. Defaults to "Quick reply".
            payload (str, optional): The payload of this quick reply. Defaults to "<DEVELOPER_DEFINED_PAYLOAD>".
            image_url ([type], optional): The image url to show beside the quick reply. Defaults to None.
            content_type (str,optional): The action to be taken by the quick reply, see "https://developers.facebook.com/docs/messenger-platform/reference/buttons/quick-replies". Defaults to "text"


        Notes:
            param title must be non-empty.
            param payload must be non-empty.
            Max characters in the param payload is 1000.
            Recommended resolution for the image in param image_url is 24x24.
            Use the get_content() method to get the content of the QuickReply object before using it.
        """
        assert isinstance(
            title, str), f"type of param title must be str , not {type(title)}"
        assert title != "", "param title must be non empty"
        assert isinstance(
            payload, str), f"type of param payload must be str , not {type(payload)}"
        assert payload != "", "param payload must be non empty"
        assert len(str(payload)) < 1000, "max character of param payload is 1000"

        self.__title = title
        self.__payload = payload
        self.__image_url = image_url
        self.__content_type = content_type

        if len(title) > 20:
            print(
                "WARNING : max characters for param title is 20 , your title won't show entirely")

    def set_title(self, title):
        assert isinstance(
            title, str), f"type of param title must be str , not {type(title)}"
        assert title != "", "param title must be non empty"
        if len(title) > 20:
            print(
                "WARNING : max characters for param title is 20 , your title won't show entirely")

        self.__title = title

    def set_payload(self, payload):
        assert isinstance(
            payload, str), f"type of param payload must be str , not {type(payload)}"
        assert payload != "", "param payload must be non empty"
        assert len(str(payload)) < 1000, "max character of param payload is 1000"

        self.__payload = str(payload)

    def set_image_url(self, image_url):
        assert isinstance(
            image_url, str), f"type of param image_url must be str , not {type(image_url)}"

        self.__image_url = image_url

    def get_content(self):
        """Return the content of the QuickReply object.

        Returns:
            dict: The content of the QuickReply object.
        """
        if self.__image_url == None:
            return {
                "content_type": self.__content_type,
                "title": self.__title,
                "payload": self.__payload
            }
        return {
            "content_type": self.__content_type,
            "title": self.__title,
            "payload": self.__payload,
            "image_url": self.__image_url
        }


class PersistentMenu:
    def __init__(self, default_locale_menu):
        """Represents a persistent menu.

        Args:
            default_locale_menu (list): A list of Button objects of the default locale.

        Notes:
            Use the get_content() method to get the content of the PersistentMenu object before using it.
        """
        assert isinstance(
            default_locale_menu, list), f"type of param default_locale_menu must be a list of Button objects"
        assert len(
            default_locale_menu) > 0, "param default_locale_menu must contains at least one Button object"

        self.__persistent_menus = [
            {
                "locale": "default",
                "composer_input_disabled": "false",
                "call_to_actions": default_locale_menu
            }
        ]

    def add_locale(self, language_code, menu):
        """Add a locale to the persistent menu , other than the default one.

        Args:
            language_code (str) : The language code used for this locale. eg.: fr-FR for French language.
            menu (list) : A list of Button objects.
        """
        assert isinstance(
            language_code, str), f"type of param language_code must be a string , not {type(language_code)}"
        assert isinstance(
            menu, list), f"type of param menu must be a list of Button object"

        self.__persistent_menus.append({
            "locale": language_code,
            "composer_input_disabled": "false",
            "call_to_actions": menu
        })

    def get_content(self):
        return self.__persistent_menus
