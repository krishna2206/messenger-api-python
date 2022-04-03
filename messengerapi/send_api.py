"""Wrapper for the Send API , version 12.0"""

import os

import requests
from requests_toolbelt import MultipartEncoder
import magic

class SendApi():
	def __init__(self , page_access_token):
		self.__graph_version = "12.0"
		self.__api_url = f"https://graph.facebook.com/v{self.__graph_version}/me/messages"
		self.__page_access_token = page_access_token

	def get_api_url(self):
		return self.__api_url

	def get_access_token(self):
		return self.__page_access_token

	def get_graph_version(self):
		return self.__graph_version

	def send_text_message(self , message , recipient_id , messaging_type="RESPONSE"):
		"""Send a text message to the recipient.

		Args:
			message (str): The message text content.
			recipient_id (str): The recipient id.
			messaging_type (str, optional): The message type (https://developers.facebook.com/docs/messenger-platform/send-messages/#messaging_types). Defaults to "RESPONSE".

		Returns:
			dict: The response body from Facebook's API's server.
		"""
		assert messaging_type in ["RESPONSE" , "UPDATE" , "MESSAGE_TAG"] , "value of param messagin_type must be \"RESPONSE\",\"UPDATE\" or \"MESSAGE_TAG\""

		request_body = {
			"messaging_type": messaging_type,
			"recipient":
			{
				"id": recipient_id
			},
			"message":
			{
				"text": message
			}
		}

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , json=request_body).json()

	"""
	Send an attachment from an URL of a file
	Max size supported is 25.0MiB , if you send an attachment that exceeds this size , this will return an error response.
	"""
	def send_image_attachment(self , attachment_url , recipient_id , is_reusable="false"):
		"""Send an local image : send_image_attachment("<IMAGE_URL>" , "<RECIPIENT_ID")"""
		return self.__send_attachment_message("image" , attachment_url , recipient_id , is_reusable)

	def send_video_attachment(self , attachment_url , recipient_id , is_reusable="false"):
		"""Send an local video : send_video_attachment("<VIDEO_URL>" , "<RECIPIENT_ID")"""
		return self.__send_attachment_message("video" , attachment_url , recipient_id , is_reusable)

	def send_audio_attachment(self , attachment_url , recipient_id , is_reusable="false"):
		"""Send an local audio : send_audio_attachment("<AUDIO_URL>" , "<RECIPIENT_ID")"""
		return self.__send_attachment_message("audio" , attachment_url , recipient_id , is_reusable)

	def send_file_attachment(self , attachment_url , recipient_id , is_reusable="false"):
		"""Send an local file : send_file_attachment("<FILE_URL>" , "<RECIPIENT_ID")"""
		return self.__send_attachment_message("file" , attachment_url , recipient_id , is_reusable)


	def send_generic_message(self , elements , recipient_id , image_aspect_ratio="horizontal" , quick_replies = None):
		"""Send a generic message (https://developers.facebook.com/docs/messenger-platform/send-messages/template/generic)

		Args:
			elements (list): A list of Element objects , contained in an Elements object.
			recipient_id (str): The recipient id.
			image_aspect_ratio (str, optional): How image is diplayed in an Element object. Defaults to "horizontal".
			quick_replies (list, optional): A list of QuickReply objects , contained in a QuickReplies object.
				efaults to None.

		Returns:
			dict: The response body from Facebook's API server.

		"""
		request_body = {
			"recipient" :
			{
				"id": recipient_id
			},
			"message" :
			{
				"attachment" :
				{
					"type": "template",
					"payload" :
					{
						"template_type": "generic",
						"image_aspect_ratio" : image_aspect_ratio,
						"elements" : elements
					}
				}
			}
		}

		if quick_replies is not None:
			assert isinstance(quick_replies , list) , f"type of param quick_replies must be a list , not {type(quick_replies)}"
			assert len(quick_replies) > 0 , "param quick_replies must be non empty"

			request_body["message"]["quick_replies"] = quick_replies

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , json=request_body).json()

	def mark_seen_message(self , recipient_id):
		"""Mark 'seen' the message"""
		return self.__send_sender_actions("mark_seen" , recipient_id)

	def typing_on_message(self , recipient_id):
		"""Send a typing on message"""
		return self.__send_sender_actions("typing_on" , recipient_id)

	def typing_off_message(self , recipient_id):
		"""Send a typing off message"""
		return self.__send_sender_actions("typing_off" , recipient_id)

	def send_quick_replies(self , message , quick_replies , recipient_id , messaging_type="RESPONSE"):
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
			"recipient":
			{
				"id": recipient_id
			},
			"messaging_type": messaging_type,
			"message":
			{
				"text": message,
				"quick_replies":
				quick_replies
			}
		}

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , json=request_body).json()

	"""
	Send an attachment from a local file
	Max size supported is 25.0MiB , if you send an attachment that exceeds this size , this will return an error response.
	"""
	def send_local_image(self , image_location , recipient_id , is_reusable="true"):
		"""Send a local image : send_local_image(<IMAGE_LOCATION> , <RECIPIENT_ID>)"""
		return self.__send_local_attachment("image" , image_location , recipient_id , is_reusable)

	def send_local_video(self , video_location , recipient_id , is_reusable="true"):
		"""Send a local video : send_local_video(<VIDEO_LOCATION> , <RECIPIENT_ID>)"""
		return self.__send_local_attachment("video" , video_location , recipient_id , is_reusable)

	def send_local_audio(self , audio_location , recipient_id , is_reusable="true"):
		"""Send a local audio : send_local_audio(<AUDIO_LOCATION> , <RECIPIENT_ID>)"""
		return self.__send_local_attachment("audio" , audio_location , recipient_id , is_reusable)

	def send_local_file(self , file_location , recipient_id , is_reusable="true"):
		"""Send a local file : send_local_file(<FILE_LOCATION> , <RECIPIENT_ID>)"""
		return self.__send_local_attachment("file" , file_location , recipient_id , is_reusable)


	def send_saved_image(self, attachment_id:str, recipient_id:str):
		"""Send a saved image to the recipient.

		Args:
			attachment_id (str): The attachment id.
			recipient_id (str): The recipient id.

		Returns:
			dict: The response body from Facebook's API server.
		"""
		return self.__send_saved_attachment(attachment_id, "image", recipient_id)

	def send_saved_video(self, attachment_id:str, recipient_id:str):
		"""Send a saved video to the recipient.

		Args:
			attachment_id (str): The attachment id.
			recipient_id (str): The recipient id.

		Returns:
			dict: The response body from Facebook's API server.
		"""
		return self.__send_saved_attachment(attachment_id, "video", recipient_id)

	def send_saved_audio(self, attachment_id:str, recipient_id:str):
		"""Send a saved audio to the recipient.

		Args:
			attachment_id (str): The attachment id.
			recipient_id (str): The recipient id.

		Returns:
			dict: The response body from Facebook's API server.
		"""
		return self.__send_saved_attachment(attachment_id, "audio", recipient_id)

	def send_saved_file(self, attachment_id:str, recipient_id:str):
		"""Send a saved file to the recipient.

		Args:
			attachment_id (str): The attachment id.
			recipient_id (str): The recipient id.

		Returns:
			dict: The response body from Facebook's API server.
		"""
		return self.__send_saved_attachment(attachment_id, "file", recipient_id)

	def send_buttons(self, text:str, buttons:list, recipient_id:str):
		"""Send a button message (https://developers.facebook.com/docs/messenger-platform/send-messages/template/button)

		Args:
			text (str): The text to accompagny the button.
			buttons (list): A list of Button objects.
			recipient_id (str): The recipient id.

		Returns:
			dict: The response body from Facebook's API server.
		"""
		request_body = {
			"recipient" :
			{
				"id": recipient_id
			},
			"message" :
			{
				"attachment" :
				{
					"type": "template",
					"payload" :
					{
						"template_type": "button",
						"text": text,
						"buttons": buttons
					}
				}
			}
		}

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , json=request_body).json()


	def __send_sender_actions(self , sender_action , recipient_id):
		request_body = {
  							"recipient":
							{
    							"id":recipient_id
  							},
  							"sender_action":sender_action
					   }

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , json=request_body).json()

	def __send_saved_attachment(self, attachment_id:str, attachment_type:str, recipient_id:str):
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

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , json=request_body).json()

	def __send_local_attachment(self , asset_type , file_location , recipient_id , is_reusable="true"):

		#! BUG
		# THERE IS A BUG THAT MAGIC RETURNS WRONG MIMETYPE IF THE FILE IS AN MP3 FILE
		# ALSO THE API RETURNS AN ERROR IF YOU SEND AN MP3 FILE (AUDIO/MPEG) AS A LOCAL/ATTACHMENT FILE
		# if (os.path.basename(file_location).endswith(".mp3") or
		# 	magic.Magic(mime=True).from_file(file_location).startswith("audio/mpeg")):
		# 	mimetype = "application/octet-stream"
		# ZIP files must be renamed to have an .pdf extension otherwise this will fail to send
		# elif (os.path.basename(file_location).endswith(".zip") or
		# 	magic.Magic(mime=True).from_file(file_location).startswith("application/zip")):
		# 	mimetype = "application/octet-stream"
		# else:
		# 	mimetype = magic.Magic(mime=True).from_file(file_location)

		if os.path.basename(file_location).endswith(".pdf"):
			mimetype = "application/octet-stream"
		else:
			mimetype = magic.Magic(mime=True).from_file(file_location)

		print(mimetype)

		request_body = MultipartEncoder(
			fields = {
				"recipient" : str({"id":recipient_id}),
				"message" : str(
					{
						"attachment" :
						{
							"type" : asset_type ,
							"payload" :
							{
								"is_reusable" : is_reusable
							}
						}
					}
				),
				"filedata" : (
					os.path.basename(file_location) ,
					open(file_location , "rb") ,
					mimetype
				)
			}
		)
		headers = {"content-type":request_body.content_type}

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , data=request_body , headers=headers).json()

	def __send_attachment_message(self , attachment_type , attachment_url , recipient_id , is_reusable="false"):
		request_body = {
			"recipient":
			{
				"id": recipient_id
			},
			"message": {
				"attachment":
				{
					"type": attachment_type,
					"payload":
					{
						"url": attachment_url,
						"is_reusable": is_reusable
					}
				}
			}
		}

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , json=request_body).json()
