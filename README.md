# messenger-api-python
[![PyPI](https://img.shields.io/pypi/v/messenger-api-python.svg?maxAge=2592000)](https://pypi.python.org/pypi/messenger-api-python)

Python Wrapper to various APIs from [Facebook Messenger Platform](https://developers.facebook.com/docs/messenger-platform).


## Features

### Send API (v12.0)
 - Send text messages
 - Send attachments from a remote file (image, audio, video, file)
 - Send attachments from a local file (image, audio, video, file)
 - Send templates (generic messages)
 - Send quick replies
 - Send buttons
### Profile API (v12.0)
- Set welcome screen
- Set persistent menu
### Attachment Upload API (v12.0)
- Upload attachments from a remote file (image, audio, video, file)
- Upload attachments from a local file (image, audio video, file)
### Reusable components
Various components used when sending messages in Facebook Messenger are wrapped into Python objects to make them reusable and easy to use.
- **Elements:** used to contains various Element objects
- **Element:** a card-like component that holds various other components
- **Buttons:** used to contains various Button objects
- **Button:** button used in various other components, can also be used alone
- **QuickReplies:** used to contains various QuickReply objects
- **QuickReply:** used when sending messages accompanied with quick replies
- **PersistentMenu:** used when setting up persistent menu

## Prerequisite
- **Python 3.7+** installed
- You'll need to setup a [Facebook App](https://developers.facebook.com/apps/), Facebook Page, get the Page Access Token and link the App to the Page.
## How to install
### From GitHub
- Clone this repository :
```bash
git clone https://github.com/krishna2206/messenger-api-python.git
```
- Navigate to the cloned repository folder and build the package :
```bash
python -m build
```
- Navigate to *dist* folder and install the package, <package_name> may vary so I don't explicitly provide the name here :
```bash
pip install <package_name>.whl
```
### From Pypi
Package from Pypi.org may not be the latest one, if you want the latest version of this package, install it from the GitHub repository (see above)
```bash
pip install messenger-api-python
```
## Usage
### Send API
```python
from messengerapi import SendApi
send_api = SendApi(<page_access_token>)
send_api.send_text_message(<message>, <recipient_id>)
```
**Note**: From Facebook regarding User IDs

> These ids are page-scoped. These ids differ from those returned from Facebook Login apps which are app-scoped. You must use ids retrieved from a Messenger integration for this page in order to function properly.

> If `app_secret` is initialized, an app_secret_proof will be generated and send with every request. Appsecret Proofs helps further secure your client access tokens. You can find out more on the [Facebook Docs](https://developers.facebook.com/docs/graph-api/securing-requests#appsecret_proof)

##### Sending a generic template message:

> [Generic Template Messages](https://developers.facebook.com/docs/messenger-platform/implementation#receive_message) allows you to add cool elements like images, text all in a single bubble.
```python
from messengerapi import SendApi
from messengerapi.components import Elements, Element, Buttons, Button, POSTBACK

send_api = SendApi(<page_access_token>)

elements = Elements()
buttons = Buttons()

button = Button(button_type=POSTBACK, title="My button")
buttons.add_button(button.get_content())
element = Element(title="My element", subtitle="The element's subtitle, image_url=<image_url>, buttons=buttons)
elements.add_element(element.get_content())

send_api.send_generic_message(elements.get_content() , recipient_id , image_aspect_ratio="horizontal")
```
##### Sending remote (from URL) image/audio/video/file:
```python
from messengerapi import SendApi

send_api = SendApi(<page_access_token>)

# To send an image
send_api.send_image_attachment(<image_url> , <recipient_id>)
# To send an audio
send_api.send_audio_attachment(<audio_url> , <recipient_id>)
# To send a video
send_api.send_video_attachment(<video_url> , <recipient_id>)
# To send a file
send_api.send_file_attachment(<file_url> , <recipient_id>)
```
##### Sending local image/audio/video/file:
```python
from messengerapi import SendApi

send_api = SendApi(<page_access_token>)

# To send an image
send_api.send_local_image(<image_location> , <recipient_id>)
# To send an audio
send_api.send_local_audio(<audio_location> , <recipient_id>)
# To send a video
send_api.send_local_video(<video_location> , <recipient_id>)
# To send a file
send_api.send_local_file(<file_location> , <recipient_id>)
```
## To do
- Securing requests
- Unit tests
