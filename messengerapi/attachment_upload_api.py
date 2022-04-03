"""Wrapper for the Attachment Upload API , version 12.0"""

import os

import requests
from requests_toolbelt import MultipartEncoder
import magic

class AttachmentUploadApi():
	def __init__(self, page_access_token:str) -> None:
		self.__graph_version = "12.0"
		self.__api_url = f"https://graph.facebook.com/v{self.__graph_version}/me/message_attachments"
		self.__page_access_token = page_access_token

	def get_api_url(self):
		return self.__api_url

	def get_access_token(self):
		return self.__page_access_token

	def get_graph_version(self):
		return self.__graph_version



	def upload_remote_image(self, image_url:str):
		return self.__upload_remote_attachement("image", image_url)

	def upload_remote_video(self, video_url:str):
		return self.__upload_remote_attachement("video", video_url)

	def upload_remote_audio(self, audio_url:str):
		return self.__upload_remote_attachement("audio", audio_url)

	def upload_remote_file(self, file_url:str):
		return self.__upload_remote_attachement("file", file_url)


	def upload_local_image(self , image_location:str):
		"""Upload local image to send it later.

		Returns:
			str: The attachment id.
		"""
		return self.__upload_local_attachment("image" , image_location)

	def upload_local_video(self , video_location:str):
		"""Upload local video to send it later.

		Returns:
			str: The attachment id.
		"""
		return self.__upload_local_attachment("video" , video_location)

	def upload_local_audio(self , audio_location:str):
		"""Upload local audio to send it later.

		Returns:
			str: The attachment id.
		"""
		return self.__upload_local_attachment("audio" , audio_location)

	def upload_local_file(self , file_location:str):
		"""Upload local file to send it later.

		Returns:
			str: The attachment id.
		"""
		return self.__upload_local_attachment("file" , file_location)


	def __upload_local_attachment(self , asset_type , file_location):
		if os.path.basename(file_location).endswith(".pdf"):
			mimetype = "application/octet-stream"
		else:
			mimetype = magic.Magic(mime=True).from_file(file_location)

		print(mimetype)

		request_body = MultipartEncoder(
			fields = {
				"message" : str(
					{
						"attachment" :
						{
							"type" : asset_type ,
							"payload" :
							{
								"is_reusable" : "true"
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

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , data=request_body , headers=headers).json()["attachment_id"]

	def __upload_remote_attachement(self, asset_type, file_url):
		request_body = {
			"message": {
				"attachment": {
					"type": asset_type,
					"payload": {
						"is_reusable": "true",
						"url": file_url
					}
				}
			}
		}

		return requests.post(self.get_api_url() , params={"access_token":self.get_access_token()} , json=request_body).json()["attachment_id"]
