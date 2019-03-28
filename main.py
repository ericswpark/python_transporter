from slackclient import SlackClient
import os
import time
import parser

# TODO: Read token from a separate file to prevent leaks
# Initialize client
SLACK_BOT_TOKEN = "xoxb-553286279156-556607535715-KolZkyBqAektJ7noQjLsaDlG"
slack_client = SlackClient(SLACK_BOT_TOKEN)

if slack_client.rtm_connect():
    # Connection to chat successful!
    while True:
        events = slack_client.rtm_read()
        for event in events:
            # Process new events
            # Let's make sure this event is a message event from a channel (make sure it's not a bot message too)
            if('channel' in event and 'text' in event and event.get('type') == 'message' and event.get('subtype') != 'bot_message'):
                print("Received message!")
                channel = event['channel']
                text = event['text']
                message = "Received link {}. Checking validity...".format(text)
                slack_client.api_call("chat.postMessage", channel=channel, text=message)

                # See if link has brackets, remove if true
                if text[0] == '<':
                    text = text[1:-1]

                status_return_code = parser.parseUrl(text)
                if status_return_code == 0:
                    message = "Download successful!"
                elif status_return_code == 1:
                    message = "Could not find a valid link. Are you sure you've only inputted the HTTP/HTTPS URL? Others are not supported."
                elif status_return_code == 2:
                    message = "This link type is not yet supported."
                else:
                    message = "An unexpected error occurred during the parsing process."
                slack_client.api_call("chat.postMessage", channel=channel, text=message)
        time.sleep(1)

else:
    print("Connection failed, invalid tokens?")