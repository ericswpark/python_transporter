from slackclient import SlackClient
import os
import time

# Initialize client
SLACK_BOT_TOKEN = "xoxb-553286279156-556607535715-KolZkyBqAektJ7noQjLsaDlG"
slack_client = SlackClient(SLACK_BOT_TOKEN)

if slack_client.rtm_connect():
    # Connection to chat successful!
    while True:
        events = slack_client.rtm_read()
        for event in events:
            print(event)
            # Process new events
            # Let's make sure this event is from the transporter channel and is valid
            if('channel' in event and 'text' in event and event.get('type') == 'message' and event.get('subtype') != 'bot_message'):
                print("Received message!")
                channel = event['channel']
                text = event['text']
                message = "Received link {}, but cannot parse right now. Try again later.".format(text)
                slack_client.api_call("chat.postMessage", channel=channel, text=message)
            else:
                print("No message received for this run. Sleeping 30 seconds...")
        time.sleep(30)
else:
    print("Connection failed, invalid tokens?")