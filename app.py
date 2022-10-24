'''
This is a very simple Slack bot for sending a welcome message to a channel and 
displaying the message in the app's home. Check out the README for more details.

Glitch app: https://coding-temple-welcome-bot.glitch.me
'''

# pip install -r requirements.txt
# FLASK_APP=app.py FLASK_ENV=development flask run -p 3000


#* Import logger
import logging
from slack_sdk.errors import SlackApiError
logger = logging.getLogger(__name__)


#* Import libraries
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


#* Load global variables
import os
from dotenv import load_dotenv
load_dotenv()


token=os.environ.get("SLACK_BOT_TOKEN")
signing_secret=os.environ.get("SLACK_SIGNING_SECRET")




#* Building your Slack Bolt app
app = App(
        token=os.environ.get("SLACK_BOT_TOKEN"),
        signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
    )
client = WebClient(os.environ.get("SLACK_BOT_TOKEN"))


bot = client.api_call("auth.test")
bot_id = client.api_call("auth.test")['bot_id']




# ** SLACK BOT FUNCTIONALITY **
#! - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@app.middleware  # or app.use(log_request)
def log_request(logger, body, next):
    # logger.debug(body)
    logger.info(body)
    return next()



# ** Welcome home/message view
# Tip: Use the Slack Block Kit Builder to build out messages (https://app.slack.com/block-kit-builder/)
class Welcome:
    HEADER = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":tada:  Welcome Coding Temple Alum!  :tada:"
            }
        }
    SUBHEAD = {
            "type": "context",
            "elements": [
                {
                    "text": "Oct 21, 2022  | CT Alumni Slack",
                    "type": "mrkdwn"
                }
            ]
        }
    TEAM_INTRO = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*MEET THE ALUMNI SUPPORT TEAM* \n\n*Marlene Tang* \t<https://calendly.com/marlenetang|Calendar> \n*Aubrey Plew* \t<https://calendly.com/aubreyplew/30min|Calendar> \n*Nate Welter* \t<https://calendly.com/d/dzy-jc3-szz|Interview Prep> | <https://calendly.com/d/dyr-28s-gcx|Mock Interview> \n*Sam Davitt* \t<https://calendly.com/d/dzy-jc3-szz|Interview Prep> | <https://calendly.com/d/dyr-28s-gcx|Mock Interview>"
            }
        }
    JOIN_CHANNELS = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*JOIN CHANNELS* \n\nPlease make sure you read through and set notifications for these channels: \n- <#whos-hiring>\n- <#jobsearchsupport>\n- <#interviews>\n- <#events>\n- <#daily-challenge>\n- <#weekly-challenge>"
            }
        }
    TECH_CHANNELS = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Here are the technical channels we will add you to: \n- <#daily-challenge>: daily whiteboard practice\n- <#interviews>: all things technical interviewing\n- <#hackathon>: quarterly hackathons for grads\n- <#continued-education>: learn and discuss new languages / frameworks here (Quarterly video series based on a poll)\n- <#fix-my-bug>: post your errors and bugs here for help from fellow grads"
            }
        }
    WEEKLY_WORKSHOPS_HEAD = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":calendar: |   *UPCOMING WEEKLY WORKSHOPS*   | :calendar:"
            }
        }
    CAREER_WORKSHOP_HEAD = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_*Personal and Career Development*_"
            }
        }
    IMPOSTER = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`Mon` *Imposter Syndrome Workshop* with Aubrey"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Join",
                    "emoji": True
                },
                "value": "imposter",
                "url": "https://codingtemple.zoom.us/my/aubreyplew",
                "action_id": "button-action"
            }
        }
    JOB_SEARCH_SUPPORT = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`Tues` *Job Search Support* with Marlene"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Join",
                    "emoji": True
                },
                "value": "job_support",
                "url": "https://codingtemple.zoom.us/my/ctalumni",
                "action_id": "button-action"
            }
        }
    TECH_WORKSHOPS_HEAD = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_*Technical Workshops*_"
            }
        }
    TUES_TECH = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`Tues 2-3 CST` *Algorithm & Data Structure* with Nate \n\n- Review and learn new algorithms/data structures that will help you in technical interviews \n- Learn how and when to apply these algorithms in an interview/whiteboarding situation \n- Revisit advanced topics from the cohort"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Join",
                    "emoji": True
                },
                "value": "algos",
                "url": "https://codingtemple.zoom.us/my/alumni.technical",
                "action_id": "button-action"
            }
        }
    WED_SAM = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`Wed 3:30-4:30 CST` *Technical Workshop* with Sam \n\n- A different topics every week"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Join",
                    "emoji": True
                },
                "value": "tech_wrkshop",
                "url": "https://codingtemple.zoom.us/my/cta.samd",
                "action_id": "button-action"
            }
        }
    THURS_TECH = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`Thurs 2-3 CST` *FAANG Interview Prep* with Nate \n\n- Advanced workshops to help prep for big-tech level interviews"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Join",
                    "emoji": True
                },
                "value": "debrief",
                "url": "https://codingtemple.zoom.us/my/alumni.technical",
                "action_id": "button-action"
            }
        }
    FRI_TECH = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "`Fri 2-3 CST` *Interview Debrief Workshop with Nate* \n\n- Discuss the best approach to questions submitted from alumni who are currently interviewing (posted in the <#interviews> channel) \n- Dissect cohort and personal projects and learn how to talk about them technically in an interview \n- Topic suggestion and question submissions are HIGHLY encouraged for this workshop!"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Join",
                    "emoji": True
                },
                "value": "algos",
                "url": "https://codingtemple.zoom.us/my/alumni.technical",
                "action_id": "button-action"
            }
        }
    PAST_WORKSHOPS = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":calendar: |   *PAST WORKSHOPS*   | :calendar: \n\nFind *recordings* in the Google Classroom"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Watch",
                    "emoji": True
                },
                "value": "watch_records",
                "url": "https://classroom.google.com/c/NDU4MjA2MjEyOTQy",
                "action_id": "button-action"
            }
        }
    HUNTR = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*TRACKING YOUR JOB SEARCH*\n\nAs you are job searching, you must track your applications in your Huntr Board. Marlene will send you an invite [please do not make your own board]. You're encouraged to take advantage of the Huntr Chrome Extension <https://chrome.google.com/webstore/detail/huntr-job-search-tracker/mihdfbecejheednfigjpdacgeilhlmnf?hl=en|here>."
            }
        }
    APP_PLATFORMS = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Platforms to apply to:\n* <Builtin.com|Builtin[city].com>\n* <Careerbuilder.com|Careerbuilder.com>\n* <Dice.com|Dice.com>\n* <Glassdoor.com|Glassdoor.com>\n* <Growjo.com|Growjo.com>\n* <Hired.com|Hired.com>\n* <Indeed.com|Indeed.com>\n* <LinkedIn.com|LinkedIn.com>\n* <Ycombinator.com|Ycombinator.com>\n* <Angel.co|Angel.co>\n* <Startup.jobs|Startup.jobs>\n* <Remotive.com|Remotive.com>"
            }
        }
    GETTING_STARTED = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ":loud_sound: *GETTING STARTED* :loud_sound: "
            }
        }
    CHECKLIST = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": " You can start off by checking these off your list! "
            },
            "accessory": {
                "type": "checkboxes",
                "options": [
                    {
                        "text": {
                            "type": "mrkdwn",
                            "text": "Update your name on your Slack and Zoom to First + Last name and your photo to match your LinkedIn profile photo"
                        },
                        "description": {
                            "type": "mrkdwn",
                            "text": "subtext"
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "mrkdwn",
                            "text": "Add yourself to our <https://www.linkedin.com/school/coding-temple/|LinkedIn Alumni Network>"
                        },
                        "description": {
                            "type": "mrkdwn",
                            "text": "subtext"
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "mrkdwn",
                            "text": "Schedule a mock interview"
                        },
                        "description": {
                            "type": "mrkdwn",
                            "text": "Please note: You will not have access to book any Interview Prep time with Sam and Nate until you have completed a Mock Interview."
                        },
                        "value": "value-2"
                    },
                    {
                        "text": {
                            "type": "mrkdwn",
                            "text": "ADD TEXT HERE"
                        },
                        "description": {
                            "type": "mrkdwn",
                            "text": "subtext"
                        },
                        "value": "value-3"
                    }
                ],
                "action_id": "checkboxes-action"
            }
        }
    FYI_PIN = {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":pushpin: If you are having trouble the information you need, this message along with all the resources listed will be pinned to the top of this channel."
                }
            ]
        }
    DIVIDER = {
            "type": "divider"
        }


    def __init__(self, channel='', timestamp=''):
        self.channel = channel
        self.timestamp = timestamp


    # get the body of the home view
    def get_view(self):
        return {
            "type": "home",
            "callback_id": "home_view",
            "blocks": [
                self.HEADER,
                self.SUBHEAD,
                self.TEAM_INTRO,
                self.DIVIDER,
                self.JOIN_CHANNELS,
                self.TECH_CHANNELS,
                self.DIVIDER,
                self.WEEKLY_WORKSHOPS_HEAD,
                self.CAREER_WORKSHOP_HEAD,
                self.IMPOSTER,
                self.JOB_SEARCH_SUPPORT,
                self.CAREER_WORKSHOP_HEAD,
                self.IMPOSTER,
                self.JOB_SEARCH_SUPPORT,
                self.TECH_WORKSHOPS_HEAD,
                self.TUES_TECH,
                self.WED_SAM,
                self.THURS_TECH,
                self.FRI_TECH,
                self.DIVIDER,
                self.PAST_WORKSHOPS,
                self.DIVIDER,
                self.HUNTR,
                self.APP_PLATFORMS,
                self.DIVIDER,
                self.FYI_PIN,
            ]
        }


    # get the body of the message
    def get_message(self):
        return {
            'ts': self.timestamp,
            'channel': self.channel,
            'text': self.HEADER['text']['text'],
            'username': "Welcome robot!",
            'icon_emoji': ":robot_face:",
            'blocks': [
                self.HEADER,
                self.SUBHEAD,
                self.TEAM_INTRO,
                self.DIVIDER,
                self.JOIN_CHANNELS,
                self.TECH_CHANNELS,
                self.DIVIDER,
                self.WEEKLY_WORKSHOPS_HEAD,
                self.CAREER_WORKSHOP_HEAD,
                self.IMPOSTER,
                self.JOB_SEARCH_SUPPORT,
                self.CAREER_WORKSHOP_HEAD,
                self.IMPOSTER,
                self.JOB_SEARCH_SUPPORT,
                self.TECH_WORKSHOPS_HEAD,
                self.TUES_TECH,
                self.WED_SAM,
                self.THURS_TECH,
                self.FRI_TECH,
                self.DIVIDER,
                self.PAST_WORKSHOPS,
                self.DIVIDER,
                self.HUNTR,
                self.APP_PLATFORMS,
                self.DIVIDER,
                self.FYI_PIN,
            ]
        }




# ** Home app opened
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # Get the user from the event data
        slack_id = event["user"]

        # Create Welcome object
        home_view = Welcome()

        # Get the view object that appears in the app home
        view = home_view.get_view()

        # Use views.publish() to push a view to the Home tab
        response = client.views_publish(
            # the user that opened your app's app home
            user_id=slack_id,
            # the main body of the view to display
            view={**view}
        )

    except SlackApiError as e:
        logger.error(f"Error publishing home tab: {e}")

    except Exception as ex:
        logger.error(f"Exception: {ex}")      



# ** Welcome command
@app.command("/welcome")
def welcome(ack, body, logger):
    ack() # must acknowledge your app received the incoming event within 3 seconds
    # print(body)
    try:
        # Create Welcome object with channel
        welcome = Welcome(channel=body['channel_id'])

        # Get the message object that will appear in the bot's message
        message = welcome.get_message()
        response = client.chat_postMessage(**message)
        
        # If you want to want to update the chat later, 
        # update the ts attribute with the response 'ts'
        # and save the object and/or ts value to reference
        # later ('ts' is the unique message ID)
        # welcome.timestamp = response['ts']        

    except SlackApiError as e:
        print(logger.error(f"Error occurred calling welcome command: \n{e}"))





# ** FLASK APPLICATION
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