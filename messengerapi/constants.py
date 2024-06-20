API_VERSION = "19.0"


class ButtonType:
    """Button types used in Element and QuickReply classes.

    POSTBACK: Button that sends a payload back to the bot.
    
    WEB_URL: Button that opens a URL in the user's browser.
    
    PHONE_NUMBER: Button that opens a call app in the user's phone
    """
    POSTBACK = "postback"
    WEB_URL = "web_url"
    PHONE_NUMPER = "phone_number"


class MessagingType:
    """Messaging types for the Send API.

    RESPONSE : Message is in response to a received message. This includes promotional and non-promotional messages sent inside the 24-hour standard messaging window. For example, use this tag to respond if a person asks for a reservation confirmation or an status update.

    UPDATE : Message is being sent proactively and is not in response to a received message. This includes promotional and non-promotional messages sent inside the the 24-hour standard messaging window.

    MESSAGE_TAG : Message is non-promotional and is being sent outside the 24-hour standard messaging window with a message tag. The message must match the allowed use case for the tag.
    """
    RESPONSE = "RESPONSE"
    UPDATE = "UPDATE"
    MESSAGE_TAG = "MESSAGE_TAG"

class QuickReplyType:
    """Quick Reply Types used in QuickReply classes.
     
    text: Sends a text button
    user_phone_number: Sends a button allowing recipient to send the phone number associated with their account.
    user_email: Sends a button allowing recipient to send the email associated with their account.
    """
    
    TEXT = "text"
    USER_PHONE_NUMBER = "user_phone_number"
    USER_EMAIL = "user_email"
    
class NotificationType:
    """Notification types for the Send API.
    Type of push notification a person will receive

    NO_PUSH : No notification

    REGULAR (default) : Sound or vibration when a message is received by a person

    SILENT_PUSH : On-screen notification only
    """
    REGULAR = "REGULAR"
    SILENT_PUSH = "SILENT_PUSH"
    NO_PUSH = "NO_PUSH"


class SenderAction:
    """Sender actions for the Send API.
    The action icon shown in the messaging window representing the action taken by the Page on a message the Page has received from a person.

    MARK_SEEN : Mark the message as seen

    TYPING_ON : Display a typing indicator

    TYPING_OFF : Remove a typing indicator
    """
    MARK_SEEN = "mark_seen"
    TYPING_ON = "typing_on"
    TYPING_OFF = "typing_off"


class MessageTag:
    """Message tags for the Send API.
    A tag that enables your Page to send a message to a person outsde the standard 24 hour messaging window.

    ACCOUNT_UPDATE : Tags the message you are sending to your customer as a non-recurring update to their application or account.

    CONFIRMED_EVENT_UPDATE : Tags the message you are sending to your customer as a reminder fo an upcoming event or an update for an event in progress for which the customer is registered.

    CUSTOMER_FEEDBACK : Tags the message you are sending to your customer as a Customer Feedback Survey. Customer feedback messages must be sent within 7 days of the customer's last message.

    HUMAN_AGENT : When this tag is added to a message to a customer, it allows a human agent to respond to a person's message. Messages can be sent within 7 days of the person's. Human agent support is for issues that cannot be resolved within the standard 24 hour messaging window ** Apps should apply for the Human Agent permission via the Developer App dashboard. Navigate to App dashboard -> App review -> Permissions & Features -> Human Agent. Those apps that were previously approved for beta access to the Human Agent permission do not need to re-apply for access.

    POST_PURCHASE_UPDATE : Tags the message you are sending to your customer as an update for a recent purchase made by the customer.
    """
    ACCOUNT_UPDATE = "ACCOUNT_UPDATE"
    CONFIRMED_EVENT_UPDATE = "CONFIRMED_EVENT_UPDATE"
    CUSTOMER_FEEDBACK = "CUSTOMER_FEEDBACK"
    HUMAN_AGENT = "HUMAN_AGENT"
    POST_PURCHASE_UPDATE = "POST_PURCHASE_UPDATE"
    
class WebViewRatio:
    """WebView allows you to open a standard webview, where you can load webpages inside Messenger.
    This lets you offer experiences and features that might be difficult to offer with message bubbles
    
    FULL: Allows you to view the full browser window 
    
    TALL: Allows you to display half of the browser window  
    
    COMPACT: Allows you to view a quarter of the browser window  
    """
    FULL = "full"
    TALL = "tall"
    COMPACT = "compact"
    
