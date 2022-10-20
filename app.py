# flask run -p 3000

import os
from dotenv import load_dotenv

load_dotenv()


from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import json


# Initializes Slack Bolt app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
client = WebClient(os.environ.get("SLACK_BOT_TOKEN"))


'''You can uncomment the text below to print the bot's info'''
# bot = client.api_call("auth.test")
# bot_id = client.api_call("auth.test")['bot_id']
# bot_user_id = client.api_call("auth.test")['user_id']
# bot_info = client.bots_info(bot=bot_id)
# print(bot_info)


@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    logger.debug(body)
    return next()



# ** SLACK BOT FUNCTIONALITY
#! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class WelcomeMessage:

    def __init__(self, user):
        self.user = user
        self.channel = user
        self.icon_emoji = ':robot_face:'
        self.timestamp = ''
        self.completed = False

    def get_message(self):
        START_TEXT = {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': (
                    f"Hi <@{self.user}>! Welcome to this awesome channel! \n\n"
                    "*Get started by completing the tasks on the home page!*"
                )
            }
        }

        DIVIDER = {'type': 'divider'}
        return {
            'ts': self.timestamp,
            'channel': self.channel,
            'text': "Welcome!",
            'username': "Welcome robot!",
            'icon_emoji': self.icon_emoji,
            'blocks': [
                START_TEXT,
                DIVIDER,
                self._get_reaction_task()
            ]
        }
    
    def _get_reaction_task(self):
        checkmark = ':white_check_mark:'
        if not self.completed:
            checkmark = ':white_large_square:'
        
        text = f'{checkmark} *React to this message!*'

        return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': text}}



welcome_messages = {}
def send_welcome_message(user):
    if user in welcome_messages:
        return

    print('Sending welcome message...')
    welcome = WelcomeMessage(user)
    message = welcome.get_message()

    response = client.chat_postMessage(**message)
    welcome.timestamp = response['ts']
    print(f"response: \n{response}")
    
    welcome_messages[user] = welcome
    print(f'welcome messages: \n{welcome_messages}')



@app.event('member_joined_channel') # @app.event('team_join')
def user_join(body, event, logger):
    print(f"member joined channel: \n{json.dumps(body, indent=2)}")
    try:
        user = event['user']
        auth_user_id = body['authorizations'][0]['user_id']
        send_welcome_message(user)

    except SlackApiError as e:
        print(logger.error(f"Error occurred during 'member_joined_channel' event: \n{e}"))



@app.event('reaction_added')
def reaction(event, logger):
    print(f"reaction added: \n{json.dumps(event, indent=2)}")
    try:
        channel = event['item']['channel']
        user = event['user']

        if f'{user}' not in welcome_messages:
            return
        
        welcome = welcome_messages[user]
        welcome.completed = True 
        welcome.channel = channel
        message = welcome.get_message() # this will get us that message that's a check mark instead of a box
        updated_message = client.chat_update(**message)
        welcome.timestamp = updated_message['ts']

        welcome_messages[user][channel] = message
    
    except SlackApiError as e:
        print(logger.error(f"Error occurred during 'reaction_added' event: {e}"))


# D047FJBUBQA
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    print(f"app home opened: \n{json.dumps(event, indent=2)}")
    try:
        client.views_publish(
            user_id = event["user"],
            view={
                "type": "home",
                "callback_id": "home_view",

                # body of the view
                "blocks": [
                {
                    "type": "section",
                    "text": {
                    "type": "mrkdwn",
                    "text": "*Welcome to your _App's Home_* :tada:"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                    "type": "mrkdwn",
                    "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                    {
                        "type": "button",
                        "text": {
                        "type": "plain_text",
                        "text": "Click me!"
                        }
                    }
                    ]
                }
                ]
            }
        )
    
    except Exception as e:
        print(logger.error(f"Error publishing home tab: {e}"))



# ** FLASK APP FACTORY
#! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from flask import Flask, request


flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/slack/actions", methods=["POST"])
def slack_actions():
    return handler.handle(request)


# Start the app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))