import utils.config as config
import sys, time

from slackclient import SlackClient

def readToken():
    try:
        return config.readConfig('auth','slack-token')
    except:
        # Token not available in configuration file
        print("It seems like you have not initialized the configuration file. Would you like to do so now? (y/n) ", end='')
        choice = input().lower()
        if(choice == 'y'):
            print("Please paste your bot token: ", end='')
            token = input()
            config.writeConfig('auth','slack-token', token)
            print("Token successfully written to configuration. Please restart!")
        sys.exit(0)

def connectSlack(slack_client):
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
                    
                    # Add to queue
            time.sleep(1)
    else:
        print("Connection failed, invalid tokens?")


if __name__ == '__main__':
    # Try reading token
    token = readToken()

    # Initialize client
    slack_client = SlackClient(token)

    # Delay for reconnecting in case of error
    delay = 0

    while True:
        try:
            connectSlack(slack_client)
        except:
            delay += 10
            print("An exception occurred. Check the stack trace for more details above.")
            print("Waiting for {delay} seconds before restarting...".format(delay=delay))
            time.sleep(delay)
