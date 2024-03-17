"""Wrapper for the Send API"""

import os
import json
import urllib

import magic
import requests
from requests_toolbelt import MultipartEncoder

from .constants import API_VERSION, MessagingType, NotificationType


class SendApi:
    def __init__(self, page_access_token: str, page_id: str = None):
        self.__graph_version = API_VERSION
        self.__def_api_url = f"https://graph.facebook.com/v{self.__graph_version}/me"
        self.__alt_api_url = (
            None if page_id is None else f"https://graph.facebook.com/v{self.__graph_version}/{page_id}")
        self.__page_id = None if page_id is None else page_id
        self.__default_endpoint = "/messages"
        self.__page_access_token = page_access_token

    def get_def_api_url(self):
        return self.__def_api_url

    def get_alt_api_url(self):
        return self.__alt_api_url

    def get_page_id(self):
        return self.__page_id

    def get_def_endpoint(self):
        return self.__default_endpoint

    def get_access_token(self):
        return self.__page_access_token

    def get_graph_version(self):
        return self.__graph_version

    def send_text_message(self, message: str, recipient_id: str,
        messaging_type: str = MessagingType.RESPONSE,
        notification_type: str = NotificationType.REGULAR, **kwargs):
        """Send a text message to the recipient.

        Args:
            message (str): The message text content.
            recipient_id (str): The recipient id.
            messaging_type (str, optional): The message type (https://developers.facebook.com/docs/messenger-platform/send-messages/#messaging_types). Defaults to "RESPONSE".

        Returns:
            dict: The response body from Facebook's API's server.
        """
        assert messaging_type in ("RESPONSE", "UPDATE", "MESSAGE_TAG"), \
            "value of param messagin_type must be \"RESPONSE\",\"UPDATE\" or \"MESSAGE_TAG\""

        request_body = {
            "messaging_type": messaging_type,
            "notification_type": notification_type,
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message
            }
        }
        if messaging_type == MessagingType.MESSAGE_TAG:
            assert kwargs.get("tag") in (
                "ACCOUNT_UPDATE", "CONFIRMED_EVENT_UPDATE", 
                "CUSTOMER_FEEDBACK", "HUMAN_AGENT", "POST_PURCHASE_UPDATE"), \
                "value of param messagin_type must be \"ACCOUNT_UPDATE\",\"CONFIRMED_EVENT_UPDATE\",\"CUSTOMER_FEEDBACK\",\"HUMAN_AGENT\" or \"POST_PURCHASE_UPDATE\""
            request_body["tag"] = kwargs.get("tag")

        return requests.post(
            self.get_def_api_url() + self.get_def_endpoint(),
            params={"access_token": self.get_access_token()},
            json=request_body).json()

    """
	Send an attachment from an URL of a file
	Max size supported is 25.0MiB , if you send an attachment that exceeds this size , this will return an error response.
	"""
    def send_image_attachment(self, attachment_url: str, recipient_id: str, is_reusable: str = "false"):
        """Send an image by url : send_image_attachment("<IMAGE_URL>" , "<RECIPIENT_ID")"""
        return self.__send_attachment_message("image", attachment_url, recipient_id, is_reusable)

    def send_video_attachment(self, attachment_url: str, recipient_id: str, is_reusable: str = "false"):
        """Send a video by url : send_video_attachment("<VIDEO_URL>" , "<RECIPIENT_ID")"""
        return self.__send_attachment_message("video", attachment_url, recipient_id, is_reusable)

    def send_audio_attachment(self, attachment_url: str, recipient_id: str, is_reusable: str = "false"):
        """Send an audio by url : send_audio_attachment("<AUDIO_URL>" , "<RECIPIENT_ID")"""
        return self.__send_attachment_message("audio", attachment_url, recipient_id, is_reusable)

    def send_file_attachment(self, attachment_url: str, recipient_id: str, is_reusable: str = "false"):
        """Send a file by url : send_file_attachment("<FILE_URL>" , "<RECIPIENT_ID")"""
        return self.__send_attachment_message("file", attachment_url, recipient_id, is_reusable)

    def send_generic_message(self, elements: str, recipient_id: str,
        image_aspect_ratio: str = "horizontal", quick_replies: str = None
    ):
        """Send a generic message (https://developers.facebook.com/docs/messenger-platform/send-messages/template/generic)

        Args:
            elements (list): A list of Element objects , contained in an Elements object.
            recipient_id (str): The recipient id.
            image_aspect_ratio (str, optional): How image is diplayed in an Element object. Defaults to "horizontal".
            quick_replies (list, optional): A list of QuickReply objects , contained in a QuickReplies object.
                defaults to None.

        Returns:
            dict: The response body from Facebook's API server.

        """
        request_body = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "image_aspect_ratio": image_aspect_ratio,
                        "elements": elements
                    }
                }
            }
        }

        if quick_replies is not None:
            assert isinstance(
                quick_replies, list), f"type of param quick_replies must be a list , not {type(quick_replies)}"
            assert len(
                quick_replies) > 0, "param quick_replies must be non empty"

            request_body["message"]["quick_replies"] = quick_replies

        return requests.post(
            self.get_def_api_url() + self.get_def_endpoint(),
            params={"access_token": self.get_access_token()},
            json=request_body).json()

    def mark_seen_message(self, recipient_id: str):
        """Mark 'seen' the message"""
        return self.__send_sender_actions("mark_seen", recipient_id)

    def typing_on_message(self, recipient_id: str):
        """Send a typing on message"""
        return self.__send_sender_actions("typing_on", recipient_id)

    def typing_off_message(self, recipient_id: str):
        """Send a typing off message"""
        return self.__send_sender_actions("typing_off", recipient_id)

    def send_quick_replies(self, message: str, quick_replies: str,
        recipient_id: str, messaging_type: str = "RESPONSE"
    ):
        """Send a quick replies message

        Args:
            message (str): The message text content.
            quick_replies (QuickReplies object): The QuickReplies object content , obtained via the QuickReplies().get_content() method.
            recipient_id (str): The recipient id.
            messaging_type (str, optional): The messaging type. Defaults to "RESPONSE".

        Returns:
            dict: The response body from Facebook's API server.
        """
        request_body = {
            "recipient": {
                "id": recipient_id
            },
            "messaging_type": messaging_type,
            "message": {
                "text": message,
                "quick_replies": quick_replies
            }
        }

        return requests.post(
            self.get_def_api_url() + self.get_def_endpoint(),
            params={"access_token": self.get_access_token()},
            json=request_body).json()

    """
	Send an attachment from a local file
	Max size supported is 25.0MiB , if you send an attachment that exceeds this size , this will return an error response.
	"""
    def send_local_image(self, image_location: str, recipient_id: str, is_reusable: str = "true"):
        """Send a local image : send_local_image(<IMAGE_LOCATION> , <RECIPIENT_ID>)"""
        return self.__send_local_attachment("image", image_location, recipient_id, is_reusable)

    def send_local_video(self, video_location: str, recipient_id: str, is_reusable: str = "true"):
        """Send a local video : send_local_video(<VIDEO_LOCATION> , <RECIPIENT_ID>)"""
        return self.__send_local_attachment("video", video_location, recipient_id, is_reusable)

    def send_local_audio(self, audio_location: str, recipient_id: str, is_reusable: str = "true"):
        """Send a local audio : send_local_audio(<AUDIO_LOCATION> , <RECIPIENT_ID>)"""
        return self.__send_local_attachment("audio", audio_location, recipient_id, is_reusable)

    def send_local_file(self, file_location: str, recipient_id: str, is_reusable: str = "true", mimetype: str = None):
        """Send a local file : send_local_file(<FILE_LOCATION> , <RECIPIENT_ID>)"""
        return self.__send_local_attachment("file", file_location, recipient_id, is_reusable, mimetype)

    def send_saved_image(self, attachment_id: str, recipient_id: str):
        """Send a saved image to the recipient.

        Args:
            attachment_id (str): The attachment id.
            recipient_id (str): The recipient id.

        Returns:
            dict: The response body from Facebook's API server.
        """
        return self.__send_saved_attachment(attachment_id, "image", recipient_id)

    def send_saved_video(self, attachment_id: str, recipient_id: str):
        """Send a saved video to the recipient.

        Args:
            attachment_id (str): The attachment id.
            recipient_id (str): The recipient id.

        Returns:
            dict: The response body from Facebook's API server.
        """
        return self.__send_saved_attachment(attachment_id, "video", recipient_id)

    def send_saved_audio(self, attachment_id: str, recipient_id: str):
        """Send a saved audio to the recipient.

        Args:
            attachment_id (str): The attachment id.
            recipient_id (str): The recipient id.

        Returns:
            dict: The response body from Facebook's API server.
        """
        return self.__send_saved_attachment(attachment_id, "audio", recipient_id)

    def send_saved_file(self, attachment_id: str, recipient_id: str):
        """Send a saved file to the recipient.

        Args:
            attachment_id (str): The attachment id.
            recipient_id (str): The recipient id.

        Returns:
            dict: The response body from Facebook's API server.
        """
        return self.__send_saved_attachment(attachment_id, "file", recipient_id)

    def send_buttons(self, text: str, buttons: list, recipient_id: str):
        """Send a button message (https://developers.facebook.com/docs/messenger-platform/send-messages/template/button)

        Args:
            text (str): The text to accompagny the button.
            buttons (list): A list of Button objects.
            recipient_id (str): The recipient id.

        Returns:
            dict: The response body from Facebook's API server.
        """
        request_body = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": buttons
                    }
                }
            }
        }

        return requests.post(
            self.get_def_api_url() + self.get_def_endpoint(),
            params={"access_token": self.get_access_token()},
            json=request_body).json()

    def __send_sender_actions(self, sender_action: str, recipient_id: str):
        assert self.get_alt_api_url() is not None, "The page id is not defined for this instance."

        request_body = {
            "recipient": {
                "id": recipient_id
            },
            "sender_action": sender_action
        }

        return requests.post(
            self.get_alt_api_url() + self.get_def_endpoint(),
            params={"access_token": self.get_access_token()},
            json=request_body).json()

    def __send_saved_attachment(self, attachment_id: str, attachment_type: str, recipient_id: str):
        request_body = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": attachment_type,
                    "payload": {
                        "attachment_id": attachment_id
                    }
                }
            }
        }

        return requests.post(
            self.get_def_api_url() + self.get_def_endpoint(),
            params={"access_token": self.get_access_token()},
            json=request_body).json()

    def __send_local_attachment(self, asset_type: str, file_location: str,
        recipient_id: str, is_reusable: str = "true", mimetype: str = None
    ):
        if mimetype is None:
            extensions = (".mp3", ".pdf")
            for extension in extensions:
                if file_location.endswith(extension):
                    mimetype = "application/octet-stream"
                    break
                elif extension == extensions[-1]:
                    mimetype = magic.Magic(mime=True).from_file(file_location)
        else:
            mimetype = mimetype

        print(f"File MIMETYPE : {mimetype}")

        multipart_data = MultipartEncoder(
            fields={
                "recipient": json.dumps({"id": recipient_id}),
                "message": json.dumps(
                    {
                        "attachment": {
                            "type": asset_type,
                            "payload": {
                                "is_reusable": is_reusable
                            }
                        }
                    }
                ),
                "filedata": (
                    os.path.basename(file_location),
                    open(file_location, "rb"),
                    mimetype

                )
            }
        )
        headers = {"content-type": multipart_data.content_type}

        # print(self.get_def_api_url() + self.get_def_endpoint())
        print(self.get_alt_api_url() + self.get_def_endpoint())

        return requests.post(
            # self.get_def_api_url() + self.get_def_endpoint(),
            self.get_alt_api_url() + self.get_def_endpoint(),
            params={"access_token": self.get_access_token()},
            data=multipart_data,
            headers=headers).json()

    def __send_attachment_message(self, attachment_type: str, attachment_url: str,
        recipient_id: str, is_reusable: str = "false"
    ):
        request_body = {
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": attachment_type,
                    "payload": {
                        "url": attachment_url,
                        "is_reusable": is_reusable
                    }
                }
            }
        }

        return requests.post(
            self.get_def_api_url() + self.get_def_endpoint(),
            params={"access_token": self.get_access_token()},
            json=request_body).json()

    def send_batch_image_attachments(self, image_urls: list, recipient_id: str):
        assert self.get_page_id() is not None, "The page id is not defined for this instance."

        batch_request_body = []
        for image_url in image_urls:
            request_body = {
                "method": "POST",
                "relative_url": f"{self.get_page_id()}" + self.get_def_endpoint(),
                "body": urllib.parse.urlencode({
                    "recipient": {"id": recipient_id},
                    "message": {
                        "attachment": {
                            "type": "image",
                            "payload": {
                                "url": image_url,
                                "is_reusable": "true"
                            }
                        }
                    }
                }, doseq=False)
            }
            batch_request_body.append(request_body)
        request_body = {
            "batch": batch_request_body
        }

        return requests.post(
            f"https://graph.facebook.com/{self.get_graph_version()}",
            params={"access_token": self.get_access_token()},
            json=request_body).json()
