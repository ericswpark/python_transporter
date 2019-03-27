#!/usr/bin/env python
'''
Script to transport and download video files

Install: slackclient from pip3

'''
# from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import time
import os

SLACK_BOT_TOKEN = "xoxb-553286279156-556607535715-KolZkyBqAektJ7noQjLsaDlG"
# SLACK_SIGNING_SECRET = "4975816e9b405530fbd1f7036dd1c23a"

# Initialize client
slack_client = SlackClient(SLACK_BOT_TOKEN)

# -----------------------
#    HELPER FUNCTIONS
# -----------------------

def processMessages():
    # Get events after last call
    events = slack_client.rtm_read()
    for event in events:
        # Process new events
        # Let's make sure this event is from the transporter channel and is valid
        if('transporter' in event and 'http' in event and event.get('type') == 'message'):
            print("Received message!")
            channel = event['channel']
            text = event['text']
            # This is valid
            message = "Received link {}, but cannot parse right now. Try again later.".format(text)
            slack_client.api_call("chat.postMessage", channel=channel, text=message)
        else:
            print("No message received for this run. Rerun?")

# ----------------------
#         MAIN
# ----------------------

if slack_client.rtm_connect():
    # Connection to chat successful!
    while True:
        processMessages()
        time.sleep(1)
else:
    print("Connection failed, invalid tokens?")





'''
# Get new messages
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message has a video link (text only), forward it
    if message.get("subtype") is None and "http" in message.get('text'):
        channel = message["channel"]
        message = "Received link {}, but cannot do anything with it right now.".format(message.get('text'))
        slack_client.api_call("chat.postMessage", channel=channel, text=message)


# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000)
'''