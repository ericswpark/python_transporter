from slackclient import SlackClient
import os
import sys
import time
import utils.parser as parser
import utils.config as config

# Try reading token
try:
    token = config.readConfig('auth','token')
except:
    # Token not available
    print("It seems like you have not initialized the configuration file. Would you like to do so now? (y/n) ", end='')
    choice = input().lower()
    if(choice == 'y'):
        print("Please paste your bot token: ", end='')
        token = input()
        config.writeConfig('auth','token', token)
        print("Token successfully written to configuration. Please restart!")
    sys.exit(0)


# Initialize client
slack_client = SlackClient(token)

if slack_client.rtm_connect():
    # Connection to chat successful!
    while True:
        events = slack_client.rtm_read() #auto_reconnect=True)
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