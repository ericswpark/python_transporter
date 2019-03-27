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
            print(event)
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
